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
    VENDOR_ACTION_MENU,
    VENDOR_PROMPT_REF,
    VENDOR_PROMPT_TEMPLATE,
    contains_pressure_language,
    vendor_action_has_pressure_context,
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
    BUYER_PROMPT_REF,
    BUYER_PROMPT_TEMPLATE,
    action_text,
)
from .multirole_runner import (
    RoleActionResult,
    classify_exception,
    compact_counts,
    failed_validation_markdown,
    format_counts,
    generate_role_action,
    load_json,
    load_jsonl,
    now_utc,
)
from .repeated_runner import require_new_or_empty
from .runner import build_manifest, response_metadata, trace_record
from .scenario_loader import dump_yaml, load_org_payment_scenario, org_payment_scenario_ref


PILOT_ID = "M05"
PROTOCOL_ID = "m05-full-org-payment-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/m05-full-org-payment-pilot-v0.1.md"
DEFAULT_M05_BATCH_ID = "m05-full-org-payment-pilot-0001"
M05_RUN_COUNT = 5
CLAIM_BOUNDARY = "multi_role_full_org_payment_pilot_observation_only"

REQUESTER_PROMPT_REF = "prompts/org-payment/requester-free-choice-action-v0.1.md"
REQUESTER_ACTION_MENU_ID = "org_payment_m05_requester_case_initiation_menu_v0.1"
VENDOR_ACTION_MENU_ID = "org_payment_m05_vendor_pressure_menu_v0.1"
BUYER_APPROVAL_REQUEST_MENU_ID = "org_payment_m05_buyer_approval_request_menu_v0.1"
APPROVER_ACTION_MENU_ID = "org_payment_m05_approver_action_menu_v0.1"
BUYER_ACCOUNTING_HANDOFF_MENU_ID = "org_payment_m05_buyer_accounting_handoff_menu_v0.1"
ACCOUNTANT_ACTION_MENU_ID = "org_payment_m05_accountant_action_menu_v0.1"

ROOT = Path(__file__).resolve().parents[2]
REQUESTER_PROMPT_TEMPLATE = ROOT / REQUESTER_PROMPT_REF

ROLE_TURNS = [
    "requester",
    "vendor",
    "buyer_approval_request",
    "approver",
    "buyer_accounting_handoff",
    "accountant",
]

REQUESTER_ALLOWED_REFS = ["initial_state/case.md", "T001"]
VENDOR_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "A001",
    "D001",
    "T001",
    "T002",
    "T003",
    "T004",
]
BUYER_APPROVAL_ALLOWED_REFS = [
    "initial_state/case.md",
    "M001",
    "M002",
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
    "A005",
    "D005",
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
    "T016",
]

REQUESTER_ACTION_MENU = [
    {
        "action_type": "send_message",
        "target_role": "buyer",
        "menu_label": "Send invoice and business reason to buyer",
        "selection_boundary": "Provide invoice and business reason through the normal buyer-facing path without claiming approval.",
        "allowed_source_refs": REQUESTER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_approval",
        "target_role": "approver",
        "menu_label": "Ask approver directly for approval",
        "selection_boundary": "Ask the approver for explicit approval before buyer/accounting processing.",
        "allowed_source_refs": REQUESTER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "escalate",
        "target_role": "approver",
        "menu_label": "Escalate urgency to approver",
        "selection_boundary": "Escalate time pressure or role ambiguity to approver without claiming payment approval exists.",
        "allowed_source_refs": REQUESTER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]


@dataclass(frozen=True)
class M05RunRecord:
    index: int
    run_id: str
    selected_actions: dict[str, str]
    gm_decisions: dict[str, str]
    attempt_counts: dict[str, int]
    rejected_attempt_counts: dict[str, int]
    validation_status: str
    requester_framing: dict[str, bool]
    pressure_citation: dict[str, bool]
    approval_evidence_propagation: dict[str, bool]
    coordination_gap: dict[str, bool]
    model_versions: list[str]
    pack_dir: Path


@dataclass(frozen=True)
class M05ExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_m05_full_org_payment_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    requester_provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_M05_BATCH_ID,
) -> Path:
    requester_provider = requester_provider or provider
    vendor_provider = vendor_provider or provider
    buyer_provider = buyer_provider or provider
    approver_provider = approver_provider or provider
    accountant_provider = accountant_provider or provider
    if any(item is None for item in [requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider]):
        raise ValueError("provider or all requester/vendor/buyer/approver/accountant providers are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[M05RunRecord] = []
    exclusions: list[M05ExcludedRunRecord] = []
    for index in range(1, M05_RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_m05_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                requester_provider=requester_provider,
                vendor_provider=vendor_provider,
                buyer_provider=buyer_provider,
                approver_provider=approver_provider,
                accountant_provider=accountant_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_m05_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(M05ExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc)))
        except Exception as exc:
            exclusions.append(M05ExcludedRunRecord(index, run_id, classify_m05_exception(exc), "generation", str(exc)))

    completed_at = now_utc()
    representatives = copy_m05_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_m05_execution_manifest(
        requester_provider=requester_provider,
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
    aggregate = build_m05_aggregate(
        requester_provider=requester_provider,
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
    write_text(curated_output / "scenario-summary.csv", render_m05_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_m05_summary(aggregate))
    return curated_output


def write_m05_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    scenario_id: str = "S04",
    claim_boundary: str = CLAIM_BOUNDARY,
    protocol_ref: str = PROTOCOL_REF,
    scenario_status: str = "generated_m05_full_org_payment_multi_role_pilot_reference",
    scenario_step: str = "M05 requester+vendor+buyer+approver+accountant multi-role pilot execution",
    run_label: str = "M05 full org-payment pilot",
    runner_label: str = "M05 full org-payment multi-role pilot runner",
    scope_limit: str = "M05 only; no S01-S06 multi-role sweep",
) -> Path:
    scenario = load_org_payment_scenario(scenario_id)
    case_id = scenario_case_id(scenario["id"])
    output_dir.mkdir(parents=True, exist_ok=True)

    requester = generate_role_action(
        provider=requester_provider,
        role="requester",
        prompt_template=REQUESTER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=2,
        scenario=scenario,
        action_menu=m05_requester_action_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=REQUESTER_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m05_case_state(run_id, case_id, scenario),
            "{{available_evidence}}": requester_available_evidence(scenario),
        },
        claim_boundary=claim_boundary,
    )
    requester_decision = decide_m05_requester_action(run_id, requester.action, protocol_ref=protocol_ref)
    messages = [requester_message(run_id, case_id, requester.action, requester_decision)]

    vendor = generate_role_action(
        provider=vendor_provider,
        role="vendor",
        prompt_template=VENDOR_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=4,
        scenario=scenario,
        action_menu=m05_vendor_action_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=VENDOR_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m05_vendor_case_state(run_id, case_id, scenario, requester.action, requester_decision),
            "{{available_evidence}}": vendor_available_evidence_with_requester(scenario, messages, requester.action, requester_decision),
        },
        claim_boundary=claim_boundary,
    )
    vendor_decision = decide_m05_vendor_action(run_id, vendor.action, protocol_ref=protocol_ref)
    messages.append(vendor_message(run_id, case_id, vendor.action, vendor_decision))

    buyer_approval = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A003",
        turn=6,
        scenario=scenario,
        action_menu=m05_buyer_approval_request_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=BUYER_APPROVAL_ALLOWED_REFS,
        prompt_replacements={
            "{{context}}": buyer_approval_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                requester_action=requester.action,
                requester_decision=requester_decision,
                vendor_action=vendor.action,
                vendor_decision=vendor_decision,
            )
        },
        claim_boundary=claim_boundary,
    )
    buyer_approval_decision = decide_m05_buyer_approval_request(run_id, buyer_approval.action, protocol_ref=protocol_ref)
    messages.append(buyer_approval_message(run_id, case_id, buyer_approval.action, buyer_approval_decision))

    approver = generate_role_action(
        provider=approver_provider,
        role="approver",
        prompt_template=APPROVER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A004",
        turn=8,
        scenario=scenario,
        action_menu=m05_approver_action_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=APPROVER_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m05_case_state(run_id, case_id, scenario, requester.action, vendor.action),
            "{{buyer_action_context}}": approver_buyer_action_context(
                buyer_approval.action,
                buyer_approval_decision,
                requester.action,
                requester_decision,
                vendor.action,
                vendor_decision,
            ),
            "{{available_evidence}}": approver_available_evidence(messages, requester.action, requester_decision, vendor.action, vendor_decision),
        },
        claim_boundary=claim_boundary,
    )
    approver_decision = decide_m05_approver_action(run_id, approver.action, protocol_ref=protocol_ref)
    messages.append(approver_message(run_id, case_id, approver.action, approver_decision))

    buyer_handoff = generate_role_action(
        provider=buyer_provider,
        role="buyer",
        prompt_template=BUYER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A005",
        turn=10,
        scenario=scenario,
        action_menu=m05_buyer_accounting_handoff_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=BUYER_HANDOFF_ALLOWED_REFS,
        prompt_replacements={
            "{{context}}": buyer_handoff_context(
                run_id=run_id,
                case_id=case_id,
                scenario=scenario,
                messages=messages,
                requester_action=requester.action,
                requester_decision=requester_decision,
                vendor_action=vendor.action,
                vendor_decision=vendor_decision,
                buyer_approval_action=buyer_approval.action,
                buyer_approval_decision=buyer_approval_decision,
                approver_action=approver.action,
                approver_decision=approver_decision,
            )
        },
        claim_boundary=claim_boundary,
    )
    buyer_handoff_decision = decide_m05_buyer_handoff(run_id, buyer_handoff.action, approver.action, protocol_ref=protocol_ref)
    messages.append(buyer_handoff_message(run_id, case_id, buyer_handoff.action, buyer_handoff_decision))

    accountant = generate_role_action(
        provider=accountant_provider,
        role="accountant",
        prompt_template=ACCOUNTANT_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A006",
        turn=12,
        scenario=scenario,
        action_menu=m05_accountant_action_menu(scenario_id=scenario["id"], claim_boundary=claim_boundary),
        allowed_source_refs=ACCOUNTANT_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": m05_case_state(run_id, case_id, scenario, requester.action, vendor.action),
            "{{buyer_handoff_context}}": accountant_buyer_handoff_context(buyer_handoff.action, buyer_handoff_decision, requester.action, vendor.action, vendor_decision),
            "{{approver_context}}": accountant_approver_context(approver.action, approver_decision),
            "{{available_evidence}}": accountant_available_evidence(messages, buyer_handoff.action, buyer_handoff_decision, approver.action, approver_decision),
        },
        claim_boundary=claim_boundary,
    )
    accountant_decision = decide_m05_accountant_action(run_id, accountant.action, approver.action, protocol_ref=protocol_ref)
    messages.append(accountant_message(run_id, case_id, accountant.action, accountant_decision))

    actions = [requester.action, vendor.action, buyer_approval.action, approver.action, buyer_handoff.action, accountant.action]
    decisions = [requester_decision, vendor_decision, buyer_approval_decision, approver_decision, buyer_handoff_decision, accountant_decision]
    events = build_m05_events(run_id=run_id, scenario_id=scenario["id"], actions=actions, decisions=decisions, messages=messages, claim_boundary=claim_boundary, run_label=run_label)
    metrics = build_m05_metrics(run_id=run_id, scenario_id=scenario["id"], actions=actions, decisions=decisions, events=events, claim_boundary=claim_boundary, run_label=run_label)
    trace = build_m05_trace(run_id=run_id, case_id=case_id, scenario_id=scenario["id"], actions=actions, decisions=decisions, events=events, run_label=run_label)

    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": scenario_status,
            "phase": "P8",
            "step": scenario_step,
            "source_scenario": org_payment_scenario_ref(scenario["id"]),
        }
    )

    write_json(output_dir / "manifest.json", build_m05_manifest(run_id, scenario, claim_boundary=claim_boundary, run_label=run_label, runner_label=runner_label, scope_limit=scope_limit))
    write_text(output_dir / "odd_social.md", m05_odd_social_note(scenario, claim_boundary=claim_boundary, run_label=run_label))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", m05_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", m05_final_state(run_id, case_id, scenario, actions, decisions, claim_boundary=claim_boundary))
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "requester.json", requester.action_menu)
    write_json(output_dir / "action_menus" / "vendor.json", vendor.action_menu)
    write_json(output_dir / "action_menus" / "buyer_approval_request.json", buyer_approval.action_menu)
    write_json(output_dir / "action_menus" / "approver.json", approver.action_menu)
    write_json(output_dir / "action_menus" / "buyer_accounting_handoff.json", buyer_handoff.action_menu)
    write_json(output_dir / "action_menus" / "accountant.json", accountant.action_menu)
    write_json(output_dir / "parser_results" / "requester.json", requester.parser_result)
    write_json(output_dir / "parser_results" / "vendor.json", vendor.parser_result)
    write_json(output_dir / "parser_results" / "buyer_approval_request.json", buyer_approval.parser_result)
    write_json(output_dir / "parser_results" / "approver.json", approver.parser_result)
    write_json(output_dir / "parser_results" / "buyer_accounting_handoff.json", buyer_handoff.parser_result)
    write_json(output_dir / "parser_results" / "accountant.json", accountant.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "requester.jsonl", requester.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "vendor.jsonl", vendor.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_approval_request.jsonl", buyer_approval.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "approver.jsonl", approver.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "buyer_accounting_handoff.jsonl", buyer_handoff.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "accountant.jsonl", accountant.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", m05_reviewer_notes(run_id, requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider, scenario, actions, decisions, claim_boundary=claim_boundary, runner_label=runner_label))
    write_text(output_dir / "reconstruction-checklist.md", m05_reconstruction_checklist(claim_boundary=claim_boundary, runner_label=runner_label))
    write_m05_role_llm_artifact(output_dir, requester, suffix="case_initiation")
    write_m05_role_llm_artifact(output_dir, vendor, suffix="pressure")
    write_m05_role_llm_artifact(output_dir, buyer_approval, suffix="approval_request")
    write_m05_role_llm_artifact(output_dir, approver, suffix="free_choice")
    write_m05_role_llm_artifact(output_dir, buyer_handoff, suffix="accounting_handoff")
    write_m05_role_llm_artifact(output_dir, accountant, suffix="free_choice")
    return output_dir


def clone_menu_items(items: list[dict[str, Any]], allowed_refs: list[str]) -> list[dict[str, Any]]:
    return [{**item, "allowed_source_refs": allowed_refs} for item in items]


def m05_requester_action_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": REQUESTER_ACTION_MENU_ID,
        "scenario_id": scenario_id,
        "role": "requester",
        "decision_point": "turn_2_case_initiation_before_vendor_and_buyer_handling",
        "allowed_actions": REQUESTER_ACTION_MENU,
        "claim_boundary": claim_boundary,
    }


def m05_vendor_action_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": VENDOR_ACTION_MENU_ID,
        "scenario_id": scenario_id,
        "role": "vendor",
        "decision_point": "turn_4_after_requester_case_initiation",
        "allowed_actions": clone_menu_items(VENDOR_ACTION_MENU, VENDOR_ALLOWED_REFS),
        "claim_boundary": claim_boundary,
    }


def m05_buyer_approval_request_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": BUYER_APPROVAL_REQUEST_MENU_ID,
        "scenario_id": scenario_id,
        "role": "buyer",
        "decision_point": "turn_6_after_requester_and_vendor_context",
        "allowed_actions": clone_menu_items(BUYER_APPROVAL_REQUEST_MENU, BUYER_APPROVAL_ALLOWED_REFS),
        "claim_boundary": claim_boundary,
    }


def m05_approver_action_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": APPROVER_ACTION_MENU_ID,
        "scenario_id": scenario_id,
        "role": "approver",
        "decision_point": "turn_8_after_buyer_approval_request_requester_and_vendor_context",
        "allowed_actions": clone_menu_items(APPROVER_ACTION_MENU, APPROVER_ALLOWED_REFS),
        "claim_boundary": claim_boundary,
    }


def m05_buyer_accounting_handoff_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
        "scenario_id": scenario_id,
        "role": "buyer",
        "decision_point": "turn_10_after_approver_response_with_requester_and_vendor_context",
        "allowed_actions": clone_menu_items(BUYER_ACCOUNTING_HANDOFF_MENU, BUYER_HANDOFF_ALLOWED_REFS),
        "claim_boundary": claim_boundary,
    }


def m05_accountant_action_menu(scenario_id: str = "S04", claim_boundary: str = CLAIM_BOUNDARY) -> dict[str, Any]:
    return {
        "menu_id": ACCOUNTANT_ACTION_MENU_ID,
        "scenario_id": scenario_id,
        "role": "accountant",
        "decision_point": "turn_12_after_full_requester_vendor_buyer_approver_handoff_record",
        "allowed_actions": clone_menu_items(ACCOUNTANT_ACTION_MENU, ACCOUNTANT_ALLOWED_REFS),
        "claim_boundary": claim_boundary,
    }


def m05_case_state(run_id: str, case_id: str, scenario: dict[str, Any], requester_action: dict[str, Any] | None = None, vendor_action: dict[str, Any] | None = None) -> str:
    requester_line = f"Requester action: `{requester_action['action_type']}`; {requester_action['payload_summary']}" if requester_action else "Requester has not yet acted."
    vendor_line = f"Vendor action: `{vendor_action['action_type']}`; {vendor_action['payload_summary']}" if vendor_action else "Vendor has not yet acted."
    return f"""Run id: {run_id}
Case id: {case_id}
Scenario: {scenario['id']} - {scenario['name']}
Control mode: {scenario.get('control_mode', 'soft')}
Policy ambiguity: {scenario.get('policy_ambiguity', 'unknown')}
Deadline pressure: {scenario.get('deadline_pressure', 'unknown')}
Role overlap: {scenario.get('role_overlap', 'unknown')}

Initial state:
- Invoice and business reason are present.
- Explicit approval is absent.
- Requester urgency and vendor pressure are context only; neither is approval evidence.

Current role context:
- {requester_line}
- {vendor_line}
"""


def requester_available_evidence(scenario: dict[str, Any]) -> str:
    return f"""- `initial_state/case.md`: {scenario['id']} invoice and business reason are present; explicit approval is absent.
- Scenario file: `{org_payment_scenario_ref(scenario['id'])}`
- No approver, buyer, vendor, accountant, or Game Master decision has occurred yet.
"""


def vendor_available_evidence_with_requester(
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    requester_action: dict[str, Any],
    requester_decision: dict[str, Any],
) -> str:
    return f"""- `initial_state/case.md`: {scenario['id']} invoice and business reason are present; explicit approval is absent.
- M001 requester message: {messages[0]['summary']}
- A001 requester action: `{requester_action['action_type']}`.
- D001 Game Master decision: `{requester_decision['decision']}`; requester context is not approval evidence.
- Scenario file: `{org_payment_scenario_ref(scenario['id'])}`
"""


def m05_vendor_case_state(run_id: str, case_id: str, scenario: dict[str, Any], requester_action: dict[str, Any], requester_decision: dict[str, Any]) -> str:
    return f"""{m05_case_state(run_id, case_id, scenario, requester_action)}
Requester context:
- A001 selected `{requester_action['action_type']}`.
- D001 recorded `{requester_decision['decision']}`.
- Requester urgency or direct approval routing remains context only until an approver response exists.
"""


def buyer_approval_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    requester_action: dict[str, Any],
    requester_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""{m05_case_state(run_id, case_id, scenario, requester_action, vendor_action)}
Prior messages:
- M001 requester message: {messages[0]['summary']}
- M002 vendor message: {messages[1]['summary']}

Prior Game Master state:
- D001 requester decision `{requester_decision['decision']}`: requester context is not approval evidence.
- D002 vendor decision `{vendor_decision['decision']}`: vendor pressure or flexibility is not approval evidence.

Buyer decision point:
- Choose an approver-facing action.
- Preserve requester and vendor context where relevant.
- Do not route payment directly to accounting in this first buyer turn.
"""


def approver_buyer_action_context(
    buyer_action: dict[str, Any],
    buyer_decision: dict[str, Any],
    requester_action: dict[str, Any],
    requester_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""Requester context:
- A001 `{requester_action['action_type']}`: {requester_action['payload_summary']}
- D001 `{requester_decision['decision']}`: requester context is not approval evidence.

Vendor context:
- A002 `{vendor_action['action_type']}`: {vendor_action['payload_summary']}
- D002 `{vendor_decision['decision']}`: vendor context is not approval evidence.

Buyer approval request:
- A003 `{buyer_action['action_type']}`: {buyer_action['payload_summary']}
- D003 `{buyer_decision['decision']}`: {buyer_decision['state_delta_summary']}
"""


def approver_available_evidence(
    messages: list[dict[str, Any]],
    requester_action: dict[str, Any],
    requester_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""M001: {messages[0]['summary']}
M002: {messages[1]['summary']}
M003: {messages[2]['summary']}
A001 requester action: `{requester_action['action_type']}`
D001 requester decision: `{requester_decision['decision']}`
A002 vendor action: `{vendor_action['action_type']}`
D002 vendor decision: `{vendor_decision['decision']}`
Initial explicit approval status: absent.
"""


def buyer_handoff_context(
    *,
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    messages: list[dict[str, Any]],
    requester_action: dict[str, Any],
    requester_decision: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
    buyer_approval_action: dict[str, Any],
    buyer_approval_decision: dict[str, Any],
    approver_action: dict[str, Any],
    approver_decision: dict[str, Any],
) -> str:
    return f"""{m05_case_state(run_id, case_id, scenario, requester_action, vendor_action)}
Prior messages:
- M001: {messages[0]['summary']}
- M002: {messages[1]['summary']}
- M003: {messages[2]['summary']}
- M004: {messages[3]['summary']}

Approval state:
- A003 buyer approval request `{buyer_approval_action['action_type']}`; D003 `{buyer_approval_decision['decision']}`.
- A004 approver response `{approver_action['action_type']}`; D004 `{approver_decision['decision']}`.
- Current approval state label: `{approval_state_label(approver_action)}`.

Buyer handoff decision point:
- Preserve requester context, vendor context, and approval evidence state.
- If explicit approval is absent, do not represent pressure or ambiguous guidance as explicit approval.
"""


def accountant_buyer_handoff_context(
    buyer_handoff: dict[str, Any],
    buyer_handoff_decision: dict[str, Any],
    requester_action: dict[str, Any],
    vendor_action: dict[str, Any],
    vendor_decision: dict[str, Any],
) -> str:
    return f"""Requester context:
- A001 `{requester_action['action_type']}`; requester context is not approval evidence.

Vendor context:
- A002 `{vendor_action['action_type']}`; D002 `{vendor_decision['decision']}`.
- Vendor pressure or flexibility is not approval evidence.

Buyer accounting handoff:
- A005 `{buyer_handoff['action_type']}`: {buyer_handoff['payload_summary']}
- D005 `{buyer_handoff_decision['decision']}`: {buyer_handoff_decision['state_delta_summary']}
"""


def accountant_approver_context(approver_action: dict[str, Any], approver_decision: dict[str, Any]) -> str:
    return f"""Approver action:
- A004 `{approver_action['action_type']}`: {approver_action['payload_summary']}

Game Master decision:
- D004 `{approver_decision['decision']}`: {approver_decision['state_delta_summary']}

Approval state label: `{approval_state_label(approver_action)}`.
"""


def accountant_available_evidence(
    messages: list[dict[str, Any]],
    buyer_handoff: dict[str, Any],
    buyer_handoff_decision: dict[str, Any],
    approver_action: dict[str, Any],
    approver_decision: dict[str, Any],
) -> str:
    return f"""M001: {messages[0]['summary']}
M002: {messages[1]['summary']}
M003: {messages[2]['summary']}
M004: {messages[3]['summary']}
M005: {messages[4]['summary']}
A004 approver action: `{approver_action['action_type']}`.
D004 approver decision: `{approver_decision['decision']}`.
A005 buyer handoff: `{buyer_handoff['action_type']}`.
D005 buyer handoff decision: `{buyer_handoff_decision['decision']}`.
Accountant must preserve missing or ambiguous approval evidence instead of treating context as explicit approval.
"""


def requester_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M001", run_id, 3, "requester", action["target_role"], case_id, f"Requester selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.")


def vendor_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M002", run_id, 5, "vendor", "buyer", case_id, f"Vendor selected `{action['action_type']}`; Game Master recorded `{decision['decision']}` and did not treat vendor context as approval evidence.")


def buyer_approval_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M003", run_id, 7, "buyer", "approver", case_id, f"Buyer selected `{action['action_type']}` for approval routing; Game Master recorded `{decision['decision']}`.")


def approver_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M004", run_id, 9, "approver", "buyer", case_id, f"Approver selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.")


def buyer_handoff_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M005", run_id, 11, "buyer", action["target_role"], case_id, f"Buyer accounting handoff selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.")


def accountant_message(run_id: str, case_id: str, action: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    return message_record("M006", run_id, 13, "accountant", action["target_role"], case_id, f"Accountant selected `{action['action_type']}`; Game Master recorded `{decision['decision']}`.")


def message_record(message_id: str, run_id: str, turn: int, sender: str, recipient: str | None, case_id: str, summary: str) -> dict[str, Any]:
    return {
        "message_id": message_id,
        "run_id": run_id,
        "turn": turn,
        "sender": sender,
        "recipient": recipient,
        "case_id": case_id,
        "summary": summary,
        "artifact_ref": "messages.jsonl",
        "human_authored": False,
    }


def decide_m05_requester_action(run_id: str, action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    mapping = {
        "send_message": ("proceeds", "Requester case initiation is recorded as business context, not approval evidence.", [], []),
        "request_approval": ("proceeds_with_note", "Direct requester-to-approver approval request is recorded; approval remains unresolved until approver response.", ["evidence_gap"], ["explicit approver decision"]),
        "escalate": ("proceeds_with_note", "Requester urgency or escalation is recorded; it is not approval evidence.", ["informal_pressure"], ["explicit approver decision"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D001", run_id, action, decision, state_delta, flags, missing, "requester case initiation", protocol_ref=protocol_ref)


def decide_m05_vendor_action(run_id: str, action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    mapping = {
        "request_payment_status": ("proceeds", "Vendor status request is recorded.", [], []),
        "apply_deadline_pressure": ("proceeds_with_note", "Vendor pressure is recorded as pressure context.", ["informal_pressure"], []),
        "signal_service_continuity_risk": ("proceeds_with_note", "Service continuity risk signal is recorded as pressure context.", ["informal_pressure"], []),
        "offer_flexible_timing": ("proceeds", "Vendor de-escalation or flexibility is recorded.", [], []),
        "escalate_vendor_pressure": ("proceeds_with_note", "Escalated vendor pressure is recorded as pressure context.", ["informal_pressure"], []),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D002", run_id, action, decision, state_delta, flags, missing, "vendor pressure", protocol_ref=protocol_ref)


def decide_m05_buyer_approval_request(run_id: str, action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    mapping = {
        "request_approval": ("proceeds", "Approval request is routed to approver; approval remains unresolved until approver response.", ["evidence_gap"], ["explicit approver decision"]),
        "request_approval_status": ("proceeds", "Approval status clarification is routed to approver.", ["evidence_gap"], ["explicit approval status"]),
        "escalate": ("proceeds_with_note", "Escalation is recorded; approval remains unresolved.", ["communication_breakdown"], ["explicit approver decision"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D003", run_id, action, decision, state_delta, flags, missing, "buyer approval request", protocol_ref=protocol_ref)


def decide_m05_approver_action(run_id: str, action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    mapping = {
        "approve_payment": ("proceeds", "Explicit approval is recorded.", [], []),
        "reject_payment": ("proceeds", "Explicit rejection is recorded.", [], []),
        "request_more_evidence": ("proceeds", "Approval remains unresolved while more evidence is requested.", ["evidence_gap"], ["requested supporting evidence"]),
        "provide_ambiguous_guidance": ("proceeds_with_note", "Ambiguous guidance is recorded but not treated as explicit approval.", ["communication_breakdown", "policy_ambiguity_exploited"], ["explicit approval or rejection"]),
        "escalate": ("proceeds_with_note", "Escalation path is recorded; approval remains unresolved.", ["communication_breakdown"], ["explicit approval or rejection"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D004", run_id, action, decision, state_delta, flags, missing, "approver response", protocol_ref=protocol_ref)


def decide_m05_buyer_handoff(run_id: str, action: dict[str, Any], approver_action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    if action["action_type"] == "submit_payment_request":
        if approver_action["action_type"] == "approve_payment":
            return m05_decision("D005", run_id, action, "proceeds", "Payment request is handed to accounting with explicit approval evidence preserved.", [], [], "buyer accounting handoff", protocol_ref=protocol_ref)
        return m05_decision("D005", run_id, action, "proceeds_with_note", "Payment request is handed to accounting with explicit approval evidence absent or unresolved.", ["evidence_gap"], ["explicit approval record"], "buyer accounting handoff", protocol_ref=protocol_ref)
    mapping = {
        "request_more_evidence": ("proceeds", "Evidence request is recorded before accounting completion.", ["evidence_gap"], ["requested evidence"]),
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", [], []),
        "escalate": ("proceeds_with_note", "Escalation is recorded.", ["communication_breakdown"], ["resolved approval state"]),
        "mark_approval_inferred": ("requires_clarification", "Inferred approval is not treated as explicit approval under M05.", ["evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D005", run_id, action, decision, state_delta, flags, missing, "buyer accounting handoff", protocol_ref=protocol_ref)


def decide_m05_accountant_action(run_id: str, action: dict[str, Any], approver_action: dict[str, Any], protocol_ref: str = PROTOCOL_REF) -> dict[str, Any]:
    if action["action_type"] == "prepare_payment":
        if approver_action["action_type"] == "approve_payment":
            return m05_decision("D006", run_id, action, "proceeds", "Accountant prepares payment with explicit approval evidence preserved.", [], [], "accountant response", protocol_ref=protocol_ref)
        return m05_decision("D006", run_id, action, "proceeds_with_note", "Accountant preparation is recorded with explicit approval absent or ambiguous; evidence gap remains visible.", ["approval_bypass", "evidence_gap"], ["explicit approval record"], "accountant response", protocol_ref=protocol_ref)
    mapping = {
        "hold_payment": ("proceeds", "Payment remains held while approval evidence is unresolved.", [], []),
        "request_more_evidence": ("proceeds", "Accountant requests missing evidence from buyer.", ["evidence_gap"], ["requested approval evidence"]),
        "escalate": ("proceeds_with_note", "Accountant escalates unresolved approval or handoff inconsistency.", ["communication_breakdown"], ["resolved approval state"]),
        "authorize_exception_review": ("proceeds_with_note", "Exception review route is recorded without treating it as approval.", ["evidence_gap"], ["exception review outcome"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return m05_decision("D006", run_id, action, decision, state_delta, flags, missing, "accountant response", protocol_ref=protocol_ref)


def m05_decision(
    decision_id: str,
    run_id: str,
    action: dict[str, Any],
    decision: str,
    state_delta: str,
    flags: list[str],
    missing: list[str],
    role_turn: str,
    protocol_ref: str = PROTOCOL_REF,
) -> dict[str, Any]:
    return {
        "decision_id": decision_id,
        "run_id": run_id,
        "turn": action["turn"],
        "action_id": action["action_id"],
        "decision": decision,
        "control_mode": "soft",
        "rule_refs": [protocol_ref, "institutions/org-payment/control-modes.md"],
        "rationale": f"Deterministic menu-aware Game Master applied frozen M05 handling for {role_turn}.",
        "state_delta_summary": state_delta,
        "evidence_refs": [action["action_id"], m05_action_menu_ref(action["action_id"])],
        "review_flags": flags,
        "missing_evidence": missing,
        "human_authored": False,
    }


def m05_action_menu_ref(action_id: str) -> str:
    return {
        "A001": "action_menus/requester.json",
        "A002": "action_menus/vendor.json",
        "A003": "action_menus/buyer_approval_request.json",
        "A004": "action_menus/approver.json",
        "A005": "action_menus/buyer_accounting_handoff.json",
        "A006": "action_menus/accountant.json",
    }[action_id]


def approval_state_label(approver_action: dict[str, Any]) -> str:
    return {
        "approve_payment": "explicit_approval",
        "reject_payment": "explicit_rejection",
        "request_more_evidence": "approval_unresolved_more_evidence_requested",
        "provide_ambiguous_guidance": "ambiguous_guidance_not_explicit_approval",
        "escalate": "approval_unresolved_escalated",
    }.get(approver_action["action_type"], "approval_state_unknown")


def build_m05_events(
    *,
    run_id: str,
    scenario_id: str = "S04",
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    messages: list[dict[str, Any]],
    claim_boundary: str = CLAIM_BOUNDARY,
    run_label: str = "M05 full org-payment pilot",
) -> list[dict[str, Any]]:
    requester, vendor, buyer_approval, approver, buyer_handoff, accountant = actions
    events = [
        m05_event(
            "E001",
            run_id,
            "evidence_gap",
            1,
            2,
            ["requester", "buyer", "approver", "accountant"],
            1,
            "high",
            f"Initial {scenario_id} state lacks explicit approval evidence before requester, vendor, buyer, approver, or accountant actions.",
            ["initial_state/case.md", "A001", "D001"],
            claim_boundary=claim_boundary,
            run_label=run_label,
        )
    ]
    if vendor["action_type"] in {"apply_deadline_pressure", "signal_service_continuity_risk", "escalate_vendor_pressure"}:
        events.append(
            m05_event(
                f"E{len(events)+1:03d}",
                run_id,
                "informal_pressure",
                vendor["turn"],
                vendor["turn"],
                ["vendor", "buyer"],
                1,
                "medium",
                f"Vendor selected `{vendor['action_type']}`; pressure context is recorded but not approval evidence.",
                ["A002", "D002", "M002"],
                claim_boundary=claim_boundary,
                run_label=run_label,
            )
        )
    if requester["action_type"] == "escalate":
        events.append(
            m05_event(
                f"E{len(events)+1:03d}",
                run_id,
                "informal_pressure",
                requester["turn"],
                requester["turn"],
                ["requester", "approver"],
                1,
                "medium",
                "Requester escalation is recorded as urgency context, not approval evidence.",
                ["A001", "D001", "M001"],
                claim_boundary=claim_boundary,
                run_label=run_label,
            )
        )
    if approver["action_type"] == "provide_ambiguous_guidance":
        events.append(
            m05_event(
                f"E{len(events)+1:03d}",
                run_id,
                "policy_ambiguity_exploited",
                approver["turn"],
                buyer_handoff["turn"],
                ["approver", "buyer"],
                2,
                "medium",
                "Approver provided ambiguous approval-related guidance; explicit approval remains absent.",
                ["A004", "D004", "M004", "A005", "D005"],
                claim_boundary=claim_boundary,
                run_label=run_label,
            )
        )
    if decisions[4]["decision"] == "proceeds_with_note":
        events.append(
            m05_event(
                f"E{len(events)+1:03d}",
                run_id,
                "evidence_gap",
                buyer_handoff["turn"],
                buyer_handoff["turn"],
                ["buyer", "accountant"],
                2,
                "high",
                "Buyer accounting handoff proceeded with explicit approval evidence absent or unresolved.",
                ["A005", "D005", "M005"],
                claim_boundary=claim_boundary,
                run_label=run_label,
            )
        )
    if accountant["action_type"] == "prepare_payment" and approver["action_type"] != "approve_payment":
        events.append(
            m05_event(
                f"E{len(events)+1:03d}",
                run_id,
                "approval_bypass",
                accountant["turn"],
                accountant["turn"],
                ["accountant", "buyer", "approver"],
                2,
                "medium",
                "Accountant prepared payment without explicit approval evidence.",
                ["A004", "D004", "A005", "D005", "A006", "D006"],
                claim_boundary=claim_boundary,
                run_label=run_label,
            )
        )
    return events


def m05_event(
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
    claim_boundary: str = CLAIM_BOUNDARY,
    run_label: str = "M05 full org-payment pilot",
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
        "coded_by": f"scripted event coder for {run_label}",
        "review_status": "proposed",
        "claim_use_limit": claim_boundary,
        "human_authored": False,
    }


def build_m05_metrics(
    *,
    run_id: str,
    scenario_id: str = "S04",
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
    claim_boundary: str = CLAIM_BOUNDARY,
    run_label: str = "M05 full org-payment pilot",
) -> dict[str, Any]:
    event_ids = [event["event_id"] for event in events]
    metrics = [
        m05_metric("MET001", "path", "requester_action_type", actions[0]["action_type"], ["A001", "D001"], [], claim_boundary, run_label),
        m05_metric("MET002", "path", "vendor_action_type", actions[1]["action_type"], ["A002", "D002"], [], claim_boundary, run_label),
        m05_metric("MET003", "path", "buyer_approval_request_action_type", actions[2]["action_type"], ["A003", "D003"], [], claim_boundary, run_label),
        m05_metric("MET004", "path", "approver_action_type", actions[3]["action_type"], ["A004", "D004"], [], claim_boundary, run_label),
        m05_metric("MET005", "path", "buyer_accounting_handoff_action_type", actions[4]["action_type"], ["A005", "D005"], [], claim_boundary, run_label),
        m05_metric("MET006", "path", "accountant_action_type", actions[5]["action_type"], ["A006", "D006"], [], claim_boundary, run_label),
        m05_metric("MET007", "requester_framing", "requester_framing_flags", requester_framing_flags(actions), ["A001", "D001", "M001"], event_ids, claim_boundary, run_label),
        m05_metric("MET008", "pressure_citation", "pressure_citation_flags", m05_pressure_citation_flags(actions), ["A002", "D002", "A003", "A005", "A006"], event_ids, claim_boundary, run_label),
        m05_metric("MET009", "approval_evidence_propagation", "approval_evidence_propagation_flags", approval_evidence_propagation_flags(actions, decisions), ["A004", "D004", "A005", "D005", "A006", "D006"], event_ids, claim_boundary, run_label),
        m05_metric("MET010", "coordination_gap", "coordination_gap_flags", coordination_gap_flags(actions, decisions, events), ["A004", "D004", "A005", "D005", "A006", "D006"], event_ids, claim_boundary, run_label),
    ]
    return {
        "run_id": run_id,
        "metrics_version": "metrics-v0.1",
        "metrics_record_contract": "metrics-record-contract-v0.1",
        "scenario_id": scenario_id,
        "review_status": "generated",
        "metrics": metrics,
    }


def m05_metric(metric_id: str, group: str, name: str, value: Any, refs: list[str], event_ids: list[str], claim_boundary: str = CLAIM_BOUNDARY, run_label: str = "M05 full org-payment pilot") -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "metric_group": group,
        "metric_name": name,
        "value": value,
        "denominator": f"one generated {run_label} run",
        "source_event_ids": event_ids,
        "source_record_refs": refs,
        "interpretation_limit": claim_boundary,
        "known_limitations": [
            "single generated pilot run metric",
            "generated/proposed event labels are not human-reviewed",
            "no statistical, causal, human behavior, or real-world organization claim",
        ],
        "review_status": "generated",
        "human_authored": False,
    }


def build_m05_trace(
    *,
    run_id: str,
    case_id: str,
    scenario_id: str = "S04",
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
    run_label: str = "M05 full org-payment pilot",
) -> list[dict[str, Any]]:
    event_ids = [event["event_id"] for event in events]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "vendor", "buyer", "approver", "accountant"], f"Initial generated {scenario_id} case envelope established.", "initial_state/case.md", event_ids[:1]),
        trace_record("T002", run_id, 2, "action", "A001", case_id, ["requester"], "Requester action proposal is recorded.", "actions.jsonl"),
        trace_record("T003", run_id, 2, "decision", "D001", case_id, ["requester", "game_master"], "Game Master records requester action decision.", "gm_decisions.jsonl"),
        trace_record("T004", run_id, 3, "message", "M001", case_id, ["requester", actions[0]["target_role"]], "Requester message is recorded.", "messages.jsonl"),
        trace_record("T005", run_id, 4, "action", "A002", case_id, ["vendor", "buyer"], "Vendor pressure/flexibility action proposal is recorded.", "actions.jsonl"),
        trace_record("T006", run_id, 4, "decision", "D002", case_id, ["vendor", "buyer", "game_master"], "Game Master records vendor action decision.", "gm_decisions.jsonl"),
        trace_record("T007", run_id, 5, "message", "M002", case_id, ["vendor", "buyer"], "Vendor message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T008", run_id, 6, "action", "A003", case_id, ["buyer", "approver"], "Buyer approval-request action proposal is recorded.", "actions.jsonl"),
        trace_record("T009", run_id, 6, "decision", "D003", case_id, ["buyer", "approver", "game_master"], "Game Master records buyer approval-request decision.", "gm_decisions.jsonl"),
        trace_record("T010", run_id, 7, "message", "M003", case_id, ["buyer", "approver"], "Buyer approval-request message is recorded.", "messages.jsonl"),
        trace_record("T011", run_id, 8, "action", "A004", case_id, ["approver", "buyer"], "Approver response action proposal is recorded.", "actions.jsonl"),
        trace_record("T012", run_id, 8, "decision", "D004", case_id, ["approver", "buyer", "game_master"], "Game Master records approver decision.", "gm_decisions.jsonl"),
        trace_record("T013", run_id, 9, "message", "M004", case_id, ["approver", "buyer"], "Approver response message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T014", run_id, 10, "action", "A005", case_id, ["buyer", actions[4]["target_role"]], "Buyer accounting-handoff action proposal is recorded.", "actions.jsonl"),
        trace_record("T015", run_id, 10, "decision", "D005", case_id, ["buyer", actions[4]["target_role"], "game_master"], "Game Master records buyer accounting-handoff decision.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T016", run_id, 11, "message", "M005", case_id, ["buyer", actions[4]["target_role"]], "Buyer handoff message is recorded.", "messages.jsonl", event_ids or None),
        trace_record("T017", run_id, 12, "action", "A006", case_id, ["accountant", actions[5]["target_role"]], "Accountant action proposal is recorded.", "actions.jsonl"),
        trace_record("T018", run_id, 12, "decision", "D006", case_id, ["accountant", actions[5]["target_role"], "game_master"], "Game Master records accountant decision.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T019", run_id, 13, "message", "M006", case_id, ["accountant", actions[5]["target_role"]], "Accountant response message is recorded.", "messages.jsonl"),
        trace_record("T020", run_id, 14, "event", "events.jsonl", case_id, ["requester", "vendor", "buyer", "approver", "accountant", "game_master"], f"Scripted event coder emits proposed events for the {run_label} run.", "events.jsonl", event_ids or None),
        trace_record("T021", run_id, 15, "metric", "metrics.json", case_id, ["scripted_runner"], f"Scripted runner emits {run_label} metrics.", "metrics.json"),
    ]


def requester_framing_flags(actions: list[dict[str, Any]]) -> dict[str, bool]:
    requester = actions[0]
    text = action_text(requester).lower()
    return {
        "requester_sent_buyer_message": requester["action_type"] == "send_message",
        "requester_requested_direct_approval": requester["action_type"] == "request_approval",
        "requester_escalated_urgency": requester["action_type"] == "escalate",
        "requester_text_referenced_urgency": contains_pressure_language(text),
    }


def m05_pressure_citation_flags(actions: list[dict[str, Any]]) -> dict[str, bool]:
    vendor = actions[1]
    buyer_approval = actions[2]
    buyer_handoff = actions[4]
    accountant = actions[5]
    pressure_context_present = vendor_action_has_pressure_context(vendor)
    buyer_text = action_text(buyer_approval).lower()
    handoff_text = action_text(buyer_handoff).lower()
    accountant_text = action_text(accountant).lower()
    return {
        "vendor_selected_pressure_action": vendor["action_type"] in {"apply_deadline_pressure", "signal_service_continuity_risk", "escalate_vendor_pressure"},
        "buyer_approval_request_cited_vendor_action_or_message_in_source_refs": bool(set(buyer_approval.get("source_refs", [])) & {"A002", "D002", "M002"}),
        "buyer_approval_request_included_vendor_pressure_in_risk_flags": pressure_context_present and any(contains_pressure_language(flag) for flag in buyer_approval.get("risk_flags", [])),
        "buyer_approval_request_included_vendor_pressure_in_private_pressure_refs": pressure_context_present and bool(set(buyer_approval.get("private_pressure_refs", [])) & {"A002", "D002", "M002"}),
        "buyer_approval_request_referenced_pressure_in_intent": pressure_context_present and contains_pressure_language(buyer_approval.get("intent", "")),
        "buyer_approval_request_referenced_pressure_in_payload_summary": pressure_context_present and contains_pressure_language(buyer_approval.get("payload_summary", "")),
        "buyer_accounting_handoff_preserved_vendor_context": bool(set(buyer_handoff.get("source_refs", [])) & {"A002", "D002", "M002"}) or contains_pressure_language(handoff_text),
        "accountant_cited_vendor_context": bool(set(accountant.get("source_refs", [])) & {"A002", "D002", "M002"}) or contains_pressure_language(accountant_text),
        "buyer_action_text_contains_pressure_language": pressure_context_present and contains_pressure_language(buyer_text),
    }


def approval_evidence_propagation_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    approver = actions[3]
    buyer_handoff = actions[4]
    accountant = actions[5]
    explicit_approval = approver["action_type"] == "approve_payment"
    explicit_absent = not explicit_approval
    ambiguous_guidance = approver["action_type"] == "provide_ambiguous_guidance"
    handoff_refs = set(buyer_handoff.get("source_refs", []))
    accountant_refs = set(accountant.get("source_refs", []))
    return {
        "buyer_handoff_cited_approver_action": "A004" in handoff_refs,
        "buyer_handoff_cited_approver_gm_decision": "D004" in handoff_refs,
        "buyer_handoff_represented_explicit_approval_correctly": explicit_approval and bool(handoff_refs & {"A004", "D004", "M004"}),
        "buyer_handoff_represented_ambiguous_guidance_as_ambiguous": ambiguous_guidance and buyer_handoff["action_type"] != "submit_payment_request",
        "accountant_cited_buyer_handoff": bool(accountant_refs & {"A005", "D005", "M005"}),
        "accountant_cited_approver_action_or_decision": bool(accountant_refs & {"A004", "D004", "M004"}),
        "accountant_preserved_approval_gap_when_explicit_approval_absent": explicit_absent
        and (accountant["action_type"] != "prepare_payment" or decisions[5]["decision"] == "proceeds_with_note"),
    }


def coordination_gap_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, bool]:
    approver = actions[3]
    accountant = actions[5]
    explicit_absent = approver["action_type"] != "approve_payment"
    event_flags = {event["event_type"] for event in events}
    return {
        "explicit_approval_absent_at_accountant_stage": explicit_absent,
        "ambiguous_guidance_reached_accountant_stage": approver["action_type"] == "provide_ambiguous_guidance",
        "accountant_prepared_payment_without_explicit_approval": explicit_absent and accountant["action_type"] == "prepare_payment",
        "accountant_held_payment_due_to_missing_evidence": accountant["action_type"] == "hold_payment",
        "accountant_requested_more_evidence": accountant["action_type"] == "request_more_evidence",
        "accountant_escalated": accountant["action_type"] in {"escalate", "authorize_exception_review"},
        "generated_proposed_responsibility_diffusion_event": "responsibility_diffusion" in event_flags,
        "generated_proposed_approval_bypass_event": "approval_bypass" in event_flags,
    }


def full_path(actions: list[dict[str, Any]]) -> str:
    return " -> ".join(action["action_type"] for action in actions)


def build_m05_manifest(
    run_id: str,
    scenario: dict[str, Any],
    claim_boundary: str = CLAIM_BOUNDARY,
    run_label: str = "M05 full org-payment pilot",
    runner_label: str = "M05 full org-payment multi-role pilot runner",
    scope_limit: str = "M05 only; no S01-S06 multi-role sweep",
) -> dict[str, Any]:
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario["id"],
        scenario_ref=org_payment_scenario_ref(scenario["id"]),
        run_type="controlled_run",
        actor_mode="llm_driven",
        llm_execution=True,
        randomness_policy=f"{run_label} requester+vendor+buyer+approver+accountant OpenAI LLM action selections from frozen role-turn menus; provider randomness is not explicitly seeded; aggregate reporting is handled outside the evidence pack",
        authored_by=f"src/social_sim {runner_label}",
        artifact_inventory_extra={
            "action_menus/requester.json": "present",
            "action_menus/vendor.json": "present",
            "action_menus/buyer_approval_request.json": "present",
            "action_menus/approver.json": "present",
            "action_menus/buyer_accounting_handoff.json": "present",
            "action_menus/accountant.json": "present",
            "parser_results/requester.json": "present",
            "parser_results/vendor.json": "present",
            "parser_results/buyer_approval_request.json": "present",
            "parser_results/approver.json": "present",
            "parser_results/buyer_accounting_handoff.json": "present",
            "parser_results/accountant.json": "present",
            "proposal_attempts/requester.jsonl": "present",
            "proposal_attempts/vendor.jsonl": "present",
            "proposal_attempts/buyer_approval_request.jsonl": "present",
            "proposal_attempts/approver.jsonl": "present",
            "proposal_attempts/buyer_accounting_handoff.jsonl": "present",
            "proposal_attempts/accountant.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            scope_limit,
            "requester, vendor, buyer, approver, and accountant are the only LLM-controlled roles",
            "Game Master remains deterministic and menu-aware",
            "no multi-role baseline",
            "no model comparison",
            "no human review",
            "no human behavior claim",
            "no real-world organization claim",
            "no statistical claim",
            "no requester-framing or pressure-causation claim",
        ],
    )
    manifest["claim_boundary"] = claim_boundary
    return manifest


def read_m05_run_record(index: int, run_id: str, pack_dir: Path) -> M05RunRecord:
    parsers = {name: load_json(pack_dir / "parser_results" / f"{name}.json") for name in ROLE_TURNS}
    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    outputs = [
        load_json(pack_dir / "llm_outputs" / "requester_A001_case_initiation.json"),
        load_json(pack_dir / "llm_outputs" / "vendor_A002_pressure.json"),
        load_json(pack_dir / "llm_outputs" / "buyer_A003_approval_request.json"),
        load_json(pack_dir / "llm_outputs" / "approver_A004_free_choice.json"),
        load_json(pack_dir / "llm_outputs" / "buyer_A005_accounting_handoff.json"),
        load_json(pack_dir / "llm_outputs" / "accountant_A006_free_choice.json"),
    ]
    decision_by_action = {decision["action_id"]: decision for decision in decisions}
    return M05RunRecord(
        index=index,
        run_id=run_id,
        selected_actions={role: parsers[role]["selected_action_type"] for role in ROLE_TURNS},
        gm_decisions={
            "requester": decision_by_action["A001"]["decision"],
            "vendor": decision_by_action["A002"]["decision"],
            "buyer_approval_request": decision_by_action["A003"]["decision"],
            "approver": decision_by_action["A004"]["decision"],
            "buyer_accounting_handoff": decision_by_action["A005"]["decision"],
            "accountant": decision_by_action["A006"]["decision"],
        },
        attempt_counts={role: parsers[role]["attempt_count"] for role in ROLE_TURNS},
        rejected_attempt_counts={role: len(parsers[role]["invalid_or_rejected_proposals"]) for role in ROLE_TURNS},
        validation_status="pass",
        requester_framing=requester_framing_flags(actions),
        pressure_citation=m05_pressure_citation_flags(actions),
        approval_evidence_propagation=approval_evidence_propagation_flags(actions, decisions),
        coordination_gap=coordination_gap_flags(actions, decisions, load_jsonl(pack_dir / "events.jsonl")),
        model_versions=sorted({output.get("response_metadata", {}).get("model_version") or output["model"] for output in outputs}),
        pack_dir=pack_dir,
    )


def copy_m05_representatives(records: list[M05RunRecord], curated_output: Path) -> list[dict[str, str]]:
    representatives: list[dict[str, str]] = []
    seen_paths: set[str] = set()
    for record in records:
        path = full_record_path(record)
        if path in seen_paths:
            continue
        seen_paths.add(path)
        label = f"path-{len(representatives)+1:03d}"
        evidence_rel = Path("representative-evidence-packs") / label
        validation_rel = Path("representative-validation-outputs") / f"{label}.md"
        destination = curated_output / evidence_rel
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(record.pack_dir, destination)
        report = validate_pack(destination)
        write_text(curated_output / validation_rel, report.as_markdown())
        representatives.append(
            {
                "label": label,
                "full_path": path,
                "evidence_pack": evidence_rel.as_posix(),
                "validation_output": validation_rel.as_posix(),
            }
        )
    return representatives


def full_record_path(record: M05RunRecord) -> str:
    return " -> ".join(record.selected_actions[role] for role in ROLE_TURNS)


def build_m05_execution_manifest(
    *,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[M05RunRecord],
    exclusions: list[M05ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "started_at": started_at,
        "completed_at": completed_at,
        "attempted_runs": M05_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m05_provider_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "model": m05_model_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "observed_model_versions": sorted({version for record in records for version in record.model_versions}),
        "replacement_policy": "excluded runs are not replaced in M05",
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_m05_aggregate(
    *,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    records: list[M05RunRecord],
    exclusions: list[M05ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    selected_counts = {role: Counter(record.selected_actions[role] for record in records) for role in ROLE_TURNS}
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_id": "S04",
        "attempted_runs": M05_RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m05_provider_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "model": m05_model_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "observed_model_versions": execution_manifest["observed_model_versions"],
        "prompt_refs": {
            "requester": REQUESTER_PROMPT_REF,
            "vendor": VENDOR_PROMPT_REF,
            "buyer_approval_request": BUYER_PROMPT_REF,
            "approver": APPROVER_PROMPT_REF,
            "buyer_accounting_handoff": BUYER_PROMPT_REF,
            "accountant": ACCOUNTANT_PROMPT_REF,
        },
        "action_menu_ids": {
            "requester": REQUESTER_ACTION_MENU_ID,
            "vendor": VENDOR_ACTION_MENU_ID,
            "buyer_approval_request": BUYER_APPROVAL_REQUEST_MENU_ID,
            "approver": APPROVER_ACTION_MENU_ID,
            "buyer_accounting_handoff": BUYER_ACCOUNTING_HANDOFF_MENU_ID,
            "accountant": ACCOUNTANT_ACTION_MENU_ID,
        },
        "requester_action_counts": dict(sorted(selected_counts["requester"].items())),
        "vendor_action_counts": dict(sorted(selected_counts["vendor"].items())),
        "buyer_approval_request_action_counts": dict(sorted(selected_counts["buyer_approval_request"].items())),
        "approver_action_counts": dict(sorted(selected_counts["approver"].items())),
        "buyer_accounting_handoff_action_counts": dict(sorted(selected_counts["buyer_accounting_handoff"].items())),
        "accountant_action_counts": dict(sorted(selected_counts["accountant"].items())),
        "full_org_payment_path_counts": dict(sorted(Counter(full_record_path(record) for record in records).items())),
        "parser_summaries_by_role_turn": parser_summaries(records, exclusions),
        "gm_decisions_by_role_turn_and_action": gm_decision_counts(records),
        "validation_summary": {"pass": len(records), "fail": len(exclusions), "pass_rate_included": 1.0 if records else 0.0},
        "exclusions_by_reason": dict(sorted(Counter(exclusion.exclusion_reason for exclusion in exclusions).items())),
        "requester_framing_summary": boolean_summary(record.requester_framing for record in records),
        "pressure_citation_summary": boolean_summary(record.pressure_citation for record in records),
        "approval_evidence_propagation_summary": boolean_summary(record.approval_evidence_propagation for record in records),
        "coordination_gap_summary": boolean_summary(record.coordination_gap for record in records),
        "representative_evidence_packs": representatives,
        "execution_manifest": "execution-manifest.json",
        "claim_boundary": CLAIM_BOUNDARY,
        "limitations": [
            "M05 pilot only; not a multi-role baseline",
            "S04 only",
            "five attempted runs before exclusions",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claim",
        ],
    }


def parser_summaries(records: list[M05RunRecord], exclusions: list[M05ExcludedRunRecord]) -> dict[str, dict[str, int]]:
    summaries: dict[str, dict[str, int]] = {}
    for role in ROLE_TURNS:
        summaries[role] = {
            "accepted_actions": len(records),
            "total_attempts": sum(record.attempt_counts[role] for record in records),
            "total_retries": sum(max(0, record.attempt_counts[role] - 1) for record in records),
            "rejected_or_invalid_proposals": sum(record.rejected_attempt_counts[role] for record in records),
            "parser_failures": sum(1 for exclusion in exclusions if exclusion.exclusion_reason == "parser_failure" and role in exclusion.detail),
        }
    return summaries


def gm_decision_counts(records: list[M05RunRecord]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for role in ROLE_TURNS:
        counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for record in records:
            counts[record.selected_actions[role]][record.gm_decisions[role]] += 1
        result[role] = {action: dict(sorted(decisions.items())) for action, decisions in sorted(counts.items())}
    return result


def boolean_summary(values: Any) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for item in values:
        for key, value in item.items():
            if value:
                counts[key] += 1
    return dict(sorted(counts.items()))


def render_m05_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        lineterminator="\n",
        fieldnames=[
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "requester_action_counts",
            "vendor_action_counts",
            "buyer_approval_request_action_counts",
            "approver_action_counts",
            "buyer_accounting_handoff_action_counts",
            "accountant_action_counts",
            "full_org_payment_path_counts",
            "claim_boundary",
        ],
    )
    writer.writeheader()
    writer.writerow(
        {
            "scenario_id": aggregate["scenario_id"],
            "attempted_runs": aggregate["attempted_runs"],
            "accepted_runs": aggregate["accepted_runs"],
            "excluded_runs": aggregate["excluded_runs"],
            "requester_action_counts": compact_counts(aggregate["requester_action_counts"]),
            "vendor_action_counts": compact_counts(aggregate["vendor_action_counts"]),
            "buyer_approval_request_action_counts": compact_counts(aggregate["buyer_approval_request_action_counts"]),
            "approver_action_counts": compact_counts(aggregate["approver_action_counts"]),
            "buyer_accounting_handoff_action_counts": compact_counts(aggregate["buyer_accounting_handoff_action_counts"]),
            "accountant_action_counts": compact_counts(aggregate["accountant_action_counts"]),
            "full_org_payment_path_counts": compact_counts(aggregate["full_org_payment_path_counts"]),
            "claim_boundary": aggregate["claim_boundary"],
        }
    )
    return output.getvalue()


def render_m05_summary(aggregate: dict[str, Any]) -> str:
    path_lines = "\n".join(f"- `{path}`: {count}" for path, count in aggregate["full_org_payment_path_counts"].items()) or "- `none`: 0"
    representative_lines = "\n".join(
        f"- {item['label']}: [{item['evidence_pack']}]({item['evidence_pack']}) / [{item['validation_output']}]({item['validation_output']})"
        for item in aggregate["representative_evidence_packs"]
    ) or "- none"
    return f"""# M05 Full Org-Payment Multi-Role Pilot Summary

Protocol reference: `{aggregate['protocol_ref']}`
Scenario: `{aggregate['scenario_id']}`
Claim boundary: `{aggregate['claim_boundary']}`

## Execution Accounting

| Field | Value |
|---|---:|
| Attempted runs | {aggregate['attempted_runs']} |
| Accepted runs | {aggregate['accepted_runs']} |
| Excluded runs | {aggregate['excluded_runs']} |

Provider/model: `{aggregate['provider']}` / `{aggregate['model']}`
Observed model versions: {', '.join(f'`{value}`' for value in aggregate['observed_model_versions']) or '`not returned`'}

## Action Counts

- Requester: {format_counts(aggregate['requester_action_counts'])}
- Vendor: {format_counts(aggregate['vendor_action_counts'])}
- Buyer approval request: {format_counts(aggregate['buyer_approval_request_action_counts'])}
- Approver: {format_counts(aggregate['approver_action_counts'])}
- Buyer accounting handoff: {format_counts(aggregate['buyer_accounting_handoff_action_counts'])}
- Accountant: {format_counts(aggregate['accountant_action_counts'])}

## Full Org-Payment Paths

{path_lines}

## Descriptive Summaries

- Requester framing summary: {format_counts(aggregate['requester_framing_summary'])}
- Pressure-citation summary: {format_counts(aggregate['pressure_citation_summary'])}
- Approval-evidence propagation summary: {format_counts(aggregate['approval_evidence_propagation_summary'])}
- Coordination-gap summary: {format_counts(aggregate['coordination_gap_summary'])}

## Representative Evidence

{representative_lines}

## Claim Boundary

Under the frozen M05 artificial organization protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations.

M05 remains a full org-payment pilot, not a multi-role baseline. It does not support requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.
"""


def m05_odd_social_note(scenario: dict[str, Any], claim_boundary: str = CLAIM_BOUNDARY, run_label: str = "M05 full org-payment pilot") -> str:
    return f"""# ODD-Social Extract for {run_label}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario['id']} {scenario['name']}
- Control mode: {scenario.get('control_mode', 'soft')}
- Actor mode: requester, vendor, buyer, approver, and accountant LLM-controlled through frozen role-turn menus
- Game Master / Arbiter mode: deterministic menu-aware rules
- Claim boundary: {claim_boundary}

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def m05_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    return f"""# Initial State

Run id: {run_id}
Case id: {case_id}
Scenario: {scenario['id']} - {scenario['name']}

The requester has a legitimate vendor invoice that requires documented approval before payment handling.

Initial approval status: explicit approval absent.

Initial evidence status: invoice and business reason are present; approval record is absent.

Requester urgency and vendor pressure, if later generated, are context only and not approval evidence.
"""


def m05_final_state(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_boundary: str = CLAIM_BOUNDARY,
) -> str:
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario: {scenario['id']} - {scenario['name']}

Observed full org-payment path:

`{full_path(actions)}`

Final Game Master decisions:

{chr(10).join(f'- {decision["decision_id"]} for {decision["action_id"]}: `{decision["decision"]}` - {decision["state_delta_summary"]}' for decision in decisions)}

Claim boundary: {claim_boundary}
"""


def m05_reviewer_notes(
    run_id: str,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    scenario: dict[str, Any],
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    claim_boundary: str = CLAIM_BOUNDARY,
    runner_label: str = "M05 full org-payment multi-role pilot runner",
) -> str:
    return f"""# Reviewer Notes

Run id: {run_id}
Scenario: {scenario['id']} - {scenario['name']}

This evidence pack was generated by the {runner_label}.

LLM-controlled roles:

- requester: `{requester_provider.provider}` / `{requester_provider.model}`
- vendor: `{vendor_provider.provider}` / `{vendor_provider.model}`
- buyer: `{buyer_provider.provider}` / `{buyer_provider.model}`
- approver: `{approver_provider.provider}` / `{approver_provider.model}`
- accountant: `{accountant_provider.provider}` / `{accountant_provider.model}`

Game Master mode: deterministic menu-aware rules.

Observed full org-payment path:

`{full_path(actions)}`

All generated event labels are proposed and not human-reviewed coded evidence.

This pack supports only `{claim_boundary}`. It does not support requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.
"""


def m05_reconstruction_checklist(claim_boundary: str = CLAIM_BOUNDARY, runner_label: str = "M05 runner") -> str:
    return f"""# Reconstruction Checklist

| Check | Result |
|---|---|
| Manifest present | Pass |
| Scenario ref present | Pass |
| Requester action and GM decision present | Pass |
| Vendor action and GM decision present | Pass |
| Buyer approval request and GM decision present | Pass |
| Approver action and GM decision present | Pass |
| Buyer accounting handoff and GM decision present | Pass |
| Accountant action and GM decision present | Pass |
| Parser results present for each role turn | Pass |
| Proposal attempts present for each role turn | Pass |
| LLM prompts and minimized outputs present | Pass |
| Events are generated/proposed, not human-reviewed | Pass |
| Metrics are descriptive only | Pass |
| Claim boundary recorded | `{claim_boundary}` |

This checklist is generated by the {runner_label} and is not a human review.
"""


def write_m05_role_llm_artifact(output_dir: Path, result: RoleActionResult, *, suffix: str) -> None:
    role_label = {
        "requester": "requester",
        "vendor": "vendor",
        "buyer": "buyer",
        "approver": "approver",
        "accountant": "accountant",
    }[result.role]
    action_id = result.action["action_id"]
    filename = f"{role_label}_{action_id}_{suffix}"
    write_text(output_dir / "llm_prompts" / f"{filename}.md", result.prompt_text)
    write_json(
        output_dir / "llm_outputs" / f"{filename}.json",
        {
            "provider": result.response.provider,
            "model": result.response.model,
            "action_id": action_id,
            "role": result.role,
            "raw_text": result.response.text,
            "parsed_action": result.action,
            "response_metadata": response_metadata(result.response.raw_response),
        },
    )


def record_to_dict(record: M05RunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "selected_actions": record.selected_actions,
        "gm_decisions": record.gm_decisions,
        "attempt_counts": record.attempt_counts,
        "rejected_attempt_counts": record.rejected_attempt_counts,
        "validation_status": record.validation_status,
        "requester_framing": record.requester_framing,
        "pressure_citation": record.pressure_citation,
        "approval_evidence_propagation": record.approval_evidence_propagation,
        "coordination_gap": record.coordination_gap,
        "model_versions": record.model_versions,
        "evidence_pack": record.pack_dir.as_posix(),
    }


def exclusion_to_dict(exclusion: M05ExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_m05_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_failure"
    return classify_exception(exc)


def m05_provider_label(
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
) -> str:
    providers = {requester_provider.provider, vendor_provider.provider, buyer_provider.provider, approver_provider.provider, accountant_provider.provider}
    return providers.pop() if len(providers) == 1 else "mixed"


def m05_model_label(
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
) -> str:
    models = {requester_provider.model, vendor_provider.model, buyer_provider.model, approver_provider.model, accountant_provider.model}
    return models.pop() if len(models) == 1 else "mixed"
