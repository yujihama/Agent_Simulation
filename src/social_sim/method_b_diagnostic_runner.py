from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .evidence_pack_writer import write_json, write_text
from .llm_actor import LLMProvider
from .method_b_targeted_runner import (
    DEFAULT_COUNT_PER_SCENARIO,
    DEFAULT_SCENARIO_IDS,
    render_summary,
    run_targeted_failure_mode_pilot,
)


PILOT_ID = "METHOD-B-DSP-0001"
PROTOCOL_REF = "protocols/failure-modes/failure-mode-diagnostic-sensitivity-v0.1.md"
DEFAULT_BATCH_ID = "method-b-diagnostic-sensitivity-pilot-0001"
CLAIM_BOUNDARY = "method_b_diagnostic_sensitivity_observation_only"
ROLE_PROMPT_ADDENDUM_REF = "prompts/org-payment/method-b-diagnostic-role-local-framing-addendum-v0.1.md"
REFERENCE_AGGREGATE_REF = "pilot-runs/org-payment/method-b-targeted-failure-mode-pilot-0001/aggregate.json"
ROOT = Path(__file__).resolve().parents[2]


def run_method_b_diagnostic_sensitivity_pilot(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider | None = None,
    requester_provider: LLMProvider | None = None,
    vendor_provider: LLMProvider | None = None,
    buyer_provider: LLMProvider | None = None,
    approver_provider: LLMProvider | None = None,
    accountant_provider: LLMProvider | None = None,
    explanation_provider: LLMProvider | None = None,
    scenario_ids: list[str] | None = None,
    count_per_scenario: int = DEFAULT_COUNT_PER_SCENARIO,
    batch_id: str = DEFAULT_BATCH_ID,
) -> Path:
    addendum_text = (ROOT / ROLE_PROMPT_ADDENDUM_REF).read_text(encoding="utf-8")
    run_targeted_failure_mode_pilot(
        output_root=output_root,
        curated_output=curated_output,
        provider=provider,
        requester_provider=requester_provider,
        vendor_provider=vendor_provider,
        buyer_provider=buyer_provider,
        approver_provider=approver_provider,
        accountant_provider=accountant_provider,
        explanation_provider=explanation_provider,
        scenario_ids=scenario_ids or DEFAULT_SCENARIO_IDS,
        count_per_scenario=count_per_scenario,
        batch_id=batch_id,
        pilot_id=PILOT_ID,
        protocol_ref=PROTOCOL_REF,
        claim_boundary=CLAIM_BOUNDARY,
        scenario_status="generated_method_b_diagnostic_sensitivity_pilot_reference",
        scenario_step="BC28 diagnostic sensitivity pilot execution",
        run_label="Method B diagnostic sensitivity pilot",
        runner_label="Method B diagnostic sensitivity pilot runner",
        scope_limit="BC28 S09/S12 prompt-framing diagnostic only; no controlled failure-mode baseline",
        artifact_label="BC28 diagnostic sensitivity",
        role_prompt_addendum=addendum_text,
        role_prompt_addendum_ref=ROLE_PROMPT_ADDENDUM_REF,
    )
    add_reference_comparison(curated_output)
    return curated_output


def add_reference_comparison(curated_output: Path) -> None:
    aggregate_path = curated_output / "aggregate.json"
    aggregate = json.loads(aggregate_path.read_text(encoding="utf-8"))
    reference_path = ROOT / REFERENCE_AGGREGATE_REF
    reference = json.loads(reference_path.read_text(encoding="utf-8"))
    comparison = build_reference_comparison(reference=reference, diagnostic=aggregate)
    aggregate["diagnostic_axis"] = "prompt_framing"
    aggregate["single_axis_change"] = ROLE_PROMPT_ADDENDUM_REF
    aggregate["reference_package"] = REFERENCE_AGGREGATE_REF
    aggregate["reference_comparison"] = comparison
    aggregate["reference_comparison_table"] = "reference-comparison.csv"
    aggregate["limitations"].append("descriptive comparison only; no prompt-causation, prompt-superiority, safety, or statistical claim")
    write_json(aggregate_path, aggregate)
    write_json(curated_output / "reference-comparison.json", comparison)
    write_text(curated_output / "reference-comparison.csv", render_reference_comparison_csv(comparison))
    write_text(curated_output / "summary.md", render_summary(aggregate))


def build_reference_comparison(*, reference: dict[str, Any], diagnostic: dict[str, Any]) -> dict[str, Any]:
    return {
        "reference_batch_id": reference["batch_id"],
        "diagnostic_batch_id": diagnostic["batch_id"],
        "reference_generated_candidate_rows": reference["generated_candidate_rows"],
        "diagnostic_generated_candidate_rows": diagnostic["generated_candidate_rows"],
        "generated_candidate_row_delta": diagnostic["generated_candidate_rows"] - reference["generated_candidate_rows"],
        "reference_event_candidate_table_rows": reference["event_candidate_table_rows"],
        "diagnostic_event_candidate_table_rows": diagnostic["event_candidate_table_rows"],
        "failure_mode_status_delta": failure_mode_status_delta(reference, diagnostic),
        "reference_full_path_counts": combined_path_counts(reference),
        "diagnostic_full_path_counts": combined_path_counts(diagnostic),
        "interpretation_limit": "descriptive prompt-framing diagnostic comparison only; no statistical, causal, prompt-superiority, safety, or real-world claim",
    }


def failure_mode_status_delta(reference: dict[str, Any], diagnostic: dict[str, Any]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    mode_names = sorted(set(reference["failure_mode_summary"]) | set(diagnostic["failure_mode_summary"]))
    for mode in mode_names:
        statuses = sorted(set(reference["failure_mode_summary"].get(mode, {})) | set(diagnostic["failure_mode_summary"].get(mode, {})))
        result[mode] = {
            status: diagnostic["failure_mode_summary"].get(mode, {}).get(status, 0) - reference["failure_mode_summary"].get(mode, {}).get(status, 0)
            for status in statuses
        }
    return result


def combined_path_counts(aggregate: dict[str, Any]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for scenario in aggregate["per_scenario"].values():
        counts.update(scenario.get("full_path_counts", {}))
    return dict(sorted(counts.items()))


def render_reference_comparison_csv(comparison: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["metric", "reference", "diagnostic", "delta"], lineterminator="\n")
    writer.writeheader()
    writer.writerow(
        {
            "metric": "generated_candidate_rows",
            "reference": comparison["reference_generated_candidate_rows"],
            "diagnostic": comparison["diagnostic_generated_candidate_rows"],
            "delta": comparison["generated_candidate_row_delta"],
        }
    )
    writer.writerow(
        {
            "metric": "event_candidate_table_rows",
            "reference": comparison["reference_event_candidate_table_rows"],
            "diagnostic": comparison["diagnostic_event_candidate_table_rows"],
            "delta": comparison["diagnostic_event_candidate_table_rows"] - comparison["reference_event_candidate_table_rows"],
        }
    )
    for mode, deltas in comparison["failure_mode_status_delta"].items():
        for status, delta in deltas.items():
            writer.writerow(
                {
                    "metric": f"{mode}:{status}",
                    "reference": "see reference aggregate",
                    "diagnostic": "see diagnostic aggregate",
                    "delta": delta,
                }
            )
    return output.getvalue()
