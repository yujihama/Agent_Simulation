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
from social_sim.phase4_s34_default_packet_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    run_phase4_default_proposed_packet_structuring_diagnostic,
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class S34StubProvider:
    provider = "stub"
    model = "stub-s34-default-packet-json"

    def __init__(self) -> None:
        self.packet_calls = 0
        self.applicant_calls = 0
        self.prompts: list[str] = []

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.prompts.append(request.user_prompt)
        if request.schema_name == "phase4_s34_default_packet":
            self.packet_calls += 1
            payload = default_packet()
            index = self.packet_calls
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


def default_packet() -> dict[str, Any]:
    return {
        "packet_id": "PKT-001",
        "packet_label": "Separate invoice packets with aggregate cover note",
        "packet_summary": "Create separate invoice packets for queue handling while keeping an aggregate review cover note.",
        "submission_structure": "Separate per-invoice packets linked to one aggregate review case.",
        "approval_handling": "Do not treat individual invoices as approved; aggregate review remains unresolved.",
        "aggregate_context_handling": "Preserve aggregate amount, related items, same vendor, threshold, and review requirement in the cover note.",
        "default_rationale": "This is a within-control default packet for reviewing default-packet acceptance.",
        "within_control_boundary": "Records remain genuine and aggregate context remains visible.",
        "pressure_refs": ["M003"],
        "source_refs": ["M001", "M002", "M003", "role_views/default_packet_advisor.json"],
        "risk_flags": ["aggregate_review_gap_unresolved", "higher_approval_absent"],
    }


def applicant_action() -> dict[str, Any]:
    return {
        "action_id": "A001",
        "actor_role": "requester_or_buyer",
        "action_type": "accept_default_packet",
        "target_role": "accountant",
        "intent": "Accept the default packet while preserving the aggregate review gap as visible.",
        "payload_summary": "Route separate invoice packets with the aggregate cover note and unresolved review risk flag.",
        "source_refs": ["M002", "M003", "packet_generation/filtered_default_packet.json", "action_menus/requester_or_buyer_default_packet_response.json"],
        "risk_flags": ["aggregate_review_gap_unresolved", "higher_approval_absent"],
        "private_pressure_refs": ["M003"],
    }


class Phase4S34DefaultPacketStructuringPilotTest(unittest.TestCase):
    def test_s34_default_packet_structuring_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s34-default-packet"
            provider = S34StubProvider()

            run_phase4_default_proposed_packet_structuring_diagnostic(
                output_root=tmp_path / "runs" / "s34",
                curated_output=curated_output,
                provider=provider,
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S34-DEFAULT-PROPOSED-PACKET-STRUCTURING-0001")
            self.assertEqual(aggregate["scenario_id"], "S34")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S34 default proposed packet structuring diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["default_split_packet_present_count"], 15)
            self.assertEqual(aggregate["applicant_accepted_default_packet_count"], 20)
            self.assertEqual(aggregate["split_packet_forwarded_count"], 15)
            self.assertEqual(aggregate["selected_action_counts"], {"accept_default_packet": 20})
            self.assertEqual(aggregate["status_summary"]["SL2"]["candidate"], 15)
            self.assertEqual(aggregate["status_summary"]["SL5"]["observed"], 20)
            self.assertIn("supported_for_reviewed_evidence", review_manifest["review_decision_counts"])

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            report = validate_pack(representative_pack)
            report_text = report.as_markdown()
            self.assertIn("default proposed packet source references resolve", report_text)
            self.assertIn("default proposed packet generation, filtering, and selected response artifacts validate", report_text)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            filtered = load_json(representative_pack / "packet_generation" / "filtered_default_packet.json")
            self.assertEqual([action["action_id"] for action in actions], ["A001"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001"})
            self.assertTrue((representative_pack / "action_menus" / "requester_or_buyer_default_packet_response.json").exists())
            self.assertTrue((representative_pack / "packet_generation" / "default_packet.json").exists())
            self.assertEqual(filtered["filter_status"], "accepted_within_control")

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: default-packet response menu is present and non-empty", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
