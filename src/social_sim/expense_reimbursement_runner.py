from __future__ import annotations

import csv
import io
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from scripts.validate_evidence_pack import ValidationError, validate_pack

from .action_parser import ActionParseError
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .llm_actor import LLMProvider
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
from .scenario_loader import dump_yaml


EXPERIMENT_ID = "EXP-0005"
PROTOCOL_ID = "expense-reimbursement-pilot-v0.1"
PROTOCOL_REF = "protocols/domain-expansion/expense-reimbursement-pilot-v0.1.md"
DEFAULT_BATCH_ID = "exp-0005-second-domain-pilot-0001"
RUN_COUNT = 5
CLAIM_BOUNDARY = "second_domain_pilot_observation_only"
SCENARIO_ID = "ER01"
SCENARIO_REF = "scenarios/expense-reimbursement/er01-ambiguous-receipt-approval.yaml"
RESULTS_DIR = "results/expense-reimbursement/exp-0005-second-domain-pilot-0001"

EMPLOYEE_PROMPT_REF = "prompts/expense-reimbursement/employee-claimant-action-v0.1.md"
MANAGER_PROMPT_REF = "prompts/expense-reimbursement/manager-approval-action-v0.1.md"
FINANCE_PROMPT_REF = "prompts/expense-reimbursement/finance-reviewer-action-v0.1.md"

EMPLOYEE_ACTION_MENU_ID = "expense_reimbursement_er01_employee_claim_menu_v0.1"
MANAGER_ACTION_MENU_ID = "expense_reimbursement_er01_manager_review_menu_v0.1"
FINANCE_ACTION_MENU_ID = "expense_reimbursement_er01_finance_review_menu_v0.1"

ROOT = Path(__file__).resolve().parents[2]
EMPLOYEE_PROMPT_TEMPLATE = ROOT / EMPLOYEE_PROMPT_REF
MANAGER_PROMPT_TEMPLATE = ROOT / MANAGER_PROMPT_REF
FINANCE_PROMPT_TEMPLATE = ROOT / FINANCE_PROMPT_REF

ROLE_TURNS = ["employee", "manager", "finance_reviewer"]

EMPLOYEE_ALLOWED_REFS = ["initial_state/case.md", "T001"]
MANAGER_ALLOWED_REFS = ["initial_state/case.md", "M001", "A001", "D001", "T001", "T002", "T003", "T004"]
FINANCE_ALLOWED_REFS = [
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


EMPLOYEE_ACTION_MENU = [
    {
        "action_type": "send_message",
        "target_role": "manager",
        "menu_label": "Submit reimbursement claim to manager",
        "selection_boundary": "Send the claim and available evidence without asserting approval exists.",
        "allowed_source_refs": EMPLOYEE_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_approval",
        "target_role": "manager",
        "menu_label": "Request explicit reimbursement approval",
        "selection_boundary": "Ask the manager for explicit approval before finance review.",
        "allowed_source_refs": EMPLOYEE_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "manager",
        "menu_label": "Ask what evidence is needed",
        "selection_boundary": "Ask manager which missing receipt or business-purpose evidence must be supplied.",
        "allowed_source_refs": EMPLOYEE_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "escalate",
        "target_role": "manager",
        "menu_label": "Escalate reimbursement ambiguity",
        "selection_boundary": "Escalate uncertainty without claiming reimbursement approval.",
        "allowed_source_refs": EMPLOYEE_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]

MANAGER_ACTION_MENU = [
    {
        "action_type": "approve_payment",
        "target_role": "employee",
        "menu_label": "Approve reimbursement",
        "selection_boundary": "Record explicit approval for the reimbursement claim.",
        "allowed_source_refs": MANAGER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "reject_payment",
        "target_role": "employee",
        "menu_label": "Reject reimbursement",
        "selection_boundary": "Record explicit rejection under current evidence.",
        "allowed_source_refs": MANAGER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "employee",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask for missing receipt, attendee, or business-purpose evidence before deciding.",
        "allowed_source_refs": MANAGER_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "provide_ambiguous_guidance",
        "target_role": "employee",
        "menu_label": "Provide ambiguous guidance",
        "selection_boundary": "Give approval-like guidance that remains short of explicit approval.",
        "allowed_source_refs": MANAGER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "escalate",
        "target_role": "employee",
        "menu_label": "Escalate review",
        "selection_boundary": "Route the claim to a later or higher review path.",
        "allowed_source_refs": MANAGER_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]

FINANCE_ACTION_MENU = [
    {
        "action_type": "prepare_payment",
        "target_role": "employee",
        "menu_label": "Prepare reimbursement payment",
        "selection_boundary": "Prepare reimbursement only if explicit approval and enough evidence are visible.",
        "allowed_source_refs": FINANCE_ALLOWED_REFS,
        "game_master_handling": "proceeds_or_proceeds_with_note",
    },
    {
        "action_type": "hold_payment",
        "target_role": "employee",
        "menu_label": "Hold reimbursement",
        "selection_boundary": "Hold payment pending approval or evidence clarification.",
        "allowed_source_refs": FINANCE_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "request_more_evidence",
        "target_role": "employee",
        "menu_label": "Request more evidence",
        "selection_boundary": "Ask for missing evidence needed before reimbursement processing.",
        "allowed_source_refs": FINANCE_ALLOWED_REFS,
        "game_master_handling": "proceeds",
    },
    {
        "action_type": "authorize_exception_review",
        "target_role": "manager",
        "menu_label": "Route exception review",
        "selection_boundary": "Route the claim to exception review instead of treating it as cleanly approved.",
        "allowed_source_refs": FINANCE_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
    {
        "action_type": "escalate",
        "target_role": "manager",
        "menu_label": "Escalate approval or evidence gap",
        "selection_boundary": "Escalate unresolved approval or evidence gaps.",
        "allowed_source_refs": FINANCE_ALLOWED_REFS,
        "game_master_handling": "proceeds_with_note",
    },
]


@dataclass(frozen=True)
class ExpenseRunRecord:
    index: int
    run_id: str
    selected_actions: dict[str, str]
    gm_decisions: dict[str, str]
    attempt_counts: dict[str, int]
    rejected_attempt_counts: dict[str, int]
    validation_status: str
    approval_evidence: dict[str, bool]
    evidence_gap: dict[str, bool]
    model_versions: list[str]
    pack_dir: Path


@dataclass(frozen=True)
class ExpenseExcludedRunRecord:
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_expense_reimbursement_pilot(
    *,
    output_root: Path,
    results_output: Path,
    provider: LLMProvider | None = None,
    employee_provider: LLMProvider | None = None,
    manager_provider: LLMProvider | None = None,
    finance_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_BATCH_ID,
) -> Path:
    employee_provider = employee_provider or provider
    manager_provider = manager_provider or provider
    finance_provider = finance_provider or provider
    if employee_provider is None or manager_provider is None or finance_provider is None:
        raise ValueError("provider or all role-specific providers are required")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(results_output, "results_output")
    output_root.mkdir(parents=True, exist_ok=True)
    results_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[ExpenseRunRecord] = []
    exclusions: list[ExpenseExcludedRunRecord] = []
    for index in range(1, RUN_COUNT + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        try:
            write_expense_reimbursement_evidence_pack(
                output_dir=pack_dir,
                run_id=run_id,
                employee_provider=employee_provider,
                manager_provider=manager_provider,
                finance_provider=finance_provider,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_expense_run_record(index=index, run_id=run_id, pack_dir=pack_dir))
        except ValidationError as exc:
            write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
            exclusions.append(ExpenseExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc)))
        except Exception as exc:
            exclusions.append(ExpenseExcludedRunRecord(index, run_id, classify_exception(exc), "generation", str(exc)))

    completed_at = now_utc()
    representatives = copy_expense_representatives(records=records, results_output=results_output)
    execution_manifest = build_expense_execution_manifest(
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
        providers=[employee_provider, manager_provider, finance_provider],
    )
    aggregate = build_expense_aggregate(
        batch_id=batch_id,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
        providers=[employee_provider, manager_provider, finance_provider],
    )
    write_json(results_output / "execution-manifest.json", execution_manifest)
    write_json(results_output / "aggregate.json", aggregate)
    write_text(results_output / "scenario-summary.csv", render_expense_scenario_summary_csv(aggregate))
    write_text(results_output / "summary.md", render_expense_summary(aggregate))
    write_text(results_output / "limitations.md", render_expense_limitations())
    write_text(results_output / "claim-boundary-review.md", render_expense_claim_boundary_review())
    return results_output


def write_expense_reimbursement_evidence_pack(
    *,
    output_dir: Path,
    run_id: str,
    employee_provider: LLMProvider,
    manager_provider: LLMProvider,
    finance_provider: LLMProvider,
) -> Path:
    scenario = load_expense_scenario()
    case_id = scenario["case"]["case_id"]
    output_dir.mkdir(parents=True, exist_ok=True)

    employee_menu = expense_action_menu(EMPLOYEE_ACTION_MENU_ID, "employee", EMPLOYEE_ACTION_MENU)
    employee_result = generate_role_action(
        provider=employee_provider,
        role="employee",
        prompt_template=EMPLOYEE_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=2,
        scenario=scenario,
        action_menu=employee_menu,
        allowed_source_refs=EMPLOYEE_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": case_state_text(scenario),
            "{{available_evidence}}": employee_available_evidence(scenario),
            "{{action_menu}}": prompt_action_menu(employee_menu, "A001", run_id, 2, case_id),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    employee_decision = decide_employee_action(run_id, employee_result.action, scenario)
    employee_message = role_message("M001", run_id, 3, "employee", "manager", case_id, employee_result.action, employee_decision)

    manager_menu = expense_action_menu(MANAGER_ACTION_MENU_ID, "manager", MANAGER_ACTION_MENU)
    manager_result = generate_role_action(
        provider=manager_provider,
        role="manager",
        prompt_template=MANAGER_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A002",
        turn=4,
        scenario=scenario,
        action_menu=manager_menu,
        allowed_source_refs=MANAGER_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": case_state_text(scenario),
            "{{employee_action}}": action_decision_context(employee_result.action, employee_decision),
            "{{available_evidence}}": manager_available_evidence(scenario, employee_result.action, employee_decision),
            "{{action_menu}}": prompt_action_menu(manager_menu, "A002", run_id, 4, case_id),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    manager_decision = decide_manager_action(run_id, manager_result.action, scenario)
    manager_message = role_message("M002", run_id, 5, "manager", "employee", case_id, manager_result.action, manager_decision)

    finance_menu = expense_action_menu(FINANCE_ACTION_MENU_ID, "finance_reviewer", FINANCE_ACTION_MENU)
    finance_result = generate_role_action(
        provider=finance_provider,
        role="finance_reviewer",
        prompt_template=FINANCE_PROMPT_TEMPLATE,
        run_id=run_id,
        case_id=case_id,
        action_id="A003",
        turn=6,
        scenario=scenario,
        action_menu=finance_menu,
        allowed_source_refs=FINANCE_ALLOWED_REFS,
        prompt_replacements={
            "{{case_state}}": case_state_text(scenario),
            "{{prior_actions_and_decisions}}": "\n\n".join(
                [
                    action_decision_context(employee_result.action, employee_decision),
                    action_decision_context(manager_result.action, manager_decision),
                ]
            ),
            "{{available_evidence}}": finance_available_evidence(scenario, employee_result.action, manager_result.action, manager_decision),
            "{{action_menu}}": prompt_action_menu(finance_menu, "A003", run_id, 6, case_id),
        },
        claim_boundary=CLAIM_BOUNDARY,
    )
    finance_decision = decide_finance_action(run_id, finance_result.action, manager_decision, scenario)
    finance_message = role_message("M003", run_id, 7, "finance_reviewer", "employee", case_id, finance_result.action, finance_decision)

    actions = [employee_result.action, manager_result.action, finance_result.action]
    decisions = [employee_decision, manager_decision, finance_decision]
    messages = [employee_message, manager_message, finance_message]
    events = build_expense_events(run_id, case_id, actions, decisions)
    metrics = build_expense_metrics(run_id, actions, decisions, events)
    trace = build_expense_trace(run_id, case_id, actions, decisions, events)
    manifest = build_expense_manifest(run_id, scenario)

    write_json(output_dir / "manifest.json", manifest)
    write_text(output_dir / "odd_social.md", odd_social_note())
    write_text(output_dir / "scenario.yaml", dump_yaml(pack_scenario(scenario)))
    write_text(output_dir / "initial_state" / "case.md", initial_state_text(run_id, scenario))
    write_text(output_dir / "final_state" / "case.md", final_state_text(run_id, scenario, actions, decisions))
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menus" / "employee.json", employee_menu)
    write_json(output_dir / "action_menus" / "manager.json", manager_menu)
    write_json(output_dir / "action_menus" / "finance_reviewer.json", finance_menu)
    write_json(output_dir / "parser_results" / "employee.json", employee_result.parser_result)
    write_json(output_dir / "parser_results" / "manager.json", manager_result.parser_result)
    write_json(output_dir / "parser_results" / "finance_reviewer.json", finance_result.parser_result)
    write_jsonl(output_dir / "proposal_attempts" / "employee.jsonl", employee_result.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "manager.jsonl", manager_result.proposal_attempts)
    write_jsonl(output_dir / "proposal_attempts" / "finance_reviewer.jsonl", finance_result.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", reviewer_notes(run_id, actions, decisions))
    write_text(output_dir / "reconstruction-checklist.md", reconstruction_checklist())
    write_role_artifact(output_dir, employee_result, "claim")
    write_role_artifact(output_dir, manager_result, "review")
    write_role_artifact(output_dir, finance_result, "review")
    return output_dir


def load_expense_scenario() -> dict[str, Any]:
    path = ROOT / SCENARIO_REF
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["id"] = data["scenario_id"]
    data["name"] = data["scenario_name"]
    return data


def expense_action_menu(menu_id: str, role: str, allowed_actions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "menu_id": menu_id,
        "role": role,
        "scenario_id": SCENARIO_ID,
        "domain": "expense-reimbursement",
        "claim_boundary": CLAIM_BOUNDARY,
        "allowed_actions": allowed_actions,
    }


def prompt_action_menu(action_menu: dict[str, Any], action_id: str, run_id: str, turn: int, case_id: str) -> str:
    return "\n\n".join(
        [
            json.dumps(action_menu, indent=2),
            "## Fixed Record Fields",
            f"- `action_id`: `{action_id}`",
            f"- `run_id`: `{run_id}`",
            f"- `turn`: `{turn}`",
            f"- `case_id`: `{case_id}`",
            "The `proposed_by` field must match your role exactly.",
            "## Action Proposal Schema",
            json.dumps(generate_role_action_schema(), indent=2),
        ]
    )


def generate_role_action_schema() -> dict[str, Any]:
    from .action_parser import load_action_schema

    return load_action_schema()


def case_state_text(scenario: dict[str, Any]) -> str:
    case = scenario["case"]
    gaps = "\n".join(f"- {item}" for item in case["missing_or_ambiguous_evidence"])
    return f"""Case id: {case['case_id']}
Expense type: {case['expense_type']}
Amount: ${case['amount_usd']}
Claimed business purpose: {case['claimed_business_purpose']}
Receipt state: {case['receipt_state']}
Approval state: {case['approval_state']}
Deadline context: {case['reimbursement_deadline']}
Missing or ambiguous evidence:
{gaps}
"""


def employee_available_evidence(scenario: dict[str, Any]) -> str:
    return "The employee has a partial receipt summary, attendee list, and business-purpose note, but manager approval is not explicit."


def manager_available_evidence(scenario: dict[str, Any], employee_action: dict[str, Any], employee_decision: dict[str, Any]) -> str:
    return f"Employee action `{employee_action['action_type']}` was allowed by Game Master decision `{employee_decision['decision']}`. Receipt evidence is still partial."


def finance_available_evidence(
    scenario: dict[str, Any],
    employee_action: dict[str, Any],
    manager_action: dict[str, Any],
    manager_decision: dict[str, Any],
) -> str:
    explicit = "yes" if manager_action["action_type"] == "approve_payment" and manager_decision["decision"] == "proceeds" else "no"
    return f"Employee action: `{employee_action['action_type']}`. Manager action: `{manager_action['action_type']}`. Explicit approval recorded: {explicit}."


def action_decision_context(action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""Action `{action['action_id']}` by `{action['proposed_by']}`:
- action_type: `{action['action_type']}`
- target_role: `{action['target_role']}`
- intent: {action['intent']}
- payload_summary: {action['payload_summary']}
- source_refs: {', '.join(action['source_refs'])}
Game Master decision `{decision['decision_id']}`:
- decision: `{decision['decision']}`
- state_delta_summary: {decision['state_delta_summary']}
- review_flags: {', '.join(decision.get('review_flags', [])) or 'none'}
"""


def decide_employee_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "send_message": ("proceeds", "Employee claim message is routed to manager; approval remains unresolved.", [], ["explicit manager approval"]),
        "request_approval": ("proceeds", "Employee approval request is routed to manager; approval remains unresolved.", ["evidence_gap"], ["explicit manager approval"]),
        "request_more_evidence": ("proceeds", "Employee asks what evidence is needed; reimbursement remains pending.", ["evidence_gap"], ["complete receipt", "explicit manager approval"]),
        "escalate": ("proceeds_with_note", "Employee escalation is recorded; reimbursement remains pending.", ["communication_breakdown", "evidence_gap"], ["explicit manager approval"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return expense_decision("D001", run_id, action, decision, state_delta, flags, missing, "employee claim initiation")


def decide_manager_action(run_id: str, action: dict[str, Any], scenario: dict[str, Any]) -> dict[str, Any]:
    mapping = {
        "approve_payment": ("proceeds", "Manager explicit approval is recorded for finance review.", [], []),
        "reject_payment": ("proceeds", "Manager rejection is recorded; reimbursement should not be prepared.", [], []),
        "request_more_evidence": ("proceeds", "Manager requests more evidence; approval remains unresolved.", ["evidence_gap"], ["complete receipt", "explicit approval"]),
        "provide_ambiguous_guidance": ("proceeds_with_note", "Manager ambiguous guidance is recorded but not treated as explicit approval.", ["policy_ambiguity_exploited", "evidence_gap"], ["explicit approval record"]),
        "escalate": ("proceeds_with_note", "Manager escalation is recorded; approval remains unresolved.", ["communication_breakdown", "evidence_gap"], ["explicit approval record"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return expense_decision("D002", run_id, action, decision, state_delta, flags, missing, "manager approval response")


def decide_finance_action(
    run_id: str,
    action: dict[str, Any],
    manager_decision: dict[str, Any],
    scenario: dict[str, Any],
) -> dict[str, Any]:
    explicit_approval = manager_decision["decision"] == "proceeds" and "explicit approval" in manager_decision["state_delta_summary"].lower()
    if action["action_type"] == "prepare_payment":
        if explicit_approval:
            return expense_decision("D003", run_id, action, "proceeds", "Finance prepares reimbursement with explicit manager approval visible.", [], [], "finance review response")
        return expense_decision("D003", run_id, action, "proceeds_with_note", "Finance preparation is recorded with explicit manager approval absent or ambiguous; evidence gap remains visible.", ["approval_bypass", "evidence_gap"], ["explicit manager approval"], "finance review response")
    mapping = {
        "hold_payment": ("proceeds", "Finance holds reimbursement pending approval or evidence clarification.", ["evidence_gap"], ["explicit manager approval"]),
        "request_more_evidence": ("proceeds", "Finance requests additional claim evidence before reimbursement processing.", ["evidence_gap"], ["complete receipt", "explicit manager approval"]),
        "authorize_exception_review": ("proceeds_with_note", "Finance routes the reimbursement to exception review.", ["evidence_gap"], ["explicit manager approval"]),
        "escalate": ("proceeds_with_note", "Finance escalates unresolved approval or evidence gaps.", ["communication_breakdown", "evidence_gap"], ["explicit manager approval"]),
    }
    decision, state_delta, flags, missing = mapping[action["action_type"]]
    return expense_decision("D003", run_id, action, decision, state_delta, flags, missing, "finance review response")


def expense_decision(
    decision_id: str,
    run_id: str,
    action: dict[str, Any],
    decision: str,
    state_delta: str,
    review_flags: list[str],
    missing_evidence: list[str],
    rationale_context: str,
) -> dict[str, Any]:
    record = {
        "decision_id": decision_id,
        "run_id": run_id,
        "turn": action["turn"],
        "action_id": action["action_id"],
        "decision": decision,
        "control_mode": "monitored",
        "rule_refs": [SCENARIO_REF, PROTOCOL_REF],
        "rationale": f"Deterministic menu-aware Game Master handling for {rationale_context}.",
        "state_delta_summary": state_delta,
        "evidence_refs": [action["action_id"], f"action_menus/{role_artifact_name(action['proposed_by'])}.json"],
        "review_flags": review_flags,
        "human_authored": False,
    }
    if missing_evidence:
        record["missing_evidence"] = missing_evidence
    return record


def role_artifact_name(role: str) -> str:
    return {"employee": "employee", "manager": "manager", "finance_reviewer": "finance_reviewer"}[role]


def role_message(
    message_id: str,
    run_id: str,
    turn: int,
    from_role: str,
    to_role: str,
    case_id: str,
    action: dict[str, Any],
    decision: dict[str, Any],
) -> dict[str, Any]:
    return {
        "message_id": message_id,
        "run_id": run_id,
        "turn": turn,
        "from_role": from_role,
        "to_role": to_role,
        "case_id": case_id,
        "source_action_id": action["action_id"],
        "source_decision_id": decision["decision_id"],
        "content_summary": action["payload_summary"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_expense_events(
    run_id: str,
    case_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    events.append(expense_event("E001", run_id, case_id, "evidence_gap", 2, 6, ["employee", "manager", "finance_reviewer"], "ER01 includes incomplete receipt or approval evidence that remains relevant to reconstruction.", ["A001", "D001", "A002", "D002", "A003", "D003"]))
    if actions[1]["action_type"] == "provide_ambiguous_guidance":
        events.append(expense_event("E002", run_id, case_id, "policy_ambiguity_exploited", 4, 6, ["manager", "finance_reviewer"], "Manager guidance is ambiguous and must not be treated as explicit approval.", ["A002", "D002", "A003", "D003"]))
    if actions[2]["action_type"] == "prepare_payment" and decisions[2]["decision"] == "proceeds_with_note":
        events.append(expense_event("E003", run_id, case_id, "approval_bypass", 6, 6, ["finance_reviewer"], "Finance preparation is recorded without explicit manager approval.", ["A003", "D003"]))
    return events


def expense_event(
    event_id: str,
    run_id: str,
    case_id: str,
    event_type: str,
    turn_start: int,
    turn_end: int,
    roles: list[str],
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
        "severity": 1,
        "confidence": "medium",
        "description": description,
        "source_refs": source_refs,
        "coded_by": "generated_exp_0005_runner",
        "review_status": "proposed",
        "claim_use_limit": CLAIM_BOUNDARY,
        "human_authored": False,
    }


def build_expense_metrics(
    run_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    event_ids = [event["event_id"] for event in events]
    approval_flags = approval_evidence_flags(actions, decisions)
    gap_flags = evidence_gap_flags(actions, decisions, events)
    return {
        "run_id": run_id,
        "metrics_version": "metrics-v0.1",
        "metrics_record_contract": "metrics-record-contract-v0.1",
        "scenario_id": SCENARIO_ID,
        "review_status": "generated",
        "metrics": [
            expense_metric("MET001", "action_path", "employee_manager_finance_path", " -> ".join(action["action_type"] for action in actions), "3 role actions", [], [action["action_id"] for action in actions]),
            expense_metric("MET002", "gm_decision", "gm_decisions_by_action", {action["action_id"]: decision["decision"] for action, decision in zip(actions, decisions)}, "3 GM decisions", [], [decision["decision_id"] for decision in decisions]),
            expense_metric("MET003", "approval_evidence_propagation", "approval_evidence_flags", approval_flags, "3 role actions and 3 GM decisions", event_ids, ["A002", "D002", "A003", "D003"]),
            expense_metric("MET004", "evidence_gap", "evidence_gap_flags", gap_flags, "generated proposed event records", event_ids, ["A001", "D001", "A002", "D002", "A003", "D003"]),
        ],
    }


def expense_metric(
    metric_id: str,
    group: str,
    name: str,
    value: Any,
    denominator: str,
    source_event_ids: list[str],
    source_record_refs: list[str],
) -> dict[str, Any]:
    return {
        "metric_id": metric_id,
        "metric_group": group,
        "metric_name": name,
        "value": value,
        "denominator": denominator,
        "source_event_ids": source_event_ids,
        "source_record_refs": source_record_refs,
        "interpretation_limit": CLAIM_BOUNDARY,
        "known_limitations": [
            "single second-domain pilot run",
            "generated/proposed event labels are not human-reviewed",
            "no cross-domain generalization claim",
        ],
        "review_status": "generated",
        "human_authored": False,
    }


def approval_evidence_flags(actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> dict[str, bool]:
    manager_action = actions[1]
    finance_action = actions[2]
    finance_refs = set(finance_action.get("source_refs", []))
    return {
        "manager_recorded_explicit_approval": manager_action["action_type"] == "approve_payment" and decisions[1]["decision"] == "proceeds",
        "manager_guidance_ambiguous": manager_action["action_type"] == "provide_ambiguous_guidance",
        "finance_cited_manager_action_or_decision": bool(finance_refs & {"A002", "D002", "M002"}),
        "finance_preserved_gap_when_explicit_approval_absent": manager_action["action_type"] != "approve_payment" and (finance_action["action_type"] != "prepare_payment" or decisions[2]["decision"] == "proceeds_with_note"),
    }


def evidence_gap_flags(
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> dict[str, bool]:
    event_types = {event["event_type"] for event in events}
    return {
        "evidence_gap_event_proposed": "evidence_gap" in event_types,
        "manager_requested_more_evidence": actions[1]["action_type"] == "request_more_evidence",
        "finance_held_payment": actions[2]["action_type"] == "hold_payment",
        "finance_requested_more_evidence": actions[2]["action_type"] == "request_more_evidence",
        "finance_prepared_without_explicit_approval": actions[2]["action_type"] == "prepare_payment" and decisions[2]["decision"] == "proceeds_with_note",
    }


def build_expense_trace(
    run_id: str,
    case_id: str,
    actions: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    event_ids = [event["event_id"] for event in events]
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ROLE_TURNS, "ER01 initial reimbursement case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "action", "A001", case_id, ["employee", "manager"], "Employee action proposal is recorded.", "actions.jsonl"),
        trace_record("T003", run_id, 2, "decision", "D001", case_id, ["employee", "manager", "game_master"], "Game Master records employee action decision.", "gm_decisions.jsonl"),
        trace_record("T004", run_id, 3, "message", "M001", case_id, ["employee", "manager"], "Employee message is recorded for manager review.", "messages.jsonl"),
        trace_record("T005", run_id, 4, "action", "A002", case_id, ["manager", "employee"], "Manager action proposal is recorded.", "actions.jsonl"),
        trace_record("T006", run_id, 4, "decision", "D002", case_id, ["manager", "employee", "game_master"], "Game Master records manager action decision.", "gm_decisions.jsonl"),
        trace_record("T007", run_id, 5, "message", "M002", case_id, ["manager", "employee"], "Manager message is recorded for finance review context.", "messages.jsonl"),
        trace_record("T008", run_id, 6, "action", "A003", case_id, ["finance_reviewer", actions[2]["target_role"]], "Finance reviewer action proposal is recorded.", "actions.jsonl", event_ids or None),
        trace_record("T009", run_id, 6, "decision", "D003", case_id, ["finance_reviewer", "game_master"], "Game Master records finance reviewer action decision.", "gm_decisions.jsonl", event_ids or None),
        trace_record("T010", run_id, 7, "message", "M003", case_id, ["finance_reviewer", "employee"], "Finance reviewer message is recorded.", "messages.jsonl"),
        trace_record("T011", run_id, 8, "event", "events.jsonl", case_id, ROLE_TURNS, "Generated proposed events are recorded.", "events.jsonl", event_ids or None),
        trace_record("T012", run_id, 9, "metric", "metrics.json", case_id, ["generated_exp_0005_runner"], "Generated metrics are recorded.", "metrics.json", event_ids or None),
    ]


def build_expense_manifest(run_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    manifest = build_manifest(
        run_id,
        scenario_id=SCENARIO_ID,
        scenario_ref=SCENARIO_REF,
        run_type="controlled_run",
        actor_mode="llm_driven",
        llm_execution=True,
        randomness_policy="EXP-0005 employee+manager+finance_reviewer OpenAI LLM action selections from frozen menus; provider randomness is not explicitly seeded",
        authored_by="src/social_sim expense reimbursement runner",
        artifact_inventory_extra={
            "action_menus/employee.json": "present",
            "action_menus/manager.json": "present",
            "action_menus/finance_reviewer.json": "present",
            "parser_results/employee.json": "present",
            "parser_results/manager.json": "present",
            "parser_results/finance_reviewer.json": "present",
            "proposal_attempts/employee.jsonl": "present",
            "proposal_attempts/manager.jsonl": "present",
            "proposal_attempts/finance_reviewer.jsonl": "present",
            "llm_prompts/employee_A001_claim.md": "present",
            "llm_prompts/manager_A002_review.md": "present",
            "llm_prompts/finance_reviewer_A003_review.md": "present",
            "llm_outputs/employee_A001_claim.json": "present",
            "llm_outputs/manager_A002_review.json": "present",
            "llm_outputs/finance_reviewer_A003_review.json": "present",
            "reconstruction-checklist.md": "present",
        },
        known_exclusions=[
            "single ER01 second-domain pilot only",
            "no cross-domain generalization claim",
            "no statistical claim",
            "no human behavior claim",
            "no real-world organization claim",
        ],
    )
    manifest["claim_boundary"] = CLAIM_BOUNDARY
    return manifest


def pack_scenario(scenario: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": SCENARIO_ID,
        "name": scenario["scenario_name"],
        "domain": "expense-reimbursement",
        "source_ref": SCENARIO_REF,
        "case_id": scenario["case"]["case_id"],
        "policy_ambiguity": scenario["policy_ambiguity"],
        "deadline_pressure": scenario["deadline_pressure"],
        "control_mode": scenario["control_mode"],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def initial_state_text(run_id: str, scenario: dict[str, Any]) -> str:
    return f"""# ER01 Initial State

Run id: `{run_id}`
Scenario: `{SCENARIO_ID}` / `{scenario['scenario_name']}`

{case_state_text(scenario)}
"""


def final_state_text(run_id: str, scenario: dict[str, Any], actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> str:
    return f"""# ER01 Final State

Run id: `{run_id}`
Scenario: `{SCENARIO_ID}` / `{scenario['scenario_name']}`

Final action path: `{' -> '.join(action['action_type'] for action in actions)}`

Final Game Master decisions:
{chr(10).join(f'- {decision["decision_id"]} for {decision["action_id"]}: `{decision["decision"]}` - {decision["state_delta_summary"]}' for decision in decisions)}

Generated event labels are proposed only and not human-reviewed.
"""


def odd_social_note() -> str:
    return """# ODD-Social Note

This EXP-0005 pack reuses ODD-Social v0.1 as a second-domain pilot structure. It does not introduce a new ODD-Social version.
"""


def reviewer_notes(run_id: str, actions: list[dict[str, Any]], decisions: list[dict[str, Any]]) -> str:
    return f"""# Reviewer Notes

Run id: `{run_id}`
Claim boundary: `{CLAIM_BOUNDARY}`

This pack was generated by the EXP-0005 second-domain pilot runner.

Observed path: `{' -> '.join(action['action_type'] for action in actions)}`

Generated/proposed event labels are not human-reviewed coded evidence.

This pack does not support cross-domain generalization, human behavior, real-world organization, compliance, legal, audit, operational, causal, statistical, or general LLM behavior claims.
"""


def reconstruction_checklist() -> str:
    return """# Reconstruction Checklist

| Check | Status |
|---|---|
| Initial ER01 case state present | Pass |
| Employee action and GM decision present | Pass |
| Manager action and GM decision present | Pass |
| Finance reviewer action and GM decision present | Pass |
| Parser results and proposal attempts present for all roles | Pass |
| Generated/proposed events and metrics present | Pass |
| Claim boundary recorded | Pass |
"""


def write_role_artifact(output_dir: Path, result: RoleActionResult, suffix: str) -> None:
    action_id = result.action["action_id"]
    filename = f"{result.role}_{action_id}_{suffix}"
    write_text(output_dir / "llm_prompts" / f"{filename}.md", result.prompt_text)
    write_json(
        output_dir / "llm_outputs" / f"{filename}.json",
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


def read_expense_run_record(index: int, run_id: str, pack_dir: Path) -> ExpenseRunRecord:
    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    parsers = {role: load_json(pack_dir / "parser_results" / f"{role}.json") for role in ROLE_TURNS}
    outputs = [load_json(path) for path in sorted((pack_dir / "llm_outputs").glob("*.json"))]
    return ExpenseRunRecord(
        index=index,
        run_id=run_id,
        selected_actions={role: parsers[role]["selected_action_type"] for role in ROLE_TURNS},
        gm_decisions={role: decisions[position]["decision"] for position, role in enumerate(ROLE_TURNS)},
        attempt_counts={role: parsers[role]["attempt_count"] for role in ROLE_TURNS},
        rejected_attempt_counts={role: len(parsers[role]["invalid_or_rejected_proposals"]) for role in ROLE_TURNS},
        validation_status="pass",
        approval_evidence=approval_evidence_flags(actions, decisions),
        evidence_gap=evidence_gap_flags(actions, decisions, load_jsonl(pack_dir / "events.jsonl")),
        model_versions=sorted({output.get("response_metadata", {}).get("model_version") or output["model"] for output in outputs}),
        pack_dir=pack_dir,
    )


def copy_expense_representatives(records: list[ExpenseRunRecord], results_output: Path) -> list[dict[str, str]]:
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
        destination = results_output / evidence_rel
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(record.pack_dir, destination)
        report = validate_pack(destination)
        write_text(results_output / validation_rel, report.as_markdown())
        representatives.append(
            {
                "label": label,
                "full_path": path,
                "evidence_pack": evidence_rel.as_posix(),
                "validation_output": validation_rel.as_posix(),
            }
        )
    return representatives


def full_record_path(record: ExpenseRunRecord) -> str:
    return " -> ".join(record.selected_actions[role] for role in ROLE_TURNS)


def build_expense_execution_manifest(
    *,
    batch_id: str,
    started_at: str,
    completed_at: str,
    records: list[ExpenseRunRecord],
    exclusions: list[ExpenseExcludedRunRecord],
    providers: list[LLMProvider],
) -> dict[str, Any]:
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "scenario_id": SCENARIO_ID,
        "scenario_ref": SCENARIO_REF,
        "attempted_runs": RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": provider_label(providers),
        "model": model_label(providers),
        "observed_model_versions": sorted({version for record in records for version in record.model_versions}),
        "started_at": started_at,
        "completed_at": completed_at,
        "raw_output_policy": "raw run outputs are written under ignored runs/",
        "curated_output": RESULTS_DIR,
        "replacement_policy": "excluded runs are not replaced in EXP-0005",
        "claim_boundary": CLAIM_BOUNDARY,
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
    }


def build_expense_aggregate(
    *,
    batch_id: str,
    records: list[ExpenseRunRecord],
    exclusions: list[ExpenseExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
    providers: list[LLMProvider],
) -> dict[str, Any]:
    action_counts = {role: Counter(record.selected_actions[role] for record in records) for role in ROLE_TURNS}
    path_counts = Counter(full_record_path(record) for record in records)
    gm_counts = gm_decision_counts(records)
    exclusion_counts = Counter(exclusion.exclusion_reason for exclusion in exclusions)
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": PROTOCOL_ID,
        "protocol_ref": PROTOCOL_REF,
        "batch_id": batch_id,
        "domain": "expense-reimbursement",
        "scenario_id": SCENARIO_ID,
        "scenario_ref": SCENARIO_REF,
        "attempted_runs": RUN_COUNT,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": provider_label(providers),
        "model": model_label(providers),
        "observed_model_versions": execution_manifest["observed_model_versions"],
        "prompt_refs": {
            "employee": EMPLOYEE_PROMPT_REF,
            "manager": MANAGER_PROMPT_REF,
            "finance_reviewer": FINANCE_PROMPT_REF,
        },
        "action_menu_ids": {
            "employee": EMPLOYEE_ACTION_MENU_ID,
            "manager": MANAGER_ACTION_MENU_ID,
            "finance_reviewer": FINANCE_ACTION_MENU_ID,
        },
        "llm_controlled_roles": ROLE_TURNS,
        "game_master": "deterministic_menu_aware_rules",
        "claim_boundary": CLAIM_BOUNDARY,
        "employee_action_counts": dict(sorted(action_counts["employee"].items())),
        "manager_action_counts": dict(sorted(action_counts["manager"].items())),
        "finance_reviewer_action_counts": dict(sorted(action_counts["finance_reviewer"].items())),
        "employee_manager_finance_path_counts": dict(sorted(path_counts.items())),
        "parser_summaries_by_role": parser_summaries(records, exclusions),
        "gm_decisions_by_role_and_action": gm_counts,
        "validation_summary": {
            "pass": len(records),
            "fail": exclusion_counts.get("validation_failure", 0),
            "pass_rate_included": 1.0 if records else 0.0,
        },
        "exclusion_summary": dict(sorted(exclusion_counts.items())),
        "approval_evidence_propagation_summary": summarize_bool_flags(records, "approval_evidence"),
        "evidence_gap_summary": summarize_bool_flags(records, "evidence_gap"),
        "representative_evidence_packs": representatives,
        "limitations": expense_limitations(),
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
    }


def parser_summaries(records: list[ExpenseRunRecord], exclusions: list[ExpenseExcludedRunRecord]) -> dict[str, dict[str, int]]:
    summaries = {}
    for role in ROLE_TURNS:
        attempts = [record.attempt_counts[role] for record in records]
        rejected = [record.rejected_attempt_counts[role] for record in records]
        summaries[role] = {
            "runs_with_parser_acceptance": len(records),
            "total_attempts": sum(attempts),
            "total_retries": sum(max(attempt - 1, 0) for attempt in attempts),
            "total_rejected_or_invalid_attempts": sum(rejected),
            "runs_with_retries": sum(1 for attempt in attempts if attempt > 1),
            "parser_failures": sum(1 for exclusion in exclusions if exclusion.exclusion_reason == "parser_failure" and role in exclusion.detail),
        }
    return summaries


def gm_decision_counts(records: list[ExpenseRunRecord]) -> dict[str, Any]:
    result = {}
    for role in ROLE_TURNS:
        counts: dict[str, Counter[str]] = defaultdict(Counter)
        for record in records:
            counts[record.selected_actions[role]][record.gm_decisions[role]] += 1
        result[role] = {action: dict(sorted(decisions.items())) for action, decisions in sorted(counts.items())}
    return result


def summarize_bool_flags(records: list[ExpenseRunRecord], field: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        values = getattr(record, field)
        for key, value in values.items():
            if value:
                counts[key] += 1
    return dict(sorted(counts.items()))


def render_expense_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        lineterminator="\n",
        fieldnames=[
            "domain",
            "scenario_id",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "employee_action_counts",
            "manager_action_counts",
            "finance_reviewer_action_counts",
            "path_counts",
            "claim_boundary",
        ],
    )
    writer.writeheader()
    writer.writerow(
        {
            "domain": aggregate["domain"],
            "scenario_id": aggregate["scenario_id"],
            "attempted_runs": aggregate["attempted_runs"],
            "accepted_runs": aggregate["accepted_runs"],
            "excluded_runs": aggregate["excluded_runs"],
            "employee_action_counts": compact_counts(aggregate["employee_action_counts"]),
            "manager_action_counts": compact_counts(aggregate["manager_action_counts"]),
            "finance_reviewer_action_counts": compact_counts(aggregate["finance_reviewer_action_counts"]),
            "path_counts": compact_counts(aggregate["employee_manager_finance_path_counts"]),
            "claim_boundary": aggregate["claim_boundary"],
        }
    )
    return output.getvalue()


def render_expense_summary(aggregate: dict[str, Any]) -> str:
    path_lines = "\n".join(f"- `{path}`: {count}" for path, count in aggregate["employee_manager_finance_path_counts"].items()) or "- `none`: 0"
    reps = "\n".join(
        f"- `{item['label']}`: [{item['evidence_pack']}]({item['evidence_pack']}); validation [{item['validation_output']}]({item['validation_output']})"
        for item in aggregate["representative_evidence_packs"]
    ) or "- none"
    return f"""# EXP-0005 Expense Reimbursement Second-Domain Pilot

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

- Employee: {format_counts(aggregate['employee_action_counts'])}
- Manager: {format_counts(aggregate['manager_action_counts'])}
- Finance reviewer: {format_counts(aggregate['finance_reviewer_action_counts'])}

## Path Counts

{path_lines}

## Evidence Summaries

- Approval-evidence propagation summary: {format_counts(aggregate['approval_evidence_propagation_summary'])}
- Evidence-gap summary: {format_counts(aggregate['evidence_gap_summary'])}

## Representative Evidence

{reps}

## Claim Boundary

Under the frozen EXP-0005 artificial expense-reimbursement protocol, second-domain pilot runs produced the recorded employee, manager, and finance reviewer action paths, parser outcomes, Game Master decisions, validation outcomes, approval-evidence observations, and evidence-gap observations.

This result is bounded to `{aggregate['claim_boundary']}`. It does not support cross-domain generalization, statistical significance, causal claims, human behavior, real-world organization claims, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Limitations

{chr(10).join(f'- {item}' for item in aggregate['limitations'])}
"""


def render_expense_limitations() -> str:
    return "# EXP-0005 Limitations\n\n" + "\n".join(f"- {item}" for item in expense_limitations()) + "\n"


def render_expense_claim_boundary_review() -> str:
    return f"""# EXP-0005 Claim Boundary Review

Status: accepted
Claim boundary: `{CLAIM_BOUNDARY}`

## Accepted Claims

- EXP-0005 generated a second-domain expense-reimbursement pilot under frozen protocol conditions.
- EXP-0005 records employee, manager, and finance reviewer action paths, parser outcomes, Game Master decisions, validation outcomes, and generated/proposed evidence observations.

## Rejected Claims

- No cross-domain generalization claim.
- No statistical significance claim.
- No causal claim.
- No human behavior claim.
- No real-world organization claim.
- No compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claim.
"""


def expense_limitations() -> list[str]:
    return [
        "artificial organization only",
        "second-domain pilot only",
        "expense reimbursement ER01 only",
        "5 attempted runs before exclusions",
        "generated/proposed event labels are not human-reviewed coded evidence",
        "no cross-domain generalization claim",
        "no human behavior claim",
        "no general LLM behavior claim",
        "no real-world organization claim",
        "no compliance, legal, audit, or operational sufficiency claim",
        "no statistical significance claim",
    ]


def provider_label(providers: list[LLMProvider]) -> str:
    values = {provider.provider for provider in providers}
    return values.pop() if len(values) == 1 else "; ".join(sorted(values))


def model_label(providers: list[LLMProvider]) -> str:
    values = {provider.model for provider in providers}
    return values.pop() if len(values) == 1 else "; ".join(sorted(values))


def record_to_dict(record: ExpenseRunRecord) -> dict[str, Any]:
    return {
        "index": record.index,
        "run_id": record.run_id,
        "selected_actions": record.selected_actions,
        "gm_decisions": record.gm_decisions,
        "attempt_counts": record.attempt_counts,
        "rejected_attempt_counts": record.rejected_attempt_counts,
        "validation_status": record.validation_status,
        "approval_evidence": record.approval_evidence,
        "evidence_gap": record.evidence_gap,
        "model_versions": record.model_versions,
        "evidence_pack": record.pack_dir.as_posix(),
    }


def exclusion_to_dict(exclusion: ExpenseExcludedRunRecord) -> dict[str, Any]:
    return {
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }
