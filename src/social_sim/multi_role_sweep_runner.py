from __future__ import annotations

import csv
import io
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
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
    ROLE_TURNS,
    REQUESTER_ACTION_MENU_ID,
    VENDOR_PROMPT_REF,
    VENDOR_ACTION_MENU_ID,
    M05ExcludedRunRecord,
    M05RunRecord,
    boolean_summary,
    full_record_path,
    m05_model_label,
    m05_provider_label,
    read_m05_run_record,
    write_m05_evidence_pack,
)
from .multirole_runner import classify_exception, compact_counts, failed_validation_markdown, format_counts, load_jsonl, now_utc
from .repeated_runner import require_new_or_empty
from .scenario_loader import ORG_PAYMENT_SCENARIO_FILES


SWEEP_ID = "MSP-0001"
PROTOCOL_ID = "multi-role-scenario-sweep-pilot-v0.1"
PROTOCOL_REF = "protocols/multi-role/multi-role-scenario-sweep-pilot-v0.1.md"
DEFAULT_SWEEP_BATCH_ID = "multi-role-scenario-sweep-pilot-0001"
DEFAULT_COUNT_PER_SCENARIO = 3
CLAIM_BOUNDARY = "multi_role_scenario_sweep_pilot_observation_only"
SCENARIO_IDS = ["S01", "S02", "S03", "S04", "S05", "S06"]


@dataclass(frozen=True)
class SweepRunRecord:
    scenario_id: str
    inner: M05RunRecord


@dataclass(frozen=True)
class SweepExcludedRunRecord:
    scenario_id: str
    inner: M05ExcludedRunRecord


def run_multi_role_scenario_sweep_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    requester_provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_SWEEP_BATCH_ID,
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
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

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
                    scenario_status="generated_multi_role_scenario_sweep_pilot_reference",
                    scenario_step="S01-S06 full org-payment multi-role scenario sweep pilot execution",
                    run_label="multi-role scenario sweep pilot",
                    runner_label="multi-role scenario sweep runner",
                    scope_limit="scenario sweep pilot only; not a multi-role baseline",
                )
                report = validate_pack(pack_dir)
                write_text(run_root / "validation-output.md", report.as_markdown())
                records.append(SweepRunRecord(scenario_id, read_m05_run_record(index=index, run_id=run_id, pack_dir=pack_dir)))
            except ValidationError as exc:
                write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
                exclusions.append(SweepExcludedRunRecord(scenario_id, M05ExcludedRunRecord(index, run_id, "validation_failure", "validation", str(exc))))
            except Exception as exc:
                exclusions.append(SweepExcludedRunRecord(scenario_id, M05ExcludedRunRecord(index, run_id, classify_sweep_exception(exc), "generation", str(exc))))

    completed_at = now_utc()
    representatives = copy_sweep_representatives(records=records, curated_output=curated_output)
    execution_manifest = build_sweep_execution_manifest(
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
    aggregate = build_sweep_aggregate(
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
    write_json(curated_output / "execution-manifest.json", execution_manifest)
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "scenario-summary.csv", render_sweep_scenario_summary_csv(aggregate))
    write_text(curated_output / "summary.md", render_sweep_summary(aggregate))
    return curated_output


def copy_sweep_representatives(records: list[SweepRunRecord], curated_output: Path) -> list[dict[str, str]]:
    representatives: list[dict[str, str]] = []
    selected: dict[str, SweepRunRecord] = {}
    for record in records:
        selected.setdefault(record.scenario_id, record)
    for scenario_id in SCENARIO_IDS:
        record = selected.get(scenario_id)
        if record is None:
            continue
        label = f"{scenario_id.lower()}-run-{record.inner.index:03d}"
        evidence_rel = Path("representative-evidence-packs") / scenario_id.lower() / label
        validation_rel = Path("representative-validation-outputs") / scenario_id.lower() / f"{label}.md"
        destination = curated_output / evidence_rel
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(record.inner.pack_dir, destination)
        report = validate_pack(destination)
        write_text(curated_output / validation_rel, report.as_markdown())
        representatives.append(
            {
                "scenario_id": scenario_id,
                "label": label,
                "full_path": full_record_path(record.inner),
                "evidence_pack": evidence_rel.as_posix(),
                "validation_output": validation_rel.as_posix(),
            }
        )
    return representatives


def build_sweep_execution_manifest(
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
        "sweep_id": SWEEP_ID,
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
        "replacement_policy": "excluded runs are not replaced in the multi-role scenario sweep",
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "claim_boundary": CLAIM_BOUNDARY,
    }


def build_sweep_aggregate(
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
        "sweep_id": SWEEP_ID,
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
            "requester": "prompts/org-payment/requester-free-choice-action-v0.1.md",
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
            scenario_id: scenario_aggregate(
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
            "scenario sweep pilot only; not a multi-role baseline",
            "S01-S06 only",
            f"{count_per_scenario} attempted runs per scenario before exclusions",
            "deterministic/rule-based Game Master",
            "generated/proposed event labels are not human-reviewed coded evidence",
            "no scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claim",
        ],
    }


def scenario_aggregate(
    *,
    scenario_id: str,
    records: list[SweepRunRecord],
    exclusions: list[SweepExcludedRunRecord],
    attempted_runs: int,
) -> dict[str, Any]:
    selected_counts = {role: Counter(record.inner.selected_actions[role] for record in records) for role in ROLE_TURNS}
    return {
        "scenario_id": scenario_id,
        "scenario_ref": f"scenarios/org-payment/{ORG_PAYMENT_SCENARIO_FILES[scenario_id]}",
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


def parser_summaries(records: list[SweepRunRecord], exclusions: list[SweepExcludedRunRecord]) -> dict[str, dict[str, int]]:
    summaries: dict[str, dict[str, int]] = {}
    for role in ROLE_TURNS:
        summaries[role] = {
            "accepted_actions": len(records),
            "total_attempts": sum(record.inner.attempt_counts[role] for record in records),
            "total_retries": sum(max(0, record.inner.attempt_counts[role] - 1) for record in records),
            "rejected_or_invalid_proposals": sum(record.inner.rejected_attempt_counts[role] for record in records),
            "parser_failures": sum(1 for exclusion in exclusions if exclusion.inner.exclusion_reason == "parser_failure" and role in exclusion.inner.detail),
        }
    return summaries


def gm_decision_counts(records: list[SweepRunRecord]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for role in ROLE_TURNS:
        counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for record in records:
            counts[record.inner.selected_actions[role]][record.inner.gm_decisions[role]] += 1
        result[role] = {action: dict(sorted(decisions.items())) for action, decisions in sorted(counts.items())}
    return result


def proposed_event_counts(records: list[SweepRunRecord]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for record in records:
        for event in load_jsonl(record.inner.pack_dir / "events.jsonl"):
            if event.get("review_status") == "proposed":
                counts[event.get("event_type", "unknown")] += 1
    return dict(sorted(counts.items()))


def render_sweep_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
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
    for scenario_id in SCENARIO_IDS:
        item = aggregate["scenarios"][scenario_id]
        writer.writerow(
            {
                "scenario_id": scenario_id,
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


def render_sweep_summary(aggregate: dict[str, Any]) -> str:
    scenario_lines = []
    for scenario_id in SCENARIO_IDS:
        item = aggregate["scenarios"][scenario_id]
        paths = "; ".join(f"`{path}`: {count}" for path, count in item["full_org_payment_path_counts"].items()) or "`none`: 0"
        scenario_lines.append(
            f"| `{scenario_id}` | {item['attempted_runs']} | {item['accepted_runs']} | {item['excluded_runs']} | {paths} |"
        )
    representative_lines = "\n".join(
        f"- `{item['scenario_id']}` {item['label']}: [{item['evidence_pack']}]({item['evidence_pack']}) / [{item['validation_output']}]({item['validation_output']})"
        for item in aggregate["representative_evidence_packs"]
    ) or "- none"
    return f"""# Multi-Role Scenario Sweep Pilot Summary

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

| Scenario | Attempted | Accepted | Excluded | Full org-payment paths |
|---|---:|---:|---:|---|
{chr(10).join(scenario_lines)}

## Representative Evidence

{representative_lines}

## Claim Boundary

Under the frozen multi-role scenario sweep pilot protocol, requester+vendor+buyer+approver+accountant LLM pilot runs produced recorded full org-payment paths, parser outcomes, GM decisions, validation outcomes, proposed event observations, requester-framing observations, pressure-citation observations, approval-evidence propagation observations, and coordination-gap observations across S01-S06.

This is a scenario sweep pilot, not a multi-role baseline. It does not support scenario-causation, requester-framing causation, pressure-causation, pressure-propagation proof, responsibility-diffusion, approval-bypass, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model comparison, or general LLM behavior claims.
"""


def exclusion_to_dict(exclusion: SweepExcludedRunRecord) -> dict[str, Any]:
    return {
        "scenario_id": exclusion.scenario_id,
        "index": exclusion.inner.index,
        "run_id": exclusion.inner.run_id,
        "exclusion_reason": exclusion.inner.exclusion_reason,
        "stage": exclusion.inner.stage,
        "detail": exclusion.inner.detail,
    }


def classify_sweep_exception(exc: Exception) -> str:
    if isinstance(exc, ActionParseError):
        return "parser_failure"
    if isinstance(exc, LLMProviderError):
        return "provider_failure"
    return classify_exception(exc)
