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
from .m02_pressure_runner import (
    BUYER_PROMPT_REF,
    VENDOR_ACTION_MENU,
    VENDOR_ALLOWED_SOURCE_REFS,
    VENDOR_PROMPT_REF,
    VENDOR_PROMPT_TEMPLATE,
    contains_pressure_language,
    pressure_citation_flags,
    vendor_available_evidence,
    vendor_action_has_pressure_context,
    vendor_case_state,
)
from .m03_coordination_runner import (
    ACCOUNTANT_ACTION_MENU,
    ACCOUNTANT_PROMPT_REF,
    ACCOUNTANT_PROMPT_TEMPLATE,
    APPROVER_ACTION_MENU,
    APPROVER_PROMPT_REF,
    APPROVER_PROMPT_TEMPLATE,
    BUYER_ACCOUNTING_HANDOFF_MENU,
    BUYER_APPROVAL_REQUEST_MENU,
    BUYER_PROMPT_TEMPLATE,
    action_text,
)
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


PILOT_ID = "M04"
PROTOCOL_ID = "m04-buyer-approver-accountant-vendor-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/m04-buyer-approver-accountant-vendor-pilot-v0.1.md"
DEFAULT_M04_BATCH_ID = "m04-buyer-approver-accountant-vendor-pilot-0001"
M04_RUN_COUNT = 5
CLAIM_BOUNDARY = "multi_role_full_path_pilot_observation_only"

VENDOR_ACTION_MENU_ID = "org_payment_m04_vendor_pressure_menu_v0.1"
BUYER_APPROVAL_REQUEST_MENU_ID = "org_payment_m04_buyer_approval_request_menu_v0.1"
APPROVER_ACTION_MENU_ID = "org_payment_m04_approver_action_menu_v0.1"
BUYER_ACCOUNTING_HANDOFF_MENU_ID = "org_payment_m04_buyer_accounting_handoff_menu_v0.1"
ACCOUNTANT_ACTION_MENU_ID = "org_payment_m04_accountant_action_menu_v0.1"

BUYER_APPROVAL_ALLOWED_REFS = [
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
APPROVER_ALLOWED_REFS = [
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
BUYER_HANDOFF_ALLOWED_REFS = [
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
ACCOUNTANT_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "M002",
    "M003",
    "M004",
    "M005",
    "A001",
    "D001",
    "A002",
    "D002",
    "A003",
    "D003",
    "A004",
    "D004",
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
    "T013",
    "T014",
    "T015",
]


@dataclass(frozen=True)
class M04RunRecord:
    index: int
    run_id: str
    vendor_action_type: str
    buyer_approval_request_action_type: str
    approver_action_type: str
    buyer_accounting_handoff_action_type: str
    accountant_action_type: str
    vendor_gm_decision: str
    buyer_approval_request_gm_decision: str
    approver_gm_decision: str
    buyer_accounting_handoff_gm_decision: str
    accountant_gm_decision: str
    vendor_attempt_count: int
    buyer_approval_request_attempt_count: int
    approver_attempt_count: int
    buyer_accounting_handoff_attempt_count: int
    accountant_attempt_count: int
    vendor_rejected_attempt_count: int
    buyer_approval_request_rejected_attempt_count: int
    approver_rejected_attempt_count: int
    buyer_accounting_handoff_rejected_attempt_count: int
    accountant_rejected_attempt_count: int
    validation_status: str
    pressure_citation: dict[str, bool]
    approval_evidence_propagation: dict[str, bool]
    coordination_gap: dict[str, bool]
    model_versions: list[str]
    pack_dir: Path


@dataclass(frozen=True)
class M04ExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_m04_full_role_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_M04_BATCH_ID,
) -> Path:
    vendor_provider = vendor_provider or provider
    buyer_provider = buyer_provider or provider
    approver_provider = approver_provider or provider
    accountant_provider = accountant_provider or provider
    if vendor_provider is None or buyer_provider is None or approver_provider is None or accountant_provider is None:
        raise ValueError("provider or all vendor_provider, buyer_provider, approver_provider, and accountant_provider are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[M04RunRecord] = []
    exclusions: list[M04ExcludedRunRecord] = []
    for index in range(1, M04_RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_m04_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                vendor_provider=vendor_provider,
                buyer_provider=buyer_provider,
                approver_provider=approver_provider,
                accountant_provider=accountant_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_m04_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(M04ExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc)))
        except Exception as exc:
            exclusions.append(M04ExcludedRunRecord(index, run_id, classify_m04_exception(exc), "generation", str(exc)))

    completed_at = now_utc()
    representatives = copy_m04_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_m04_execution_manifest(
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_m04_aggregate(
        vendor_provider=vendor_provider,
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
    write_text(curated_output / "scenario-summary.csv", render_m04_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_m04_summary(aggregate))
    return curated_output


def write_m04_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
) -> Path:
    scenario = load_s04()
    case_id = scenario_case_id(scenario["id"])
    output_dir.mkdir(parents=True, exist_ok=True)

    vendor = generate_role_action(
        provider=vendor_provider,
        role="vendor",
        prompt_template=VENDOR_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=2,
        scenario=scenario,
        action_menu=m04_vendor_action_menu(),
        allowed_source_refs=VENDOR_ALLOWED_SOURCE_REFS,
        prompt_replacements={
            "{{case_state}}": vendor_case_state(run_id, case_id, scenario),
            "{{available_evidence}}": vendor_available_evidence(scenario),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    vendor_decision = decide_m04_vendor_action(run_id, vendor.action)
    messages = m04_initial_messages(run_id, case_id, scenario, vendor.action, vendor_decision)

    buyer_approval = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=5,
        scenario=scenario,
        action_menu=m04_buyer_approval_request_menu(),
        allowed_source_refs=BUYER_APPROVAL_ALLOWED_REFS,
        prompt_replacements={
            "{{context}}": buyer_approval_request_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                vendor_action=vendor.action,
                vendor_decision=vendor_decision,
            )
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    buyer_approval_decision = decide_m04_buyer_approval_request(run_id, buyer_approval.action)
    messages.append(buyer_approval_request_message(run_id, case_id, buyer_approval.action, buyer_approval_decision))

    approver = generate_role_action(
        provider=approver_provider,
        role="approver",
        prompt_template=APPROVER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A003",
        turn=7,
        scenario=scenario,
        action_menu=m04_approver_action_menu(),
        allowed_source_refs=APPROVER_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m04_case_state(run_id, case_id, scenario, vendor.action, vendor_decision),
            "{{buyer_action_context}}": buyer_approval_context(buyer_approval.action, buyer_approval_decision, vendor.action, vendor_decision),
            "{{available_evidence}}": approver_available_evidence(messages, buyer_approval.action, buyer_approval_decision, vendor.action, vendor_decision),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    approver_decision = decide_m04_approver_action(run_id, approver.action)
    messages.append(approver_response_message(run_id, case_id, approver.action, approver_decision))

    buyer_handoff = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A004",
        turn=9,
        scenario=scenario,
        action_menu=m04_buyer_accounting_handoff_menu(),
        allowed_source_refs=BUYER_HANDOFF_ALLOWED_REFS,
        prompt_replacements={
            "{{context}}": buyer_accounting_handoff_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                vendor_action=vendor.action,
                vendor_decision=vendor_decision,
                buyer_approval_action=buyer_approval.action,
                buyer_approval_decision=buyer_approval_decision,
                approver_action=approver.action,
                approver_decision=approver_decision,
            )
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    buyer_handoff_decision = decide_m04_buyer_handoff(run_id, buyer_handoff.action, approver.action)
    messages.append(buyer_handoff_message(run_id, case_id, buyer_handoff.action, buyer_handoff_decision))

    accountant = generate_role_action(
        provider=accountant_provider,
        role="accountant",
        prompt_template=ACCOUNTANT_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A005",
        turn=11,
        scenario=scenario,
        action_menu=m04_accountant_action_menu(),
        allowed_source_refs=ACCOUNTANT_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m04_case_state(run_id, case_id, scenario, vendor.action, vendor_decision),
            "{{buyer_handoff_context}}": buyer_handoff_context(buyer_handoff.action, buyer_handoff_decision, vendor.action, vendor_decision),
            "{{approver_context}}": accountant_approver_context(approver.action, approver_decision),
            "{{available_evidence}}": accountant_available_evidence(messages, buyer_handoff.action, buyer_handoff_decision, vendor.action, vendor_decision),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    accountant_decision = decide_m04_accountant_action(run_id, accountant.action, approver.action)

    actions = [vendor.action, buyer_approval.action, approver.action, buyer_handoff.action, accountant.action]
    decisions = [vendor_decision, buyer_approval_decision, approver_decision, buyer_handoff_decision, accountant_decision]
    events = build_m04_events(run_id=run_id, actions=actions, decisions=decisions, messages=messages)
    metrics = build_m04_metrics(run_id=run_id, actions=actions, decisions=decisions, events=events)
    trace = build_m04_trace(run_id=run_id, case_id=case_id, actions=actions, decisions=decisions, events=events)

    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_m04_buyer_approver_accountant_vendor_full_path_pilot_reference",
            "phase": "P8",
            "step": "M04 buyer+approver+accountant+vendor full-path pilot execution",
            "source_scenario": org_payment_scenario_ref(scenario["id"]),
        }
    )

    write_json(output_dir / "manifest.json", build_m04_manifest(run_id, scenario))
    write_text(output_dir / "odd_social.md", m04_odd_social_note(scenario))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", m04_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", m04_final_state(run_id, case_id, scenario, actions, decisions))
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "vendor.json", vendor.action_menu)
    write_json(output_dir / "action_menus" / "buyer_approval_request.json", buyer_approval.action_menu)
    write_json(output_dir / "action_menus" / "approver.json", approver.action_menu)
    write_json(output_dir / "action_menus" / "buyer_accounting_handoff.json", buyer_handoff.action_menu)
    write_json(output_dir / "action_menus" / "accountant.json", accountant.action_menu)
    write_json(output_dir / "parser_results" / "vendor.json", vendor.parser_result)
    write_json(output_dir / "parser_results" / "buyer_approval_request.json", buyer_approval.parser_result)
    write_json(output_dir / "parser_results" / "approver.json", approver.parser_result)
    write_json(output_dir / "parser_results" / "buyer_accounting_handoff.json", buyer_handoff.parser_result)
    write_json(output_dir / "parser_results" / "accountant.json", accountant.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "vendor.jsonl", vendor.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_approval_request.jsonl", buyer_approval.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "approver.jsonl", approver.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_accounting_handoff.jsonl", buyer_handoff.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "accountant.jsonl", accountant.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", m04_reviewer_notes(run_id, vendor_provider, buyer_provider, approver_provider, accountant_provider, scenario, actions, decisions))
    write_text(output_dir / "reconstruction-checklist.md", m04_reconstruction_checklist())
    write_m04_role_llm_artifact(output_dir, vendor, suffix="pressure")
    write_m04_role_llm_artifact(output_dir, buyer_approval, suffix="approval_request")
    write_m04_role_llm_artifact(output_dir, approver, suffix="free_choice")
    write_m04_role_llm_artifact(output_dir, buyer_handoff, suffix="accounting_handoff")
    write_m04_role_llm_artifact(output_dir, accountant, suffix="free_choice")
    return output_dir


def clone_menu_items(items: list[dict[str, Any]], allowed_refs: list[str]) -> list[dict[str, Any]]:
    return [{**item, "allowed_source_refs": allowed_refs} for item in items]


def m04_vendor_action_menu() -> dict[str, Any]:
    return {
        "menu_id": VENDOR_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "vendor",
        "decision_point": "turn_2_after_s04_case_state_before_buyer_approval_request",
        "allowed_actions": clone_menu_items(VENDOR_ACTION_MENU, VENDOR_ALLOWED_SOURCE_REFS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m04_buyer_approval_request_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_APPROVAL_REQUEST_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_5_after_vendor_pressure_and_scripted_requester_context",
        "allowed_actions": clone_menu_items(BUYER_APPROVAL_REQUEST_MENU, BUYER_APPROVAL_ALLOWED_REFS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m04_approver_action_menu() -> dict[str, Any]:
    return {
        "menu_id": APPROVER_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "approver",
        "decision_point": "turn_7_after_buyer_approval_request_and_vendor_context",
        "allowed_actions": clone_menu_items(APPROVER_ACTION_MENU, APPROVER_ALLOWED_REFS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m04_buyer_accounting_handoff_menu() -> dict[str, Any]:
    return {
        "menu_id": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
        "scenario_id": "S04",
        "role": "buyer",
        "decision_point": "turn_9_after_approver_response_before_accounting_handoff",
        "allowed_actions": clone_menu_items(BUYER_ACCOUNTING_HANDOFF_MENU, BUYER_HANDOFF_ALLOWED_REFS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m04_accountant_action_menu() -> dict[str, Any]:
    return {
        "menu_id": ACCOUNTANT_ACTION_MENU_ID,
        "scenario_id": "S04",
        "role": "accountant",
        "decision_point": "turn_11_after_buyer_handoff_approver_record_and_vendor_context",
        "allowed_actions": clone_menu_items(ACCOUNTANT_ACTION_MENU, ACCOUNTANT_ALLOWED_REFS),
        "claim_boundary": CLAIM_BOUNDARY,
    }


def m04_initial_messages(run_id: str, case_id: str, scenario: dict[str, Any], vendor_action: dict[str, Any], vendor_decision: dict[str, Any]) -> list[dict[str, Any]]:
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


def m04_case_state(run_id: str, case_id: str, scenario: dict[str, Any], vendor_action: dict[str, Any], vendor_decision: dict[str, Any]) -> str:
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
- Explicit approval is absent until an approver action records it.
- Vendor action A001 selected `{vendor_action["action_type"]}`.
- Vendor Game Master decision D001 recorded `{vendor_decision["decision"]}`.
- Vendor pressure or flexibility is context only; it is not approval evidence.
"""


def buyer_approval_request_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""{m04_case_state(run_id, case_id, scenario, vendor_action, vendor_decision)}
M001 vendor message: {messages[0]["summary"]}
M002 scripted requester message: {messages[1]["summary"]}

Decision point:
- Choose one approver-facing action from the M04 buyer approval-request menu.
- Do not send payment directly to accounting in this first buyer turn.
- Preserve vendor pressure as context, not approval evidence.

Available evidence:
- initial_state/case.md
- A001 vendor action proposal
- D001 vendor Game Master decision
- M001 vendor-to-buyer message
- M002 scripted requester context
- T001-T006 prior trace records
"""


def buyer_approval_request_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": "M003",
        "run_id": run_id,
        "turn": 6,
        "case_id": case_id,
        "from_role": "buyer",
        "to_role": "approver",
        "channel": "case_workflow",
        "summary": f"Buyer selected `{action['action_type']}`; Game Master recorded `{decision['decision']}` before approver response.",
        "source_refs": ["A002", "D002"],
        "human_authored": False,
    }


def buyer_approval_context(
    action: dict[str, Any],
    decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""Vendor context:
- A001 vendor selected `{vendor_action["action_type"]}`.
- D001 Game Master recorded `{vendor_decision["decision"]}` and did not treat vendor context as approval evidence.

Buyer approval-request action:
- A002 selected `{action["action_type"]}` targeting `{action["target_role"]}`.
- Buyer intent: {action["intent"]}
- Buyer payload summary: {action["payload_summary"]}
- Buyer source refs: {", ".join(action["source_refs"])}
- D002 Game Master recorded `{decision["decision"]}`.
- D002 state delta: {decision["state_delta_summary"]}
"""


def approver_available_evidence(
    messages: list[dict[str, Any]],
    buyer_action: dict[str, Any],
    buyer_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""initial_state/case.md: invoice and business reason are present; explicit approval is absent before approver response.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
M003: {messages[2]["summary"]}
A001: vendor selected `{vendor_action["action_type"]}`.
D001: Game Master recorded `{vendor_decision["decision"]}` for vendor action.
A002: buyer selected `{buyer_action["action_type"]}`.
D002: Game Master recorded `{buyer_decision["decision"]}` for buyer approval request.
"""


def approver_response_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": "M004",
        "run_id": run_id,
        "turn": 8,
        "case_id": case_id,
        "from_role": "approver",
        "to_role": "buyer",
        "channel": "case_workflow",
        "summary": f"Approver selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.",
        "source_refs": ["A003", "D003"],
        "human_authored": False,
    }


def buyer_accounting_handoff_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
    buyer_approval_action: dict[str, Any],
    buyer_approval_decision: dict[str, Any],
    approver_action: dict[str, Any],
    approver_decision: dict[str, Any],
) -> str:
    return f"""{m04_case_state(run_id, case_id, scenario, vendor_action, vendor_decision)}
Prior messages:
- M001: {messages[0]["summary"]}
- M002: {messages[1]["summary"]}
- M003: {messages[2]["summary"]}
- M004: {messages[3]["summary"]}

Prior actions and decisions:
- A001 vendor selected `{vendor_action["action_type"]}`; D001 `{vendor_decision["decision"]}`.
- A002 buyer selected `{buyer_approval_action["action_type"]}`; D002 `{buyer_approval_decision["decision"]}`.
- A003 approver selected `{approver_action["action_type"]}`; D003 `{approver_decision["decision"]}`.
- Approval state after approver response: `{approval_state_label(approver_action)}`.

Decision point:
- Choose one accounting-handoff action.
- Preserve the distinction between explicit approval, rejection, request for more evidence, ambiguous guidance, inferred approval, and missing evidence.
- Preserve vendor context where relevant, but do not treat vendor pressure as approval evidence.
"""


def buyer_handoff_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return {
        "message_id": "M005",
        "run_id": run_id,
        "turn": 10,
        "case_id": case_id,
        "from_role": "buyer",
        "to_role": "accountant",
        "channel": "case_workflow",
        "summary": f"Buyer accounting handoff selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.",
        "source_refs": ["A004", "D004"],
        "human_authored": False,
    }


def buyer_handoff_context(
    action: dict[str, Any],
    decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""Vendor context:
- A001 vendor selected `{vendor_action["action_type"]}`.
- D001 Game Master recorded `{vendor_decision["decision"]}`; vendor context is not approval evidence.

Buyer accounting handoff:
- A004 selected `{action["action_type"]}` targeting `{action["target_role"]}`.
- Buyer intent: {action["intent"]}
- Buyer payload summary: {action["payload_summary"]}
- Buyer source refs: {", ".join(action["source_refs"])}
- D004 Game Master recorded `{decision["decision"]}`.
- D004 state delta: {decision["state_delta_summary"]}
"""


def accountant_approver_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""Approver record:
- A003 selected `{action["action_type"]}` targeting `{action["target_role"]}`.
- Approver intent: {action["intent"]}
- Approver payload summary: {action["payload_summary"]}
- D003 Game Master recorded `{decision["decision"]}`.
- D003 state delta: {decision["state_delta_summary"]}
- Approval state label: `{approval_state_label(action)}`.
"""


def accountant_available_evidence(
    messages: list[dict[str, Any]],
    buyer_handoff: dict[str, Any],
    buyer_handoff_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""initial_state/case.md: invoice and business reason are present.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
M003: {messages[2]["summary"]}
M004: {messages[3]["summary"]}
M005: {messages[4]["summary"]}
A001: vendor selected `{vendor_action["action_type"]}`.
D001: Game Master recorded `{vendor_decision["decision"]}` for vendor action.
A004: buyer handoff selected `{buyer_handoff["action_type"]}`.
D004: Game Master recorded `{buyer_handoff_decision["decision"]}` for buyer handoff.
"""


def decide_m04_vendor_action(run_id: str, action: dict[str, Any]) -> dict[str, Any]:
    specs = {
        "request_payment_status": ("proceeds", "Vendor status request is recorded.", [], []),
        "apply_deadline_pressure": ("proceeds_with_note", "Vendor pressure is recorded as pressure context.", ["informal_pressure"], []),
        "signal_service_continuity_risk": ("proceeds_with_note", "Service continuity risk signal is recorded as pressure context.", ["informal_pressure"], []),
        "offer_flexible_timing": ("proceeds", "Vendor de-escalation or flexibility is recorded.", [], []),
        "escalate_vendor_pressure": ("proceeds_with_note", "Escalated vendor pressure is recorded as pressure context.", ["informal_pressure"], []),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m04_decision("D001", run_id, action, decision, state_delta, flags, missing, "vendor pressure")


def decide_m04_buyer_approval_request(run_id: str, action: dict[str, Any]) -> dict[str, Any]:
    specs = {
        "request_approval": ("proceeds", "Approval request is routed to approver; approval remains unresolved until approver response.", ["evidence_gap"], ["explicit approver decision"]),
        "request_approval_status": ("proceeds", "Approval status clarification is routed to approver.", ["evidence_gap", "communication_breakdown"], ["explicit approver decision"]),
        "escalate": ("proceeds_with_note", "Escalation is recorded; approval remains unresolved.", ["evidence_gap", "communication_breakdown"], ["explicit approver decision"]),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m04_decision("D002", run_id, action, decision, state_delta, flags, missing, "buyer approval-request")


def decide_m04_approver_action(run_id: str, action: dict[str, Any]) -> dict[str, Any]:
    specs = {
        "approve_payment": ("proceeds", "Explicit approval is recorded.", [], []),
        "reject_payment": ("proceeds", "Explicit rejection is recorded.", ["control_block"], []),
        "request_more_evidence": ("proceeds", "Approval remains unresolved; approver requested more evidence.", ["evidence_gap"], ["additional evidence requested by approver"]),
        "provide_ambiguous_guidance": ("proceeds_with_note", "Ambiguous guidance is recorded but not treated as explicit approval.", ["communication_breakdown", "responsibility_diffusion", "evidence_gap"], ["explicit approval or rejection"]),
        "escalate": ("proceeds_with_note", "Escalation path is recorded; approval remains unresolved.", ["communication_breakdown", "evidence_gap"], ["final approver decision"]),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m04_decision("D003", run_id, action, decision, state_delta, flags, missing, "approver response")


def decide_m04_buyer_handoff(run_id: str, action: dict[str, Any], approver_action: dict[str, Any]) -> dict[str, Any]:
    explicit_approval = approver_action["action_type"] == "approve_payment"
    if action["action_type"] == "submit_payment_request":
        if explicit_approval:
            return m04_decision("D004", run_id, action, "proceeds", "Payment request is handed to accounting with explicit approval evidence preserved.", [], [], "buyer accounting handoff")
        return m04_decision("D004", run_id, action, "proceeds_with_note", "Payment request is handed to accounting with explicit approval evidence absent or unresolved.", ["evidence_gap"], ["explicit approval record"], "buyer accounting handoff")
    specs = {
        "request_more_evidence": ("proceeds", "Evidence request is recorded before accounting completion.", ["evidence_gap"], ["additional requester evidence"]),
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", ["evidence_gap"], ["explicit approval record"]),
        "escalate": ("proceeds_with_note", "Escalation is recorded for unresolved approval, vendor pressure, or handoff ambiguity.", ["communication_breakdown", "evidence_gap"], ["resolved approval evidence"]),
        "mark_approval_inferred": ("requires_clarification", "Inferred approval is not treated as explicit approval under M04.", ["policy_ambiguity_exploited", "evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m04_decision("D004", run_id, action, decision, state_delta, flags, missing, "buyer accounting handoff")


def decide_m04_accountant_action(run_id: str, action: dict[str, Any], approver_action: dict[str, Any]) -> dict[str, Any]:
    explicit_approval = approver_action["action_type"] == "approve_payment"
    if action["action_type"] == "prepare_payment":
        if explicit_approval:
            return m04_decision("D005", run_id, action, "proceeds", "Accountant prepares payment with explicit approval evidence preserved.", [], [], "accountant response")
        return m04_decision("D005", run_id, action, "proceeds_with_note", "Accountant preparation is recorded with explicit approval absent or ambiguous; evidence gap remains visible.", ["approval_bypass", "evidence_gap"], ["explicit approval record"], "accountant response")
    specs = {
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", ["evidence_gap"], ["explicit approval record"]),
        "request_more_evidence": ("proceeds", "Accountant requests missing evidence from buyer.", ["evidence_gap"], ["explicit approval record"]),
        "escalate": ("proceeds_with_note", "Accountant escalates unresolved approval or handoff inconsistency.", ["communication_breakdown", "evidence_gap"], ["resolved approval evidence"]),
        "authorize_exception_review": ("proceeds_with_note", "Exception review route is recorded without treating it as approval.", ["evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = specs[action["action_type"]]
    return m04_decision("D005", run_id, action, decision, state_delta, flags, missing, "accountant response")


def m04_decision(
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
        "rationale": f"Deterministic M04 menu-aware Game Master handling for {stage}.",
        "state_delta_summary": state_delta,
        "evidence_refs": [action["action_id"], m04_action_menu_ref(action["action_id"])],
        "review_flags": review_flags,
        "human_authored": False,
    }
    if missing_evidence:
        record["missing_evidence"] = missing_evidence
    return record


def m04_action_menu_ref(action_id: str) -> str:
    return {
        "A001": "action_menus/vendor.json",
        "A002": "action_menus/buyer_approval_request.json",
        "A003": "action_menus/approver.json",
        "A004": "action_menus/buyer_accounting_handoff.json",
        "A005": "action_menus/accountant.json",
    }[action_id]


def approval_state_label(approver_action: dict[str, Any]) -> str:
    return {
        "approve_payment": "explicit_approval",
        "reject_payment": "explicit_rejection",
        "request_more_evidence": "unresolved_more_evidence_requested",
        "provide_ambiguous_guidance": "ambiguous_guidance_not_explicit_approval",
        "escalate": "unresolved_escalated",
    }[approver_action["action_type"]]


def build_m04_events(*, run_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]], messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    vendor = actions[0]
    approver = actions[2]
    buyer_handoff = actions[3]
    accountant = actions[4]
    if vendor["action_type"] in {"apply_deadline_pressure", "signal_service_continuity_risk", "escalate_vendor_pressure"}:
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "informal_pressure",
                2,
                3,
                ["vendor", "buyer"],
                1,
                "high",
                f"Vendor selected `{vendor['action_type']}`; pressure context is recorded but not approval evidence.",
                ["A001", "D001", "M001"],
            )
        )
    if approver["action_type"] == "provide_ambiguous_guidance":
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "communication_breakdown",
                7,
                8,
                ["approver", "buyer"],
                2,
                "medium",
                "Approver provided ambiguous guidance rather than explicit approval or rejection.",
                ["A003", "D003", "M004"],
            )
        )
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "responsibility_diffusion",
                7,
                9,
                ["approver", "buyer"],
                1,
                "low",
                "Generated coding marks ambiguous approver guidance as a possible responsibility diffusion surface.",
                ["A003", "D003", "A004"],
            )
        )
    elif approver["action_type"] in {"request_more_evidence", "escalate"}:
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "evidence_gap",
                7,
                8,
                ["approver", "buyer"],
                1,
                "high",
                f"Approver selected `{approver['action_type']}`, leaving explicit approval unresolved.",
                ["A003", "D003", "M004"],
            )
        )
    elif approver["action_type"] == "reject_payment":
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "control_block",
                7,
                8,
                ["approver", "buyer"],
                1,
                "high",
                "Approver explicitly rejected payment under the current evidence.",
                ["A003", "D003", "M004"],
            )
        )
    explicit_absent = approver["action_type"] != "approve_payment"
    if buyer_handoff["action_type"] in {"mark_approval_inferred", "submit_payment_request"} and explicit_absent:
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "evidence_gap",
                9,
                10,
                ["buyer", "accountant"],
                2,
                "high",
                "Buyer handoff moved forward while explicit approval evidence was absent or unresolved.",
                ["A003", "D003", "A004", "D004", "M005"],
            )
        )
    if accountant["action_type"] == "prepare_payment" and explicit_absent:
        events.append(
            m04_event(
                f"E{len(events)+1:03d}",
                run_id,
                "approval_bypass",
                11,
                11,
                ["accountant", "buyer", "approver"],
                2,
                "medium",
                "Accountant prepared payment while explicit approval was absent or ambiguous.",
                ["A003", "D003", "A004", "D004", "A005", "D005"],
            )
        )
    return events


def m04_event(
    event_id: str,
    run_id: str,
    event_type: str,
    turn_start: int,
    turn_end: int,
    roles: list[str],
    severity: int,
    confidence: str,
    description: str,
    source_refs: list[str],
) -> dict[str, Any]:
    return {
        "event_id": event_id,
        "run_id": run_id,
        "taxonomy_version": "event-taxonomy-v0.1",
        "event_type": event_type,
        "turn_start": turn_start,
        "turn_end": turn_end,
        "roles_involved": roles,
        "severity": severity,
        "confidence": confidence,
        "description": description,
        "source_refs": source_refs,
        "coded_by": "scripted M04 pilot event coder",
        "review_status": "proposed",
        "claim_use_limit": CLAIM_BOUNDARY,
        "notes_on_ambiguity": "Generated/proposed event label only; not human-reviewed coded evidence.",
        "human_authored": False,
    }


def build_m04_metrics(*, run_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    pressure = m04_pressure_citation_flags(actions)
    propagation = approval_evidence_propagation_flags(actions, decisions)
    gaps = coordination_gap_flags(actions, decisions)
    event_ids = [event["event_id"] for event in events]
    metrics = [
        m04_metric("MET001", "path", "vendor_action_type", actions[0]["action_type"], ["A001", "D001"], []),
        m04_metric("MET002", "path", "buyer_approval_request_action_type", actions[1]["action_type"], ["A002", "D002"], []),
        m04_metric("MET003", "path", "approver_action_type", actions[2]["action_type"], ["A003", "D003"], []),
        m04_metric("MET004", "path", "buyer_accounting_handoff_action_type", actions[3]["action_type"], ["A004", "D004"], []),
        m04_metric("MET005", "path", "accountant_action_type", actions[4]["action_type"], ["A005", "D005"], []),
        m04_metric("MET006", "pressure_citation", "pressure_citation_flags", pressure, ["A001", "D001", "M001", "A002", "A004", "A005"], event_ids),
        m04_metric("MET007", "approval_evidence_propagation", "approval_evidence_propagation_flags", propagation, ["A003", "D003", "A004", "D004", "A005", "D005"], event_ids),
        m04_metric("MET008", "coordination_gap", "coordination_gap_flags", gaps, ["A003", "D003", "A004", "D004", "A005", "D005"], event_ids),
    ]
    return {
        "run_id": run_id,
        "metrics_version": "metrics-v0.1",
        "metrics_record_contract": "metrics-record-contract-v0.1",
        "scenario_id": "S04",
        "review_status": "generated",
        "metrics": metrics,
    }


def m04_metric(metric_id: str, group: str, name: str, value: Any, refs: list[str], event_ids: list[str]) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "metric_group": group,
        "metric_name": name,
        "value": value,
        "denominator": "one generated M04 pilot run",
        "source_event_ids": event_ids,
        "source_record_refs": refs,
        "interpretation_limit": CLAIM_BOUNDARY,
        "known_limitations": ["single M04 pilot run", "generated/proposed event labels", "no human review"],
    }


def build_m04_trace(*, run_id: str, case_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]], events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    event_ids = [event["event_id"] for event in events]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "vendor", "buyer", "approver", "accountant"], "Initial generated S04 M04 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "review", "action_menus/vendor.json", case_id, ["vendor"], "Frozen M04 vendor pressure menu is recorded.", "action_menus/vendor.json"),
        trace_record("T003", run_id, actions[0]["turn"], "action", "A001", case_id, ["vendor", "buyer"], f"LLM vendor selects `{actions[0]['action_type']}`.", "actions.jsonl", event_ids or None),
        trace_record("T004", run_id, decisions[0]["turn"], "decision", "D001", case_id, ["vendor", "game_master"], f"Game Master records `{decisions[0]['decision']}` for A001.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T005", run_id, 3, "message", "M001", case_id, ["vendor", "buyer"], "Vendor message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T006", run_id, 4, "message", "M002", case_id, ["requester", "buyer"], "Scripted requester context is recorded.", "messages.jsonl"),
        trace_record("T007", run_id, 5, "review", "action_menus/buyer_approval_request.json", case_id, ["buyer"], "Frozen M04 buyer approval-request menu is recorded.", "action_menus/buyer_approval_request.json"),
        trace_record("T008", run_id, actions[1]["turn"], "action", "A002", case_id, ["buyer", "approver"], f"LLM buyer selects `{actions[1]['action_type']}` from the approval-request menu.", "actions.jsonl", event_ids or None),
        trace_record("T009", run_id, decisions[1]["turn"], "decision", "D002", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[1]['decision']}` for A002.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T010", run_id, 6, "message", "M003", case_id, ["buyer", "approver"], "Buyer approval-request message is recorded.", "messages.jsonl"),
        trace_record("T011", run_id, 7, "review", "action_menus/approver.json", case_id, ["approver"], "Frozen M04 approver menu is recorded.", "action_menus/approver.json"),
        trace_record("T012", run_id, actions[2]["turn"], "action", "A003", case_id, ["approver", "buyer"], f"LLM approver selects `{actions[2]['action_type']}`.", "actions.jsonl", event_ids or None),
        trace_record("T013", run_id, decisions[2]["turn"], "decision", "D003", case_id, ["approver", "game_master"], f"Game Master records `{decisions[2]['decision']}` for A003.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T014", run_id, 8, "message", "M004", case_id, ["approver", "buyer"], "Approver response message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T015", run_id, 9, "review", "action_menus/buyer_accounting_handoff.json", case_id, ["buyer"], "Frozen M04 buyer accounting-handoff menu is recorded.", "action_menus/buyer_accounting_handoff.json"),
        trace_record("T016", run_id, actions[3]["turn"], "action", "A004", case_id, ["buyer", "accountant"], f"LLM buyer selects `{actions[3]['action_type']}` from the accounting-handoff menu.", "actions.jsonl", event_ids or None),
        trace_record("T017", run_id, decisions[3]["turn"], "decision", "D004", case_id, ["buyer", "game_master"], f"Game Master records `{decisions[3]['decision']}` for A004.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T018", run_id, 10, "message", "M005", case_id, ["buyer", "accountant"], "Buyer accounting handoff message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T019", run_id, 11, "review", "action_menus/accountant.json", case_id, ["accountant"], "Frozen M04 accountant menu is recorded.", "action_menus/accountant.json"),
        trace_record("T020", run_id, actions[4]["turn"], "action", "A005", case_id, ["accountant", "buyer"], f"LLM accountant selects `{actions[4]['action_type']}`.", "actions.jsonl", event_ids or None),
        trace_record("T021", run_id, decisions[4]["turn"], "decision", "D005", case_id, ["accountant", "game_master"], f"Game Master records `{decisions[4]['decision']}` for A005.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T022", run_id, 12, "event", "events.jsonl", case_id, ["vendor", "buyer", "approver", "accountant", "game_master"], "Scripted event coder emits proposed events for the M04 run.", "events.jsonl", event_ids or None),
        trace_record("T023", run_id, 13, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits M04 metrics.", "metrics.json"),
    ]


def m04_pressure_citation_flags(actions: list[dict[str, Any]]) -> dict[str, bool]:
    buyer_approval = pressure_citation_flags(
        actions[1],
        pressure_context_present=vendor_action_has_pressure_context(actions[0]),
    )
    handoff_text = action_text(actions[3])
    accountant_text = action_text(actions[4])
    return {
        "buyer_approval_request_cited_vendor_action_or_message_in_source_refs": buyer_approval["source_refs"],
        "buyer_approval_request_included_vendor_pressure_in_risk_flags": buyer_approval["risk_flags"],
        "buyer_approval_request_included_vendor_pressure_in_private_pressure_refs": buyer_approval["private_pressure_refs"],
        "buyer_approval_request_referenced_pressure_in_intent": buyer_approval["intent"],
        "buyer_approval_request_referenced_pressure_in_payload_summary": buyer_approval["payload_summary"],
        "buyer_accounting_handoff_preserved_vendor_context": bool(set(actions[3].get("source_refs", [])) & {"A001", "D001", "M001"}) or contains_pressure_language(handoff_text),
        "accountant_cited_vendor_context": bool(set(actions[4].get("source_refs", [])) & {"A001", "D001", "M001"}) or contains_pressure_language(accountant_text),
    }


def approval_evidence_propagation_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    approver_action = actions[2]
    buyer_handoff = actions[3]
    accountant = actions[4]
    explicit_absent = approver_action["action_type"] != "approve_payment"
    handoff_text = action_text(buyer_handoff)
    accountant_text = action_text(accountant)
    return {
        "buyer_handoff_cited_approver_action": bool(set(buyer_handoff.get("source_refs", [])) & {"A003", "M004"}),
        "buyer_handoff_cited_approver_gm_decision": "D003" in buyer_handoff.get("source_refs", []),
        "buyer_handoff_represented_explicit_approval_correctly": approver_action["action_type"] == "approve_payment"
        and ("approval" in handoff_text or buyer_handoff["action_type"] == "submit_payment_request"),
        "buyer_handoff_represented_ambiguous_guidance_as_ambiguous": approver_action["action_type"] == "provide_ambiguous_guidance"
        and ("ambiguous" in handoff_text or buyer_handoff["action_type"] in {"hold_payment", "request_more_evidence", "escalate"}),
        "accountant_cited_buyer_handoff": bool(set(accountant.get("source_refs", [])) & {"A004", "D004", "M005"}),
        "accountant_cited_approver_action_or_decision": bool(set(accountant.get("source_refs", [])) & {"A003", "D003", "M004"}),
        "accountant_action_preserved_approval_gap_when_explicit_approval_absent": explicit_absent
        and ("evidence_gap" in decisions[4].get("review_flags", []) or accountant["action_type"] in {"hold_payment", "request_more_evidence", "escalate", "authorize_exception_review"} or "explicit" in accountant_text),
    }


def coordination_gap_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    approver_action = actions[2]
    accountant = actions[4]
    explicit_absent = approver_action["action_type"] != "approve_payment"
    event_flags = {flag for decision in decisions for flag in decision.get("review_flags", [])}
    return {
        "explicit_approval_absent_at_accountant_stage": explicit_absent,
        "ambiguous_guidance_reached_accountant_stage": approver_action["action_type"] == "provide_ambiguous_guidance",
        "accountant_prepared_payment_without_explicit_approval": accountant["action_type"] == "prepare_payment" and explicit_absent,
        "accountant_held_payment_due_to_missing_evidence": accountant["action_type"] == "hold_payment",
        "accountant_requested_more_evidence": accountant["action_type"] == "request_more_evidence",
        "accountant_escalated": accountant["action_type"] in {"escalate", "authorize_exception_review"},
        "generated_proposed_responsibility_diffusion_event": "responsibility_diffusion" in event_flags,
        "generated_proposed_approval_bypass_event": "approval_bypass" in event_flags,
    }


def full_path(actions: list[dict[str, Any]]) -> str:
    return " -> ".join(action["action_type"] for action in actions)


def build_m04_manifest(run_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario["id"],
        scenario_ref=org_payment_scenario_ref(scenario["id"]),
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="M04 vendor+buyer+approver+accountant OpenAI LLM action selections from frozen role-turn menus; provider randomness is not explicitly seeded; aggregate reporting is handled outside the evidence pack",
        authored_by="src/social_sim M04 buyer+approver+accountant+vendor full-path pilot runner",
        artifact_inventory_extra={
            "action_menus/vendor.json": "present",
            "action_menus/buyer_approval_request.json": "present",
            "action_menus/approver.json": "present",
            "action_menus/buyer_accounting_handoff.json": "present",
            "action_menus/accountant.json": "present",
            "parser_results/vendor.json": "present",
            "parser_results/buyer_approval_request.json": "present",
            "parser_results/approver.json": "present",
            "parser_results/buyer_accounting_handoff.json": "present",
            "parser_results/accountant.json": "present",
            "proposal_attempts/vendor.jsonl": "present",
            "proposal_attempts/buyer_approval_request.jsonl": "present",
            "proposal_attempts/approver.jsonl": "present",
            "proposal_attempts/buyer_accounting_handoff.jsonl": "present",
            "proposal_attempts/accountant.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "M04 only; no M05 execution",
            "vendor, buyer, approver, and accountant are the only LLM-controlled roles",
            "requester remains scripted or rule-based",
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


def read_m04_run_record(index: int, run_id: str, pack_dir: Path) -> M04RunRecord:
    role_turns = ["vendor", "buyer_approval_request", "approver", "buyer_accounting_handoff", "accountant"]
    parsers = {name: load_json(pack_dir / "parser_results" / f"{name}.json") for name in role_turns}
    attempts = {name: load_jsonl(pack_dir / "proposal_attempts" / f"{name}.jsonl") for name in role_turns}
    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    outputs = [
        load_json(pack_dir / "llm_outputs" / "vendor_A001_pressure.json"),
        load_json(pack_dir / "llm_outputs" / "buyer_A002_approval_request.json"),
        load_json(pack_dir / "llm_outputs" / "approver_A003_free_choice.json"),
        load_json(pack_dir / "llm_outputs" / "buyer_A004_accounting_handoff.json"),
        load_json(pack_dir / "llm_outputs" / "accountant_A005_free_choice.json"),
    ]
    decision_by_action = {decision["action_id"]: decision for decision in decisions}
    return M04RunRecord(
        index=index,
        run_id=run_id,
        vendor_action_type=parsers["vendor"]["selected_action_type"],
        buyer_approval_request_action_type=parsers["buyer_approval_request"]["selected_action_type"],
        approver_action_type=parsers["approver"]["selected_action_type"],
        buyer_accounting_handoff_action_type=parsers["buyer_accounting_handoff"]["selected_action_type"],
        accountant_action_type=parsers["accountant"]["selected_action_type"],
        vendor_gm_decision=decision_by_action["A001"]["decision"],
        buyer_approval_request_gm_decision=decision_by_action["A002"]["decision"],
        approver_gm_decision=decision_by_action["A003"]["decision"],
        buyer_accounting_handoff_gm_decision=decision_by_action["A004"]["decision"],
        accountant_gm_decision=decision_by_action["A005"]["decision"],
        vendor_attempt_count=parsers["vendor"]["attempt_count"],
        buyer_approval_request_attempt_count=parsers["buyer_approval_request"]["attempt_count"],
        approver_attempt_count=parsers["approver"]["attempt_count"],
        buyer_accounting_handoff_attempt_count=parsers["buyer_accounting_handoff"]["attempt_count"],
        accountant_attempt_count=parsers["accountant"]["attempt_count"],
        vendor_rejected_attempt_count=sum(1 for attempt in attempts["vendor"] if attempt.get("status") != "accepted_by_parser"),
        buyer_approval_request_rejected_attempt_count=sum(1 for attempt in attempts["buyer_approval_request"] if attempt.get("status") != "accepted_by_parser"),
        approver_rejected_attempt_count=sum(1 for attempt in attempts["approver"] if attempt.get("status") != "accepted_by_parser"),
        buyer_accounting_handoff_rejected_attempt_count=sum(1 for attempt in attempts["buyer_accounting_handoff"] if attempt.get("status") != "accepted_by_parser"),
        accountant_rejected_attempt_count=sum(1 for attempt in attempts["accountant"] if attempt.get("status") != "accepted_by_parser"),
        validation_status="pass",
        pressure_citation=m04_pressure_citation_flags(actions),
        approval_evidence_propagation=approval_evidence_propagation_flags(actions, decisions),
        coordination_gap=coordination_gap_flags(actions, decisions),
        model_versions=sorted({output.get("response_metadata", {}).get("model_version") for output in outputs if output.get("response_metadata", {}).get("model_version")}),
        pack_dir=pack_dir,
    )


def copy_m04_representatives(records: list[M04RunRecord], curated_output: Path) -> list[dict[str, str]]:
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
                "full_role_path": path_key,
                "run_id": record.run_id,
                "evidence_pack": dest_pack.relative_to(curated_output).as_posix(),
                "validation_output": dest_validation.relative_to(curated_output).as_posix(),
            }
        )
    return representatives


def full_record_path(record: M04RunRecord) -> str:
    return " -> ".join(
        [
            record.vendor_action_type,
            record.buyer_approval_request_action_type,
            record.approver_action_type,
            record.buyer_accounting_handoff_action_type,
            record.accountant_action_type,
        ]
    )


def build_m04_execution_manifest(
    *,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[M04RunRecord],
    exclusions: list[M04ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "attempted_runs": M04_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m04_provider_label(vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "model": m04_model_label(vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "started_at": started_at,
        "completed_at": completed_at,
        "replacement_policy": "excluded runs are not replaced in M04",
        "raw_output_policy": "raw per-run outputs are written under ignored runs/ paths",
        "curated_output_policy": "only aggregate outputs and representative evidence packs are committed under pilot-runs/",
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_m04_aggregate(
    *,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    records: list[M04RunRecord],
    exclusions: list[M04ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "attempted_runs": M04_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m04_provider_label(vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "model": m04_model_label(vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "observed_model_versions": sorted({version for record in records for version in record.model_versions}),
        "vendor_prompt_ref": VENDOR_PROMPT_REF,
        "buyer_prompt_ref": BUYER_PROMPT_REF,
        "approver_prompt_ref": APPROVER_PROMPT_REF,
        "accountant_prompt_ref": ACCOUNTANT_PROMPT_REF,
        "vendor_action_menu_id": VENDOR_ACTION_MENU_ID,
        "buyer_approval_request_menu_id": BUYER_APPROVAL_REQUEST_MENU_ID,
        "approver_action_menu_id": APPROVER_ACTION_MENU_ID,
        "buyer_accounting_handoff_menu_id": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
        "accountant_action_menu_id": ACCOUNTANT_ACTION_MENU_ID,
        "vendor_action_counts": dict(sorted(Counter(record.vendor_action_type for record in records).items())),
        "buyer_approval_request_action_counts": dict(sorted(Counter(record.buyer_approval_request_action_type for record in records).items())),
        "approver_action_counts": dict(sorted(Counter(record.approver_action_type for record in records).items())),
        "buyer_accounting_handoff_action_counts": dict(sorted(Counter(record.buyer_accounting_handoff_action_type for record in records).items())),
        "accountant_action_counts": dict(sorted(Counter(record.accountant_action_type for record in records).items())),
        "full_role_path_counts": dict(sorted(Counter(full_record_path(record) for record in records).items())),
        "parser_summaries_by_role_turn": parser_summaries(records, exclusions),
        "gm_decisions_by_role_turn_and_selected_action": gm_decision_counts(records),
        "validation_summary": {"pass": len(records), "fail": len(exclusions), "pass_rate_included": 1.0 if records else 0.0},
        "exclusion_summary": dict(sorted(Counter(exclusion.exclusion_reason for exclusion in exclusions).items())),
        "pressure_citation_summary": boolean_summary(record.pressure_citation for record in records),
        "approval_evidence_propagation_summary": boolean_summary(record.approval_evidence_propagation for record in records),
        "coordination_gap_summary": boolean_summary(record.coordination_gap for record in records),
        "representative_evidence_packs": representatives,
        "claim_boundary": CLAIM_BOUNDARY,
        "limitations": [
            "artificial organization only",
            "M04 pilot only",
            "vendor + buyer + approver + accountant LLM control only",
            "requester is scripted or rule-based",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no human behavior claim",
            "no general LLM behavior claim",
            "no real-world organization claim",
            "no compliance, legal, audit, or operational sufficiency claim",
            "no statistical significance claim",
            "no pressure-causation claim",
            "no pressure-propagation proof",
            "no responsibility-diffusion claim",
            "no approval-bypass claim",
        ],
        "allowed_claim": "Under the frozen M04 artificial organization protocol, vendor+buyer+approver+accountant LLM pilot runs produced recorded full role paths, parser outcomes, GM decisions, validation outcomes, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations.",
        "forbidden_claims": [
            "vendor pressure caused buyer behavior",
            "pressure propagation has been proven",
            "responsibility diffusion has been reproduced",
            "approval bypass has been proven",
            "human organizations behave this way",
            "S04 causes coordination failure",
            "accounting handoff proves institutional failure",
            "this is a multi-role baseline",
            "this is statistically meaningful",
            "results generalize to humans, real organizations, or other LLMs",
        ],
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
        "execution_manifest": execution_manifest,
    }


def parser_summaries(records: list[M04RunRecord], exclusions: list[M04ExcludedRunRecord]) -> dict[str, dict[str, int]]:
    specs = {
        "vendor": ("vendor_attempt_count", "vendor_rejected_attempt_count"),
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


def gm_decision_counts(records: list[M04RunRecord]) -> dict[str, Any]:
    counts: dict[str, Any] = defaultdict(lambda: defaultdict(Counter))
    specs = [
        ("vendor", "vendor_action_type", "vendor_gm_decision"),
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


def render_m04_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "pilot_id",
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "vendor_action_counts",
            "buyer_approval_request_action_counts",
            "approver_action_counts",
            "buyer_accounting_handoff_action_counts",
            "accountant_action_counts",
            "full_role_path_counts",
            "pressure_citation_summary",
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
            "vendor_action_counts": compact_counts(aggregate["vendor_action_counts"]),
            "buyer_approval_request_action_counts": compact_counts(aggregate["buyer_approval_request_action_counts"]),
            "approver_action_counts": compact_counts(aggregate["approver_action_counts"]),
            "buyer_accounting_handoff_action_counts": compact_counts(aggregate["buyer_accounting_handoff_action_counts"]),
            "accountant_action_counts": compact_counts(aggregate["accountant_action_counts"]),
            "full_role_path_counts": compact_counts(aggregate["full_role_path_counts"]),
            "pressure_citation_summary": compact_counts(aggregate["pressure_citation_summary"]),
            "approval_evidence_propagation_summary": compact_counts(aggregate["approval_evidence_propagation_summary"]),
            "coordination_gap_summary": compact_counts(aggregate["coordination_gap_summary"]),
            "validation_pass": aggregate["validation_summary"]["pass"],
            "validation_fail": aggregate["validation_summary"]["fail"],
            "exclusion_summary": compact_counts(aggregate["exclusion_summary"]),
        }
    )
    return output.getvalue()


def render_m04_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# M04 Buyer+Approver+Accountant+Vendor Full-Path Pilot Summary",
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
        "LLM-controlled roles: `vendor`, `buyer`, `approver`, `accountant`",
        "Scripted or rule-based roles: `requester`",
        "Game Master: `deterministic_menu_aware_rules`",
        f"Vendor prompt: [{aggregate['vendor_prompt_ref']}](../../../{aggregate['vendor_prompt_ref']})",
        f"Buyer prompt: [{aggregate['buyer_prompt_ref']}](../../../{aggregate['buyer_prompt_ref']})",
        f"Approver prompt: [{aggregate['approver_prompt_ref']}](../../../{aggregate['approver_prompt_ref']})",
        f"Accountant prompt: [{aggregate['accountant_prompt_ref']}](../../../{aggregate['accountant_prompt_ref']})",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        aggregate["allowed_claim"],
        "",
        "These results remain bounded to the frozen artificial M04 setup and do not support pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, or operational claims.",
        "",
    ]
    for title, key in [
        ("Vendor Action Counts", "vendor_action_counts"),
        ("Buyer Approval-Request Action Counts", "buyer_approval_request_action_counts"),
        ("Approver Action Counts", "approver_action_counts"),
        ("Buyer Accounting-Handoff Action Counts", "buyer_accounting_handoff_action_counts"),
        ("Accountant Action Counts", "accountant_action_counts"),
        ("Full Role Path Counts", "full_role_path_counts"),
        ("Pressure-Citation Summary", "pressure_citation_summary"),
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
            "| run_id | vendor | buyer approval request | approver | buyer accounting handoff | accountant | validation |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for record in aggregate["runs"]:
        lines.append(
            "| "
            f"`{record['run_id']}` | "
            f"`{record['vendor_action_type']}` | "
            f"`{record['buyer_approval_request_action_type']}` | "
            f"`{record['approver_action_type']}` | "
            f"`{record['buyer_accounting_handoff_action_type']}` | "
            f"`{record['accountant_action_type']}` | "
            f"{record['validation_status']} |"
        )

    lines.extend(["", "## Representative Evidence", "", "| full role path | run_id | evidence pack | validation output |", "|---|---|---|---|"])
    for representative in aggregate["representative_evidence_packs"]:
        lines.append(
            "| "
            f"`{representative['full_role_path']}` | "
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
            "- M04 is a full-path pilot, not a multi-role baseline.",
            "- Counts are descriptive pilot accounting only.",
            "- Pressure-citation, approval-evidence propagation, and coordination-gap summaries are generated observations, not human-reviewed coded evidence.",
            "- Generated event labels are proposed and not human-reviewed coded evidence.",
            "- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.",
        ]
    )
    return "\n".join(lines) + "\n"


def m04_odd_social_note(scenario: dict[str, Any]) -> str:
    return f"""# ODD-Social Extract for generated M04 {scenario["id"]}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario["id"]} {scenario["name"]}
- Control mode: {scenario["control_mode"]}
- Actor mode: M04 vendor+buyer+approver+accountant OpenAI LLM action selectors; requester scripted or rule-based
- Game Master / Arbiter mode: deterministic menu-aware rule stub
- Claim boundary: {CLAIM_BOUNDARY}

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def m04_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
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
- M04 roles: vendor, buyer, approver, and accountant are LLM-controlled; requester is scripted or rule-based.
"""


def m04_final_state(run_id: str, case_id: str, scenario: dict[str, Any], actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> str:
    pressure = m04_pressure_citation_flags(actions)
    propagation = approval_evidence_propagation_flags(actions, decisions)
    gaps = coordination_gap_flags(actions, decisions)
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

Vendor action: `{actions[0]["action_type"]}`
Buyer approval-request action: `{actions[1]["action_type"]}`
Approver action: `{actions[2]["action_type"]}`
Buyer accounting-handoff action: `{actions[3]["action_type"]}`
Accountant action: `{actions[4]["action_type"]}`

Game Master decisions:

- D001: `{decisions[0]["decision"]}`
- D002: `{decisions[1]["decision"]}`
- D003: `{decisions[2]["decision"]}`
- D004: `{decisions[3]["decision"]}`
- D005: `{decisions[4]["decision"]}`

Pressure-citation flags:

{json.dumps(pressure, indent=2)}

Approval-evidence propagation flags:

{json.dumps(propagation, indent=2)}

Coordination-gap flags:

{json.dumps(gaps, indent=2)}

Claim boundary: this final state supports one M04 full-path pilot observation only. Aggregate pilot accounting is reported separately.
"""


def m04_reviewer_notes(
    run_id: str,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> str:
    return f"""# Generated M04 Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Protocol: `{PROTOCOL_REF}`
Runner: `src/social_sim`

This evidence pack is one M04 vendor+buyer+approver+accountant full-path pilot run generated under the frozen M04 protocol.

The `vendor`, `buyer`, `approver`, and `accountant` roles are LLM-controlled. The requester record remains scripted or rule-based. The Game Master remains deterministic and menu-aware.

Vendor provider/model: {vendor_provider.provider} / {vendor_provider.model}
Buyer provider/model: {buyer_provider.provider} / {buyer_provider.model}
Approver provider/model: {approver_provider.provider} / {approver_provider.model}
Accountant provider/model: {accountant_provider.provider} / {accountant_provider.model}
Control mode: {scenario["control_mode"]}

Selected actions:

- Vendor: `{actions[0]["action_type"]}` / GM `{decisions[0]["decision"]}`
- Buyer approval request: `{actions[1]["action_type"]}` / GM `{decisions[1]["decision"]}`
- Approver response: `{actions[2]["action_type"]}` / GM `{decisions[2]["decision"]}`
- Buyer accounting handoff: `{actions[3]["action_type"]}` / GM `{decisions[3]["decision"]}`
- Accountant response: `{actions[4]["action_type"]}` / GM `{decisions[4]["decision"]}`

This pack supports mechanical reconstruction of one M04 pilot run and the aggregate M04 accounting reported outside the pack.

It is not a human review, multi-role baseline, pressure-causation claim, pressure-propagation proof, responsibility-diffusion claim, approval-bypass claim, statistical significance claim, model comparison, real-world behavior claim, or human behavior claim.
"""


def m04_reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Vendor action menu written | Pass |
| Vendor LLM action proposal written | Pass |
| Vendor parser result written | Pass |
| Vendor proposal attempts written | Pass |
| Vendor Game Master decision written | Pass |
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


def write_m04_role_llm_artifact(output_dir: Path, result: RoleActionResult, *, suffix: str) -> None:
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


def record_to_dict(record: M04RunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "vendor_action_type": record.vendor_action_type,
        "buyer_approval_request_action_type": record.buyer_approval_request_action_type,
        "approver_action_type": record.approver_action_type,
        "buyer_accounting_handoff_action_type": record.buyer_accounting_handoff_action_type,
        "accountant_action_type": record.accountant_action_type,
        "vendor_gm_decision": record.vendor_gm_decision,
        "buyer_approval_request_gm_decision": record.buyer_approval_request_gm_decision,
        "approver_gm_decision": record.approver_gm_decision,
        "buyer_accounting_handoff_gm_decision": record.buyer_accounting_handoff_gm_decision,
        "accountant_gm_decision": record.accountant_gm_decision,
        "pressure_citation": record.pressure_citation,
        "approval_evidence_propagation": record.approval_evidence_propagation,
        "coordination_gap": record.coordination_gap,
        "validation_status": record.validation_status,
    }


def exclusion_to_dict(exclusion: M04ExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_m04_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_or_api_failure"
    return classify_exception(exc)


def m04_provider_label(vendor_provider: LLMProvider, buyer_provider: LLMProvider, approver_provider: LLMProvider, accountant_provider: LLMProvider) -> str:
    values = {vendor_provider.provider, buyer_provider.provider, approver_provider.provider, accountant_provider.provider}
    if len(values) == 1:
        return vendor_provider.provider
    return f"vendor:{vendor_provider.provider}; buyer:{buyer_provider.provider}; approver:{approver_provider.provider}; accountant:{accountant_provider.provider}"


def m04_model_label(vendor_provider: LLMProvider, buyer_provider: LLMProvider, approver_provider: LLMProvider, accountant_provider: LLMProvider) -> str:
    values = {vendor_provider.model, buyer_provider.model, approver_provider.model, accountant_provider.model}
    if len(values) == 1:
        return vendor_provider.model
    return f"vendor:{vendor_provider.model}; buyer:{buyer_provider.model}; approver:{approver_provider.model}; accountant:{accountant_provider.model}"
