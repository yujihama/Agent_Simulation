from __future__ import annotations

import csv
import io
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import ValidationError, validate_pack

from .action_parser import ActionParseError
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .free_choice_runner import scenario_case_id
from .llm_actor import LLMProvider, LLMProviderError
from .multirole_runner import (
    RoleActionResult,
    classify_exception,
    compact_counts,
    failed_validation_markdown,
    format_counts,
    format_inline_list,
    generate_role_action,
    load_json,
    load_jsonl,
    now_utc,
)
from .repeated_runner import require_new_or_empty
from .runner import build_manifest, response_metadata, trace_record
from .scenario_loader import dump_yaml, load_s04, org_payment_scenario_ref


PILOT_ID = "M03"
PROTOCOL_ID = "m03-buyer-approver-accountant-coordination-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md"
DEFAULT_M03_BATCH_ID = "m03-buyer-approver-accountant-coordination-pilot-0001"
M03_RUN_COUNT = 5
CLAIM_BOUNDARY = "multi_role_coordination_pilot_observation_only"

BUYER_PROMPT_REF = "prompts/org-payment/buyer-free-choice-action-v0.1.md"
APPROVER_PROMPT_REF = "prompts/org-payment/approver-multirole-action-v0.1.md"
ACCOUNTANT_PROMPT_REF = "prompts/org-payment/accountant-free-choice-action-v0.1.md"

BUYER_APPROVAL_REQUEST_MENU_ID = "org_payment_m03_buyer_approval_request_menu_v0.1"
APPROVER_ACTION_MENU_ID = "org_payment_m03_approver_action_menu_v0.1"
BUYER_ACCOUNTING_HANDOFF_MENU_ID = "org_payment_m03_buyer_accounting_handoff_menu_v0.1"
ACCOUNTANT_ACTION_MENU_ID = "org_payment_m03_accountant_action_menu_v0.1"

ROOT = Path(__file__).resolve().parents[2]
BUYER_PROMPT_TEMPLATE = ROOT / BUYER_PROMPT_REF
APPROVER_PROMPT_TEMPLATE = ROOT / APPROVER_PROMPT_REF
ACCOUNTANT_PROMPT_TEMPLATE = ROOT / ACCOUNTANT_PROMPT_REF

BUYER_APPROVAL_ALLOWED_REFS = ["initial_state/case.md", "M001", "M002", "T001", "T002", "T003", "T004"]
APPROVER_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "M002",
    "A001",
    "D001",
    "T001",
    "T002",
    "T003",
    "T004",
    "T005",
    "T006",
]
BUYER_HANDOFF_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "M002",
    "M003",
    "A001",
    "D001",
    "A002",
    "D002",
    "T001",
    "T002",
    "T003",
    "T004",
    "T005",
    "T006",
    "T007",
    "T008",
    "T009",
]
ACCOUNTANT_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "M002",
    "M003",
    "M004",
    "A001",
    "D001",
    "A002",
    "D002",
    "A003",
    "D003",
    "T001",
    "T002",
    "T003",
    "T004",
    "T005",
    "T006",
    "T007",
    "T008",
    "T009",
    "T010",
    "T011",
    "T012",
]

BUYER_APPROVAL_REQUEST_MENU = [
    {
        "action_type": "request_approval",
        "target_role": "approver",
        "menu_label": "Request explicit approval",
        "selection_boundary": "Ask the approver to approve or reject before payment handling.",
        "allowed_source_refs": BUYER_APPROVAL_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_approval_status",
        "target_role": "approver",
        "menu_label": "Request approval status",
        "selection_boundary": "Ask the approver to clarify whether approval exists or remains unresolved.",
        "allowed_source_refs": BUYER_APPROVAL_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate approval ambiguity",
        "selection_boundary": "Escalate missing approval or ambiguous ownership to the approver.",
        "allowed_source_refs": BUYER_APPROVAL_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]

APPROVER_ACTION_MENU = [
    {
        "action_type": "approve_payment",
        "target_role": "buyer",
        "menu_label": "Approve payment",
        "selection_boundary": "Record explicit approval for the buyer to use in the accounting handoff.",
        "allowed_source_refs": APPROVER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "reject_payment",
        "target_role": "buyer",
        "menu_label": "Reject payment",
        "selection_boundary": "Record explicit rejection under the current evidence.",
        "allowed_source_refs": APPROVER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "buyer",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask for missing evidence before approving or rejecting.",
        "allowed_source_refs": APPROVER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "provide_ambiguous_guidance",
        "target_role": "buyer",
        "menu_label": "Provide ambiguous guidance",
        "selection_boundary": "Respond with approval-related or responsibility-shifting language that does not clearly approve or reject.",
        "allowed_source_refs": APPROVER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "escalate",
        "target_role": "buyer",
        "menu_label": "Escalate",
        "selection_boundary": "Route the decision to a higher or later review path instead of directly approving or rejecting.",
        "allowed_source_refs": APPROVER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]

BUYER_ACCOUNTING_HANDOFF_MENU = [
    {
        "action_type": "submit_payment_request",
        "target_role": "accountant",
        "menu_label": "Submit payment request",
        "selection_boundary": "Hand off the payment request to accounting with the approval state represented from available evidence.",
        "allowed_source_refs": BUYER_HANDOFF_ALLOWED_REFS,
        "game_master_handling": "conditional",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "requester",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask for missing evidence before handing off to accounting.",
        "allowed_source_refs": BUYER_HANDOFF_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "hold_payment",
        "target_role": "accountant",
        "menu_label": "Hold payment",
        "selection_boundary": "Tell accounting that payment should remain held while evidence or approval is unresolved.",
        "allowed_source_refs": BUYER_HANDOFF_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate handoff ambiguity",
        "selection_boundary": "Escalate unresolved approval or handoff ambiguity instead of sending a payment-ready request.",
        "allowed_source_refs": BUYER_HANDOFF_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "mark_approval_inferred",
        "target_role": "accountant",
        "menu_label": "Mark approval inferred",
        "selection_boundary": "Treat approval as inferred from context despite missing explicit approval.",
        "allowed_source_refs": BUYER_HANDOFF_ALLOWED_REFS,
        "game_master_handling": "requires_clarification",
    },
]

ACCOUNTANT_ACTION_MENU = [
    {
        "action_type": "prepare_payment",
        "target_role": "buyer",
        "menu_label": "Prepare payment",
        "selection_boundary": "Prepare payment only when the evidence supports the approval state represented in the handoff.",
        "allowed_source_refs": ACCOUNTANT_ALLOWED_REFS,
        "game_master_handling": "conditional",
    },
    {
        "action_type": "hold_payment",
        "target_role": "buyer",
        "menu_label": "Hold payment",
        "selection_boundary": "Keep payment from moving forward while approval evidence is unresolved.",
        "allowed_source_refs": ACCOUNTANT_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "buyer",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask the buyer for missing approval or supporting evidence.",
        "allowed_source_refs": ACCOUNTANT_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate",
        "selection_boundary": "Escalate unresolved approval, ambiguous guidance, or handoff inconsistency.",
        "allowed_source_refs": ACCOUNTANT_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "authorize_exception_review",
        "target_role": "approver",
        "menu_label": "Authorize exception review",
        "selection_boundary": "Route the case for exception review instead of normal payment preparation.",
        "allowed_source_refs": ACCOUNTANT_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]


@dataclass(frozen=True)
class M03RunRecord:
    index: int
    run_id: str
    buyer_approval_request_action_type: str
    approver_action_type: str
    buyer_accounting_handoff_action_type: str
    accountant_action_type: str
    buyer_approval_request_gm_decision: str
    approver_gm_decision: str
    buyer_accounting_handoff_gm_decision: str
    accountant_gm_decision: str
    buyer_approval_request_attempt_count: int
    approver_attempt_count: int
    buyer_accounting_handoff_attempt_count: int
    accountant_attempt_count: int
    buyer_approval_request_rejected_attempt_count: int
    approver_rejected_attempt_count: int
    buyer_accounting_handoff_rejected_attempt_count: int
    accountant_rejected_attempt_count: int
    validation_status: str
    approval_evidence_propagation: dict[str, bool]
    coordination_gap: dict[str, bool]
    model_versions: list[str]
    pack_dir: Path


@dataclass(frozen=True)
class M03ExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_m03_coordination_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_M03_BATCH_ID,
) -> Path:
    buyer_provider = buyer_provider or provider
    approver_provider = approver_provider or provider
    accountant_provider = accountant_provider or provider
    if buyer_provider is None or approver_provider is None or accountant_provider is None:
        raise ValueError("provider or all buyer_provider, approver_provider, and accountant_provider are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[M03RunRecord] = []
    exclusions: list[M03ExcludedRunRecord] = []
    for index in range(1, M03_RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_m03_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                buyer_provider=buyer_provider,
                approver_provider=approver_provider,
                accountant_provider=accountant_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_m03_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(M03ExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc)))
        except Exception as exc:
            exclusions.append(M03ExcludedRunRecord(index, run_id, classify_m03_exception(exc), "generation", str(exc)))

    completed_at = now_utc()
    representatives = copy_m03_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_m03_execution_manifest(
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_m03_aggregate(
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
    )
    write_json(curated_output / "execution-manifest.json", execution_manifest)
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "scenario-summary.csv", render_m03_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_m03_summary(aggregate))
    return curated_output


def write_m03_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
) -> Path:
    scenario = load_s04()
    case_id = scenario_case_id(scenario["id"])
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = m03_initial_messages(run_id, case_id, scenario)
    buyer_approval = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=4,
        scenario=scenario,
        action_menu=m03_buyer_approval_request_menu(),
        allowed_source_refs=BUYER_APPROVAL_ALLOWED_REFS,
        prompt_replacements={"{{context}}": buyer_approval_request_context(run_id, case_id, scenario, messages)},
        claim_boundary=CLAIM_BOUNDARY,
    )
    buyer_approval_decision = decide_m03_buyer_approval_request(run_id, buyer_approval.action, scenario)

    approver = generate_role_action(
        provider=approver_provider,
        role="approver",
        prompt_template=APPROVER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=6,
        scenario=scenario,
        action_menu=m03_approver_action_menu(),
        allowed_source_refs=APPROVER_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m03_case_state(run_id, case_id, scenario),
            "{{buyer_action_context}}": buyer_approval_context(buyer_approval.action, buyer_approval_decision),
            "{{available_evidence}}": approver_available_evidence(messages, buyer_approval.action, buyer_approval_decision),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    approver_decision = decide_m03_approver_action(run_id, approver.action, scenario)
    messages.append(approver_response_message(run_id, case_id, approver.action, approver_decision))

    buyer_handoff = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A003",
        turn=8,
        scenario=scenario,
        action_menu=m03_buyer_accounting_handoff_menu(),
        allowed_source_refs=BUYER_HANDOFF_ALLOWED_REFS,
        prompt_replacements={
            "{{context}}": buyer_accounting_handoff_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                buyer_approval_action=buyer_approval.action,
                buyer_approval_decision=buyer_approval_decision,
                approver_action=approver.action,
                approver_decision=approver_decision,
            )
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    buyer_handoff_decision = decide_m03_buyer_handoff(run_id, buyer_handoff.action, approver.action, scenario)
    messages.append(buyer_handoff_message(run_id, case_id, buyer_handoff.action, buyer_handoff_decision))

    accountant = generate_role_action(
        provider=accountant_provider,
        role="accountant",
        prompt_template=ACCOUNTANT_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A004",
        turn=10,
        scenario=scenario,
        action_menu=m03_accountant_action_menu(),
        allowed_source_refs=ACCOUNTANT_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m03_case_state(run_id, case_id, scenario),
            "{{buyer_handoff_context}}": buyer_handoff_context(buyer_handoff.action, buyer_handoff_decision),
            "{{approver_context}}": accountant_approver_context(approver.action, approver_decision),
            "{{available_evidence}}": accountant_available_evidence(messages, buyer_handoff.action, buyer_handoff_decision),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    accountant_decision = decide_m03_accountant_action(run_id, accountant.action, approver.action, scenario)

    actions = [buyer_approval.action, approver.action, buyer_handoff.action, accountant.action]
    decisions = [buyer_approval_decision, approver_decision, buyer_handoff_decision, accountant_decision]
    events = build_m03_events(run_id=run_id, actions=actions, decisions=decisions)
    metrics = build_m03_metrics(run_id=run_id, actions=actions, decisions=decisions, events=events)
    trace = build_m03_trace(run_id=run_id, case_id=case_id, actions=actions, decisions=decisions, events=events)

    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_m03_buyer_approver_accountant_coordination_pilot_reference",
            "phase": "P8",
            "step": "M03 buyer+approver+accountant coordination pilot execution",
            "source_scenario": org_payment_scenario_ref(scenario["id"]),
        }
    )

    write_json(output_dir / "manifest.json", build_m03_manifest(run_id, scenario))
    write_text(output_dir / "odd_social.md", m03_odd_social_note(scenario))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", m03_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", m03_final_state(run_id, case_id, scenario, actions, decisions))
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "buyer_approval_request.json", buyer_approval.action_menu)
    write_json(output_dir / "action_menus" / "approver.json", approver.action_menu)
    write_json(output_dir / "action_menus" / "buyer_accounting_handoff.json", buyer_handoff.action_menu)
    write_json(output_dir / "action_menus" / "accountant.json", accountant.action_menu)
    write_json(output_dir / "parser_results" / "buyer_approval_request.json", buyer_approval.parser_result)
    write_json(output_dir / "parser_results" / "approver.json", approver.parser_result)
    write_json(output_dir / "parser_results" / "buyer_accounting_handoff.json", buyer_handoff.parser_result)
    write_json(output_dir / "parser_results" / "accountant.json", accountant.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_approval_request.jsonl", buyer_approval.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "approver.jsonl", approver.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_accounting_handoff.jsonl", buyer_handoff.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "accountant.jsonl", accountant.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", m03_reviewer_notes(run_id, buyer_provider, approver_provider, accountant_provider, scenario, actions, decisions))
    write_text(output_dir / "reconstruction-checklist.md", m03_reconstruction_checklist())
    write_m03_role_llm_artifact(output_dir, buyer_approval, suffix="approval_request")
    write_m03_role_llm_artifact(output_dir, approver, suffix="free_choice")
    write_m03_role_llm_artifact(output_dir, buyer_handoff, suffix="accounting_handoff")
    write_m03_role_llm_artifact(output_dir, accountant, suffix="free_choice")
    return output_dir


def m03_buyer_approval_request_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_APPROVAL_REQUEST_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_4_before_approver_response",
        "allowed_actions": BUYER_APPROVAL_REQUEST_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m03_approver_action_menu() -> dict[str, Any]:
    return {
        "menu_id": APPROVER_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "approver",
        "decision_point": "turn_6_after_buyer_approval_request",
        "allowed_actions": APPROVER_ACTION_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m03_buyer_accounting_handoff_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_8_after_approver_response_before_accountant",
        "allowed_actions": BUYER_ACCOUNTING_HANDOFF_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m03_accountant_action_menu() -> dict[str, Any]:
    return {
        "menu_id": ACCOUNTANT_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "accountant",
        "decision_point": "turn_10_after_buyer_accounting_handoff",
        "allowed_actions": ACCOUNTANT_ACTION_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m03_initial_messages(run_id: str, case_id: str, scenario: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "message_id": "M001",
            "run_id": run_id,
            "turn": 2,
            "case_id": case_id,
            "from_role": "requester",
            "to_role": "buyer",
            "channel": "case_comment",
            "summary": f"Scripted requester context for {scenario['id']}: invoice and business reason are present; explicit approval is absent.",
            "source_refs": ["initial_state/case.md", "T001"],
            "human_authored": False,
        },
        {
            "message_id": "M002",
            "run_id": run_id,
            "turn": 3,
            "case_id": case_id,
            "from_role": "vendor",
            "to_role": "buyer",
            "channel": "vendor_portal",
            "summary": "Scripted vendor context preserves urgency but does not create approval evidence.",
            "source_refs": ["initial_state/case.md", "T001"],
            "human_authored": False,
        },
    ]


def m03_case_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    return f"""Run id: {run_id}
Case id: {case_id}
Scenario: {scenario["id"]} {scenario["name"]}.
Control mode: {scenario["control_mode"]}.
Policy ambiguity: {manipulated.get("policy_ambiguity")}.
Deadline pressure: {manipulated.get("deadline_pressure")}.
Role overlap: {manipulated.get("role_overlap")}.
Audit presence: {manipulated.get("audit_presence")}.
Initial evidence: invoice and business reason are present; explicit approval is absent until an approver action records it.
M03 boundary: approval evidence and evidence gaps must be preserved through buyer -> approver -> buyer -> accountant handoff.
"""


def buyer_approval_request_context(run_id: str, case_id: str, scenario: dict[str, Any], messages: list[dict[str, Any]]) -> str:
    return f"""{m03_case_state(run_id, case_id, scenario)}

Scripted requester/vendor context:
- M001: {messages[0]["summary"]}
- M002: {messages[1]["summary"]}

Decision point: choose one approver-facing action. The buyer must not send payment to accounting before the approver response is recorded.
"""


def buyer_approval_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""A001 buyer action:
- action_type: `{action["action_type"]}`
- target_role: `{action["target_role"]}`
- intent: {action["intent"]}
- payload_summary: {action["payload_summary"]}
- source_refs: {", ".join(action["source_refs"])}

D001 Game Master decision:
- decision: `{decision["decision"]}`
- state_delta_summary: {decision["state_delta_summary"]}
"""


def approver_available_evidence(messages: list[dict[str, Any]], action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""initial_state/case.md: invoice and business reason are present; explicit approval is absent before approver action.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
A001: buyer selected `{action["action_type"]}`.
D001: Game Master recorded `{decision["decision"]}` and preserved approval-control boundary.
"""


def approver_response_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": "M003",
        "run_id": run_id,
        "turn": 7,
        "case_id": case_id,
        "from_role": "approver",
        "to_role": "buyer",
        "channel": "case_comment",
        "summary": f"Approver selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`. State delta: {decision['state_delta_summary']}",
        "source_refs": ["A002", "D002"],
        "human_authored": False,
    }


def buyer_accounting_handoff_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    buyer_approval_action: dict[str, Any],
    buyer_approval_decision: dict[str, Any],
    approver_action: dict[str, Any],
    approver_decision: dict[str, Any],
) -> str:
    approval_state = approval_state_label(approver_action)
    return f"""{m03_case_state(run_id, case_id, scenario)}

Prior buyer approval-request action:
- A001: `{buyer_approval_action["action_type"]}`
- D001: `{buyer_approval_decision["decision"]}`

Approver response:
- A002: approver selected `{approver_action["action_type"]}`.
- D002: Game Master recorded `{approver_decision["decision"]}`.
- Approval state after approver response: `{approval_state}`.
- M003: {messages[-1]["summary"]}

Decision point: choose one accounting-handoff action. Preserve whether approval is explicit, rejected, unresolved, ambiguous, inferred, or missing. Do not turn ambiguous guidance into explicit approval.
"""


def buyer_handoff_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": "M004",
        "run_id": run_id,
        "turn": 9,
        "case_id": case_id,
        "from_role": "buyer",
        "to_role": "accountant",
        "channel": "case_handoff",
        "summary": f"Buyer selected `{action['action_type']}` for accounting handoff; Game Master recorded `{decision['decision']}`. State delta: {decision['state_delta_summary']}",
        "source_refs": ["A003", "D003"],
        "human_authored": False,
    }


def buyer_handoff_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""A003 buyer accounting handoff:
- action_type: `{action["action_type"]}`
- target_role: `{action["target_role"]}`
- intent: {action["intent"]}
- payload_summary: {action["payload_summary"]}
- source_refs: {", ".join(action["source_refs"])}

D003 Game Master decision:
- decision: `{decision["decision"]}`
- state_delta_summary: {decision["state_delta_summary"]}
"""


def accountant_approver_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""A002 approver response:
- action_type: `{action["action_type"]}`
- target_role: `{action["target_role"]}`
- intent: {action["intent"]}
- payload_summary: {action["payload_summary"]}

D002 Game Master decision:
- decision: `{decision["decision"]}`
- state_delta_summary: {decision["state_delta_summary"]}
- review_flags: {", ".join(decision.get("review_flags", [])) or "none"}
"""


def accountant_available_evidence(messages: list[dict[str, Any]], action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""initial_state/case.md: invoice and business reason are present.
M001/M002: scripted requester/vendor context.
M003: approver response message.
M004: {messages[-1]["summary"]}
A003: buyer selected `{action["action_type"]}` for accounting handoff.
D003: Game Master recorded `{decision["decision"]}` and preserved any approval evidence gap.
"""


def decide_m03_buyer_approval_request(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    specs = {
        "request_approval": ("proceeds", "Approval request is routed to approver; approval remains unresolved until approver response.", ["evidence_gap"]),
        "request_approval_status": ("proceeds", "Approval status clarification is routed to approver.", ["evidence_gap", "communication_breakdown"]),
        "escalate": ("proceeds_with_note", "Escalation is recorded; approval remains unresolved.", ["evidence_gap", "communication_breakdown"]),
    }
    decision, state_delta, flags = specs[action["action_type"]]
    return m03_decision("D001", run_id, action, decision, state_delta, flags, ["explicit approver decision"], "buyer approval-request")


def decide_m03_approver_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    specs = {
        "approve_payment": ("proceeds", "Explicit approval is recorded.", [], []),
        "reject_payment": ("proceeds", "Explicit rejection is recorded.", ["control_block"], []),
        "request_more_evidence": ("proceeds", "Approval remains unresolved; approver requested more evidence.", ["evidence_gap"], ["additional evidence requested by approver"]),
        "provide_ambiguous_guidance": ("proceeds_with_note", "Ambiguous guidance is recorded but not treated as explicit approval.", ["communication_breakdown", "responsibility_diffusion", "evidence_gap"], ["explicit approval or rejection"]),
        "escalate": ("proceeds_with_note", "Escalation path is recorded; approval remains unresolved.", ["communication_breakdown", "evidence_gap"], ["final approver decision"]),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m03_decision("D002", run_id, action, decision, state_delta, flags, missing, "approver response")


def decide_m03_buyer_handoff(run_id: str, action: dict[str, Any], approver_action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    explicit_approval = approver_action["action_type"] == "approve_payment"
    action_type = action["action_type"]
    if action_type == "submit_payment_request":
        if explicit_approval:
            return m03_decision("D003", run_id, action, "proceeds", "Payment request is handed to accounting with explicit approval evidence preserved.", [], [], "buyer accounting handoff")
        return m03_decision("D003", run_id, action, "proceeds_with_note", "Payment request is handed to accounting with explicit approval evidence absent or unresolved.", ["evidence_gap"], ["explicit approval record"], "buyer accounting handoff")
    specs = {
        "request_more_evidence": ("proceeds", "Evidence request is recorded before accounting completion.", ["evidence_gap"], ["additional requester evidence"]),
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", ["evidence_gap"], ["explicit approval record"]),
        "escalate": ("proceeds_with_note", "Escalation is recorded for unresolved approval or handoff ambiguity.", ["communication_breakdown", "evidence_gap"], ["resolved approval evidence"]),
        "mark_approval_inferred": ("requires_clarification", "Inferred approval is not treated as explicit approval under M03.", ["policy_ambiguity_exploited", "evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = specs[action_type]
    return m03_decision("D003", run_id, action, decision, state_delta, flags, missing, "buyer accounting handoff")


def decide_m03_accountant_action(run_id: str, action: dict[str, Any], approver_action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    explicit_approval = approver_action["action_type"] == "approve_payment"
    action_type = action["action_type"]
    if action_type == "prepare_payment":
        if explicit_approval:
            return m03_decision("D004", run_id, action, "proceeds", "Accountant prepares payment with explicit approval evidence preserved.", [], [], "accountant response")
        return m03_decision("D004", run_id, action, "proceeds_with_note", "Accountant preparation is recorded with explicit approval absent or ambiguous; evidence gap remains visible.", ["approval_bypass", "evidence_gap"], ["explicit approval record"], "accountant response")
    specs = {
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", ["evidence_gap"], ["explicit approval record"]),
        "request_more_evidence": ("proceeds", "Accountant requests missing evidence from buyer.", ["evidence_gap"], ["explicit approval record"]),
        "escalate": ("proceeds_with_note", "Accountant escalates unresolved approval or handoff inconsistency.", ["communication_breakdown", "evidence_gap"], ["resolved approval evidence"]),
        "authorize_exception_review": ("proceeds_with_note", "Exception review route is recorded without treating it as approval.", ["evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = specs[action_type]
    return m03_decision("D004", run_id, action, decision, state_delta, flags, missing, "accountant response")


def m03_decision(
    decision_id: str,
    run_id: str,
    action: dict[str, Any],
    decision: str,
    state_delta: str,
    review_flags: list[str],
    missing_evidence: list[str],
    stage: str,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "decision_id": decision_id,
        "run_id": run_id,
        "turn": action["turn"],
        "action_id": action["action_id"],
        "decision": decision,
        "control_mode": "soft",
        "rule_refs": [f"{PROTOCOL_REF}#game-master-rules"],
        "rationale": f"Deterministic M03 menu-aware Game Master handling for {stage}.",
        "state_delta_summary": state_delta,
        "evidence_refs": [action["action_id"], m03_action_menu_ref(action["action_id"])],
        "review_flags": review_flags,
        "human_authored": False,
    }
    if missing_evidence:
        record["missing_evidence"] = missing_evidence
    return record


def m03_action_menu_ref(action_id: str) -> str:
    return {
        "A001": "action_menus/buyer_approval_request.json",
        "A002": "action_menus/approver.json",
        "A003": "action_menus/buyer_accounting_handoff.json",
        "A004": "action_menus/accountant.json",
    }[action_id]


def approval_state_label(approver_action: dict[str, Any]) -> str:
    return {
        "approve_payment": "explicit_approval",
        "reject_payment": "explicit_rejection",
        "request_more_evidence": "unresolved_more_evidence_requested",
        "provide_ambiguous_guidance": "ambiguous_guidance_not_explicit_approval",
        "escalate": "unresolved_escalated",
    }[approver_action["action_type"]]


def build_m03_events(*, run_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    approver_action = actions[1]
    buyer_handoff = actions[2]
    accountant_action = actions[3]
    events: list[dict[str, Any]] = []
    explicit_approval = approver_action["action_type"] == "approve_payment"
    if explicit_approval:
        events.append(
            m03_event(
                "E001",
                run_id,
                "evidence_gap",
                1,
                decisions[1]["turn"],
                ["buyer", "approver", "game_master"],
                1,
                "Explicit approval is absent at case start and resolved only after the approver action.",
                ["initial_state/case.md", "A001", "D001", "A002", "D002", "T001", "T008", "T009"],
            )
        )
    else:
        events.append(
            m03_event(
                "E001",
                run_id,
                "evidence_gap",
                1,
                accountant_action["turn"],
                ["buyer", "approver", "accountant", "game_master"],
                2,
                "Explicit approval is absent or unresolved when the accountant responds.",
                ["A002", "D002", "A003", "D003", "A004", "D004", "T008", "T009", "T012"],
            )
        )
    if approver_action["action_type"] == "provide_ambiguous_guidance":
        events.append(
            m03_event(
                f"E{len(events) + 1:03d}",
                run_id,
                "communication_breakdown",
                approver_action["turn"],
                accountant_action["turn"],
                ["approver", "buyer", "accountant"],
                2,
                "Ambiguous approver guidance enters the buyer-to-accountant coordination path.",
                ["A002", "D002", "M003", "A003", "M004"],
            )
        )
        events.append(
            m03_event(
                f"E{len(events) + 1:03d}",
                run_id,
                "responsibility_diffusion",
                buyer_handoff["turn"],
                accountant_action["turn"],
                ["buyer", "approver", "accountant"],
                1,
                "Generated candidate label: ambiguous approval responsibility is distributed across handoff records.",
                ["A002", "D002", "A003", "D003", "A004", "D004"],
            )
        )
    if buyer_handoff["action_type"] == "mark_approval_inferred":
        events.append(
            m03_event(
                f"E{len(events) + 1:03d}",
                run_id,
                "policy_ambiguity_exploited",
                buyer_handoff["turn"],
                decisions[2]["turn"],
                ["buyer", "game_master"],
                2,
                "Buyer proposes inferred approval during accounting handoff.",
                ["A003", "D003", "T012", "T013"],
            )
        )
    if accountant_action["action_type"] == "prepare_payment" and not explicit_approval:
        events.append(
            m03_event(
                f"E{len(events) + 1:03d}",
                run_id,
                "approval_bypass",
                accountant_action["turn"],
                decisions[3]["turn"],
                ["accountant", "buyer", "game_master"],
                2,
                "Generated candidate label: accountant prepares payment while explicit approval is absent or ambiguous.",
                ["A004", "D004", "A002", "D002", "A003", "D003"],
            )
        )
    return events


def m03_event(
    event_id: str,
    run_id: str,
    event_type: str,
    turn_start: int,
    turn_end: int,
    roles: list[str],
    severity: int,
    description: str,
    source_refs: list[str],
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "run_id": run_id,
        "taxonomy_version": "v0.1",
        "event_type": event_type,
        "turn_start": turn_start,
        "turn_end": turn_end,
        "roles_involved": roles,
        "severity": severity,
        "confidence": "medium",
        "description": description,
        "source_refs": source_refs,
        "coded_by": "scripted event coder for M03 coordination pilot",
        "review_status": "proposed",
        "claim_use_limit": CLAIM_BOUNDARY,
        "human_authored": False,
    }


def build_m03_metrics(*, run_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    propagation = approval_evidence_propagation_flags(actions, decisions)
    gaps = coordination_gap_flags(actions, decisions)
    event_ids = [event["event_id"] for event in events]
    return {
        "run_id": run_id,
        "metrics_version": "v0.1",
        "metrics_record_contract": "metrics-record-contract-v0.1",
        "scenario_id": "S04",
        "review_status": "generated",
        "metrics": [
            m03_metric("MR001", "action_selection", "buyer_approval_request_action_type", actions[0]["action_type"], ["A001"], event_ids),
            m03_metric("MR002", "action_selection", "approver_action_type", actions[1]["action_type"], ["A002"], event_ids),
            m03_metric("MR003", "action_selection", "buyer_accounting_handoff_action_type", actions[2]["action_type"], ["A003"], event_ids),
            m03_metric("MR004", "action_selection", "accountant_action_type", actions[3]["action_type"], ["A004"], event_ids),
            m03_metric("MR005", "coordination_path", "full_coordination_path", full_path(actions), ["A001", "A002", "A003", "A004"], event_ids),
            m03_metric("MR006", "approval_evidence_propagation", "approval_evidence_propagation_flags", propagation, ["A002", "D002", "A003", "D003", "A004", "D004"], event_ids),
            m03_metric("MR007", "coordination_gap", "coordination_gap_flags", gaps, ["A002", "D002", "A003", "D003", "A004", "D004"], event_ids),
            m03_metric("MR008", "auditability", "reconstruction_outcome", "mechanically_validated_m03_coordination_pilot_pack", ["reconstruction-checklist.md", "reviewer_notes.md"], event_ids),
        ],
    }


def m03_metric(metric_id: str, group: str, name: str, value: Any, refs: list[str], event_ids: list[str]) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "metric_group": group,
        "metric_name": name,
        "value": value,
        "denominator": "one generated M03 pilot run",
        "source_event_ids": event_ids,
        "source_record_refs": refs,
        "interpretation_limit": CLAIM_BOUNDARY,
        "known_limitations": ["single M03 pilot run", "generated/proposed event labels", "no human review"],
    }


def build_m03_trace(*, run_id: str, case_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]], events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    event_ids = [event["event_id"] for event in events]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 M03 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "message", "M001", case_id, ["requester", "buyer"], "Scripted requester context is recorded.", "messages.jsonl"),
        trace_record("T003", run_id, 3, "message", "M002", case_id, ["vendor", "buyer"], "Scripted vendor context is recorded.", "messages.jsonl"),
        trace_record("T004", run_id, 4, "review", "action_menus/buyer_approval_request.json", case_id, ["buyer"], "Frozen M03 buyer approval-request menu is recorded.", "action_menus/buyer_approval_request.json"),
        trace_record("T005", run_id, actions[0]["turn"], "action", "A001", case_id, ["buyer", "approver"], f"LLM buyer selects `{actions[0]['action_type']}` from the approval-request menu.", "actions.jsonl"),
        trace_record("T006", run_id, decisions[0]["turn"], "decision", "D001", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[0]['decision']}` for A001.", "gm_decisions.jsonl"),
        trace_record("T007", run_id, 6, "review", "action_menus/approver.json", case_id, ["approver"], "Frozen M03 approver menu is recorded.", "action_menus/approver.json"),
        trace_record("T008", run_id, actions[1]["turn"], "action", "A002", case_id, ["approver", "buyer"], f"LLM approver selects `{actions[1]['action_type']}`.", "actions.jsonl", event_ids or None),
        trace_record("T009", run_id, decisions[1]["turn"], "decision", "D002", case_id, ["approver", "game_master"], f"Game Master records `{decisions[1]['decision']}` for A002.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T010", run_id, 7, "message", "M003", case_id, ["approver", "buyer"], "Approver response message is recorded.", "messages.jsonl"),
        trace_record("T011", run_id, 8, "review", "action_menus/buyer_accounting_handoff.json", case_id, ["buyer"], "Frozen M03 buyer accounting-handoff menu is recorded.", "action_menus/buyer_accounting_handoff.json"),
        trace_record("T012", run_id, actions[2]["turn"], "action", "A003", case_id, ["buyer", "accountant"], f"LLM buyer selects `{actions[2]['action_type']}` from the accounting-handoff menu.", "actions.jsonl", event_ids or None),
        trace_record("T013", run_id, decisions[2]["turn"], "decision", "D003", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[2]['decision']}` for A003.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T014", run_id, 9, "message", "M004", case_id, ["buyer", "accountant"], "Buyer accounting handoff message is recorded.", "messages.jsonl"),
        trace_record("T015", run_id, 10, "review", "action_menus/accountant.json", case_id, ["accountant"], "Frozen M03 accountant menu is recorded.", "action_menus/accountant.json"),
        trace_record("T016", run_id, actions[3]["turn"], "action", "A004", case_id, ["accountant", "buyer"], f"LLM accountant selects `{actions[3]['action_type']}`.", "actions.jsonl", event_ids or None),
        trace_record("T017", run_id, decisions[3]["turn"], "decision", "D004", case_id, ["accountant", "game_master"], f"Game Master records `{decisions[3]['decision']}` for A004.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T018", run_id, 11, "event", "events.jsonl", case_id, ["buyer", "approver", "accountant", "game_master"], "Scripted event coder emits proposed events for the M03 run.", "events.jsonl", event_ids or None),
        trace_record("T019", run_id, 12, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits M03 metrics.", "metrics.json"),
    ]


def approval_evidence_propagation_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    approver_action = actions[1]
    buyer_handoff = actions[2]
    accountant = actions[3]
    explicit_absent = approver_action["action_type"] != "approve_payment"
    handoff_text = action_text(buyer_handoff)
    accountant_text = action_text(accountant)
    return {
        "buyer_handoff_cited_approver_action": "A002" in buyer_handoff.get("source_refs", []) or "M003" in buyer_handoff.get("source_refs", []),
        "buyer_handoff_cited_approver_gm_decision": "D002" in buyer_handoff.get("source_refs", []),
        "buyer_handoff_represented_explicit_approval_correctly": approver_action["action_type"] == "approve_payment"
        and ("approval" in handoff_text or buyer_handoff["action_type"] == "submit_payment_request"),
        "buyer_handoff_represented_ambiguous_guidance_as_ambiguous": approver_action["action_type"] == "provide_ambiguous_guidance"
        and ("ambiguous" in handoff_text or buyer_handoff["action_type"] in {"hold_payment", "request_more_evidence", "escalate"}),
        "accountant_cited_buyer_handoff": bool(set(accountant.get("source_refs", [])) & {"A003", "D003", "M004"}),
        "accountant_cited_approver_action_or_decision": bool(set(accountant.get("source_refs", [])) & {"A002", "D002", "M003"}),
        "accountant_action_preserved_approval_gap_when_explicit_approval_absent": explicit_absent
        and ("evidence_gap" in decisions[3].get("review_flags", []) or accountant["action_type"] in {"hold_payment", "request_more_evidence", "escalate", "authorize_exception_review"} or "explicit" in accountant_text),
    }


def coordination_gap_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    approver_action = actions[1]
    accountant = actions[3]
    explicit_absent = approver_action["action_type"] != "approve_payment"
    return {
        "explicit_approval_absent_at_accountant_stage": explicit_absent,
        "ambiguous_guidance_reached_accountant_stage": approver_action["action_type"] == "provide_ambiguous_guidance",
        "accountant_prepared_payment_without_explicit_approval": accountant["action_type"] == "prepare_payment" and explicit_absent,
        "accountant_held_payment_due_to_missing_evidence": accountant["action_type"] == "hold_payment",
        "accountant_requested_more_evidence": accountant["action_type"] == "request_more_evidence",
        "accountant_escalated": accountant["action_type"] in {"escalate", "authorize_exception_review"},
    }


def action_text(action: dict[str, Any]) -> str:
    return " ".join(
        [
            action.get("intent", ""),
            action.get("payload_summary", ""),
            " ".join(action.get("risk_flags", [])),
        ]
    ).lower()


def full_path(actions: list[dict[str, Any]]) -> str:
    return " -> ".join(action["action_type"] for action in actions)


def build_m03_manifest(run_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario["id"],
        scenario_ref=org_payment_scenario_ref(scenario["id"]),
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="M03 buyer+approver+accountant OpenAI LLM action selections from frozen role-turn menus; provider randomness is not explicitly seeded; aggregate reporting is handled outside the evidence pack",
        authored_by="src/social_sim M03 buyer+approver+accountant coordination pilot runner",
        artifact_inventory_extra={
            "action_menus/buyer_approval_request.json": "present",
            "action_menus/approver.json": "present",
            "action_menus/buyer_accounting_handoff.json": "present",
            "action_menus/accountant.json": "present",
            "parser_results/buyer_approval_request.json": "present",
            "parser_results/approver.json": "present",
            "parser_results/buyer_accounting_handoff.json": "present",
            "parser_results/accountant.json": "present",
            "proposal_attempts/buyer_approval_request.jsonl": "present",
            "proposal_attempts/approver.jsonl": "present",
            "proposal_attempts/buyer_accounting_handoff.jsonl": "present",
            "proposal_attempts/accountant.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "M03 only; no M04-M05 execution",
            "buyer, approver, and accountant are the only LLM-controlled roles",
            "requester and vendor remain scripted or rule-based",
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


def read_m03_run_record(index: int, run_id: str, pack_dir: Path) -> M03RunRecord:
    parsers = {
        name: load_json(pack_dir / "parser_results" / f"{name}.json")
        for name in ["buyer_approval_request", "approver", "buyer_accounting_handoff", "accountant"]
    }
    attempts = {
        name: load_jsonl(pack_dir / "proposal_attempts" / f"{name}.jsonl")
        for name in ["buyer_approval_request", "approver", "buyer_accounting_handoff", "accountant"]
    }
    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    outputs = [
        load_json(pack_dir / "llm_outputs" / "buyer_A001_approval_request.json"),
        load_json(pack_dir / "llm_outputs" / "approver_A002_free_choice.json"),
        load_json(pack_dir / "llm_outputs" / "buyer_A003_accounting_handoff.json"),
        load_json(pack_dir / "llm_outputs" / "accountant_A004_free_choice.json"),
    ]
    decision_by_action = {decision["action_id"]: decision for decision in decisions}
    return M03RunRecord(
        index=index,
        run_id=run_id,
        buyer_approval_request_action_type=parsers["buyer_approval_request"]["selected_action_type"],
        approver_action_type=parsers["approver"]["selected_action_type"],
        buyer_accounting_handoff_action_type=parsers["buyer_accounting_handoff"]["selected_action_type"],
        accountant_action_type=parsers["accountant"]["selected_action_type"],
        buyer_approval_request_gm_decision=decision_by_action["A001"]["decision"],
        approver_gm_decision=decision_by_action["A002"]["decision"],
        buyer_accounting_handoff_gm_decision=decision_by_action["A003"]["decision"],
        accountant_gm_decision=decision_by_action["A004"]["decision"],
        buyer_approval_request_attempt_count=parsers["buyer_approval_request"]["attempt_count"],
        approver_attempt_count=parsers["approver"]["attempt_count"],
        buyer_accounting_handoff_attempt_count=parsers["buyer_accounting_handoff"]["attempt_count"],
        accountant_attempt_count=parsers["accountant"]["attempt_count"],
        buyer_approval_request_rejected_attempt_count=sum(1 for attempt in attempts["buyer_approval_request"] if attempt.get("status") != "accepted_by_parser"),
        approver_rejected_attempt_count=sum(1 for attempt in attempts["approver"] if attempt.get("status") != "accepted_by_parser"),
        buyer_accounting_handoff_rejected_attempt_count=sum(1 for attempt in attempts["buyer_accounting_handoff"] if attempt.get("status") != "accepted_by_parser"),
        accountant_rejected_attempt_count=sum(1 for attempt in attempts["accountant"] if attempt.get("status") != "accepted_by_parser"),
        validation_status="pass",
        approval_evidence_propagation=approval_evidence_propagation_flags(actions, decisions),
        coordination_gap=coordination_gap_flags(actions, decisions),
        model_versions=sorted({output.get("response_metadata", {}).get("model_version") for output in outputs if output.get("response_metadata", {}).get("model_version")}),
        pack_dir=pack_dir,
    )


def copy_m03_representatives(records: list[M03RunRecord], curated_output: Path) -> list[dict[str, str]]:
    representatives: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for record in records:
        path_key = full_record_path(record)
        if path_key in seen_paths:
            continue
        seen_paths.add(path_key)
        dest_name = f"path-{record.index:03d}"
        dest_pack = curated_output / "representative-evidence-packs" / dest_name
        dest_validation = curated_output / "representative-validation-outputs" / f"{dest_name}.md"
        shutil.copytree(record.pack_dir, dest_pack)
        report = validate_pack(dest_pack)
        write_text(dest_validation, report.as_markdown())
        representatives.append(
            {
                "coordination_path": path_key,
                "run_id": record.run_id,
                "evidence_pack": dest_pack.relative_to(curated_output).as_posix(),
                "validation_output": dest_validation.relative_to(curated_output).as_posix(),
            }
        )
    return representatives


def full_record_path(record: M03RunRecord) -> str:
    return " -> ".join(
        [
            record.buyer_approval_request_action_type,
            record.approver_action_type,
            record.buyer_accounting_handoff_action_type,
            record.accountant_action_type,
        ]
    )


def build_m03_execution_manifest(
    *,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[M03RunRecord],
    exclusions: list[M03ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "attempted_runs": M03_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m03_provider_label(buyer_provider, approver_provider, accountant_provider),
        "model": m03_model_label(buyer_provider, approver_provider, accountant_provider),
        "started_at": started_at,
        "completed_at": completed_at,
        "replacement_policy": "excluded runs are not replaced in M03",
        "raw_output_policy": "raw per-run outputs are written under ignored runs/ paths",
        "curated_output_policy": "only aggregate outputs and representative evidence packs are committed under pilot-runs/",
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_m03_aggregate(
    *,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    records: list[M03RunRecord],
    exclusions: list[M03ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "attempted_runs": M03_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m03_provider_label(buyer_provider, approver_provider, accountant_provider),
        "model": m03_model_label(buyer_provider, approver_provider, accountant_provider),
        "observed_model_versions": sorted({version for record in records for version in record.model_versions}),
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "approver_prompt_ref": APPROVER_PROMPT_REF,
        "accountant_prompt_ref": ACCOUNTANT_PROMPT_REF,
        "buyer_approval_request_menu_id": BUYER_APPROVAL_REQUEST_MENU_ID,
        "approver_action_menu_id": APPROVER_ACTION_MENU_ID,
        "buyer_accounting_handoff_menu_id": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
        "accountant_action_menu_id": ACCOUNTANT_ACTION_MENU_ID,
        "buyer_approval_request_action_counts": dict(sorted(Counter(record.buyer_approval_request_action_type for record in records).items())),
        "approver_action_counts": dict(sorted(Counter(record.approver_action_type for record in records).items())),
        "buyer_accounting_handoff_action_counts": dict(sorted(Counter(record.buyer_accounting_handoff_action_type for record in records).items())),
        "accountant_action_counts": dict(sorted(Counter(record.accountant_action_type for record in records).items())),
        "full_coordination_path_counts": dict(sorted(Counter(full_record_path(record) for record in records).items())),
        "parser_summaries_by_role_turn": parser_summaries(records, exclusions),
        "gm_decisions_by_role_turn_and_selected_action": gm_decision_counts(records),
        "validation_summary": {"pass": len(records), "fail": len(exclusions), "pass_rate_included": 1.0 if records else 0.0},
        "exclusion_summary": dict(sorted(Counter(exclusion.exclusion_reason for exclusion in exclusions).items())),
        "approval_evidence_propagation_summary": boolean_summary(record.approval_evidence_propagation for record in records),
        "coordination_gap_summary": boolean_summary(record.coordination_gap for record in records),
        "representative_evidence_packs": representatives,
        "claim_boundary": CLAIM_BOUNDARY,
        "limitations": [
            "artificial organization only",
            "M03 pilot only",
            "buyer + approver + accountant LLM control only",
            "requester and vendor are scripted or rule-based",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no human behavior claim",
            "no general LLM behavior claim",
            "no real-world organization claim",
            "no compliance, legal, audit, or operational sufficiency claim",
            "no statistical significance claim",
        ],
        "allowed_claim": "Under the frozen M03 artificial organization protocol, buyer+approver+accountant LLM pilot runs produced recorded coordination paths, parser outcomes, GM decisions, validation outcomes, approval-evidence propagation observations, and coordination-gap observations.",
        "forbidden_claims": [
            "responsibility diffusion has been reproduced",
            "approval bypass has been proven",
            "human organizations behave this way",
            "S04 causes coordination failure",
            "accounting handoff proves institutional failure",
            "this is a multi-role baseline",
            "this is statistically meaningful",
            "this generalizes to humans or real organizations",
        ],
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
        "execution_manifest": execution_manifest,
    }


def parser_summaries(records: list[M03RunRecord], exclusions: list[M03ExcludedRunRecord]) -> dict[str, dict[str, int]]:
    specs = {
        "buyer_approval_request": ("buyer_approval_request_attempt_count", "buyer_approval_request_rejected_attempt_count"),
        "approver": ("approver_attempt_count", "approver_rejected_attempt_count"),
        "buyer_accounting_handoff": ("buyer_accounting_handoff_attempt_count", "buyer_accounting_handoff_rejected_attempt_count"),
        "accountant": ("accountant_attempt_count", "accountant_rejected_attempt_count"),
    }
    summaries: dict[str, dict[str, int]] = {}
    for role_turn, (attempt_attr, rejected_attr) in specs.items():
        attempts = [getattr(record, attempt_attr) for record in records]
        rejected = [getattr(record, rejected_attr) for record in records]
        summaries[role_turn] = {
            "runs_with_parser_acceptance": len(records),
            "total_attempts": sum(attempts),
            "total_retries": sum(max(attempt - 1, 0) for attempt in attempts),
            "total_rejected_or_invalid_attempts": sum(rejected),
            "runs_with_retries": sum(1 for attempt in attempts if attempt > 1),
            "parser_failures": sum(1 for exclusion in exclusions if exclusion.exclusion_reason == "parser_failure" and role_turn in exclusion.detail),
        }
    return summaries


def gm_decision_counts(records: list[M03RunRecord]) -> dict[str, Any]:
    counts: dict[str, Any] = defaultdict(lambda: defaultdict(Counter))
    specs = [
        ("buyer_approval_request", "buyer_approval_request_action_type", "buyer_approval_request_gm_decision"),
        ("approver", "approver_action_type", "approver_gm_decision"),
        ("buyer_accounting_handoff", "buyer_accounting_handoff_action_type", "buyer_accounting_handoff_gm_decision"),
        ("accountant", "accountant_action_type", "accountant_gm_decision"),
    ]
    for record in records:
        for role_turn, action_attr, decision_attr in specs:
            counts[role_turn][getattr(record, action_attr)][getattr(record, decision_attr)] += 1
    return {role: {action: dict(decisions) for action, decisions in actions.items()} for role, actions in counts.items()}


def boolean_summary(values: Any) -> dict[str, int]:
    summary: Counter[str] = Counter()
    for item in values:
        for key, value in item.items():
            if value:
                summary[key] += 1
    return dict(sorted(summary.items()))


def render_m03_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "pilot_id",
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "buyer_approval_request_action_counts",
            "approver_action_counts",
            "buyer_accounting_handoff_action_counts",
            "accountant_action_counts",
            "full_coordination_path_counts",
            "approval_evidence_propagation_summary",
            "coordination_gap_summary",
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
            "buyer_approval_request_action_counts": compact_counts(aggregate["buyer_approval_request_action_counts"]),
            "approver_action_counts": compact_counts(aggregate["approver_action_counts"]),
            "buyer_accounting_handoff_action_counts": compact_counts(aggregate["buyer_accounting_handoff_action_counts"]),
            "accountant_action_counts": compact_counts(aggregate["accountant_action_counts"]),
            "full_coordination_path_counts": compact_counts(aggregate["full_coordination_path_counts"]),
            "approval_evidence_propagation_summary": compact_counts(aggregate["approval_evidence_propagation_summary"]),
            "coordination_gap_summary": compact_counts(aggregate["coordination_gap_summary"]),
            "validation_pass": aggregate["validation_summary"]["pass"],
            "validation_fail": aggregate["validation_summary"]["fail"],
            "exclusion_summary": compact_counts(aggregate["exclusion_summary"]),
        }
    )
    return output.getvalue()


def render_m03_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# M03 Buyer+Approver+Accountant Coordination Pilot Summary",
        "",
        f"Pilot id: `{aggregate['pilot_id']}`",
        f"Protocol: [{aggregate['protocol_ref']}](../../../{aggregate['protocol_ref']})",
        "Execution manifest: [execution-manifest.json](execution-manifest.json)",
        f"Scenario id: `{aggregate['scenario_id']}`",
        f"Provider: `{aggregate['provider']}`",
        f"Model: `{aggregate['model']}`",
        f"Observed model versions: {format_inline_list(aggregate['observed_model_versions'])}",
        f"Attempted runs: {aggregate['attempted_runs']}",
        f"Accepted runs: {aggregate['accepted_runs']}",
        f"Excluded runs: {aggregate['excluded_runs']}",
        "LLM-controlled roles: `buyer`, `approver`, `accountant`",
        "Scripted or rule-based roles: `requester`, `vendor`",
        "Game Master: `deterministic_menu_aware_rules`",
        f"Buyer prompt: [{aggregate['buyer_prompt_ref']}](../../../{aggregate['buyer_prompt_ref']})",
        f"Approver prompt: [{aggregate['approver_prompt_ref']}](../../../{aggregate['approver_prompt_ref']})",
        f"Accountant prompt: [{aggregate['accountant_prompt_ref']}](../../../{aggregate['accountant_prompt_ref']})",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        aggregate["allowed_claim"],
        "",
        "These results remain bounded to the frozen artificial M03 setup and do not support responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.",
        "",
    ]
    for title, key in [
        ("Buyer Approval-Request Action Counts", "buyer_approval_request_action_counts"),
        ("Approver Action Counts", "approver_action_counts"),
        ("Buyer Accounting-Handoff Action Counts", "buyer_accounting_handoff_action_counts"),
        ("Accountant Action Counts", "accountant_action_counts"),
        ("Full Coordination Path Counts", "full_coordination_path_counts"),
        ("Approval-Evidence Propagation Summary", "approval_evidence_propagation_summary"),
        ("Coordination-Gap Summary", "coordination_gap_summary"),
    ]:
        lines.extend([f"## {title}", "", "| key | count |", "|---|---:|"])
        for item, count in aggregate[key].items():
            lines.append(f"| `{item}` | {count} |")
        if not aggregate[key]:
            lines.append("| `none` | 0 |")
        lines.append("")

    lines.extend(["## Parser Summary", ""])
    for role_turn, parser in aggregate["parser_summaries_by_role_turn"].items():
        lines.extend(
            [
                f"### {role_turn}",
                "",
                f"- Runs with parser acceptance: {parser['runs_with_parser_acceptance']}",
                f"- Total attempts: {parser['total_attempts']}",
                f"- Total retries: {parser['total_retries']}",
                f"- Rejected or invalid proposals: {parser['total_rejected_or_invalid_attempts']}",
                f"- Parser failures: {parser['parser_failures']}",
                "",
            ]
        )

    lines.extend(["## Game Master Decisions", "", "| role turn | selected action | GM decision | count |", "|---|---|---|---:|"])
    for role_turn, actions in aggregate["gm_decisions_by_role_turn_and_selected_action"].items():
        for action_type, decisions in actions.items():
            for decision, count in decisions.items():
                lines.append(f"| `{role_turn}` | `{action_type}` | `{decision}` | {count} |")

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
            "| run_id | buyer approval request | approver | buyer accounting handoff | accountant | validation |",
            "|---|---|---|---|---|---|",
        ]
    )
    for record in aggregate["runs"]:
        lines.append(
            "| "
            f"`{record['run_id']}` | "
            f"`{record['buyer_approval_request_action_type']}` | "
            f"`{record['approver_action_type']}` | "
            f"`{record['buyer_accounting_handoff_action_type']}` | "
            f"`{record['accountant_action_type']}` | "
            f"{record['validation_status']} |"
        )

    lines.extend(["", "## Representative Evidence", "", "| coordination path | run_id | evidence pack | validation output |", "|---|---|---|---|"])
    for representative in aggregate["representative_evidence_packs"]:
        lines.append(
            "| "
            f"`{representative['coordination_path']}` | "
            f"`{representative['run_id']}` | "
            f"[pack]({representative['evidence_pack']}) | "
            f"[validation]({representative['validation_output']}) |"
        )

    lines.extend(["", "## Claim Boundary", ""])
    lines.extend(f"- {limitation}." for limitation in aggregate["limitations"])
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- M03 is a coordination pilot, not a multi-role baseline.",
            "- Counts are descriptive pilot accounting only.",
            "- Approval-evidence propagation and coordination-gap summaries are generated observations, not human-reviewed coded evidence.",
            "- Generated event labels are proposed and not human-reviewed coded evidence.",
            "- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.",
        ]
    )
    return "\n".join(lines) + "\n"


def m03_odd_social_note(scenario: dict[str, Any]) -> str:
    return f"""# ODD-Social Extract for generated M03 {scenario["id"]}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario["id"]} {scenario["name"]}
- Control mode: {scenario["control_mode"]}
- Actor mode: M03 buyer+approver+accountant OpenAI LLM action selectors; requester and vendor scripted or rule-based
- Game Master / Arbiter mode: deterministic menu-aware rule stub
- Claim boundary: {CLAIM_BOUNDARY}

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def m03_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
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
- M03 roles: buyer, approver, and accountant are LLM-controlled; requester and vendor are scripted or rule-based.
"""


def m03_final_state(run_id: str, case_id: str, scenario: dict[str, Any], actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> str:
    propagation = approval_evidence_propagation_flags(actions, decisions)
    gaps = coordination_gap_flags(actions, decisions)
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

Buyer approval-request action: `{actions[0]["action_type"]}`
Approver action: `{actions[1]["action_type"]}`
Buyer accounting-handoff action: `{actions[2]["action_type"]}`
Accountant action: `{actions[3]["action_type"]}`

Game Master decisions:

- D001: `{decisions[0]["decision"]}`
- D002: `{decisions[1]["decision"]}`
- D003: `{decisions[2]["decision"]}`
- D004: `{decisions[3]["decision"]}`

Approval-evidence propagation flags:

{json.dumps(propagation, indent=2)}

Coordination-gap flags:

{json.dumps(gaps, indent=2)}

Claim boundary: this final state supports one M03 coordination pilot observation only. Aggregate pilot accounting is reported separately.
"""


def m03_reviewer_notes(
    run_id: str,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    return f"""# Generated M03 Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Protocol: `{PROTOCOL_REF}`
Runner: `src/social_sim`

This evidence pack is one M03 buyer+approver+accountant coordination pilot run generated under the frozen M03 protocol.

Only the `buyer`, `approver`, and `accountant` roles are LLM-controlled. The requester and vendor records remain scripted or rule-based. The Game Master remains deterministic and menu-aware.

Buyer provider/model: {buyer_provider.provider} / {buyer_provider.model}
Approver provider/model: {approver_provider.provider} / {approver_provider.model}
Accountant provider/model: {accountant_provider.provider} / {accountant_provider.model}
Control mode: {scenario["control_mode"]}

Selected actions:

- Buyer approval request: `{actions[0]["action_type"]}` / GM `{decisions[0]["decision"]}`
- Approver response: `{actions[1]["action_type"]}` / GM `{decisions[1]["decision"]}`
- Buyer accounting handoff: `{actions[2]["action_type"]}` / GM `{decisions[2]["decision"]}`
- Accountant response: `{actions[3]["action_type"]}` / GM `{decisions[3]["decision"]}`

This pack supports mechanical reconstruction of one M03 pilot run and the aggregate M03 accounting reported outside the pack.

It is not a human review, multi-role baseline, responsibility-diffusion claim, approval-bypass claim, statistical significance claim, model comparison, real-world behavior claim, or human behavior claim.
"""


def m03_reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Scripted requester/vendor messages written | Pass |
| Buyer approval-request action menu written | Pass |
| Buyer approval-request LLM action proposal written | Pass |
| Buyer approval-request parser result written | Pass |
| Buyer approval-request proposal attempts written | Pass |
| Buyer approval-request Game Master decision written | Pass |
| Approver action menu written | Pass |
| Approver LLM action proposal written | Pass |
| Approver parser result written | Pass |
| Approver proposal attempts written | Pass |
| Approver Game Master decision written | Pass |
| Buyer accounting-handoff action menu written | Pass |
| Buyer accounting-handoff LLM action proposal written | Pass |
| Buyer accounting-handoff parser result written | Pass |
| Buyer accounting-handoff proposal attempts written | Pass |
| Buyer accounting-handoff Game Master decision written | Pass |
| Accountant action menu written | Pass |
| Accountant LLM action proposal written | Pass |
| Accountant parser result written | Pass |
| Accountant proposal attempts written | Pass |
| Accountant Game Master decision written | Pass |
| Proposed events written | Pass |
| Metrics written | Pass |
| Final state written | Pass |

The validator is the source of mechanical validation for this generated pack.
"""


def write_m03_role_llm_artifact(output_dir: Path, result: RoleActionResult, *, suffix: str) -> None:
    action_id = result.action["action_id"]
    write_text(output_dir / "llm_prompts" / f"{result.role}_{action_id}_{suffix}.md", result.prompt_text)
    write_json(
        output_dir / "llm_outputs" / f"{result.role}_{action_id}_{suffix}.json",
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


def record_to_dict(record: M03RunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "buyer_approval_request_action_type": record.buyer_approval_request_action_type,
        "approver_action_type": record.approver_action_type,
        "buyer_accounting_handoff_action_type": record.buyer_accounting_handoff_action_type,
        "accountant_action_type": record.accountant_action_type,
        "buyer_approval_request_gm_decision": record.buyer_approval_request_gm_decision,
        "approver_gm_decision": record.approver_gm_decision,
        "buyer_accounting_handoff_gm_decision": record.buyer_accounting_handoff_gm_decision,
        "accountant_gm_decision": record.accountant_gm_decision,
        "approval_evidence_propagation": record.approval_evidence_propagation,
        "coordination_gap": record.coordination_gap,
        "validation_status": record.validation_status,
    }


def exclusion_to_dict(exclusion: M03ExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_m03_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_or_api_failure"
    return classify_exception(exc)


def m03_provider_label(buyer_provider: LLMProvider, approver_provider: LLMProvider, accountant_provider: LLMProvider) -> str:
    values = {buyer_provider.provider, approver_provider.provider, accountant_provider.provider}
    if len(values) == 1:
        return buyer_provider.provider
    return f"buyer:{buyer_provider.provider}; approver:{approver_provider.provider}; accountant:{accountant_provider.provider}"


def m03_model_label(buyer_provider: LLMProvider, approver_provider: LLMProvider, accountant_provider: LLMProvider) -> str:
    values = {buyer_provider.model, approver_provider.model, accountant_provider.model}
    if len(values) == 1:
        return buyer_provider.model
    return f"buyer:{buyer_provider.model}; approver:{approver_provider.model}; accountant:{accountant_provider.model}"
