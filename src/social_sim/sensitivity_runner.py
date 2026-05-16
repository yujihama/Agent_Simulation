from __future__ import annotations

import csv
import io
import json
import shutil
from pathlib import Path
from typing import Any

from .evidence_pack_writer import write_json, write_text
from .llm_actor import LLMProvider
from .multi_role_baseline_runner import run_multi_role_baseline
from .multi_role_sweep_runner import SCENARIO_IDS
from .multirole_runner import compact_counts, load_json


EXPERIMENT_ID = "EXP-0004"
PROTOCOL_ID = "exp-0004-provider-randomness-sensitivity-v0.1"
PROTOCOL_REF = "protocols/evaluation/exp-0004-provider-randomness-sensitivity-v0.1.md"
DEFAULT_BATCH_ID = "exp-0004-provider-randomness-sensitivity-0001"
DEFAULT_COUNT_PER_SCENARIO = 2
CLAIM_BOUNDARY = "provider_randomness_sensitivity_observation_only"
BASELINE_AGGREGATE_REF = "results/org-payment/exp-0002-multi-role-baseline/aggregate.json"
PRESSURE_CORRECTION_REF = "protocols/evaluation/pressure-citation-metric-correction-v0.1.md"
MAX_COMMITTED_REPRESENTATIVE_PACKS = 2


def run_provider_randomness_sensitivity(
    *,
    output_root: Path,
    results_output: Path,
    provider: LLMProvider | None = None,
    requester_provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    batch_id: str = DEFAULT_BATCH_ID,
    count_per_scenario: int = DEFAULT_COUNT_PER_SCENARIO,
    baseline_aggregate_path: Path = Path(BASELINE_AGGREGATE_REF),
) -> Path:
    run_multi_role_baseline(
        output_root=output_root,
        results_output=results_output,
        provider=provider,
        requester_provider=requester_provider,
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        batch_id=batch_id,
        count_per_scenario=count_per_scenario,
        experiment_id=EXPERIMENT_ID,
        protocol_id=PROTOCOL_ID,
        protocol_ref=PROTOCOL_REF,
        claim_boundary=CLAIM_BOUNDARY,
        scenario_status="generated_exp_0004_provider_randomness_sensitivity_reference",
        scenario_step="EXP-0004 provider-randomness sensitivity execution",
        run_label="EXP-0004 provider-randomness sensitivity",
        runner_label="EXP-0004 provider-randomness sensitivity runner",
        scope_limit="provider-randomness sensitivity observation only; no model, prompt, menu, GM, scenario, statistical, causal, human, or real-world claim",
        replacement_policy="excluded runs are not replaced in EXP-0004",
    )
    augment_sensitivity_results(
        results_output=results_output,
        baseline_aggregate_path=baseline_aggregate_path,
    )
    return results_output


def augment_sensitivity_results(*, results_output: Path, baseline_aggregate_path: Path) -> None:
    aggregate_path = results_output / "aggregate.json"
    aggregate = load_json(aggregate_path)
    baseline = load_json(baseline_aggregate_path)
    comparison = build_comparison(aggregate, baseline)
    aggregate["representative_evidence_packs"] = prune_sensitivity_representatives(
        results_output=results_output,
        representatives=aggregate.get("representative_evidence_packs", []),
        comparison=comparison,
    )
    aggregate["baseline_comparator_ref"] = BASELINE_AGGREGATE_REF
    aggregate["sensitivity_axis"] = "provider_randomness_repeat_run_stability"
    aggregate["pressure_citation_correction_ref"] = PRESSURE_CORRECTION_REF
    aggregate["comparison_to_exp_0002"] = comparison
    aggregate["limitations"] = sensitivity_limitations(aggregate)
    write_json(aggregate_path, aggregate)
    write_text(results_output / "comparison-table.csv", render_comparison_csv(comparison))
    write_text(results_output / "limitations.md", render_limitations())
    write_text(results_output / "claim-boundary-review.md", render_claim_boundary_review())
    write_text(results_output / "summary.md", render_summary(aggregate))


def build_comparison(aggregate: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    scenario_comparisons = {}
    for scenario_id in SCENARIO_IDS:
        current = aggregate["scenarios"][scenario_id]
        base = baseline["scenarios"][scenario_id]
        current_paths = current.get("full_org_payment_path_counts", {})
        baseline_paths = base.get("full_org_payment_path_counts", {})
        scenario_comparisons[scenario_id] = {
            "baseline_accepted_runs": base["accepted_runs"],
            "sensitivity_accepted_runs": current["accepted_runs"],
            "baseline_full_org_payment_path_counts": baseline_paths,
            "sensitivity_full_org_payment_path_counts": current_paths,
            "overlapping_paths": sorted(set(current_paths) & set(baseline_paths)),
            "new_paths_in_sensitivity": sorted(set(current_paths) - set(baseline_paths)),
            "baseline_paths_not_observed_in_sensitivity": sorted(set(baseline_paths) - set(current_paths)),
            "baseline_coordination_gap_summary": base.get("coordination_gap_summary", {}),
            "sensitivity_coordination_gap_summary": current.get("coordination_gap_summary", {}),
            "baseline_event_counts": base.get("proposed_event_counts", {}),
            "sensitivity_event_counts": current.get("proposed_event_counts", {}),
            "descriptive_status": scenario_status(current_paths, baseline_paths),
        }
    return {
        "comparison_type": "descriptive_small_n_repeat_run",
        "baseline_experiment_id": baseline["experiment_id"],
        "sensitivity_experiment_id": aggregate["experiment_id"],
        "baseline_runs_per_scenario": baseline["runs_per_scenario"],
        "sensitivity_runs_per_scenario": aggregate["runs_per_scenario"],
        "scenario_comparisons": scenario_comparisons,
        "claim_status": "descriptive_only_no_statistical_or_generalization_claim",
    }


def prune_sensitivity_representatives(
    *,
    results_output: Path,
    representatives: list[dict[str, str]],
    comparison: dict[str, Any],
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    selected_keys: set[str] = set()

    def add_candidate(item: dict[str, str]) -> None:
        if len(selected) >= MAX_COMMITTED_REPRESENTATIVE_PACKS:
            return
        key = item["evidence_pack"]
        if key in selected_keys:
            return
        selected.append(item)
        selected_keys.add(key)

    by_scenario: dict[str, list[dict[str, str]]] = {scenario_id: [] for scenario_id in SCENARIO_IDS}
    for item in representatives:
        by_scenario.setdefault(item["scenario_id"], []).append(item)

    for scenario_id in SCENARIO_IDS:
        scenario_comparison = comparison["scenario_comparisons"][scenario_id]
        new_paths = set(scenario_comparison["new_paths_in_sensitivity"])
        for item in by_scenario.get(scenario_id, []):
            if item["full_path"] in new_paths:
                add_candidate(item)

    for scenario_id in SCENARIO_IDS:
        for item in by_scenario.get(scenario_id, []):
            add_candidate(item)

    kept = set()
    for item in selected:
        kept.add(item["evidence_pack"])
        kept.add(item["validation_output"])

    for item in representatives:
        for key in ("evidence_pack", "validation_output"):
            relative_path = item[key]
            if relative_path in kept:
                continue
            path = results_output / relative_path
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()

    remove_empty_directories(results_output / "representative-evidence-packs")
    remove_empty_directories(results_output / "representative-validation-outputs")
    return selected


def remove_empty_directories(path: Path) -> None:
    if not path.exists():
        return
    for child in sorted((item for item in path.rglob("*") if item.is_dir()), key=lambda item: len(item.parts), reverse=True):
        try:
            child.rmdir()
        except OSError:
            pass


def scenario_status(current_paths: dict[str, int], baseline_paths: dict[str, int]) -> str:
    current_set = set(current_paths)
    baseline_set = set(baseline_paths)
    if current_set == baseline_set:
        return "same_path_set_observed"
    if current_set <= baseline_set:
        return "subset_of_baseline_paths_observed"
    if current_set & baseline_set:
        return "overlap_with_new_sensitivity_path"
    return "different_path_set_observed"


def render_comparison_csv(comparison: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        lineterminator="\n",
        fieldnames=[
            "scenario_id",
            "baseline_accepted_runs",
            "sensitivity_accepted_runs",
            "baseline_paths",
            "sensitivity_paths",
            "overlapping_paths",
            "new_paths_in_sensitivity",
            "baseline_paths_not_observed_in_sensitivity",
            "descriptive_status",
        ],
    )
    writer.writeheader()
    for scenario_id in SCENARIO_IDS:
        item = comparison["scenario_comparisons"][scenario_id]
        writer.writerow(
            {
                "scenario_id": scenario_id,
                "baseline_accepted_runs": item["baseline_accepted_runs"],
                "sensitivity_accepted_runs": item["sensitivity_accepted_runs"],
                "baseline_paths": compact_counts(item["baseline_full_org_payment_path_counts"]),
                "sensitivity_paths": compact_counts(item["sensitivity_full_org_payment_path_counts"]),
                "overlapping_paths": "; ".join(item["overlapping_paths"]) or "none",
                "new_paths_in_sensitivity": "; ".join(item["new_paths_in_sensitivity"]) or "none",
                "baseline_paths_not_observed_in_sensitivity": "; ".join(item["baseline_paths_not_observed_in_sensitivity"]) or "none",
                "descriptive_status": item["descriptive_status"],
            }
        )
    return output.getvalue()


def render_summary(aggregate: dict[str, Any]) -> str:
    comparison = aggregate["comparison_to_exp_0002"]
    rows = []
    for scenario_id in SCENARIO_IDS:
        item = comparison["scenario_comparisons"][scenario_id]
        rows.append(
            f"| `{scenario_id}` | {item['baseline_accepted_runs']} | {item['sensitivity_accepted_runs']} | `{item['descriptive_status']}` | `{'; '.join(item['new_paths_in_sensitivity']) or 'none'}` |"
        )
    return f"""# EXP-0004 Provider-Randomness Sensitivity Summary

Protocol reference: `{aggregate['protocol_ref']}`
Baseline comparator: `{BASELINE_AGGREGATE_REF}`
Claim boundary: `{aggregate['claim_boundary']}`

## Execution Accounting

| Field | Value |
|---|---:|
| Attempted runs | {aggregate['attempted_runs']} |
| Accepted runs | {aggregate['accepted_runs']} |
| Excluded runs | {aggregate['excluded_runs']} |

Provider/model: `{aggregate['provider']}` / `{aggregate['model']}`
Observed model versions: {', '.join(f'`{value}`' for value in aggregate['observed_model_versions']) or '`not returned`'}

## EXP-0002 Comparison

| Scenario | EXP-0002 accepted | EXP-0004 accepted | Descriptive status | New paths in EXP-0004 |
|---|---:|---:|---|---|
{chr(10).join(rows)}

Detailed path counts are recorded in `aggregate.json` and `comparison-table.csv`.
Committed full representative evidence packs are limited to {MAX_COMMITTED_REPRESENTATIVE_PACKS} selected packs so this execution PR remains reviewable. The aggregate and execution manifest still account for all attempted and accepted runs.

## Claim Boundary

EXP-0004 is a small provider-randomness repeat-run sensitivity check. It keeps model, prompts, action menus, scenarios, parser rules, metrics, and deterministic Game Master behavior fixed. It does not support model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, scenario wording comparison, statistical significance, causal claims, human behavior claims, real-world organization claims, compliance, legal, audit, operational sufficiency claims, or general LLM behavior claims.

## Limitations

{chr(10).join(f'- {item}' for item in aggregate['limitations'])}
"""


def sensitivity_limitations(aggregate: dict[str, Any]) -> list[str]:
    return [
        "provider-randomness sensitivity observation only",
        "2 attempted runs per scenario before exclusions",
        "small-n descriptive comparison against EXP-0002 only",
        f"committed full representative evidence packs are capped at {MAX_COMMITTED_REPRESENTATIVE_PACKS} selected packs to keep the execution PR reviewable",
        "model, prompts, action menus, scenario wording, parser rules, metrics, and Game Master behavior are held fixed",
        "provider default randomness is not explicitly seeded or controlled",
        "no statistical significance claim",
        "no causal claim",
        "no model comparison claim",
        "no prompt sensitivity claim",
        "no action-menu sensitivity claim",
        "no Game Master strictness sensitivity claim",
        "no scenario wording sensitivity claim",
        "no human behavior or real-world organization claim",
    ]


def render_limitations() -> str:
    return """# EXP-0004 Limitations

- EXP-0004 isolates provider-randomness repeat-run stability only.
- It uses 2 attempted runs per scenario and compares descriptively against EXP-0002's 5 runs per scenario.
- Committed full representative evidence packs are capped at 2 selected packs so the execution PR remains reviewable.
- The provider default randomness is not explicitly seeded or controlled.
- Model, prompts, action menus, scenario wording, parser rules, metrics, and Game Master behavior are held fixed.
- Any new or missing path is a small-sample sensitivity observation, not a statistical result.
- No model comparison, prompt comparison, action-menu comparison, Game Master strictness comparison, scenario wording comparison, causal, statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, or general LLM behavior claim is supported.
"""


def render_claim_boundary_review() -> str:
    return """# EXP-0004 Claim Boundary Review

Status: accepted

## Accepted Claims

- EXP-0004 generated a small provider-randomness repeat-run set under frozen EXP-0004 conditions.
- EXP-0004 compares fresh run paths descriptively with EXP-0002.
- EXP-0004 records run-to-run stability or variation under unchanged model, prompt, menu, scenario, parser, metric, and Game Master conditions.

## Rejected Claims

- No model comparison claim.
- No prompt comparison claim.
- No action-menu comparison claim.
- No Game Master strictness comparison claim.
- No scenario wording comparison claim.
- No statistical significance claim.
- No causal claim.
- No human behavior claim.
- No real-world organization claim.
- No compliance, legal, audit, operational sufficiency, or general LLM behavior claim.
"""
