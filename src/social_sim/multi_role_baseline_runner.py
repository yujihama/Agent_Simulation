from __future__ import annotations

import csv
import io
import shutil
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import ValidationError, validate_pack

from .action_parser import ActionParseError
from .evidence_pack_writer import write_json, write_text
from .llm_actor import LLMProvider, LLMProviderError
from .m05_full_org_runner import (
    ACCOUNTANT_ACTION_MENU_ID,
    ACCOUNTANT_PROMPT_REF,
    APPROVER_ACTION_MENU_ID,
    APPROVER_PROMPT_REF,
    BUYER_ACCOUNTING_HANDOFF_MENU_ID,
    BUYER_APPROVAL_REQUEST_MENU_ID,
    BUYER_PROMPT_REF,
    REQUESTER_ACTION_MENU_ID,
    REQUESTER_PROMPT_REF,
    ROLE_TURNS,
    VENDOR_ACTION_MENU_ID,
    VENDOR_PROMPT_REF,
    M05ExcludedRunRecord,
    M05RunRecord,
    boolean_summary,
    full_record_path,
    m05_model_label,
    m05_provider_label,
    read_m05_run_record,
    write_m05_evidence_pack,
)
from .multi_role_sweep_runner import (
    SCENARIO_IDS,
    SweepExcludedRunRecord,
    SweepRunRecord,
    classify_sweep_exception,
    exclusion_to_dict,
    gm_decision_counts,
    parser_summaries,
    proposed_event_counts,
)
from .multirole_runner import compact_counts, failed_validation_markdown, format_counts, now_utc
from .repeated_runner import require_new_or_empty
from .scenario_loader import ORG_PAYMENT_SCENARIO_FILES, load_org_payment_scenario


EXPERIMENT_ID = "EXP-0002"
PROTOCOL_ID = "multi-role-baseline-v0.1"
PROTOCOL_REF = "protocols/baseline/multi-role-baseline-v0.1.md"
DEFAULT_BASELINE_BATCH_ID = "exp-0002-multi-role-baseline"
DEFAULT_COUNT_PER_SCENARIO = 5
CLAIM_BOUNDARY = "multi_role_baseline_observation_only"


def run_multi_role_baseline(
    *,
    output_root: Path,
    results_output: Path,
    provider: LLMProvider | None = None,
    requester_provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_BASELINE_BATCH_ID,
    count_per_scenario: int = DEFAULT_COUNT_PER_SCENARIO,
) -> Path:
    requester_provider = requester_provider or provider
    vendor_provider = vendor_provider or provider
    buyer_provider = buyer_provider or provider
    approver_provider = approver_provider or provider
    accountant_provider = accountant_provider or provider
    if any(item is None for item in [requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider]):
        raise ValueError("provider or all requester/vendor/buyer/approver/accountant providers are required")
    if count_per_scenario <= 0:
        raise ValueError("count_per_scenario must be positive")

    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(results_output, "results_output")
    output_root.mkdir(parents=True, exist_ok=True)
    results_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    records: list[SweepRunRecord] = []
    exclusions: list[SweepExcludedRunRecord] = []
    for scenario_id in SCENARIO_IDS:
        for index in range(1, count_per_scenario + 1):
            run_id = f"{batch_id}-{scenario_id.lower()}-run-{index:03d}"
            run_root = output_root / scenario_id.lower() / f"run-{index:03d}"
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
                    scenario_id=scenario_id,
                    claim_boundary=CLAIM_BOUNDARY,
                    protocol_ref=PROTOCOL_REF,
                    scenario_status="generated_exp_0002_multi_role_baseline_reference",
                    scenario_step="EXP-0002 multi-role controlled baseline execution",
                    run_label="EXP-0002 multi-role baseline",
                    runner_label="EXP-0002 multi-role baseline runner",
                    scope_limit="multi-role baseline observation only; no statistical, causal, human, or real-world claim",
                )
                report = validate_pack(pack_dir)
                write_text(run_root / "validation-output.md", report.as_markdown())
                records.append(SweepRunRecord(scenario_id, read_m05_run_record(index=index, run_id=run_id, pack_dir=pack_dir)))
            except ValidationError as exc:
                write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
                exclusions.append(SweepExcludedRunRecord(scenario_id, M05ExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc))))
            except Exception as exc:
                exclusions.append(SweepExcludedRunRecord(scenario_id, M05ExcludedRunRecord(index, run_id, classify_baseline_exception(exc), "generation", str(exc))))

    completed_at = now_utc()
    representatives = copy_baseline_representatives(records=records, results_output=results_output)
    execution_manifest = build_baseline_execution_manifest(
        requester_provider=requester_provider,
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        count_per_scenario=count_per_scenario,
        started_at=started_at,
        completed_at=completed_at,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_baseline_aggregate(
        requester_provider=requester_provider,
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        count_per_scenario=count_per_scenario,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
    )
    write_json(results_output / "execution-manifest.json", execution_manifest)
    write_json(results_output / "aggregate.json", aggregate)
    write_text(results_output / "scenario-summary.csv", render_baseline_scenario_summary_csv(aggregate))
    write_text(results_output / "summary.md", render_baseline_summary(aggregate))
    return results_output


def copy_baseline_representatives(records: list[SweepRunRecord], results_output: Path) -> list[dict[str, str]]:
    representatives: list[dict[str, str]] = []
    selected: dict[tuple[str, str], SweepRunRecord] = {}
    for record in records:
        scenario_id = record.scenario_id
        path = full_record_path(record.inner)
        selected.setdefault((scenario_id, "__first__"), record)
        selected.setdefault((scenario_id, path), record)

    ordered_keys = sorted(selected.keys(), key=lambda item: (SCENARIO_IDS.index(item[0]), 0 if item[1] == "__first__" else 1, item[1]))
    seen_records: set[tuple[str, int]] = set()
    per_scenario_counts: Counter[str] = Counter()
    for scenario_id, _path_key in ordered_keys:
        record = selected[(scenario_id, _path_key)]
        record_key = (record.scenario_id, record.inner.index)
        if record_key in seen_records:
            continue
        seen_records.add(record_key)
        per_scenario_counts[scenario_id] += 1
        label = f"{scenario_id.lower()}-path-{per_scenario_counts[scenario_id]:03d}"
        evidence_rel = Path("representative-evidence-packs") / scenario_id.lower() / label
        validation_rel = Path("representative-validation-outputs") / scenario_id.lower() / f"{label}.md"
        destination = results_output / evidence_rel
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(record.inner.pack_dir, destination)
        report = validate_pack(destination)
        write_text(results_output / validation_rel, report.as_markdown())
        representatives.append(
            {
                "scenario_id": scenario_id,
                "label": label,
                "run_id": record.inner.run_id,
                "full_path": full_record_path(record.inner),
                "evidence_pack": evidence_rel.as_posix(),
                "validation_output": validation_rel.as_posix(),
            }
        )
    return representatives


def build_baseline_execution_manifest(
    *,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    count_per_scenario: int,
    started_at: str,
    completed_at: str,
    records: list[SweepRunRecord],
    exclusions: list[SweepExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": PROTOCOL_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_set": SCENARIO_IDS,
        "runs_per_scenario": count_per_scenario,
        "total_planned_attempted_runs": count_per_scenario * len(SCENARIO_IDS),
        "started_at": started_at,
        "completed_at": completed_at,
        "attempted_runs": count_per_scenario * len(SCENARIO_IDS),
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "provider": m05_provider_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "model": m05_model_label(requester_provider, vendor_provider, buyer_provider, approver_provider, accountant_provider),
        "observed_model_versions": sorted({version for record in records for version in record.inner.model_versions}),
        "replacement_policy": "excluded runs are not replaced in EXP-0002 unless a later protocol revision freezes a replacement policy",
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_baseline_aggregate(
    *,
    requester_provider: LLMProvider,
    vendor_provider: LLMProvider,
    buyer_provider: LLMProvider,
    approver_provider: LLMProvider,
    accountant_provider: LLMProvider,
    batch_id: str,
    count_per_scenario: int,
    records: list[SweepRunRecord],
    exclusions: list[SweepExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
) -> dict[str, Any]:
    by_scenario = {scenario_id: [record for record in records if record.scenario_id == scenario_id] for scenario_id in SCENARIO_IDS}
    exclusions_by_scenario = {scenario_id: [exclusion for exclusion in exclusions if exclusion.scenario_id == scenario_id] for scenario_id in SCENARIO_IDS}
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": PROTOCOL_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "scenario_set": SCENARIO_IDS,
        "runs_per_scenario": count_per_scenario,
        "attempted_runs": count_per_scenario * len(SCENARIO_IDS),
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
        "claim_boundary": CLAIM_BOUNDARY,
        "scenarios": {
            scenario_id: baseline_scenario_aggregate(
                scenario_id=scenario_id,
                records=by_scenario[scenario_id],
                exclusions=exclusions_by_scenario[scenario_id],
                attempted_runs=count_per_scenario,
            )
            for scenario_id in SCENARIO_IDS
        },
        "validation_summary": {
            "pass": len(records),
            "fail": len(exclusions),
            "pass_rate_included": 1.0 if records else 0.0,
        },
        "exclusions_by_reason": dict(sorted(Counter(exclusion.inner.exclusion_reason for exclusion in exclusions).items())),
        "representative_evidence_packs": representatives,
        "execution_manifest": "execution-manifest.json",
        "limitations": [
            "multi-role baseline observation only",
            "S01-S06 only",
            f"{count_per_scenario} attempted runs per scenario before exclusions",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical significance, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claim",
        ],
    }


def baseline_scenario_aggregate(
    *,
    scenario_id: str,
    records: list[SweepRunRecord],
    exclusions: list[SweepExcludedRunRecord],
    attempted_runs: int,
) -> dict[str, Any]:
    scenario = load_org_payment_scenario(scenario_id)
    manipulated = scenario.get("manipulated_variables", {})
    selected_counts = {role: Counter(record.inner.selected_actions[role] for record in records) for role in ROLE_TURNS}
    return {
        "scenario_id": scenario_id,
        "scenario_ref": f"scenarios/org-payment/{ORG_PAYMENT_SCENARIO_FILES[scenario_id]}",
        "scenario_name": scenario.get("name"),
        "policy_ambiguity": manipulated.get("policy_ambiguity"),
        "deadline_pressure": manipulated.get("deadline_pressure"),
        "role_overlap": manipulated.get("role_overlap"),
        "audit_presence": manipulated.get("audit_presence"),
        "control_mode": scenario.get("control_mode"),
        "attempted_runs": attempted_runs,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "requester_action_counts": dict(sorted(selected_counts["requester"].items())),
        "vendor_action_counts": dict(sorted(selected_counts["vendor"].items())),
        "buyer_approval_request_action_counts": dict(sorted(selected_counts["buyer_approval_request"].items())),
        "approver_action_counts": dict(sorted(selected_counts["approver"].items())),
        "buyer_accounting_handoff_action_counts": dict(sorted(selected_counts["buyer_accounting_handoff"].items())),
        "accountant_action_counts": dict(sorted(selected_counts["accountant"].items())),
        "full_org_payment_path_counts": dict(sorted(Counter(full_record_path(record.inner) for record in records).items())),
        "parser_summaries_by_role_turn": parser_summaries(records, exclusions),
        "gm_decisions_by_role_turn_and_action": gm_decision_counts(records),
        "validation_summary": {"pass": len(records), "fail": len(exclusions), "pass_rate_included": 1.0 if records else 0.0},
        "exclusions_by_reason": dict(sorted(Counter(exclusion.inner.exclusion_reason for exclusion in exclusions).items())),
        "proposed_event_counts": proposed_event_counts(records),
        "requester_framing_summary": boolean_summary(record.inner.requester_framing for record in records),
        "pressure_citation_summary": boolean_summary(record.inner.pressure_citation for record in records),
        "approval_evidence_propagation_summary": boolean_summary(record.inner.approval_evidence_propagation for record in records),
        "coordination_gap_summary": boolean_summary(record.inner.coordination_gap for record in records),
    }


def render_baseline_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        lineterminator="\n",
        fieldnames=[
            "scenario_id",
            "policy_ambiguity",
            "deadline_pressure",
            "role_overlap",
            "audit_presence",
            "control_mode",
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
    for scenario_id in SCENARIO_IDS:
        item = aggregate["scenarios"][scenario_id]
        writer.writerow(
            {
                "scenario_id": scenario_id,
                "policy_ambiguity": item["policy_ambiguity"],
                "deadline_pressure": item["deadline_pressure"],
                "role_overlap": item["role_overlap"],
                "audit_presence": item["audit_presence"],
                "control_mode": item["control_mode"],
                "attempted_runs": item["attempted_runs"],
                "accepted_runs": item["accepted_runs"],
                "excluded_runs": item["excluded_runs"],
                "requester_action_counts": compact_counts(item["requester_action_counts"]),
                "vendor_action_counts": compact_counts(item["vendor_action_counts"]),
                "buyer_approval_request_action_counts": compact_counts(item["buyer_approval_request_action_counts"]),
                "approver_action_counts": compact_counts(item["approver_action_counts"]),
                "buyer_accounting_handoff_action_counts": compact_counts(item["buyer_accounting_handoff_action_counts"]),
                "accountant_action_counts": compact_counts(item["accountant_action_counts"]),
                "full_org_payment_path_counts": compact_counts(item["full_org_payment_path_counts"]),
                "claim_boundary": aggregate["claim_boundary"],
            }
        )
    return output.getvalue()


def render_baseline_summary(aggregate: dict[str, Any]) -> str:
    scenario_lines = []
    for scenario_id in SCENARIO_IDS:
        item = aggregate["scenarios"][scenario_id]
        paths = "; ".join(f"`{path}`: {count}" for path, count in item["full_org_payment_path_counts"].items()) or "`none`: 0"
        scenario_lines.append(
            f"| `{scenario_id}` | `{item['policy_ambiguity']}` | `{item['deadline_pressure']}` | `{item['role_overlap']}` | `{item['audit_presence']}` | `{item['control_mode']}` | {item['attempted_runs']} | {item['accepted_runs']} | {item['excluded_runs']} | {paths} |"
        )
    representative_lines = "\n".join(
        f"- `{item['scenario_id']}` {item['label']}: [{item['evidence_pack']}]({item['evidence_pack']}) / [{item['validation_output']}]({item['validation_output']})"
        for item in aggregate["representative_evidence_packs"]
    ) or "- none"
    return f"""# EXP-0002 Multi-Role Baseline Summary

Protocol reference: `{aggregate['protocol_ref']}`
Scenario set: `{', '.join(aggregate['scenario_set'])}`
Claim boundary: `{aggregate['claim_boundary']}`

## Execution Accounting

| Field | Value |
|---|---:|
| Attempted runs | {aggregate['attempted_runs']} |
| Accepted runs | {aggregate['accepted_runs']} |
| Excluded runs | {aggregate['excluded_runs']} |

Provider/model: `{aggregate['provider']}` / `{aggregate['model']}`
Observed model versions: {', '.join(f'`{value}`' for value in aggregate['observed_model_versions']) or '`not returned`'}

## Scenario Path Summary

| Scenario | Policy ambiguity | Deadline pressure | Role overlap | Audit presence | Control mode | Attempted | Accepted | Excluded | Full org-payment paths |
|---|---|---|---|---|---|---:|---:|---:|---|
{chr(10).join(scenario_lines)}

## Descriptive Summaries

This report provides denominator-explicit descriptive counts only. It does not include inferential statistical tests.

Representative scenario-level action, parser, Game Master, proposed event, requester-framing, pressure-citation, approval-evidence, and coordination-gap summaries are recorded in `aggregate.json` and `scenario-summary.csv`.

## Representative Evidence

{representative_lines}

## Claim Boundary

Under the frozen EXP-0002 artificial organization protocol, multi-role LLM runs produced the recorded full org-payment action paths, parser outcomes, Game Master decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

This result is bounded to `multi_role_baseline_observation_only`. It does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical significance, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.

## Limitations

{chr(10).join(f'- {item}' for item in aggregate['limitations'])}
"""


def classify_baseline_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_failure"
    return classify_sweep_exception(exc)
