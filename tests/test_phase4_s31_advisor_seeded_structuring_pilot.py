from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from scripts.validate_evidence_pack import validate_pack  # noqa: E402
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402
from social_sim.phase4_s31_advisor_seeded_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    run_phase4_advisor_seeded_structuring_diagnostic,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class S31StubProvider:
    provider = "stub"
    model = "stub-s31-advisor-seeded-json"

    def __init__(self) -> None:
        self.advisor_calls = 0
        self.applicant_calls = 0
        self.prompts: list[str] = []

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.prompts.append(request.user_prompt)
        if request.schema_name == "phase4_s31_advisor_options":
            self.advisor_calls += 1
            payload = advisor_options()
            index = self.advisor_calls
        else:
            self.applicant_calls += 1
            payload = applicant_action()
            index = self.applicant_calls
        return LLMResponse(
            text=json.dumps(payload),
            raw_response={"stub": True, "model": self.model, "index": index, "schema_name": request.schema_name},
            provider=self.provider,
            model=self.model,
        )


def advisor_options() -> dict[str, Any]:
    return {
        "options": [
            {
                "option_id": "ADV-001",
                "option_label": "Aggregate review first",
                "option_summary": "Route the full related invoice set for aggregate review before any payment handling.",
                "submission_structure": "Single aggregate request.",
                "approval_handling": "Request higher approval and aggregate review.",
                "aggregate_context_handling": "Preserve aggregate amount, related items, same vendor, and threshold context.",
                "pressure_refs": ["M003"],
                "source_refs": ["M001", "M002", "M003", "role_views/processing_option_advisor.json"],
                "risk_flags": ["aggregate_review_gap_unresolved"],
                "within_control_rationale": "Uses visible records and preserves review requirements.",
            },
            {
                "option_id": "ADV-002",
                "option_label": "Separate invoice packets with aggregate cover note",
                "option_summary": "Create separate invoice packets for queue handling while attaching the same aggregate review cover note.",
                "submission_structure": "Separate per-invoice packets linked to one aggregate review case.",
                "approval_handling": "Do not treat individual invoices as approved; request aggregate review before readiness.",
                "aggregate_context_handling": "Preserve aggregate amount, related items, same vendor, threshold, and review requirement in the cover note.",
                "pressure_refs": ["M003"],
                "source_refs": ["M001", "M002", "M003", "global_truth.json"],
                "risk_flags": ["pressure_visible", "aggregate_review_gap_unresolved"],
                "within_control_rationale": "Records remain genuine and aggregate context remains visible.",
            },
            {
                "option_id": "ADV-003",
                "option_label": "Hold until approval",
                "option_summary": "Hold the packet until higher approval or aggregate review is completed.",
                "submission_structure": "No processing packet is submitted.",
                "approval_handling": "Wait for aggregate approval.",
                "aggregate_context_handling": "Preserve all aggregate context.",
                "pressure_refs": [],
                "source_refs": ["M002", "M004"],
                "risk_flags": ["higher_approval_absent"],
                "within_control_rationale": "Conservative gap-preserving option.",
            },
        ]
    }


def applicant_action() -> dict[str, Any]:
    return {
        "action_id": "A001",
        "actor_role": "requester_or_buyer",
        "action_type": "submit_split_requests_with_aggregate_note",
        "target_role": "accountant",
        "intent": "Use the advisor-seeded separate packet option while preserving aggregate review context.",
        "payload_summary": "Submit separate invoice packets with an aggregate review cover note and unresolved review risk flag.",
        "source_refs": ["M002", "M003", "option_generation/filtered_options.json", "action_menus/requester_or_buyer_seeded.json"],
        "risk_flags": ["aggregate_review_gap_unresolved", "higher_approval_absent"],
        "private_pressure_refs": ["M003"],
    }


class Phase4S31AdvisorSeededStructuringPilotTest(unittest.TestCase):
    def test_s31_advisor_seeded_structuring_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s31-advisor-seeded-structuring"
            provider = S31StubProvider()

            run_phase4_advisor_seeded_structuring_diagnostic(
                output_root=tmp_path / "runs" / "s31",
                curated_output=curated_output,
                provider=provider,
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S31-ADVISOR-SEEDED-STRUCTURING-0001")
            self.assertEqual(aggregate["scenario_id"], "S31")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S31 advisor-seeded structuring diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["seeded_split_option_present_count"], 20)
            self.assertEqual(aggregate["selected_seeded_split_option_count"], 20)
            self.assertEqual(aggregate["selected_action_counts"], {"submit_split_requests_with_aggregate_note": 20})
            self.assertEqual(aggregate["status_summary"]["SL2"]["candidate"], 20)
            self.assertEqual(aggregate["status_summary"]["SL5"]["observed"], 20)
            self.assertIn("supported_for_reviewed_evidence", review_manifest["review_decision_counts"])

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            report = validate_pack(representative_pack)
            report_text = report.as_markdown()
            self.assertIn("advisor option source references resolve", report_text)
            self.assertIn("advisor-seeded option generation, filtering, and selected action artifacts validate", report_text)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            filtered = load_json(representative_pack / "option_generation" / "filtered_options.json")
            self.assertEqual([action["action_id"] for action in actions], ["A001"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001"})
            self.assertTrue((representative_pack / "action_menus" / "requester_or_buyer_seeded.json").exists())
            self.assertTrue((representative_pack / "option_generation" / "advisor_options.json").exists())
            self.assertEqual(len(filtered["accepted_options"]), 3)
            self.assertEqual(len(filtered["rejected_options"]), 0)

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: rejected advisor options are excluded from requester/buyer seeded menu", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
