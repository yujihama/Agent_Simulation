from __future__ import annotations

import json
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
import sys

sys.path.insert(0, str(SRC))

from social_sim.baseline_runner import (  # noqa: E402
    FROZEN_RUNS_PER_SCENARIO,
    FROZEN_TOTAL_PLANNED_RUNS,
    RESULT_CLAIM_BOUNDARY,
    run_buyer_only_baseline,
)
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402


TARGET_ROLES = {
    "request_approval": "approver",
    "request_more_evidence": "requester",
    "hold_payment": "accountant",
    "escalate": "approver",
    "mark_approval_inferred": "accountant",
}

ACTION_BY_SCENARIO = {
    "s01": "request_approval",
    "s02": "request_more_evidence",
    "s03": "escalate",
    "s04": "hold_payment",
    "s05": "request_approval",
    "s06": "mark_approval_inferred",
}


class BaselineStubProvider:
    provider = "stub"
    model = "gpt-4.1-mini"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        scenario_key = re.search(r"baseline-(s\d\d)-run", run_id)
        if scenario_key is None:
            raise AssertionError(f"unexpected run_id: {run_id}")
        action_type = ACTION_BY_SCENARIO[scenario_key.group(1)]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": 4,
            "proposed_by": "buyer",
            "target_role": TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} for the frozen EXP-0001 baseline stub.",
            "payload_summary": f"Buyer selected {action_type} in the frozen baseline stub.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval absent"],
            "source_refs": ["M002", "T003"],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["approval_evidence_gap"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={
                "stub": True,
                "action_id": action_id,
                "model": self.model,
                "model_version": "gpt-4.1-mini-stub",
            },
            provider=self.provider,
            model=self.model,
        )


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class BuyerOnlyBaselineTest(unittest.TestCase):
    def test_baseline_writes_frozen_result_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "baseline"
            results_output = tmp_path / "results" / "baseline"
            run_buyer_only_baseline(
                output_root=raw_output,
                results_output=results_output,
                provider=BaselineStubProvider(),
            )

            aggregate = load_json(results_output / "aggregate.json")
            manifest = load_json(results_output / "execution-manifest.json")
            self.assertEqual(aggregate["experiment_id"], "EXP-0001")
            self.assertEqual(aggregate["protocol_id"], "buyer-only-baseline-v0.1")
            self.assertEqual(aggregate["runs_per_scenario"], FROZEN_RUNS_PER_SCENARIO)
            self.assertEqual(aggregate["total_planned_runs"], FROZEN_TOTAL_PLANNED_RUNS)
            self.assertEqual(aggregate["attempted_runs"], 30)
            self.assertEqual(aggregate["accepted_runs"], 30)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in EXP-0001")
            self.assertEqual(aggregate["claim_boundary"], RESULT_CLAIM_BOUNDARY)

            summaries = {item["scenario_id"]: item for item in aggregate["scenario_summaries"]}
            self.assertEqual(summaries["S01"]["attempted_runs"], 5)
            self.assertEqual(summaries["S01"]["accepted_runs"], 5)
            self.assertEqual(summaries["S01"]["selected_action_type_counts"], {"request_approval": 5})
            self.assertEqual(
                summaries["S06"]["gm_decisions_by_selected_action"],
                {"mark_approval_inferred": {"blocked": 5}},
            )
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 6)
            self.assertTrue((results_output / "scenario-summary.csv").exists())

            summary = (results_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("Under the frozen EXP-0001 artificial organization protocol", summary)
            self.assertIn("All included runs passed mechanical evidence-pack validation", summary)
            self.assertIn("No statistical significance claim", summary)

            representative_pack = (
                results_output / "representative-evidence-packs" / "s01" / "request_approval-run-001"
            )
            representative_manifest = load_json(representative_pack / "manifest.json")
            representative_metrics = load_json(representative_pack / "metrics.json")
            representative_notes = (representative_pack / "reviewer_notes.md").read_text(encoding="utf-8")
            self.assertEqual(representative_manifest["claim_boundary"], RESULT_CLAIM_BOUNDARY)
            self.assertIn("one included EXP-0001 buyer-only baseline run", representative_notes)
            self.assertNotIn("no baseline result", representative_notes.lower())
            metric_values = {metric["metric_id"]: metric["value"] for metric in representative_metrics["metrics"]}
            self.assertEqual(metric_values["MR004"], "mechanically_validated_buyer_only_baseline_pack")


if __name__ == "__main__":
    unittest.main()
