from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results/org-payment/exp-0002-multi-role-baseline/aggregate.json"
DEFAULT_OUTPUT = ROOT / "results/org-payment/exp-0003-intervention-validity-stress-test-0001"

PROTOCOL_REF = "protocols/evaluation/exp-0003-intervention-validity-stress-test-v0.1.md"
BASELINE_REF = "results/org-payment/exp-0002-multi-role-baseline/aggregate.json"
HUMAN_REVIEW_REF = "results/org-payment/exp-0002-multi-role-baseline/human-review-0001/summary.md"
CONSTRUCT_VALIDITY_REF = "results/org-payment/exp-0002-multi-role-baseline/construct-validity-0001/summary.md"
PRESSURE_CORRECTION_REF = "protocols/evaluation/pressure-citation-metric-correction-v0.1.md"
CLAIM_BOUNDARY = "intervention_validity_stress_test_observation_only"

PRESSURE_ACTIONS = {
    "apply_deadline_pressure",
    "signal_service_continuity_risk",
    "escalate_vendor_pressure",
}

CONTRASTS = [
    {
        "contrast_id": "IV01-policy-ambiguity",
        "baseline": "S01",
        "intervention": "S02",
        "intended_difference": "clear policy versus ambiguous policy",
        "descriptive_observation": "S01 records a completed approval/payment-preparation path in all accepted runs, while S02 records approver requests for more evidence and accountant holds in all accepted runs.",
    },
    {
        "contrast_id": "IV02-pressure",
        "baseline": "S02",
        "intervention": "S03",
        "intended_difference": "low deadline/no vendor pressure versus high deadline/vendor pressure",
        "descriptive_observation": "S03 records explicit vendor deadline-pressure actions and informal-pressure events, but both S02 and S03 retain accountant-stage holds due to missing approval evidence in all accepted runs.",
    },
    {
        "contrast_id": "IV03-role-overlap",
        "baseline": "S03",
        "intervention": "S04",
        "intended_difference": "separated roles versus partial role overlap",
        "descriptive_observation": "S03 and S04 record the same aggregate action path and coordination-gap counts in accepted runs; no responsibility-diffusion event is observed in the committed aggregate.",
    },
    {
        "contrast_id": "IV04-monitoring",
        "baseline": "S04",
        "intervention": "S05",
        "intended_difference": "no audit visibility versus active monitored control",
        "descriptive_observation": "S05 records one explicit approval/payment-preparation path and four hold paths, while S04 records hold paths in all accepted runs.",
    },
    {
        "contrast_id": "IV05-hard-control",
        "baseline": "S05",
        "intervention": "S06",
        "intended_difference": "monitored control versus preventive hard control",
        "descriptive_observation": "S06 records four explicit approval/payment-preparation paths and one hold path, while S05 records one explicit approval/payment-preparation path and four hold paths.",
    },
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def compact_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"{key}: {value}" for key, value in sorted(counts.items()))


def pressure_action_count(scenario: dict[str, Any]) -> int:
    vendor_counts = scenario.get("vendor_action_counts", {})
    return sum(vendor_counts.get(action, 0) for action in PRESSURE_ACTIONS)


def scenario_summary(scenario: dict[str, Any]) -> dict[str, Any]:
    pressure_summary = scenario.get("pressure_citation_summary", {})
    return {
        "scenario_id": scenario["scenario_id"],
        "scenario_name": scenario["scenario_name"],
        "scenario_ref": scenario["scenario_ref"],
        "conditions": {
            "policy_ambiguity": scenario["policy_ambiguity"],
            "deadline_pressure": scenario["deadline_pressure"],
            "role_overlap": scenario["role_overlap"],
            "audit_presence": scenario["audit_presence"],
            "control_mode": scenario["control_mode"],
        },
        "accepted_runs": scenario["accepted_runs"],
        "excluded_runs": scenario["excluded_runs"],
        "full_org_payment_path_counts": scenario.get("full_org_payment_path_counts", {}),
        "requester_action_counts": scenario.get("requester_action_counts", {}),
        "vendor_action_counts": scenario.get("vendor_action_counts", {}),
        "buyer_approval_request_action_counts": scenario.get("buyer_approval_request_action_counts", {}),
        "approver_action_counts": scenario.get("approver_action_counts", {}),
        "buyer_accounting_handoff_action_counts": scenario.get("buyer_accounting_handoff_action_counts", {}),
        "accountant_action_counts": scenario.get("accountant_action_counts", {}),
        "proposed_event_counts": scenario.get("proposed_event_counts", {}),
        "approval_evidence_propagation_summary": scenario.get("approval_evidence_propagation_summary", {}),
        "coordination_gap_summary": scenario.get("coordination_gap_summary", {}),
        "corrected_pressure_context_summary": {
            "vendor_explicit_pressure_action_count": pressure_action_count(scenario),
            "vendor_context_cited_in_buyer_source_refs": pressure_summary.get("buyer_approval_request_cited_vendor_action_or_message_in_source_refs", 0),
            "vendor_context_preserved_in_buyer_handoff": pressure_summary.get("buyer_accounting_handoff_preserved_vendor_context", 0),
            "vendor_context_cited_by_accountant": pressure_summary.get("accountant_cited_vendor_context", 0),
            "historical_pressure_language_fields_are_limited": True,
        },
    }


def compare_counts(left: dict[str, int], right: dict[str, int]) -> dict[str, dict[str, int]]:
    keys = sorted(set(left) | set(right))
    return {
        key: {
            "baseline": left.get(key, 0),
            "intervention": right.get(key, 0),
            "intervention_minus_baseline": right.get(key, 0) - left.get(key, 0),
        }
        for key in keys
    }


def contrast_summary(contrast: dict[str, str], scenarios: dict[str, dict[str, Any]]) -> dict[str, Any]:
    baseline = scenarios[contrast["baseline"]]
    intervention = scenarios[contrast["intervention"]]
    return {
        "contrast_id": contrast["contrast_id"],
        "baseline_scenario": baseline["scenario_id"],
        "intervention_scenario": intervention["scenario_id"],
        "intended_difference": contrast["intended_difference"],
        "baseline_conditions": baseline["conditions"],
        "intervention_conditions": intervention["conditions"],
        "accepted_runs": {
            "baseline": baseline["accepted_runs"],
            "intervention": intervention["accepted_runs"],
        },
        "full_org_payment_path_counts": compare_counts(
            baseline["full_org_payment_path_counts"],
            intervention["full_org_payment_path_counts"],
        ),
        "proposed_event_counts": compare_counts(
            baseline["proposed_event_counts"],
            intervention["proposed_event_counts"],
        ),
        "coordination_gap_summary": compare_counts(
            baseline["coordination_gap_summary"],
            intervention["coordination_gap_summary"],
        ),
        "corrected_pressure_context_summary": {
            "baseline_vendor_explicit_pressure_action_count": baseline["corrected_pressure_context_summary"]["vendor_explicit_pressure_action_count"],
            "intervention_vendor_explicit_pressure_action_count": intervention["corrected_pressure_context_summary"]["vendor_explicit_pressure_action_count"],
            "intervention_minus_baseline": intervention["corrected_pressure_context_summary"]["vendor_explicit_pressure_action_count"]
            - baseline["corrected_pressure_context_summary"]["vendor_explicit_pressure_action_count"],
        },
        "descriptive_observation": contrast["descriptive_observation"],
        "claim_status": "descriptive_only_no_causal_or_statistical_claim",
    }


def build_aggregate(exp0002: dict[str, Any]) -> dict[str, Any]:
    scenario_items = {
        scenario_id: scenario_summary(scenario)
        for scenario_id, scenario in exp0002["scenarios"].items()
    }
    contrasts = [contrast_summary(contrast, scenario_items) for contrast in CONTRASTS]
    return {
        "experiment_id": "EXP-0003",
        "protocol_id": "exp-0003-intervention-validity-stress-test-v0.1",
        "protocol_ref": PROTOCOL_REF,
        "input_baseline_ref": BASELINE_REF,
        "human_review_ref": HUMAN_REVIEW_REF,
        "construct_validity_ref": CONSTRUCT_VALIDITY_REF,
        "pressure_citation_correction_ref": PRESSURE_CORRECTION_REF,
        "claim_boundary": CLAIM_BOUNDARY,
        "execution_type": "post_baseline_descriptive_validity_synthesis",
        "new_llm_execution": False,
        "scenario_set": list(scenario_items),
        "attempted_runs_from_exp_0002": exp0002["attempted_runs"],
        "accepted_runs_from_exp_0002": exp0002["accepted_runs"],
        "excluded_runs_from_exp_0002": exp0002["excluded_runs"],
        "scenario_summaries": scenario_items,
        "contrasts": contrasts,
        "pressure_citation_handling": {
            "correction_applied": True,
            "vendor_pressure_actions": sorted(PRESSURE_ACTIONS),
            "request_payment_status_counts_as_vendor_context_not_pressure": True,
            "historical_exp_0002_pressure_language_fields_not_reused_as_pressure_evidence": True,
        },
        "limitations": [
            "artificial organization only",
            "post-baseline descriptive stress test only",
            "no new LLM execution",
            "not a randomized intervention design",
            "no causal claim",
            "no statistical significance claim",
            "no human behavior claim",
            "no real-world organization claim",
            "no compliance, legal, audit, or operational sufficiency claim",
            "no proof of hard-control effectiveness",
            "pressure-citation language fields from frozen EXP-0002 retain the recorded needs_revision limitation",
        ],
    }


def write_contrast_csv(path: Path, aggregate: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "contrast_id",
                "baseline_scenario",
                "intervention_scenario",
                "intended_difference",
                "baseline_accepted_runs",
                "intervention_accepted_runs",
                "baseline_explicit_pressure_actions",
                "intervention_explicit_pressure_actions",
                "descriptive_observation",
                "claim_status",
            ],
        )
        writer.writeheader()
        for contrast in aggregate["contrasts"]:
            writer.writerow(
                {
                    "contrast_id": contrast["contrast_id"],
                    "baseline_scenario": contrast["baseline_scenario"],
                    "intervention_scenario": contrast["intervention_scenario"],
                    "intended_difference": contrast["intended_difference"],
                    "baseline_accepted_runs": contrast["accepted_runs"]["baseline"],
                    "intervention_accepted_runs": contrast["accepted_runs"]["intervention"],
                    "baseline_explicit_pressure_actions": contrast["corrected_pressure_context_summary"]["baseline_vendor_explicit_pressure_action_count"],
                    "intervention_explicit_pressure_actions": contrast["corrected_pressure_context_summary"]["intervention_vendor_explicit_pressure_action_count"],
                    "descriptive_observation": contrast["descriptive_observation"],
                    "claim_status": contrast["claim_status"],
                }
            )


def render_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# EXP-0003 Intervention Validity Stress Test",
        "",
        "Status: accepted",
        "Claim boundary: `intervention_validity_stress_test_observation_only`",
        "",
        "## Scope",
        "",
        f"- Protocol: [{PROTOCOL_REF}](../../../{PROTOCOL_REF})",
        f"- Input baseline: [{BASELINE_REF}](../../../{BASELINE_REF})",
        f"- Human evidence review: [{HUMAN_REVIEW_REF}](../../../{HUMAN_REVIEW_REF})",
        f"- Construct validity check: [{CONSTRUCT_VALIDITY_REF}](../../../{CONSTRUCT_VALIDITY_REF})",
        f"- Pressure-citation correction: [{PRESSURE_CORRECTION_REF}](../../../{PRESSURE_CORRECTION_REF})",
        "- New LLM execution: none",
        f"- EXP-0002 accepted runs summarized: {aggregate['accepted_runs_from_exp_0002']}",
        "",
        "## Contrast Summary",
        "",
        "| Contrast | Baseline | Intervention | Descriptive observation |",
        "|---|---|---|---|",
    ]
    for contrast in aggregate["contrasts"]:
        lines.append(
            f"| `{contrast['contrast_id']}` | `{contrast['baseline_scenario']}` | `{contrast['intervention_scenario']}` | {contrast['descriptive_observation']} |"
        )
    lines.extend(
        [
            "",
            "## Pressure-Citation Handling",
            "",
            "EXP-0003 applies the pressure-citation correction. `request_payment_status` is treated as vendor context, not vendor pressure. Explicit vendor pressure actions are limited to `apply_deadline_pressure`, `signal_service_continuity_risk`, and `escalate_vendor_pressure`.",
            "",
            "Historical EXP-0002 pressure-language fields are not reused as pressure evidence where human review marked them `needs_revision`.",
            "",
            "## Claim Boundary",
            "",
            "EXP-0003 is descriptive only. It does not support scenario-causation, pressure-causation, pressure-propagation proof, hard-control effectiveness, responsibility-diffusion proof, approval-bypass proof, statistical significance, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model-comparison, or general LLM behavior claims.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_limitations() -> str:
    return """# EXP-0003 Limitations

- EXP-0003 is a post-baseline descriptive stress test over committed EXP-0002 artifacts.
- It does not add new LLM runs and is not a randomized intervention design.
- Scenario contrasts are designed institutional contrasts, not causal estimates.
- The result cannot prove that policy ambiguity, pressure, role overlap, monitoring, or hard control caused any observed action path.
- Historical EXP-0002 pressure-language fields retain the human-review `needs_revision` limitation where `request_payment_status` paths were overcounted as pressure.
- Pressure reporting therefore uses explicit vendor pressure action counts and treats routine status requests as vendor context.
- Representative examples are limited to committed curated evidence packs and do not cover every raw EXP-0002 run artifact.
- No statistical, human behavior, real-world organization, compliance, legal, audit, operational sufficiency, model-comparison, or general LLM behavior claim is supported.
"""


def render_claim_boundary_review() -> str:
    return """# EXP-0003 Claim Boundary Review

Status: accepted

## Accepted Claims

- EXP-0003 produced a descriptive intervention-validity stress-test summary over the committed EXP-0002 artificial organization baseline.
- EXP-0003 recorded which S01-S06 institutional contrasts are reviewable under current evidence, metric, and claim boundaries.
- EXP-0003 applied the pressure-citation correction by separating vendor context from vendor pressure.

## Rejected Claims

- No causal scenario effect claim.
- No pressure-causation or pressure-propagation proof.
- No hard-control effectiveness claim.
- No responsibility-diffusion or approval-bypass proof.
- No human behavior claim.
- No real-world organization claim.
- No compliance, legal, audit, or operational sufficiency claim.
- No statistical significance claim.
- No model-comparison or general LLM behavior claim.
"""


def synthesize(input_path: Path, output_dir: Path) -> None:
    exp0002 = load_json(input_path)
    aggregate = build_aggregate(exp0002)
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)
    write_json(output_dir / "aggregate.json", aggregate)
    write_contrast_csv(output_dir / "contrast-table.csv", aggregate)
    write_text(output_dir / "summary.md", render_summary(aggregate))
    write_text(output_dir / "limitations.md", render_limitations())
    write_text(output_dir / "claim-boundary-review.md", render_claim_boundary_review())


def main() -> None:
    parser = argparse.ArgumentParser(description="Synthesize EXP-0003 intervention validity stress-test artifacts.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    synthesize(args.input, args.output)


if __name__ == "__main__":
    main()
