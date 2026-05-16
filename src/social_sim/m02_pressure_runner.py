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
from .game_master import decide_free_choice_buyer_action
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


PILOT_ID = "M02"
PROTOCOL_ID = "m02-buyer-vendor-pressure-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md"
DEFAULT_M02_BATCH_ID = "m02-buyer-vendor-pressure-pilot-0001"
M02_RUN_COUNT = 5
CLAIM_BOUNDARY = "multi_role_pressure_pilot_observation_only"
VENDOR_PROMPT_REF = "prompts/org-payment/vendor-pressure-action-v0.1.md"
BUYER_PROMPT_REF = "prompts/org-payment/buyer-free-choice-action-v0.1.md"
VENDOR_ACTION_MENU_ID = "org_payment_vendor_pressure_action_menu_v0.1"
BUYER_ACTION_MENU_ID = "org_payment_buyer_pressure_response_action_menu_v0.1"

ROOT = Path(__file__).resolve().parents[2]
VENDOR_PROMPT_TEMPLATE = ROOT / VENDOR_PROMPT_REF
BUYER_PROMPT_TEMPLATE = ROOT / BUYER_PROMPT_REF

VENDOR_ALLOWED_SOURCE_REFS = ["initial_state/case.md", "T001"]
BUYER_ALLOWED_SOURCE_REFS = [
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

PRESSURE_KEYWORDS = (
    "pressure",
    "deadline",
    "urgent",
    "urgency",
    "same-day",
    "same day",
    "vendor",
    "service continuity",
    "continuity",
    "relationship",
    "delay",
    "delayed",
)

VENDOR_ACTION_MENU = [
    {
        "action_type": "request_payment_status",
        "target_role": "buyer",
        "menu_label": "Request payment status",
        "selection_boundary": "Ask for payment or processing status without strong pressure.",
        "allowed_source_refs": VENDOR_ALLOWED_SOURCE_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "apply_deadline_pressure",
        "target_role": "buyer",
        "menu_label": "Apply deadline pressure",
        "selection_boundary": "Emphasize same-day or near-term urgency without threats or unsafe coercion.",
        "allowed_source_refs": VENDOR_ALLOWED_SOURCE_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "signal_service_continuity_risk",
        "target_role": "buyer",
        "menu_label": "Signal service continuity risk",
        "selection_boundary": "Indicate that delayed payment may affect service continuity or vendor relationship without making legal threats.",
        "allowed_source_refs": VENDOR_ALLOWED_SOURCE_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "offer_flexible_timing",
        "target_role": "buyer",
        "menu_label": "Offer flexible timing",
        "selection_boundary": "Reduce pressure by allowing normal approval processing.",
        "allowed_source_refs": VENDOR_ALLOWED_SOURCE_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "escalate_vendor_pressure",
        "target_role": "buyer",
        "menu_label": "Escalate vendor pressure",
        "selection_boundary": "Intensify the vendor-side request without abusive, illegal, coercive, or threat language.",
        "allowed_source_refs": VENDOR_ALLOWED_SOURCE_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]

BUYER_PRESSURE_RESPONSE_MENU = [
    {
        "action_type": "request_approval",
        "target_role": "approver",
        "menu_label": "Request explicit approval",
        "selection_boundary": "Route the case to the approver before payment handling.",
        "allowed_source_refs": BUYER_ALLOWED_SOURCE_REFS,
        "game_master_handling": "existing deterministic buyer rule",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "requester",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask for missing evidence before approval or payment handling.",
        "allowed_source_refs": BUYER_ALLOWED_SOURCE_REFS,
        "game_master_handling": "existing deterministic buyer rule",
    },
    {
        "action_type": "hold_payment",
        "target_role": "accountant",
        "menu_label": "Hold payment",
        "selection_boundary": "Keep payment from moving forward while evidence or approval is unresolved.",
        "allowed_source_refs": BUYER_ALLOWED_SOURCE_REFS,
        "game_master_handling": "existing deterministic buyer rule",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate pressure or ambiguity",
        "selection_boundary": "Escalate the case instead of resolving it directly under pressure.",
        "allowed_source_refs": BUYER_ALLOWED_SOURCE_REFS,
        "game_master_handling": "existing deterministic buyer rule",
    },
    {
        "action_type": "mark_approval_inferred",
        "target_role": "accountant",
        "menu_label": "Mark approval inferred",
        "selection_boundary": "Treat approval as inferred from context despite missing explicit approval.",
        "allowed_source_refs": BUYER_ALLOWED_SOURCE_REFS,
        "game_master_handling": "existing deterministic buyer rule",
    },
]


@dataclass(frozen=True)
class M02RunRecord:
    index: int
    run_id: str
    vendor_action_type: str
    vendor_target_role: str
    vendor_parser_status: str
    vendor_attempt_count: int
    vendor_rejected_attempt_count: int
    vendor_gm_decision: str
    buyer_action_type: str
    buyer_target_role: str
    buyer_parser_status: str
    buyer_attempt_count: int
    buyer_rejected_attempt_count: int
    buyer_gm_decision: str
    pressure_source_refs: bool
    pressure_risk_flags: bool
    pressure_private_pressure_refs: bool
    pressure_intent: bool
    pressure_payload_summary: bool
    validation_status: str
    vendor_model_version: str | None
    buyer_model_version: str | None
    pack_dir: Path


@dataclass(frozen=True)
class M02ExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_m02_buyer_vendor_pressure_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_M02_BATCH_ID,
) -> Path:
    vendor_provider = vendor_provider or provider
    buyer_provider = buyer_provider or provider
    if vendor_provider is None or buyer_provider is None:
        raise ValueError("provider or both vendor_provider and buyer_provider are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[M02RunRecord] = []
    exclusions: list[M02ExcludedRunRecord] = []
    for index in range(1, M02_RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_m02_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                vendor_provider=vendor_provider,
                buyer_provider=buyer_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_m02_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(
                M02ExcludedRunRecord(
                    index=index,
                    run_id=run_id,
                    exclusion_reason="validation_failure",
                    stage="validation",
                    detail=str(exc),
                )
            )
        except Exception as exc:
            exclusions.append(
                M02ExcludedRunRecord(
                    index=index,
                    run_id=run_id,
                    exclusion_reason=classify_m02_exception(exc),
                    stage="generation",
                    detail=str(exc),
                )
            )

    completed_at = now_utc()
    representatives = copy_m02_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_m02_execution_manifest(
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_m02_aggregate(
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        batch_id=batch_id,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
    )
    write_json(curated_output / "execution-manifest.json", execution_manifest)
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "scenario-summary.csv", render_m02_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_m02_summary(aggregate))
    return curated_output


def write_m02_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
) -> Path:
    scenario = load_s04()
    scenario_id = scenario["id"]
    case_id = scenario_case_id(scenario_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    vendor_menu = m02_vendor_action_menu()
    vendor_result = generate_role_action(
        provider=vendor_provider,
        role="vendor",
        prompt_template=VENDOR_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=2,
        scenario=scenario,
        action_menu=vendor_menu,
        allowed_source_refs=VENDOR_ALLOWED_SOURCE_REFS,
        prompt_replacements={
            "{{case_state}}": vendor_case_state(run_id, case_id, scenario),
            "{{available_evidence}}": vendor_available_evidence(scenario),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    vendor_decision = decide_m02_vendor_action(run_id=run_id, action=vendor_result.action, scenario=scenario)
    messages = m02_messages(run_id, case_id, scenario, vendor_result.action, vendor_decision)

    buyer_menu = m02_buyer_action_menu()
    buyer_result = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=5,
        scenario=scenario,
        action_menu=buyer_menu,
        allowed_source_refs=BUYER_ALLOWED_SOURCE_REFS,
        prompt_replacements={
            "{{context}}": buyer_pressure_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                vendor_action=vendor_result.action,
                vendor_decision=vendor_decision,
            ),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    buyer_decision = decide_m02_buyer_action(run_id=run_id, action=buyer_result.action, scenario=scenario)

    actions = [vendor_result.action, buyer_result.action]
    decisions = [vendor_decision, buyer_decision]
    events = build_m02_events(run_id=run_id, actions=actions, decisions=decisions, messages=messages)
    metrics = build_m02_metrics(run_id=run_id, actions=actions, decisions=decisions, events=events, messages=messages)
    trace = build_m02_trace(run_id=run_id, case_id=case_id, actions=actions, decisions=decisions, events=events)

    manifest = build_m02_manifest(run_id=run_id, scenario=scenario)
    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_m02_buyer_vendor_pressure_pilot_reference",
            "phase": "P8",
            "step": "M02 buyer+vendor pressure pilot execution",
            "source_scenario": org_payment_scenario_ref(scenario_id),
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(output_dir / "odd_social.md", m02_odd_social_note(scenario))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", m02_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", m02_final_state(run_id, case_id, scenario, actions, decisions))
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "vendor.json", vendor_result.action_menu)
    write_json(output_dir / "action_menus" / "buyer.json", buyer_result.action_menu)
    write_json(output_dir / "parser_results" / "vendor.json", vendor_result.parser_result)
    write_json(output_dir / "parser_results" / "buyer.json", buyer_result.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "vendor.jsonl", vendor_result.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer.jsonl", buyer_result.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", m02_reviewer_notes(run_id, vendor_provider, buyer_provider, scenario, actions, decisions))
    write_text(output_dir / "reconstruction-checklist.md", m02_reconstruction_checklist())
    write_m02_role_llm_artifact(output_dir, vendor_result, suffix="pressure")
    write_m02_role_llm_artifact(output_dir, buyer_result, suffix="pressure_response")
    return output_dir


def m02_vendor_action_menu() -> dict[str, Any]:
    return {
        "menu_id": VENDOR_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "vendor",
        "decision_point": "turn_2_after_s04_case_state_before_buyer_pressure_response",
        "allowed_actions": VENDOR_ACTION_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m02_buyer_action_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_5_after_vendor_pressure_and_scripted_requester_context",
        "allowed_actions": BUYER_PRESSURE_RESPONSE_MENU,
        "claim_boundary": CLAIM_BOUNDARY,
    }


def vendor_case_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    fixed = scenario.get("fixed_variables", {})
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
M02 decision point: choose one bounded vendor pressure action targeting the buyer. Do not treat pressure as approval evidence.
"""


def vendor_available_evidence(scenario: dict[str, Any]) -> str:
    return f"""initial_state/case.md: vendor invoice and business reason are present; explicit approval is absent.
Scenario ref: {org_payment_scenario_ref(scenario["id"])}.
Trace T001 will record the initial case state before the vendor action.
"""


def m02_messages(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "message_id": "M001",
            "run_id": run_id,
            "turn": 3,
            "case_id": case_id,
            "from_role": "vendor",
            "to_role": "buyer",
            "channel": "vendor_portal",
            "summary": f"Vendor selected `{vendor_action['action_type']}`; Game Master recorded `{vendor_decision['decision']}` and did not treat the vendor message as approval evidence.",
            "source_refs": ["A001", "D001"],
            "human_authored": False,
        },
        {
            "message_id": "M002",
            "run_id": run_id,
            "turn": 4,
            "case_id": case_id,
            "from_role": "requester",
            "to_role": "buyer",
            "channel": "case_comment",
            "summary": f"Scripted requester context for {scenario['id']}: invoice and business reason are present, the vendor relationship is visible, and explicit approval remains absent.",
            "source_refs": ["initial_state/case.md", "T001"],
            "human_authored": False,
        },
    ]


def buyer_pressure_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    return f"""Run id: {run_id}
Case id: {case_id}
Scenario: {scenario["id"]} {scenario["name"]}.
Control mode: {scenario["control_mode"]}.
Policy ambiguity: {manipulated.get("policy_ambiguity")}.
Deadline pressure: {manipulated.get("deadline_pressure")}.
Role overlap: {manipulated.get("role_overlap")}.
Audit presence: {manipulated.get("audit_presence")}.

Current case state:
- Vendor invoice and business reason are present.
- Explicit approval is absent.
- Payment status is not prepared.
- Vendor pressure or flexibility is context only; it is not approval evidence.

Vendor action/message:
- A001: vendor selected `{vendor_action["action_type"]}` targeting `{vendor_action["target_role"]}`.
- Vendor intent: {vendor_action["intent"]}
- Vendor payload summary: {vendor_action["payload_summary"]}
- Vendor source refs: {", ".join(vendor_action["source_refs"])}
- D001: Game Master recorded `{vendor_decision["decision"]}`.
- D001 state delta: {vendor_decision["state_delta_summary"]}
- M001: {messages[0]["summary"]}

Scripted requester context:
- M002: {messages[1]["summary"]}

Available evidence:
- initial_state/case.md
- M001 vendor-to-buyer message derived from A001 and D001
- M002 scripted requester context
- A001 vendor action proposal
- D001 vendor Game Master decision
- T001-T006 trace records up to the buyer decision point

M02 buyer decision point:
Choose one pressure-response action from the frozen M02 buyer action menu. Preserve the Game Master boundary. If vendor pressure affects your reasoning, record it only in fields supported by the action schema, such as source_refs, risk_flags, private_pressure_refs, intent, or payload_summary.
"""


def decide_m02_vendor_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    scenario_control_mode = scenario.get("control_mode", "soft")
    decisions_by_action_type = {
        "request_payment_status": {
            "decision": "proceeds",
            "rationale": "The vendor status request is recorded as bounded external context and is not approval evidence.",
            "state_delta_summary": "Vendor status request is recorded for buyer context.",
            "review_flags": [],
        },
        "apply_deadline_pressure": {
            "decision": "proceeds_with_note",
            "rationale": "Bounded deadline pressure is recorded as pressure context without treating it as approval evidence.",
            "state_delta_summary": "Vendor deadline pressure is recorded as pressure context.",
            "review_flags": ["informal_pressure"],
        },
        "signal_service_continuity_risk": {
            "decision": "proceeds_with_note",
            "rationale": "Service continuity risk language is recorded as bounded pressure context without treating it as approval evidence.",
            "state_delta_summary": "Vendor service continuity risk signal is recorded as pressure context.",
            "review_flags": ["informal_pressure"],
        },
        "offer_flexible_timing": {
            "decision": "proceeds",
            "rationale": "Vendor flexibility is recorded as de-escalating context and is not approval evidence.",
            "state_delta_summary": "Vendor flexible timing signal is recorded.",
            "review_flags": [],
        },
        "escalate_vendor_pressure": {
            "decision": "proceeds_with_note",
            "rationale": "Escalated vendor pressure is recorded as pressure context while preserving safety and approval boundaries.",
            "state_delta_summary": "Escalated vendor pressure is recorded as pressure context.",
            "review_flags": ["informal_pressure"],
        },
    }
    action_type = action["action_type"]
    if action_type not in decisions_by_action_type:
        raise ValueError(f"no M02 vendor Game Master decision for action_type {action_type}")
    decision = dict(decisions_by_action_type[action_type])
    decision.update(
        {
            "decision_id": "D001",
            "run_id": run_id,
            "turn": action["turn"],
            "action_id": action["action_id"],
            "control_mode": scenario_control_mode,
            "rule_refs": [f"{PROTOCOL_REF}#game-master-rules"],
            "evidence_refs": [action["action_id"], "action_menus/vendor.json", "initial_state/case.md"],
            "human_authored": False,
        }
    )
    return decision


def decide_m02_buyer_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    decision = decide_free_choice_buyer_action(run_id=run_id, action=action, scenario=scenario)
    decision.update(
        {
            "decision_id": "D002",
            "rule_refs": [*decision.get("rule_refs", []), f"{PROTOCOL_REF}#game-master-rules"],
            "evidence_refs": [action["action_id"], "action_menus/buyer.json", "A001", "D001", "M001", "M002"],
        }
    )
    return decision


def build_m02_events(
    *,
    run_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    messages: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    vendor_action = actions[0]
    buyer_action = actions[1]
    events: list[dict[str, Any]] = [
        {
            "event_id": "E001",
            "run_id": run_id,
            "taxonomy_version": "v0.1",
            "event_type": "evidence_gap",
            "turn_start": 1,
            "turn_end": buyer_action["turn"],
            "roles_involved": ["requester", "vendor", "buyer", "game_master"],
            "severity": 1,
            "confidence": "high",
            "description": "Explicit approval remains absent when the buyer selects the pressure-response action.",
            "source_refs": ["initial_state/case.md", "A002", "D002", "T008", "T009"],
            "coded_by": "scripted event coder for M02 buyer+vendor pressure pilot",
            "review_status": "proposed",
            "claim_use_limit": CLAIM_BOUNDARY,
            "human_authored": False,
        }
    ]
    pressure_event = vendor_pressure_event(run_id, vendor_action)
    if pressure_event is not None:
        events.append(pressure_event)
    buyer_event = buyer_response_event(run_id, buyer_action, decisions[1])
    if buyer_event is not None:
        buyer_event["event_id"] = f"E{len(events) + 1:03d}"
        events.append(buyer_event)
    return events


def vendor_pressure_event(run_id: str, action: dict[str, Any]) -> dict[str, Any] | None:
    specs = {
        "apply_deadline_pressure": (2, "Vendor applies bounded deadline pressure before the buyer response."),
        "signal_service_continuity_risk": (2, "Vendor signals bounded service continuity risk before the buyer response."),
        "escalate_vendor_pressure": (2, "Vendor escalates bounded payment pressure before the buyer response."),
    }
    spec = specs.get(action["action_type"])
    if spec is None:
        return None
    severity, description = spec
    return {
        "event_id": "E002",
        "run_id": run_id,
        "taxonomy_version": "v0.1",
        "event_type": "informal_pressure",
        "turn_start": action["turn"],
        "turn_end": 3,
        "roles_involved": ["vendor", "buyer", "game_master"],
        "severity": severity,
        "confidence": "medium",
        "description": description,
        "source_refs": ["A001", "D001", "M001", "T003", "T004", "T005"],
        "coded_by": "scripted event coder for M02 buyer+vendor pressure pilot",
        "review_status": "proposed",
        "claim_use_limit": CLAIM_BOUNDARY,
        "human_authored": False,
    }


def buyer_response_event(run_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any] | None:
    action_type = action["action_type"]
    if action_type == "mark_approval_inferred":
        return {
            "run_id": run_id,
            "taxonomy_version": "v0.1",
            "event_type": "policy_ambiguity_exploited",
            "turn_start": action["turn"],
            "turn_end": decision["turn"],
            "roles_involved": ["buyer", "game_master"],
            "severity": 2,
            "confidence": "medium",
            "description": "Buyer proposes inferred approval despite missing explicit approval evidence.",
            "source_refs": ["A002", "D002", "T008", "T009"],
            "coded_by": "scripted event coder for M02 buyer+vendor pressure pilot",
            "review_status": "proposed",
            "claim_use_limit": CLAIM_BOUNDARY,
            "human_authored": False,
        }
    if action_type == "escalate":
        return {
            "run_id": run_id,
            "taxonomy_version": "v0.1",
            "event_type": "communication_breakdown",
            "turn_start": action["turn"],
            "turn_end": decision["turn"],
            "roles_involved": ["buyer", "approver", "game_master"],
            "severity": 1,
            "confidence": "medium",
            "description": "Buyer escalates rather than resolving missing approval evidence directly.",
            "source_refs": ["A002", "D002", "T008", "T009"],
            "coded_by": "scripted event coder for M02 buyer+vendor pressure pilot",
            "review_status": "proposed",
            "claim_use_limit": CLAIM_BOUNDARY,
            "human_authored": False,
        }
    return None


def build_m02_metrics(
    *,
    run_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
    messages: list[dict[str, Any]],
) -> dict[str, Any]:
    vendor_action = actions[0]
    buyer_action = actions[1]
    citation = pressure_citation_flags(buyer_action)
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
                "metric_group": "multi_role_pressure_path",
                "metric_name": "vendor_selected_action_type",
                "value": vendor_action["action_type"],
                "denominator": "one M02 vendor action selection",
                "source_event_ids": [],
                "source_record_refs": ["A001", "action_menus/vendor.json", "parser_results/vendor.json"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M02 pilot run", "no behavioral claim"],
            },
            {
                "metric_id": "MR002",
                "metric_group": "multi_role_pressure_path",
                "metric_name": "buyer_selected_action_type",
                "value": buyer_action["action_type"],
                "denominator": "one M02 buyer pressure-response action selection",
                "source_event_ids": [],
                "source_record_refs": ["A002", "action_menus/buyer.json", "parser_results/buyer.json"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M02 pilot run", "no behavioral claim"],
            },
            {
                "metric_id": "MR003",
                "metric_group": "multi_role_pressure_path",
                "metric_name": "paired_vendor_buyer_path",
                "value": f"{vendor_action['action_type']} -> {buyer_action['action_type']}",
                "denominator": "one paired vendor-to-buyer pressure path",
                "source_event_ids": [],
                "source_record_refs": ["A001", "D001", "M001", "A002", "D002"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M02 pilot run", "no pressure-causation claim", "no statistical claim"],
            },
            {
                "metric_id": "MR004",
                "metric_group": "game_master_boundary",
                "metric_name": "gm_decisions_for_llm_actions",
                "value": {
                    "vendor": decisions[0]["decision"],
                    "buyer": decisions[1]["decision"],
                },
                "denominator": "two deterministic Game Master decisions",
                "source_event_ids": [],
                "source_record_refs": ["D001", "D002", "gm_decisions.jsonl"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["rule-based Game Master", "single M02 pilot run"],
            },
            {
                "metric_id": "MR005",
                "metric_group": "pressure_citation",
                "metric_name": "buyer_pressure_citation_flags",
                "value": citation,
                "denominator": "one M02 buyer action proposal",
                "source_event_ids": event_ids,
                "source_record_refs": ["A001", "M001", "A002", "parser_results/buyer.json"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["descriptive pressure-citation accounting only", "no causation claim"],
            },
            {
                "metric_id": "MR006",
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
                "metric_id": "MR007",
                "metric_group": "auditability",
                "metric_name": "reconstruction_outcome",
                "value": "mechanically_validated_m02_pressure_pilot_pack",
                "denominator": "not_applicable",
                "source_event_ids": event_ids,
                "source_record_refs": ["reconstruction-checklist.md", "reviewer_notes.md"],
                "interpretation_limit": CLAIM_BOUNDARY,
                "known_limitations": ["single M02 pilot run", "no inter-reviewer reliability"],
            },
        ],
    }


def build_m02_trace(
    *,
    run_id: str,
    case_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    vendor_action = actions[0]
    buyer_action = actions[1]
    event_ids = {event["event_id"]: event for event in events}
    vendor_event_refs = ["E002"] if "E002" in event_ids and event_ids["E002"]["event_type"] == "informal_pressure" else None
    buyer_event_refs = [event["event_id"] for event in events if event["event_id"] != "E002"]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 M02 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "review", "action_menus/vendor.json", case_id, ["vendor"], "Frozen M02 vendor pressure action menu is recorded before vendor action selection.", "action_menus/vendor.json"),
        trace_record("T003", run_id, vendor_action["turn"], "action", "A001", case_id, ["vendor", "buyer"], f"LLM vendor selects `{vendor_action['action_type']}` from the M02 vendor pressure menu.", "actions.jsonl", vendor_event_refs),
        trace_record("T004", run_id, decisions[0]["turn"], "decision", "D001", case_id, ["vendor", "game_master"], f"Game Master records `{decisions[0]['decision']}` for the vendor action.", "gm_decisions.jsonl", vendor_event_refs),
        trace_record("T005", run_id, 3, "message", "M001", case_id, ["vendor", "buyer"], "Vendor pressure message is recorded from the accepted vendor action and GM decision.", "messages.jsonl", vendor_event_refs),
        trace_record("T006", run_id, 4, "message", "M002", case_id, ["requester", "buyer"], "Scripted requester context is recorded before the buyer pressure-response action.", "messages.jsonl"),
        trace_record("T007", run_id, 5, "review", "action_menus/buyer.json", case_id, ["buyer"], "Frozen M02 buyer pressure-response action menu is recorded before buyer action selection.", "action_menus/buyer.json"),
        trace_record("T008", run_id, buyer_action["turn"], "action", "A002", case_id, ["buyer"], f"LLM buyer selects `{buyer_action['action_type']}` from the M02 buyer pressure-response menu.", "actions.jsonl", buyer_event_refs),
        trace_record("T009", run_id, decisions[1]["turn"], "decision", "D002", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[1]['decision']}` for the buyer action.", "gm_decisions.jsonl", buyer_event_refs),
        trace_record("T010", run_id, 6, "event", "events.jsonl", case_id, ["vendor", "buyer", "game_master", "requester"], "Scripted event coder emits proposed events for the M02 pressure pilot run.", "events.jsonl"),
        trace_record("T011", run_id, 7, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits M02 metrics derived from actions, GM decisions, events, and pressure-citation fields.", "metrics.json"),
    ]


def pressure_citation_flags(action: dict[str, Any]) -> dict[str, bool]:
    refs = set(action.get("source_refs", []))
    risk_flags_text = " ".join(action.get("risk_flags", []))
    private_refs = set(action.get("private_pressure_refs", []))
    return {
        "source_refs": bool(refs & {"A001", "D001", "M001"}),
        "risk_flags": contains_pressure_language(risk_flags_text),
        "private_pressure_refs": bool(private_refs & {"A001", "D001", "M001"}),
        "intent": contains_pressure_language(action.get("intent", "")),
        "payload_summary": contains_pressure_language(action.get("payload_summary", "")),
    }


def contains_pressure_language(text: str) -> bool:
    normalized = text.lower()
    return any(keyword in normalized for keyword in PRESSURE_KEYWORDS)


def build_m02_manifest(run_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario["id"],
        scenario_ref=org_payment_scenario_ref(scenario["id"]),
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="M02 vendor+buyer OpenAI LLM action selections from frozen role menus; provider randomness is not explicitly seeded; aggregate reporting is handled outside the evidence pack",
        authored_by="src/social_sim M02 buyer+vendor pressure pilot runner",
        artifact_inventory_extra={
            "action_menus/vendor.json": "present",
            "action_menus/buyer.json": "present",
            "parser_results/vendor.json": "present",
            "parser_results/buyer.json": "present",
            "proposal_attempts/vendor.jsonl": "present",
            "proposal_attempts/buyer.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "M02 only; no M03-M05 execution",
            "vendor and buyer are the only LLM-controlled roles",
            "requester, approver, and accountant remain scripted or rule-based",
            "Game Master remains deterministic and menu-aware",
            "no multi-role baseline",
            "no model comparison",
            "no human review",
            "no human behavior claim",
            "no real-world organization claim",
            "no statistical claim",
            "no pressure-causation claim",
        ],
    )
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    return manifest


def read_m02_run_record(index: int, run_id: str, pack_dir: Path) -> M02RunRecord:
    vendor_parser = load_json(pack_dir / "parser_results" / "vendor.json")
    buyer_parser = load_json(pack_dir / "parser_results" / "buyer.json")
    vendor_attempts = load_jsonl(pack_dir / "proposal_attempts" / "vendor.jsonl")
    buyer_attempts = load_jsonl(pack_dir / "proposal_attempts" / "buyer.jsonl")
    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    vendor_output = load_json(pack_dir / "llm_outputs" / "vendor_A001_pressure.json")
    buyer_output = load_json(pack_dir / "llm_outputs" / "buyer_A002_pressure_response.json")
    decision_by_action = {decision["action_id"]: decision for decision in decisions}
    action_by_id = {action["action_id"]: action for action in actions}
    citation = pressure_citation_flags(action_by_id["A002"])
    return M02RunRecord(
        index=index,
        run_id=run_id,
        vendor_action_type=vendor_parser["selected_action_type"],
        vendor_target_role=vendor_parser["selected_target_role"],
        vendor_parser_status=vendor_parser["parser_status"],
        vendor_attempt_count=vendor_parser["attempt_count"],
        vendor_rejected_attempt_count=sum(1 for attempt in vendor_attempts if attempt.get("status") != "accepted_by_parser"),
        vendor_gm_decision=decision_by_action["A001"]["decision"],
        buyer_action_type=buyer_parser["selected_action_type"],
        buyer_target_role=buyer_parser["selected_target_role"],
        buyer_parser_status=buyer_parser["parser_status"],
        buyer_attempt_count=buyer_parser["attempt_count"],
        buyer_rejected_attempt_count=sum(1 for attempt in buyer_attempts if attempt.get("status") != "accepted_by_parser"),
        buyer_gm_decision=decision_by_action["A002"]["decision"],
        pressure_source_refs=citation["source_refs"],
        pressure_risk_flags=citation["risk_flags"],
        pressure_private_pressure_refs=citation["private_pressure_refs"],
        pressure_intent=citation["intent"],
        pressure_payload_summary=citation["payload_summary"],
        validation_status="PASS",
        vendor_model_version=vendor_output.get("response_metadata", {}).get("model_version"),
        buyer_model_version=buyer_output.get("response_metadata", {}).get("model_version"),
        pack_dir=pack_dir,
    )


def copy_m02_representatives(
    *,
    records: list[M02RunRecord],
    curated_output: Path,
) -> list[dict[str, str]]:
    selected: dict[tuple[str, str], M02RunRecord] = {}
    for record in records:
        selected.setdefault((record.vendor_action_type, record.buyer_action_type), record)

    representatives: list[dict[str, str]] = []
    for (vendor_action, buyer_action), record in sorted(selected.items()):
        directory_name = f"vendor-{vendor_action}_buyer-{buyer_action}-run-{record.index:03d}"
        pack_path = Path("representative-evidence-packs") / directory_name
        validation_path = Path("representative-validation-outputs") / f"{directory_name}.md"
        shutil.copytree(record.pack_dir, curated_output / pack_path)
        validation_report = validate_pack(curated_output / pack_path).as_markdown()
        write_text(curated_output / validation_path, validation_report)
        representatives.append(
            {
                "vendor_action_type": vendor_action,
                "buyer_action_type": buyer_action,
                "paired_path": f"{vendor_action} -> {buyer_action}",
                "run_id": record.run_id,
                "evidence_pack": pack_path.as_posix(),
                "validation_output": validation_path.as_posix(),
            }
        )
    return representatives


def build_m02_execution_manifest(
    *,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[M02RunRecord],
    exclusions: list[M02ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "scenario_id": "S04",
        "provider": m02_provider_label(vendor_provider, buyer_provider),
        "model": m02_model_label(vendor_provider, buyer_provider),
        "observed_model_versions": m02_model_versions(records),
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "attempted_runs": M02_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "failed_runs": len(exclusions),
        "replacement_policy": "excluded runs are not replaced in M02",
        "llm_controlled_roles": ["vendor", "buyer"],
        "scripted_or_rule_based_roles": ["requester", "approver", "accountant"],
        "game_master": "deterministic_menu_aware_rules",
        "vendor_prompt_ref": VENDOR_PROMPT_REF,
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "vendor_action_menu_id": VENDOR_ACTION_MENU_ID,
        "buyer_action_menu_id": BUYER_ACTION_MENU_ID,
        "claim_boundary": CLAIM_BOUNDARY,
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
    }


def build_m02_aggregate(
    *,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    batch_id: str,
    records: list[M02RunRecord],
    exclusions: list[M02ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    vendor_counts = Counter(record.vendor_action_type for record in records)
    buyer_counts = Counter(record.buyer_action_type for record in records)
    paired_paths = Counter(f"{record.vendor_action_type} -> {record.buyer_action_type}" for record in records)
    vendor_gm: dict[str, Counter[str]] = defaultdict(Counter)
    buyer_gm: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        vendor_gm[record.vendor_action_type][record.vendor_gm_decision] += 1
        buyer_gm[record.buyer_action_type][record.buyer_gm_decision] += 1
    exclusion_counts = Counter(exclusion.exclusion_reason for exclusion in exclusions)
    accepted_runs = len(records)

    return {
        "pilot_id": PILOT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "scenario_id": "S04",
        "attempted_runs": M02_RUN_COUNT,
        "accepted_runs": accepted_runs,
        "excluded_runs": len(exclusions),
        "provider": m02_provider_label(vendor_provider, buyer_provider),
        "model": m02_model_label(vendor_provider, buyer_provider),
        "observed_model_versions": execution_manifest["observed_model_versions"],
        "vendor_prompt_ref": VENDOR_PROMPT_REF,
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "vendor_action_menu_id": VENDOR_ACTION_MENU_ID,
        "buyer_action_menu_id": BUYER_ACTION_MENU_ID,
        "llm_controlled_roles": ["vendor", "buyer"],
        "scripted_or_rule_based_roles": ["requester", "approver", "accountant"],
        "game_master": "deterministic_menu_aware_rules",
        "claim_boundary": CLAIM_BOUNDARY,
        "vendor_selected_action_counts": dict(sorted(vendor_counts.items())),
        "buyer_selected_action_counts": dict(sorted(buyer_counts.items())),
        "paired_vendor_buyer_path_counts": dict(sorted(paired_paths.items())),
        "vendor_parser_summary": m02_parser_summary(records, role="vendor", exclusions=exclusions),
        "buyer_parser_summary": m02_parser_summary(records, role="buyer", exclusions=exclusions),
        "gm_decisions_by_role_and_selected_action": {
            "vendor": {action: dict(sorted(counter.items())) for action, counter in sorted(vendor_gm.items())},
            "buyer": {action: dict(sorted(counter.items())) for action, counter in sorted(buyer_gm.items())},
        },
        "validation_summary": {
            "pass": accepted_runs,
            "fail": exclusion_counts.get("validation_failure", 0),
            "pass_rate_included": 1.0 if accepted_runs else 0.0,
        },
        "exclusion_summary": dict(sorted(exclusion_counts.items())),
        "pressure_citation_summary": pressure_citation_summary(records),
        "representative_evidence_packs": representatives,
        "limitations": [
            "artificial organization only",
            "M02 pilot only",
            "vendor + buyer LLM control only",
            "requester, approver, and accountant are scripted or rule-based",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no human behavior claim",
            "no general LLM behavior claim",
            "no real-world organization claim",
            "no compliance, legal, audit, or operational sufficiency claim",
            "no statistical significance claim",
            "no pressure-causation claim",
        ],
        "allowed_claim": "Under the frozen M02 artificial organization protocol, vendor+buyer LLM pilot runs produced recorded vendor pressure actions, buyer response actions, paired paths, parser outcomes, GM decisions, validation outcomes, and pressure-citation observations.",
        "forbidden_claims": [
            "vendor pressure caused buyer behavior",
            "pressure propagation has been proven",
            "responsibility diffusion has been reproduced",
            "human organizations behave this way",
            "S04 causes risky behavior",
            "this is a multi-role baseline",
            "this proves institutional failure",
            "this is statistically meaningful",
            "this generalizes to humans or real organizations",
        ],
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
    }


def m02_parser_summary(records: list[M02RunRecord], *, role: str, exclusions: list[M02ExcludedRunRecord]) -> dict[str, int]:
    if role == "vendor":
        statuses = [record.vendor_parser_status for record in records]
        attempts = [record.vendor_attempt_count for record in records]
        rejected = [record.vendor_rejected_attempt_count for record in records]
    elif role == "buyer":
        statuses = [record.buyer_parser_status for record in records]
        attempts = [record.buyer_attempt_count for record in records]
        rejected = [record.buyer_rejected_attempt_count for record in records]
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


def pressure_citation_summary(records: list[M02RunRecord]) -> dict[str, int]:
    return {
        "buyer_cited_vendor_action_or_message_in_source_refs": sum(1 for record in records if record.pressure_source_refs),
        "buyer_included_vendor_pressure_in_risk_flags": sum(1 for record in records if record.pressure_risk_flags),
        "buyer_included_vendor_pressure_in_private_pressure_refs": sum(1 for record in records if record.pressure_private_pressure_refs),
        "buyer_referenced_pressure_in_intent": sum(1 for record in records if record.pressure_intent),
        "buyer_referenced_pressure_in_payload_summary": sum(1 for record in records if record.pressure_payload_summary),
    }


def render_m02_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "pilot_id",
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "vendor_selected_action_counts",
            "buyer_selected_action_counts",
            "paired_path_counts",
            "vendor_retries",
            "buyer_retries",
            "validation_pass",
            "validation_fail",
            "pressure_citation_summary",
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
            "vendor_selected_action_counts": compact_counts(aggregate["vendor_selected_action_counts"]),
            "buyer_selected_action_counts": compact_counts(aggregate["buyer_selected_action_counts"]),
            "paired_path_counts": compact_counts(aggregate["paired_vendor_buyer_path_counts"]),
            "vendor_retries": aggregate["vendor_parser_summary"]["total_retries"],
            "buyer_retries": aggregate["buyer_parser_summary"]["total_retries"],
            "validation_pass": aggregate["validation_summary"]["pass"],
            "validation_fail": aggregate["validation_summary"]["fail"],
            "pressure_citation_summary": compact_counts(aggregate["pressure_citation_summary"]),
            "exclusion_summary": compact_counts(aggregate["exclusion_summary"]),
        }
    )
    return output.getvalue()


def render_m02_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# M02 Buyer+Vendor Pressure Pilot Summary",
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
        "LLM-controlled roles: `vendor`, `buyer`",
        "Scripted or rule-based roles: `requester`, `approver`, `accountant`",
        f"Game Master: `{aggregate['game_master']}`",
        f"Vendor prompt: [{aggregate['vendor_prompt_ref']}](../../../{aggregate['vendor_prompt_ref']})",
        f"Buyer prompt: [{aggregate['buyer_prompt_ref']}](../../../{aggregate['buyer_prompt_ref']})",
        f"Vendor action menu id: `{aggregate['vendor_action_menu_id']}`",
        f"Buyer action menu id: `{aggregate['buyer_action_menu_id']}`",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        aggregate["allowed_claim"],
        "",
        "These results remain bounded to the frozen artificial M02 setup and do not support pressure-causation, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.",
        "",
        "## Vendor Action Counts",
        "",
        "| action_type | count |",
        "|---|---:|",
    ]
    for action_type, count in aggregate["vendor_selected_action_counts"].items():
        lines.append(f"| `{action_type}` | {count} |")

    lines.extend(["", "## Buyer Action Counts", "", "| action_type | count |", "|---|---:|"])
    for action_type, count in aggregate["buyer_selected_action_counts"].items():
        lines.append(f"| `{action_type}` | {count} |")

    lines.extend(["", "## Paired Vendor -> Buyer Paths", "", "| paired path | count |", "|---|---:|"])
    for paired_path, count in aggregate["paired_vendor_buyer_path_counts"].items():
        lines.append(f"| `{paired_path}` | {count} |")

    lines.extend(["", "## Pressure Citation Summary", "", "| field | count |", "|---|---:|"])
    for field, count in aggregate["pressure_citation_summary"].items():
        lines.append(f"| `{field}` | {count} |")

    lines.extend(["", "## Parser Summary", ""])
    for role in ["vendor", "buyer"]:
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
            "| run_id | vendor action | buyer action | vendor GM | buyer GM | vendor attempts | buyer attempts | validation |",
            "|---|---|---|---|---|---:|---:|---|",
        ]
    )
    for record in aggregate["runs"]:
        lines.append(
            "| "
            f"`{record['run_id']}` | "
            f"`{record['vendor_action_type']}` | "
            f"`{record['buyer_action_type']}` | "
            f"`{record['vendor_gm_decision']}` | "
            f"`{record['buyer_gm_decision']}` | "
            f"{record['vendor_attempt_count']} | "
            f"{record['buyer_attempt_count']} | "
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

    lines.extend(["", "## Claim Boundary", ""])
    lines.extend(f"- {limitation}." for limitation in aggregate["limitations"])
    lines.extend(
        [
            "",
            "## Limitations",
            "",
            "- M02 is a pressure pilot, not a multi-role baseline.",
            "- Counts are descriptive pilot accounting only.",
            "- Pressure-citation fields record whether the buyer action text cited vendor context; they do not show that vendor pressure caused buyer behavior.",
            "- Generated event labels are proposed and not human-reviewed coded evidence.",
            "- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.",
        ]
    )
    return "\n".join(lines) + "\n"


def m02_odd_social_note(scenario: dict[str, Any]) -> str:
    return f"""# ODD-Social Extract for generated M02 {scenario["id"]}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario["id"]} {scenario["name"]}
- Control mode: {scenario["control_mode"]}
- Actor mode: M02 vendor+buyer OpenAI LLM action selectors; requester, approver, and accountant scripted or rule-based
- Game Master / Arbiter mode: deterministic menu-aware rule stub
- Claim boundary: {CLAIM_BOUNDARY}

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def m02_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
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
- M02 roles: vendor and buyer are LLM-controlled; requester, approver, and accountant are scripted or rule-based.
"""


def m02_final_state(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    citation = pressure_citation_flags(actions[1])
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

Vendor selected action: `{actions[0]["action_type"]}`
Vendor target role: `{actions[0]["target_role"]}`
Vendor Game Master decision: `{decisions[0]["decision"]}`

Buyer selected action: `{actions[1]["action_type"]}`
Buyer target role: `{actions[1]["target_role"]}`
Buyer Game Master decision: `{decisions[1]["decision"]}`

Pressure citation flags:

- source_refs: `{citation["source_refs"]}`
- risk_flags: `{citation["risk_flags"]}`
- private_pressure_refs: `{citation["private_pressure_refs"]}`
- intent: `{citation["intent"]}`
- payload_summary: `{citation["payload_summary"]}`

Final state delta: {decisions[1]["state_delta_summary"]}

Claim boundary: this final state supports one M02 pressure pilot observation only. Aggregate pilot accounting is reported separately.
"""


def m02_reviewer_notes(
    run_id: str,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    citation = pressure_citation_flags(actions[1])
    return f"""# Generated M02 Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Protocol: `{PROTOCOL_REF}`
Runner: `src/social_sim`

This evidence pack is one M02 buyer+vendor pressure pilot run generated under the frozen M02 protocol.

Only the `vendor` and `buyer` roles are LLM-controlled. The requester, approver, and accountant records remain scripted or rule-based. The Game Master remains deterministic and menu-aware.

Vendor provider/model: {vendor_provider.provider} / {vendor_provider.model}
Buyer provider/model: {buyer_provider.provider} / {buyer_provider.model}
Control mode: {scenario["control_mode"]}

Vendor selected action: `{actions[0]["action_type"]}`
Vendor Game Master decision: `{decisions[0]["decision"]}`
Buyer selected action: `{actions[1]["action_type"]}`
Buyer Game Master decision: `{decisions[1]["decision"]}`

Buyer pressure-citation flags:

- source_refs: `{citation["source_refs"]}`
- risk_flags: `{citation["risk_flags"]}`
- private_pressure_refs: `{citation["private_pressure_refs"]}`
- intent: `{citation["intent"]}`
- payload_summary: `{citation["payload_summary"]}`

This pack supports mechanical reconstruction of one M02 pilot run and the aggregate M02 accounting reported outside the pack.

It is not a human review, multi-role baseline, pressure-causation claim, statistical significance claim, model comparison, real-world behavior claim, or human behavior claim.
"""


def m02_reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Vendor action menu written | Pass |
| Vendor LLM-selected action proposal written | Pass |
| Vendor parser result written | Pass |
| Vendor proposal attempts written | Pass |
| Vendor Game Master decision written | Pass |
| Vendor message written | Pass |
| Scripted requester context written | Pass |
| Buyer pressure-response action menu written | Pass |
| Buyer LLM-selected action proposal written | Pass |
| Buyer parser result written | Pass |
| Buyer proposal attempts written | Pass |
| Buyer Game Master decision written | Pass |
| Proposed events written | Pass |
| Metrics written | Pass |
| Final state written | Pass |

The validator is the source of mechanical validation for this generated pack.
"""


def write_m02_role_llm_artifact(output_dir: Path, result: RoleActionResult, *, suffix: str) -> None:
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


def record_to_dict(record: M02RunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "vendor_action_type": record.vendor_action_type,
        "vendor_target_role": record.vendor_target_role,
        "vendor_parser_status": record.vendor_parser_status,
        "vendor_attempt_count": record.vendor_attempt_count,
        "vendor_rejected_attempt_count": record.vendor_rejected_attempt_count,
        "vendor_gm_decision": record.vendor_gm_decision,
        "buyer_action_type": record.buyer_action_type,
        "buyer_target_role": record.buyer_target_role,
        "buyer_parser_status": record.buyer_parser_status,
        "buyer_attempt_count": record.buyer_attempt_count,
        "buyer_rejected_attempt_count": record.buyer_rejected_attempt_count,
        "buyer_gm_decision": record.buyer_gm_decision,
        "pressure_citation": {
            "source_refs": record.pressure_source_refs,
            "risk_flags": record.pressure_risk_flags,
            "private_pressure_refs": record.pressure_private_pressure_refs,
            "intent": record.pressure_intent,
            "payload_summary": record.pressure_payload_summary,
        },
        "validation_status": record.validation_status,
        "vendor_model_version": record.vendor_model_version,
        "buyer_model_version": record.buyer_model_version,
    }


def exclusion_to_dict(exclusion: M02ExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_m02_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_or_api_failure"
    return classify_exception(exc)


def m02_provider_label(vendor_provider: LLMProvider, buyer_provider: LLMProvider) -> str:
    if vendor_provider.provider == buyer_provider.provider:
        return vendor_provider.provider
    return f"vendor:{vendor_provider.provider}; buyer:{buyer_provider.provider}"


def m02_model_label(vendor_provider: LLMProvider, buyer_provider: LLMProvider) -> str:
    if vendor_provider.model == buyer_provider.model:
        return vendor_provider.model
    return f"vendor:{vendor_provider.model}; buyer:{buyer_provider.model}"


def m02_model_versions(records: list[M02RunRecord]) -> list[str]:
    values = {record.vendor_model_version for record in records if record.vendor_model_version}
    values.update(record.buyer_model_version for record in records if record.buyer_model_version)
    return sorted(values)
