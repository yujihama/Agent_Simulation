from __future__ import annotations

import csv
import io
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import ValidationError, validate_pack

from .action_parser import ActionParseError, load_action_schema, parse_action_proposal
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .free_choice_runner import build_scenario_messages, scenario_case_id
from .llm_actor import LLMProvider, LLMProviderError, LLMRequest, LLMResponse
from .repeated_runner import require_new_or_empty
from .runner import build_manifest, response_metadata, trace_record
from .scenario_loader import dump_yaml, load_s04, org_payment_scenario_ref


PILOT_ID = "M01"
PROTOCOL_ID = "multi-role-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/multi-role-pilot-v0.1.md"
DEFAULT_M01_BATCH_ID = "m01-buyer-approver-pilot-0001"
M01_RUN_COUNT = 5
CLAIM_BOUNDARY = "multi_role_pilot_observation_only"
BUYER_PROMPT_REF = "prompts/org-payment/buyer-free-choice-action-v0.1.md"
APPROVER_PROMPT_REF = "prompts/org-payment/approver-free-choice-action-v0.1.md"
BUYER_ACTION_MENU_ID = "org_payment_buyer_to_approver_action_menu_v0.1"
APPROVER_ACTION_MENU_ID = "org_payment_approver_constrained_action_menu_v0.1"

ROOT = Path(__file__).resolve().parents[2]
BUYER_PROMPT_TEMPLATE = ROOT / BUYER_PROMPT_REF
APPROVER_PROMPT_TEMPLATE = ROOT / APPROVER_PROMPT_REF

BUYER_ACTION_MENU = [
    {
        "action_type": "request_approval",
        "target_role": "approver",
        "menu_label": "Request explicit approval",
        "selection_boundary": "Open an explicit approval request before payment handling.",
    },
    {
        "action_type": "request_approval_status",
        "target_role": "approver",
        "menu_label": "Request approval clarification",
        "selection_boundary": "Ask the approver to clarify whether approval exists or what approval status should be recorded.",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate ambiguity",
        "selection_boundary": "Escalate the ambiguous approval state to the approver.",
    },
]

APPROVER_ACTION_MENU = [
    {
        "action_type": "approve_payment",
        "target_role": "buyer",
        "menu_label": "Approve payment",
        "selection_boundary": "Record explicit approval for the buyer to use before payment handling.",
    },
    {
        "action_type": "reject_payment",
        "target_role": "buyer",
        "menu_label": "Reject payment",
        "selection_boundary": "Record explicit rejection or refusal to approve payment under current evidence.",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "buyer",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask the buyer or requester-facing process for missing evidence before approving.",
    },
    {
        "action_type": "provide_ambiguous_guidance",
        "target_role": "buyer",
        "menu_label": "Provide ambiguous guidance",
        "selection_boundary": "Respond with approval-like or responsibility-shifting language that does not clearly approve or reject.",
    },
    {
        "action_type": "escalate",
        "target_role": "buyer",
        "menu_label": "Escalate",
        "selection_boundary": "Route the decision to a higher or later review path instead of directly approving or rejecting.",
    },
]


@dataclass(frozen=True)
class RoleActionResult:
    role: str
    action: dict[str, Any]
    prompt_text: str
    response: LLMResponse
    action_menu: dict[str, Any]
    parser_result: dict[str, Any]
    proposal_attempts: list[dict[str, Any]]


@dataclass(frozen=True)
class M01RunRecord:
    index: int
    run_id: str
    buyer_action_type: str
    buyer_target_role: str
    buyer_parser_status: str
    buyer_attempt_count: int
    buyer_rejected_attempt_count: int
    buyer_gm_decision: str
    approver_action_type: str
    approver_target_role: str
    approver_parser_status: str
    approver_attempt_count: int
    approver_rejected_attempt_count: int
    approver_gm_decision: str
    validation_status: str
    buyer_model_version: str | None
    approver_model_version: str | None
    pack_dir: Path


@dataclass(frozen=True)
class M01ExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_m01_buyer_approver_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_M01_BATCH_ID,
) -> Path:
    buyer_provider = buyer_provider or provider
    approver_provider = approver_provider or provider
    if buyer_provider is None or approver_provider is None:
        raise ValueError("provider or both buyer_provider and approver_provider are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[M01RunRecord] = []
    exclusions: list[M01ExcludedRunRecord] = []
    for index in range(1, M01_RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_m01_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                buyer_provider=buyer_provider,
                approver_provider=approver_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_m01_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(
                M01ExcludedRunRecord(
                    index=index,
                    run_id=run_id,
                    exclusion_reason="validation_failure",
                    stage="validation",
                    detail=str(exc),
                )
            )
        except Exception as exc:
            exclusions.append(
                M01ExcludedRunRecord(
                    index=index,
                    run_id=run_id,
                    exclusion_reason=classify_exception(exc),
                    stage="generation",
                    detail=str(exc),
                )
            )

    completed_at = now_utc()
    representatives = copy_m01_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_m01_execution_manifest(
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_m01_aggregate(
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        batch_id=batch_id,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
    )
    write_json(curated_output / "execution-manifest.json", execution_manifest)
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "scenario-summary.csv", render_m01_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_m01_summary(aggregate))
    return curated_output


def write_m01_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
) -> Path:
    scenario = load_s04()
    scenario_id = scenario["id"]
    case_id = scenario_case_id(scenario_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = build_scenario_messages(run_id=run_id, case_id=case_id, scenario=scenario)
    buyer_menu = m01_buyer_action_menu()
    buyer_result = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=4,
        scenario=scenario,
        action_menu=buyer_menu,
        allowed_source_refs=["initial_state/case.md", "M001", "M002", "T001", "T002", "T003"],
        prompt_replacements={
            "{{context}}": buyer_context(run_id=run_id, case_id=case_id, messages=messages, scenario=scenario),
        },
    )
    buyer_decision = decide_m01_buyer_action(run_id=run_id, action=buyer_result.action, scenario=scenario)

    approver_menu = m01_approver_action_menu()
    approver_result = generate_role_action(
        provider=approver_provider,
        role="approver",
        prompt_template=APPROVER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=6,
        scenario=scenario,
        action_menu=approver_menu,
        allowed_source_refs=["initial_state/case.md", "M001", "M002", "A001", "D001", "T001", "T002", "T003", "T004", "T005", "T006"],
        prompt_replacements={
            "{{case_state}}": approver_case_state(run_id, case_id, scenario),
            "{{buyer_action_context}}": buyer_action_context(buyer_result.action, buyer_decision),
            "{{available_evidence}}": approver_available_evidence(messages, buyer_result.action, buyer_decision),
        },
    )
    approver_decision = decide_m01_approver_action(run_id=run_id, action=approver_result.action, scenario=scenario)

    messages_with_response = messages + [approver_response_message(run_id, case_id, approver_result.action, approver_decision)]
    actions = [buyer_result.action, approver_result.action]
    decisions = [buyer_decision, approver_decision]
    events = build_m01_events(run_id=run_id, actions=actions, decisions=decisions)
    metrics = build_m01_metrics(run_id=run_id, actions=actions, decisions=decisions, events=events)
    trace = build_m01_trace(run_id=run_id, case_id=case_id, actions=actions, decisions=decisions)

    manifest = build_m01_manifest(run_id=run_id, scenario=scenario)
    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_m01_buyer_approver_pilot_reference",
            "phase": "P8",
            "step": "M01 buyer+approver multi-role pilot execution",
            "source_scenario": org_payment_scenario_ref(scenario_id),
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(output_dir / "odd_social.md", m01_odd_social_note(scenario))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", m01_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", m01_final_state(run_id, case_id, scenario, actions, decisions))
    write_jsonl(output_dir / "messages.jsonl", messages_with_response)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "buyer.json", buyer_result.action_menu)
    write_json(output_dir / "action_menus" / "approver.json", approver_result.action_menu)
    write_json(output_dir / "parser_results" / "buyer.json", buyer_result.parser_result)
    write_json(output_dir / "parser_results" / "approver.json", approver_result.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "buyer.jsonl", buyer_result.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "approver.jsonl", approver_result.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", m01_reviewer_notes(run_id, buyer_provider, approver_provider, scenario, actions, decisions))
    write_text(output_dir / "reconstruction-checklist.md", m01_reconstruction_checklist())
    write_role_llm_artifact(output_dir, buyer_result)
    write_role_llm_artifact(output_dir, approver_result)
    return output_dir


def generate_role_action(
    *,
    provider: LLMProvider,
    role: str,
    prompt_template: Path,
    run_id: str,
    case_id: str,
    action_id: str,
    turn: int,
    scenario: dict[str, Any],
    action_menu: dict[str, Any],
    allowed_source_refs: list[str],
    prompt_replacements: dict[str, str],
    attempts: int = 2,
) -> RoleActionResult:
    schema = load_action_schema()
    expected_fields = {
        "action_id": action_id,
        "run_id": run_id,
        "turn": turn,
        "proposed_by": role,
        "case_id": case_id,
        "human_authored": False,
    }
    prompt_text = render_role_prompt(
        prompt_template=prompt_template,
        run_id=run_id,
        case_id=case_id,
        action_id=action_id,
        turn=turn,
        scenario=scenario,
        action_menu=action_menu,
        allowed_source_refs=allowed_source_refs,
        schema=schema,
        prompt_replacements=prompt_replacements,
    )

    proposal_attempts: list[dict[str, Any]] = []
    last_error: ActionParseError | None = None
    for attempt in range(1, attempts + 1):
        user_prompt = prompt_text
        if last_error is not None:
            user_prompt += f"\n\nPrevious output failed local validation: {last_error}. Return corrected JSON only."
        response = provider.complete_json(
            LLMRequest(
                system_prompt=role_system_prompt(role),
                user_prompt=user_prompt,
                schema_name="action_proposal_v0_1",
                schema=schema,
            )
        )
        try:
            action = parse_action_proposal(
                response.text,
                expected_fields=expected_fields,
                allowed_source_refs=set(allowed_source_refs),
                schema=schema,
            )
            validate_role_menu_selection(action, action_menu)
            proposal_attempts.append(
                {
                    "attempt": attempt,
                    "role": role,
                    "status": "accepted_by_parser",
                    "selected_action_type": action["action_type"],
                    "selected_target_role": action["target_role"],
                    "selected_action_id": action["action_id"],
                    "parser_error": None,
                }
            )
            return RoleActionResult(
                role=role,
                action=action,
                prompt_text=user_prompt,
                response=response,
                action_menu=action_menu,
                parser_result=role_parser_result(role, action, action_menu, proposal_attempts),
                proposal_attempts=proposal_attempts,
            )
        except ActionParseError as exc:
            last_error = exc
            proposal_attempts.append(
                {
                    "attempt": attempt,
                    "role": role,
                    "status": "rejected_by_parser",
                    "parser_error": str(exc),
                    "raw_text": response.text,
                }
            )

    raise ActionParseError(f"{role} proposal failed validation after {attempts} attempts: {last_error}")


def render_role_prompt(
    *,
    prompt_template: Path,
    run_id: str,
    case_id: str,
    action_id: str,
    turn: int,
    scenario: dict[str, Any],
    action_menu: dict[str, Any],
    allowed_source_refs: list[str],
    schema: dict[str, Any],
    prompt_replacements: dict[str, str],
) -> str:
    text = prompt_template.read_text(encoding="utf-8")
    replacements = {
        "{{scenario_id}}": scenario["id"],
        "{{scenario_name}}": scenario["name"],
        "{{action_id}}": action_id,
        "{{run_id}}": run_id,
        "{{turn}}": str(turn),
        "{{case_id}}": case_id,
        "{{action_menu_json}}": json.dumps(action_menu, indent=2),
        "{{allowed_source_refs}}": "\n".join(f"- {ref}" for ref in allowed_source_refs),
        "{{schema_json}}": json.dumps(schema, indent=2),
    }
    replacements.update(prompt_replacements)
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    return text


def role_system_prompt(role: str) -> str:
    return f"""You are a controlled {role} actor in a research simulation.
Choose one action from the provided constrained action menu.
Return exactly one schema-valid JSON action proposal for the selected action.
Do not invent actions outside the menu. Do not simulate other roles.
Do not bypass the Game Master. Do not make claims outside the provided scenario context."""


def validate_role_menu_selection(action: dict[str, Any], action_menu: dict[str, Any]) -> None:
    for item in action_menu["allowed_actions"]:
        if action["action_type"] == item["action_type"]:
            if action.get("target_role") != item["target_role"]:
                raise ActionParseError(
                    f"target_role for {action['action_type']} must be {item['target_role']!r}, "
                    f"got {action.get('target_role')!r}"
                )
            return
    allowed = [item["action_type"] for item in action_menu["allowed_actions"]]
    raise ActionParseError(f"action_type must be selected from menu {allowed!r}, got {action['action_type']!r}")


def role_parser_result(
    role: str,
    action: dict[str, Any],
    action_menu: dict[str, Any],
    attempts: list[dict[str, Any]],
) -> dict[str, Any]:
    rejected = [attempt for attempt in attempts if attempt["status"] == "rejected_by_parser"]
    return {
        "parser_status": "accepted",
        "role": role,
        "selected_action_type": action["action_type"],
        "selected_target_role": action["target_role"],
        "selected_action_id": action["action_id"],
        "allowed_action_types": [item["action_type"] for item in action_menu["allowed_actions"]],
        "attempt_count": len(attempts),
        "invalid_or_rejected_proposals": rejected,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m01_buyer_action_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_4_after_vendor_and_requester_pressure_before_explicit_approval",
        "allowed_actions": BUYER_ACTION_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m01_approver_action_menu() -> dict[str, Any]:
    return {
        "menu_id": APPROVER_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "approver",
        "decision_point": "turn_6_after_buyer_action_and_game_master_decision",
        "allowed_actions": APPROVER_ACTION_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def decide_m01_buyer_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    scenario_control_mode = scenario.get("control_mode", "soft")
    decisions_by_action_type = {
        "request_approval": {
            "decision": "proceeds",
            "rationale": "The buyer request is routed to the approver while preserving the approval-control boundary.",
            "state_delta_summary": "Approval request is opened; approval remains unresolved until the approver responds.",
            "review_flags": ["evidence_gap"],
            "missing_evidence": ["explicit approver decision"],
        },
        "request_approval_status": {
            "decision": "proceeds",
            "rationale": "The buyer clarification request is routed to the approver without treating clarification as approval.",
            "state_delta_summary": "Approval status clarification is requested; payment status remains not prepared.",
            "review_flags": ["evidence_gap", "communication_breakdown"],
            "missing_evidence": ["explicit approval status"],
        },
        "escalate": {
            "decision": "proceeds_with_note",
            "rationale": "The buyer escalation is routed to the approver as a low-risk way to resolve pressure and missing approval evidence.",
            "state_delta_summary": "Escalation is opened; payment status remains not prepared.",
            "review_flags": ["evidence_gap", "communication_breakdown"],
            "missing_evidence": ["explicit approver decision"],
        },
    }
    action_type = action["action_type"]
    if action_type not in decisions_by_action_type:
        raise ValueError(f"no M01 buyer Game Master decision for action_type {action_type}")
    decision = dict(decisions_by_action_type[action_type])
    decision.update(
        {
            "decision_id": "D001",
            "run_id": run_id,
            "turn": action["turn"],
            "action_id": action["action_id"],
            "control_mode": scenario_control_mode,
            "rule_refs": ["protocols/multi-role/multi-role-pilot-v0.1.md#game-master-rules"],
            "evidence_refs": [action["action_id"], "action_menus/buyer.json"],
            "human_authored": False,
        }
    )
    return decision


def decide_m01_approver_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    scenario_control_mode = scenario.get("control_mode", "soft")
    decisions_by_action_type = {
        "approve_payment": {
            "decision": "proceeds",
            "rationale": "The approver records explicit approval, making approval evidence available to the buyer-side process.",
            "state_delta_summary": "Explicit approval is recorded as available evidence; payment handling remains subject to later process steps.",
            "review_flags": [],
        },
        "reject_payment": {
            "decision": "proceeds",
            "rationale": "The approver records explicit rejection under the current evidence.",
            "state_delta_summary": "Explicit rejection is recorded; payment should not proceed under current evidence.",
            "review_flags": ["control_block"],
        },
        "request_more_evidence": {
            "decision": "proceeds",
            "rationale": "The approver asks for missing evidence before approving or rejecting.",
            "state_delta_summary": "Evidence request is recorded; approval remains unresolved.",
            "review_flags": ["evidence_gap"],
            "missing_evidence": ["additional support requested by approver"],
        },
        "provide_ambiguous_guidance": {
            "decision": "proceeds_with_note",
            "rationale": "Ambiguous approver guidance is recorded but is not treated as explicit approval.",
            "state_delta_summary": "Ambiguous guidance is recorded; approval remains unresolved as explicit approval evidence.",
            "review_flags": ["communication_breakdown", "responsibility_diffusion", "evidence_gap"],
            "missing_evidence": ["explicit approval or rejection"],
        },
        "escalate": {
            "decision": "proceeds_with_note",
            "rationale": "The approver escalates instead of approving or rejecting under current evidence.",
            "state_delta_summary": "Escalation path is recorded; approval remains unresolved.",
            "review_flags": ["communication_breakdown"],
            "missing_evidence": ["final approver decision"],
        },
    }
    action_type = action["action_type"]
    if action_type not in decisions_by_action_type:
        raise ValueError(f"no M01 approver Game Master decision for action_type {action_type}")
    decision = dict(decisions_by_action_type[action_type])
    decision.update(
        {
            "decision_id": "D002",
            "run_id": run_id,
            "turn": action["turn"],
            "action_id": action["action_id"],
            "control_mode": scenario_control_mode,
            "rule_refs": ["protocols/multi-role/multi-role-pilot-v0.1.md#game-master-rules"],
            "evidence_refs": [action["action_id"], "action_menus/approver.json", "A001", "D001"],
            "human_authored": False,
        }
    )
    return decision


def buyer_context(run_id: str, case_id: str, messages: list[dict[str, Any]], scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    fixed = scenario.get("fixed_variables", {})
    initial_state = scenario.get("initial_state", {})
    return f"""Run id: {run_id}
Case id: {case_id}
Scenario: {scenario["id"]} {scenario["name"]}.
Control mode: {scenario["control_mode"]}.
Policy ambiguity: {manipulated.get("policy_ambiguity")}.
Deadline pressure: {manipulated.get("deadline_pressure")}.
Role overlap: {manipulated.get("role_overlap")}.
Audit presence: {manipulated.get("audit_presence")}.
External pressure: {manipulated.get("external_pressure")}.
Information asymmetry: {fixed.get("information_asymmetry")}.
Initial state: vendor invoice is present; business reason is present; explicit approval is absent.
Approver available: {initial_state.get("approver_is_available")}.
Accountant available: {initial_state.get("accountant_is_available")}.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
Buyer decision point: choose one approver-facing action from the frozen M01 buyer action menu. The choice must preserve the Game Master boundary and remain within the evidence available so far.
"""


def approver_case_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    return f"""Run id: {run_id}
Case id: {case_id}
Scenario: {scenario["id"]} {scenario["name"]}.
Control mode: {scenario["control_mode"]}.
Policy ambiguity: {manipulated.get("policy_ambiguity")}.
Deadline pressure: {manipulated.get("deadline_pressure")}.
Role overlap: {manipulated.get("role_overlap")}.
Initial approval status: explicit approval is absent before approver response.
Payment status: not prepared.
"""


def buyer_action_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""Buyer action {action["action_id"]}: `{action["action_type"]}` targeting `{action["target_role"]}`.
Buyer intent: {action["intent"]}
Buyer payload summary: {action["payload_summary"]}
Game Master decision {decision["decision_id"]}: `{decision["decision"]}`.
Game Master state delta: {decision["state_delta_summary"]}
"""


def approver_available_evidence(
    messages: list[dict[str, Any]],
    action: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    return f"""initial_state/case.md: vendor invoice and business reason are present; explicit approval is absent.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
A001: buyer selected `{action["action_type"]}` and cited {', '.join(action["source_refs"])}.
D001: Game Master recorded `{decision["decision"]}` for A001.
"""


def approver_response_message(
    run_id: str,
    case_id: str,
    action: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    return {
        "message_id": "M003",
        "run_id": run_id,
        "turn": 7,
        "case_id": case_id,
        "from_role": "approver",
        "to_role": "buyer",
        "channel": "case_comment",
        "summary": f"Approver selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.",
        "source_refs": ["A002", "D002"],
        "human_authored": False,
    }


def build_m01_events(
    *,
    run_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    buyer_action = actions[0]
    approver_action = actions[1]
    approver_decision = decisions[1]
    events = [
        {
            "event_id": "E001",
            "run_id": run_id,
            "taxonomy_version": "v0.1",
            "event_type": "informal_pressure",
            "turn_start": 2,
            "turn_end": 3,
            "roles_involved": ["vendor", "requester", "buyer"],
            "severity": 1,
            "confidence": "high",
            "description": "Vendor and requester pressure create urgency before the buyer action choice.",
            "source_refs": ["M001", "M002", "T002", "T003"],
            "coded_by": "scripted event coder for M01 buyer+approver pilot",
            "review_status": "proposed",
            "claim_use_limit": CLAIM_BOUNDARY,
            "human_authored": False,
        },
        {
            "event_id": "E002",
            "run_id": run_id,
            "taxonomy_version": "v0.1",
            "event_type": "evidence_gap",
            "turn_start": 1,
            "turn_end": buyer_action["turn"],
            "roles_involved": ["requester", "buyer", "approver"],
            "severity": 1,
            "confidence": "high",
            "description": "Explicit approval is absent when the buyer routes the case to the approver.",
            "source_refs": ["initial_state/case.md", "A001", "D001", "T005", "T006"],
            "coded_by": "scripted event coder for M01 buyer+approver pilot",
            "review_status": "proposed",
            "claim_use_limit": CLAIM_BOUNDARY,
            "human_authored": False,
        },
    ]
    approver_event = approver_event_for_action(run_id, approver_action, approver_decision)
    if approver_event is not None:
        events.append(approver_event)
    return events


def approver_event_for_action(
    run_id: str,
    action: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any] | None:
    action_type = action["action_type"]
    event_by_action = {
        "approve_payment": None,
        "reject_payment": ("control_block", 2, "Approver records rejection under the current evidence."),
        "request_more_evidence": ("evidence_gap", 1, "Approver requests more evidence instead of approving or rejecting."),
        "provide_ambiguous_guidance": ("communication_breakdown", 2, "Approver provides guidance that is not explicit approval or rejection."),
        "escalate": ("communication_breakdown", 1, "Approver escalates the decision instead of directly approving or rejecting."),
    }
    event_spec = event_by_action[action_type]
    if event_spec is None:
        return None
    event_type, severity, description = event_spec
    alternative_labels = ["responsibility_diffusion"] if action_type == "provide_ambiguous_guidance" else None
    event = {
        "event_id": "E003",
        "run_id": run_id,
        "taxonomy_version": "v0.1",
        "event_type": event_type,
        "turn_start": action["turn"],
        "turn_end": decision["turn"],
        "roles_involved": ["approver", "buyer", "game_master"],
        "severity": severity,
        "confidence": "medium",
        "description": description,
        "source_refs": ["A002", "D002", "T008", "T009"],
        "coded_by": "scripted event coder for M01 buyer+approver pilot",
        "review_status": "proposed",
        "claim_use_limit": CLAIM_BOUNDARY,
        "human_authored": False,
    }
    if alternative_labels:
        event["alternative_labels"] = alternative_labels
        event["notes_on_ambiguity"] = "Generated label is proposed and not human-reviewed; no responsibility-diffusion claim is made."
    return event


def build_m01_metrics(
    *,
    run_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    buyer_action = actions[0]
    approver_action = actions[1]
    event_counts = Counter(event["event_type"] for event in events)
    event_ids = [event["event_id"] for event in events]
    return {
        "run_id": run_id,
        "metrics_version": "v0.1",
        "metrics_record_contract": "v0.1",
        "scenario_id": "S04",
        "review_status": "not_human_reviewed",
        "metrics": [
            {
                "metric_id": "MR001",
                "metric_group": "multi_role_action_path",
                "metric_name": "buyer_selected_action_type",
                "value": buyer_action["action_type"],
                "denominator": "one M01 buyer action selection",
                "source_event_ids": [],
                "source_record_refs": ["A001", "action_menus/buyer.json", "parser_results/buyer.json"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M01 pilot run", "no behavioral claim"],
            },
            {
                "metric_id": "MR002",
                "metric_group": "multi_role_action_path",
                "metric_name": "approver_selected_action_type",
                "value": approver_action["action_type"],
                "denominator": "one M01 approver action selection",
                "source_event_ids": [],
                "source_record_refs": ["A002", "action_menus/approver.json", "parser_results/approver.json"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M01 pilot run", "no behavioral claim"],
            },
            {
                "metric_id": "MR003",
                "metric_group": "multi_role_action_path",
                "metric_name": "paired_buyer_approver_path",
                "value": f"{buyer_action['action_type']} -> {approver_action['action_type']}",
                "denominator": "one paired buyer-to-approver path",
                "source_event_ids": [],
                "source_record_refs": ["A001", "D001", "A002", "D002"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M01 pilot run", "no statistical claim"],
            },
            {
                "metric_id": "MR004",
                "metric_group": "game_master_boundary",
                "metric_name": "gm_decisions_for_llm_actions",
                "value": {
                    "buyer": decisions[0]["decision"],
                    "approver": decisions[1]["decision"],
                },
                "denominator": "two deterministic Game Master decisions",
                "source_event_ids": [],
                "source_record_refs": ["D001", "D002", "gm_decisions.jsonl"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["rule-based Game Master", "single M01 pilot run"],
            },
            {
                "metric_id": "MR005",
                "metric_group": "event_counts",
                "metric_name": "event_count_by_type",
                "value": dict(sorted(event_counts.items())),
                "denominator": f"{len(events)} proposed event records",
                "source_event_ids": event_ids,
                "source_record_refs": ["events.jsonl"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["generated event labels", "not human-reviewed coded evidence"],
            },
            {
                "metric_id": "MR006",
                "metric_group": "auditability",
                "metric_name": "reconstruction_outcome",
                "value": "mechanically_validated_m01_multi_role_pilot_pack",
                "denominator": "not_applicable",
                "source_event_ids": event_ids,
                "source_record_refs": ["reconstruction-checklist.md", "reviewer_notes.md"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M01 pilot run", "no inter-reviewer reliability"],
            },
        ],
    }


def build_m01_trace(
    *,
    run_id: str,
    case_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    buyer_action = actions[0]
    approver_action = actions[1]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 M01 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "message", "M001", case_id, ["vendor", "requester"], "Vendor message is recorded for the S04 pressure condition.", "messages.jsonl", ["E001"]),
        trace_record("T003", run_id, 3, "message", "M002", case_id, ["requester", "buyer"], "Requester message is recorded for the S04 pressure condition.", "messages.jsonl", ["E001"]),
        trace_record("T004", run_id, 4, "review", "action_menus/buyer.json", case_id, ["buyer"], "Frozen M01 buyer action menu is recorded before buyer action selection.", "action_menus/buyer.json"),
        trace_record("T005", run_id, buyer_action["turn"], "action", "A001", case_id, ["buyer", "approver"], f"LLM buyer selects `{buyer_action['action_type']}` from the M01 buyer action menu.", "actions.jsonl", ["E002"]),
        trace_record("T006", run_id, decisions[0]["turn"], "decision", "D001", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[0]['decision']}` for the buyer action.", "gm_decisions.jsonl", ["E002"]),
        trace_record("T007", run_id, 5, "review", "action_menus/approver.json", case_id, ["approver"], "Frozen M01 approver action menu is recorded before approver action selection.", "action_menus/approver.json"),
        trace_record("T008", run_id, approver_action["turn"], "action", "A002", case_id, ["approver", "buyer"], f"LLM approver selects `{approver_action['action_type']}` from the M01 approver action menu.", "actions.jsonl", ["E003"] if approver_action["action_type"] != "approve_payment" else None),
        trace_record("T009", run_id, decisions[1]["turn"], "decision", "D002", case_id, ["approver", "game_master"], f"Game Master records `{decisions[1]['decision']}` for the approver action.", "gm_decisions.jsonl", ["E003"] if approver_action["action_type"] != "approve_payment" else None),
        trace_record("T010", run_id, 7, "message", "M003", case_id, ["approver", "buyer"], "Approver response message is recorded from the accepted approver action and GM decision.", "messages.jsonl"),
        trace_record("T011", run_id, 8, "event", "events.jsonl", case_id, ["vendor", "requester", "buyer", "approver", "game_master"], "Scripted event coder emits proposed events for the M01 pilot run.", "events.jsonl"),
        trace_record("T012", run_id, 9, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits M01 metrics derived from actions, GM decisions, and events.", "metrics.json"),
    ]


def build_m01_manifest(run_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario["id"],
        scenario_ref=org_payment_scenario_ref(scenario["id"]),
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="M01 buyer+approver OpenAI LLM action selections from frozen role menus; provider randomness is not explicitly seeded; aggregate reporting is handled outside the evidence pack",
        authored_by="src/social_sim M01 buyer+approver multi-role pilot runner",
        artifact_inventory_extra={
            "action_menus/buyer.json": "present",
            "action_menus/approver.json": "present",
            "parser_results/buyer.json": "present",
            "parser_results/approver.json": "present",
            "proposal_attempts/buyer.jsonl": "present",
            "proposal_attempts/approver.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "M01 only; no M02-M05 execution",
            "buyer and approver are the only LLM-controlled roles",
            "requester, accountant, and vendor remain scripted or rule-based",
            "Game Master remains deterministic and menu-aware",
            "no multi-role baseline",
            "no model comparison",
            "no human review",
            "no human behavior claim",
            "no real-world organization claim",
            "no statistical claim",
        ],
    )
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    return manifest


def read_m01_run_record(index: int, run_id: str, pack_dir: Path) -> M01RunRecord:
    buyer_parser = load_json(pack_dir / "parser_results" / "buyer.json")
    approver_parser = load_json(pack_dir / "parser_results" / "approver.json")
    buyer_attempts = load_jsonl(pack_dir / "proposal_attempts" / "buyer.jsonl")
    approver_attempts = load_jsonl(pack_dir / "proposal_attempts" / "approver.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    buyer_output = load_json(pack_dir / "llm_outputs" / "buyer_A001_free_choice.json")
    approver_output = load_json(pack_dir / "llm_outputs" / "approver_A002_free_choice.json")
    decision_by_action = {decision["action_id"]: decision for decision in decisions}
    return M01RunRecord(
        index=index,
        run_id=run_id,
        buyer_action_type=buyer_parser["selected_action_type"],
        buyer_target_role=buyer_parser["selected_target_role"],
        buyer_parser_status=buyer_parser["parser_status"],
        buyer_attempt_count=buyer_parser["attempt_count"],
        buyer_rejected_attempt_count=sum(1 for attempt in buyer_attempts if attempt.get("status") != "accepted_by_parser"),
        buyer_gm_decision=decision_by_action["A001"]["decision"],
        approver_action_type=approver_parser["selected_action_type"],
        approver_target_role=approver_parser["selected_target_role"],
        approver_parser_status=approver_parser["parser_status"],
        approver_attempt_count=approver_parser["attempt_count"],
        approver_rejected_attempt_count=sum(1 for attempt in approver_attempts if attempt.get("status") != "accepted_by_parser"),
        approver_gm_decision=decision_by_action["A002"]["decision"],
        validation_status="PASS",
        buyer_model_version=buyer_output.get("response_metadata", {}).get("model_version"),
        approver_model_version=approver_output.get("response_metadata", {}).get("model_version"),
        pack_dir=pack_dir,
    )


def copy_m01_representatives(
    *,
    records: list[M01RunRecord],
    curated_output: Path,
) -> list[dict[str, str]]:
    selected: dict[tuple[str, str], M01RunRecord] = {}
    for record in records:
        selected.setdefault((record.buyer_action_type, record.approver_action_type), record)

    representatives: list[dict[str, str]] = []
    for (buyer_action, approver_action), record in sorted(selected.items()):
        directory_name = f"buyer-{buyer_action}_approver-{approver_action}-run-{record.index:03d}"
        pack_path = Path("representative-evidence-packs") / directory_name
        validation_path = Path("representative-validation-outputs") / f"{directory_name}.md"
        shutil.copytree(record.pack_dir, curated_output / pack_path)
        validation_report = validate_pack(curated_output / pack_path).as_markdown()
        write_text(curated_output / validation_path, validation_report)
        representatives.append(
            {
                "buyer_action_type": buyer_action,
                "approver_action_type": approver_action,
                "paired_path": f"{buyer_action} -> {approver_action}",
                "run_id": record.run_id,
                "evidence_pack": pack_path.as_posix(),
                "validation_output": validation_path.as_posix(),
            }
        )
    return representatives


def build_m01_execution_manifest(
    *,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[M01RunRecord],
    exclusions: list[M01ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "scenario_id": "S04",
        "provider": provider_label(buyer_provider, approver_provider),
        "model": model_label(buyer_provider, approver_provider),
        "observed_model_versions": model_versions(records),
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "attempted_runs": M01_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "failed_runs": len(exclusions),
        "replacement_policy": "excluded runs are not replaced in M01",
        "llm_controlled_roles": ["buyer", "approver"],
        "scripted_or_rule_based_roles": ["requester", "accountant", "vendor"],
        "game_master": "deterministic_menu_aware_rules",
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "approver_prompt_ref": APPROVER_PROMPT_REF,
        "buyer_action_menu_id": BUYER_ACTION_MENU_ID,
        "approver_action_menu_id": APPROVER_ACTION_MENU_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
    }


def build_m01_aggregate(
    *,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    batch_id: str,
    records: list[M01RunRecord],
    exclusions: list[M01ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    buyer_counts = Counter(record.buyer_action_type for record in records)
    approver_counts = Counter(record.approver_action_type for record in records)
    paired_paths = Counter(f"{record.buyer_action_type} -> {record.approver_action_type}" for record in records)
    buyer_gm: dict[str, Counter[str]] = defaultdict(Counter)
    approver_gm: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        buyer_gm[record.buyer_action_type][record.buyer_gm_decision] += 1
        approver_gm[record.approver_action_type][record.approver_gm_decision] += 1
    exclusion_counts = Counter(exclusion.exclusion_reason for exclusion in exclusions)
    accepted_runs = len(records)

    return {
        "pilot_id": PILOT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "scenario_id": "S04",
        "attempted_runs": M01_RUN_COUNT,
        "accepted_runs": accepted_runs,
        "excluded_runs": len(exclusions),
        "provider": provider_label(buyer_provider, approver_provider),
        "model": model_label(buyer_provider, approver_provider),
        "observed_model_versions": execution_manifest["observed_model_versions"],
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "approver_prompt_ref": APPROVER_PROMPT_REF,
        "buyer_action_menu_id": BUYER_ACTION_MENU_ID,
        "approver_action_menu_id": APPROVER_ACTION_MENU_ID,
        "llm_controlled_roles": ["buyer", "approver"],
        "scripted_or_rule_based_roles": ["requester", "accountant", "vendor"],
        "game_master": "deterministic_menu_aware_rules",
        "claim_boundary": CLAIM_BOUNDARY,
        "buyer_selected_action_counts": dict(sorted(buyer_counts.items())),
        "approver_selected_action_counts": dict(sorted(approver_counts.items())),
        "paired_buyer_approver_path_counts": dict(sorted(paired_paths.items())),
        "buyer_parser_summary": parser_summary(records, role="buyer", exclusions=exclusions),
        "approver_parser_summary": parser_summary(records, role="approver", exclusions=exclusions),
        "gm_decisions_by_role_and_selected_action": {
            "buyer": {action: dict(sorted(counter.items())) for action, counter in sorted(buyer_gm.items())},
            "approver": {action: dict(sorted(counter.items())) for action, counter in sorted(approver_gm.items())},
        },
        "validation_summary": {
            "pass": accepted_runs,
            "fail": exclusion_counts.get("validation_failure", 0),
            "pass_rate_included": 1.0 if accepted_runs else 0.0,
        },
        "exclusion_summary": dict(sorted(exclusion_counts.items())),
        "representative_evidence_packs": representatives,
        "limitations": [
            "artificial organization only",
            "M01 pilot only",
            "buyer + approver LLM control only",
            "requester, accountant, and vendor are scripted or rule-based",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no human behavior claim",
            "no general LLM behavior claim",
            "no real-world organization claim",
            "no compliance, legal, audit, or operational sufficiency claim",
            "no statistical significance claim",
        ],
        "allowed_claim": "Under the frozen M01 artificial organization protocol, buyer+approver LLM pilot runs produced the recorded buyer action, approver action, paired path, parser, GM decision, and validation outcomes.",
        "forbidden_claims": [
            "responsibility diffusion has been reproduced",
            "human organization behavior has been simulated",
            "S04 causes ambiguity or failure",
            "hard control effectiveness has been shown",
            "multi-role baseline is complete",
            "this proves institutional failure",
            "this is statistically meaningful",
            "this generalizes to humans or real organizations",
        ],
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
    }


def parser_summary(records: list[M01RunRecord], *, role: str, exclusions: list[M01ExcludedRunRecord]) -> dict[str, int]:
    if role == "buyer":
        statuses = [record.buyer_parser_status for record in records]
        attempts = [record.buyer_attempt_count for record in records]
        rejected = [record.buyer_rejected_attempt_count for record in records]
    elif role == "approver":
        statuses = [record.approver_parser_status for record in records]
        attempts = [record.approver_attempt_count for record in records]
        rejected = [record.approver_rejected_attempt_count for record in records]
    else:
        raise ValueError(f"unknown role {role}")
    return {
        "runs_with_parser_acceptance": sum(1 for status in statuses if status == "accepted"),
        "total_attempts": sum(attempts),
        "total_retries": sum(max(attempt - 1, 0) for attempt in attempts),
        "total_rejected_or_invalid_attempts": sum(rejected),
        "runs_with_retries": sum(1 for attempt in attempts if attempt > 1),
        "parser_failures": sum(
            1
            for exclusion in exclusions
            if exclusion.exclusion_reason == "parser_failure" and (role in exclusion.detail.lower() or role in exclusion.stage.lower())
        ),
    }


def render_m01_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "pilot_id",
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "buyer_selected_action_counts",
            "approver_selected_action_counts",
            "paired_path_counts",
            "buyer_retries",
            "approver_retries",
            "validation_pass",
            "validation_fail",
            "exclusion_summary",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerow(
        {
            "pilot_id": aggregate["pilot_id"],
            "scenario_id": aggregate["scenario_id"],
            "attempted_runs": aggregate["attempted_runs"],
            "accepted_runs": aggregate["accepted_runs"],
            "excluded_runs": aggregate["excluded_runs"],
            "buyer_selected_action_counts": compact_counts(aggregate["buyer_selected_action_counts"]),
            "approver_selected_action_counts": compact_counts(aggregate["approver_selected_action_counts"]),
            "paired_path_counts": compact_counts(aggregate["paired_buyer_approver_path_counts"]),
            "buyer_retries": aggregate["buyer_parser_summary"]["total_retries"],
            "approver_retries": aggregate["approver_parser_summary"]["total_retries"],
            "validation_pass": aggregate["validation_summary"]["pass"],
            "validation_fail": aggregate["validation_summary"]["fail"],
            "exclusion_summary": compact_counts(aggregate["exclusion_summary"]),
        }
    )
    return output.getvalue()


def render_m01_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# M01 Buyer+Approver Multi-Role Pilot Summary",
        "",
        f"Pilot id: `{aggregate['pilot_id']}`",
        f"Protocol: [{aggregate['protocol_ref']}](../../../{aggregate['protocol_ref']})",
        f"Execution manifest: [execution-manifest.json](execution-manifest.json)",
        f"Scenario id: `{aggregate['scenario_id']}`",
        f"Provider: `{aggregate['provider']}`",
        f"Model: `{aggregate['model']}`",
        f"Observed model versions: {format_inline_list(aggregate['observed_model_versions'])}",
        f"Attempted runs: {aggregate['attempted_runs']}",
        f"Accepted runs: {aggregate['accepted_runs']}",
        f"Excluded runs: {aggregate['excluded_runs']}",
        "LLM-controlled roles: `buyer`, `approver`",
        "Scripted or rule-based roles: `requester`, `accountant`, `vendor`",
        f"Game Master: `{aggregate['game_master']}`",
        f"Buyer prompt: [{aggregate['buyer_prompt_ref']}](../../../{aggregate['buyer_prompt_ref']})",
        f"Approver prompt: [{aggregate['approver_prompt_ref']}](../../../{aggregate['approver_prompt_ref']})",
        f"Buyer action menu id: `{aggregate['buyer_action_menu_id']}`",
        f"Approver action menu id: `{aggregate['approver_action_menu_id']}`",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        aggregate["allowed_claim"],
        "",
        "These results remain bounded to the frozen artificial M01 setup and do not support statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.",
        "",
        "## Buyer Action Counts",
        "",
        "| action_type | count |",
        "|---|---:|",
    ]
    for action_type, count in aggregate["buyer_selected_action_counts"].items():
        lines.append(f"| `{action_type}` | {count} |")

    lines.extend(["", "## Approver Action Counts", "", "| action_type | count |", "|---|---:|"])
    for action_type, count in aggregate["approver_selected_action_counts"].items():
        lines.append(f"| `{action_type}` | {count} |")

    lines.extend(["", "## Paired Buyer -> Approver Paths", "", "| paired path | count |", "|---|---:|"])
    for paired_path, count in aggregate["paired_buyer_approver_path_counts"].items():
        lines.append(f"| `{paired_path}` | {count} |")

    lines.extend(["", "## Parser Summary", ""])
    for role in ["buyer", "approver"]:
        parser = aggregate[f"{role}_parser_summary"]
        lines.extend(
            [
                f"### {role.title()}",
                "",
                f"- Runs with parser acceptance: {parser['runs_with_parser_acceptance']}",
                f"- Total attempts: {parser['total_attempts']}",
                f"- Total retries: {parser['total_retries']}",
                f"- Rejected or invalid proposals: {parser['total_rejected_or_invalid_attempts']}",
                f"- Parser failures: {parser['parser_failures']}",
                "",
            ]
        )

    lines.extend(["## Game Master Decisions", "", "| role | selected action | GM decision | count |", "|---|---|---|---:|"])
    for role, actions in aggregate["gm_decisions_by_role_and_selected_action"].items():
        for action_type, decisions in actions.items():
            for decision, count in decisions.items():
                lines.append(f"| `{role}` | `{action_type}` | `{decision}` | {count} |")

    validation = aggregate["validation_summary"]
    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Validation pass: {validation['pass']}",
            f"- Validation fail: {validation['fail']}",
            f"- Exclusions by reason: {format_counts(aggregate['exclusion_summary'])}",
            "",
            "## Run Summary",
            "",
            "| run_id | buyer action | approver action | buyer GM | approver GM | buyer attempts | approver attempts | validation |",
            "|---|---|---|---|---|---:|---:|---|",
        ]
    )
    for record in aggregate["runs"]:
        lines.append(
            "| "
            f"`{record['run_id']}` | "
            f"`{record['buyer_action_type']}` | "
            f"`{record['approver_action_type']}` | "
            f"`{record['buyer_gm_decision']}` | "
            f"`{record['approver_gm_decision']}` | "
            f"{record['buyer_attempt_count']} | "
            f"{record['approver_attempt_count']} | "
            f"{record['validation_status']} |"
        )

    lines.extend(
        [
            "",
            "## Representative Evidence",
            "",
            "| paired path | run_id | evidence pack | validation output |",
            "|---|---|---|---|",
        ]
    )
    for representative in aggregate["representative_evidence_packs"]:
        lines.append(
            "| "
            f"`{representative['paired_path']}` | "
            f"`{representative['run_id']}` | "
            f"[pack]({representative['evidence_pack']}) | "
            f"[validation]({representative['validation_output']}) |"
        )

    lines.extend(
        [
            "",
            "## Claim Boundary",
            "",
        ]
    )
    lines.extend(f"- {limitation}." for limitation in aggregate["limitations"])
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- M01 is a pilot, not a multi-role baseline.",
            "- Counts are descriptive pilot accounting only.",
            "- Generated event labels are proposed and not human-reviewed coded evidence.",
            "- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.",
        ]
    )
    return "\n".join(lines) + "\n"


def m01_odd_social_note(scenario: dict[str, Any]) -> str:
    return f"""# ODD-Social Extract for generated M01 {scenario["id"]}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario["id"]} {scenario["name"]}
- Control mode: {scenario["control_mode"]}
- Actor mode: M01 buyer+approver OpenAI LLM action selectors; requester, accountant, and vendor scripted or rule-based
- Game Master / Arbiter mode: deterministic menu-aware rule stub
- Claim boundary: {CLAIM_BOUNDARY}

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def m01_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    return f"""# Initial State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

The requester has a legitimate vendor invoice that requires documented approval before payment handling.

Initial approval status: not requested.

Initial evidence status: invoice and business reason are present; approval record is absent.

Scenario conditions:

- Policy ambiguity: `{manipulated.get("policy_ambiguity")}`
- Deadline pressure: `{manipulated.get("deadline_pressure")}`
- Role overlap: `{manipulated.get("role_overlap")}`
- Audit presence: `{manipulated.get("audit_presence")}`
- Control mode: `{scenario.get("control_mode")}`
- M01 roles: buyer and approver are LLM-controlled; requester, accountant, and vendor are scripted or rule-based.
"""


def m01_final_state(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

Buyer selected action: `{actions[0]["action_type"]}`
Buyer target role: `{actions[0]["target_role"]}`
Buyer Game Master decision: `{decisions[0]["decision"]}`

Approver selected action: `{actions[1]["action_type"]}`
Approver target role: `{actions[1]["target_role"]}`
Approver Game Master decision: `{decisions[1]["decision"]}`

Final state delta: {decisions[1]["state_delta_summary"]}

Claim boundary: this final state supports one M01 multi-role pilot observation only. Aggregate pilot accounting is reported separately.
"""


def m01_reviewer_notes(
    run_id: str,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    return f"""# Generated M01 Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Protocol: `{PROTOCOL_REF}`
Runner: `src/social_sim`

This evidence pack is one M01 buyer+approver multi-role pilot run generated under the frozen M01 protocol.

Only the `buyer` and `approver` roles are LLM-controlled. The requester, accountant, and vendor records remain scripted or rule-based. The Game Master remains deterministic and menu-aware.

Buyer provider/model: {buyer_provider.provider} / {buyer_provider.model}
Approver provider/model: {approver_provider.provider} / {approver_provider.model}
Control mode: {scenario["control_mode"]}

Buyer selected action: `{actions[0]["action_type"]}`
Buyer Game Master decision: `{decisions[0]["decision"]}`
Approver selected action: `{actions[1]["action_type"]}`
Approver Game Master decision: `{decisions[1]["decision"]}`

This pack supports mechanical reconstruction of one M01 pilot run and the aggregate M01 accounting reported outside the pack.

It is not a human review, multi-role baseline, statistical significance claim, model comparison, real-world behavior claim, or human behavior claim.
"""


def m01_reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Scripted requester/vendor messages written | Pass |
| Buyer action menu written | Pass |
| Buyer LLM-selected action proposal written | Pass |
| Buyer parser result written | Pass |
| Buyer proposal attempts written | Pass |
| Buyer Game Master decision written | Pass |
| Approver action menu written | Pass |
| Approver LLM-selected action proposal written | Pass |
| Approver parser result written | Pass |
| Approver proposal attempts written | Pass |
| Approver Game Master decision written | Pass |
| Proposed events written | Pass |
| Metrics written | Pass |
| Final state written | Pass |

The validator is the source of mechanical validation for this generated pack.
"""


def write_role_llm_artifact(output_dir: Path, result: RoleActionResult) -> None:
    action_id = result.action["action_id"]
    write_text(output_dir / "llm_prompts" / f"{result.role}_{action_id}_free_choice.md", result.prompt_text)
    write_json(
        output_dir / "llm_outputs" / f"{result.role}_{action_id}_free_choice.json",
        {
            "provider": result.response.provider,
            "model": result.response.model,
            "role": result.role,
            "action_id": action_id,
            "raw_text": result.response.text,
            "parsed_action": result.action,
            "parser_result": result.parser_result,
            "response_metadata": response_metadata(result.response.raw_response),
        },
    )


def record_to_dict(record: M01RunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "buyer_action_type": record.buyer_action_type,
        "buyer_target_role": record.buyer_target_role,
        "buyer_parser_status": record.buyer_parser_status,
        "buyer_attempt_count": record.buyer_attempt_count,
        "buyer_rejected_attempt_count": record.buyer_rejected_attempt_count,
        "buyer_gm_decision": record.buyer_gm_decision,
        "approver_action_type": record.approver_action_type,
        "approver_target_role": record.approver_target_role,
        "approver_parser_status": record.approver_parser_status,
        "approver_attempt_count": record.approver_attempt_count,
        "approver_rejected_attempt_count": record.approver_rejected_attempt_count,
        "approver_gm_decision": record.approver_gm_decision,
        "validation_status": record.validation_status,
        "buyer_model_version": record.buyer_model_version,
        "approver_model_version": record.approver_model_version,
    }


def exclusion_to_dict(exclusion: M01ExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_or_api_failure"
    name = exc.__class__.__name__.lower()
    message = str(exc).lower()
    if "parse" in name or "parser" in message or "schema" in message or "json" in message:
        return "parser_failure"
    if "provider" in name or "api" in message or "openai" in message or "http" in message:
        return "provider_or_api_failure"
    return "generation_failure"


def failed_validation_markdown(pack_dir: Path, detail: str) -> str:
    return "\n".join(
        [
            "# Evidence Pack Validation Output",
            "",
            f"Evidence pack: `{pack_dir.as_posix()}`",
            "",
            "Result: FAIL",
            "",
            "## Failure",
            "",
            detail,
            "",
            "## Boundary",
            "",
            "This validation is mechanical. It does not support statistical claims or real-world behavior claims.",
            "",
        ]
    )


def provider_label(buyer_provider: LLMProvider, approver_provider: LLMProvider) -> str:
    if buyer_provider.provider == approver_provider.provider:
        return buyer_provider.provider
    return f"buyer:{buyer_provider.provider}; approver:{approver_provider.provider}"


def model_label(buyer_provider: LLMProvider, approver_provider: LLMProvider) -> str:
    if buyer_provider.model == approver_provider.model:
        return buyer_provider.model
    return f"buyer:{buyer_provider.model}; approver:{approver_provider.model}"


def model_versions(records: list[M01RunRecord]) -> list[str]:
    values = {record.buyer_model_version for record in records if record.buyer_model_version}
    values.update(record.approver_model_version for record in records if record.approver_model_version)
    return sorted(values)


def compact_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "`none`"
    return ", ".join(f"`{key}`: {value}" for key, value in sorted(counts.items()))


def format_inline_list(values: list[str]) -> str:
    if not values:
        return "`not returned`"
    return ", ".join(f"`{value}`" for value in values)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
