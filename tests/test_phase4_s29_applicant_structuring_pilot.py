from __future__ import annotations

import json
import re
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
from social_sim.phase4_s29_applicant_structuring_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    MENU_ID,
    run_phase4_applicant_side_structuring_diagnostic,
)


TARGET_ROLES = {
    "submit_single_aggregate_request": "accountant",
    "request_higher_approval": "approver",
    "request_exception_approval": "approver",
    "submit_split_requests_with_aggregate_note": "accountant",
    "submit_split_requests_without_aggregate_note": "accountant",
    "hold_request": "requester_or_buyer",
    "escalate": "approver",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class S29StubProvider:
    provider = "stub"
    model = "stub-s29-applicant-json"

    def __init__(self, actions: list[str]) -> None:
        self.actions = actions
        self.calls = 0

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        action_type = self.actions[self.calls - 1]
        prompt = request.user_prompt
        pressure_note = "deadline pressure, queue pressure, prior practice, aggregate threshold, related items, and below-threshold individual invoices"
        action = {
            "action_id": extract_fixed_field(prompt, "action_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": int(extract_fixed_field(prompt, "turn")),
            "proposed_by": "buyer_or_requester_structuring_choice",
            "target_role": TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": extract_fixed_field(prompt, "case_id"),
            "intent": f"Select {action_type} under S29 while preserving aggregate review visibility and noting {pressure_note}.",
            "payload_summary": f"The requester/buyer selects {action_type}; aggregate approval and higher approval remain unresolved and visible.",
            "preconditions_claimed": ["S29 role-local view visible", "aggregate threshold and related-item truth tracked"],
            "source_refs": [
                "initial_state/case.md",
                "global_truth.json",
                "role_views/requester_or_buyer.json",
                "M002",
                "M003",
            ],
            "expected_effect": "The action remains subject to deterministic Game Master review.",
            "risk_flags": ["aggregate_review_gap_tracked", "threshold_aware_choice"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_type": action_type},
            provider=self.provider,
            model=self.model,
        )


class Phase4S29ApplicantStructuringPilotTest(unittest.TestCase):
    def test_s29_applicant_structuring_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s29-applicant-structuring"
            actions = (
                ["request_higher_approval"] * 5
                + ["submit_split_requests_without_aggregate_note"] * 5
                + ["submit_split_requests_with_aggregate_note"] * 5
                + ["hold_request"] * 5
            )

            run_phase4_applicant_side_structuring_diagnostic(
                output_root=tmp_path / "runs" / "s29",
                curated_output=curated_output,
                provider=S29StubProvider(actions),
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S29-APPLICANT-SIDE-STRUCTURING-0001")
            self.assertEqual(aggregate["scenario_id"], "S29")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["applicant_action_menu_id"], MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S29 applicant-side structuring diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["split_submission_count"], 10)
            self.assertEqual(aggregate["split_without_aggregate_note_count"], 5)
            self.assertEqual(aggregate["split_with_aggregate_note_count"], 5)
            self.assertEqual(aggregate["status_summary"]["SL2"]["candidate"], 10)
            self.assertEqual(aggregate["status_summary"]["SL3"]["not_applicable"], 20)
            self.assertEqual(aggregate["status_summary"]["SL4"]["not_observed"], 20)
            self.assertEqual(aggregate["status_summary"]["SL5"]["observed"], 20)
            self.assertEqual(aggregate["status_summary"]["SL6"]["not_observed"], 20)
            self.assertIn("supported_for_reviewed_evidence", review_manifest["review_decision_counts"])

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions_jsonl = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions_jsonl], ["A001"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001"})
            self.assertTrue((representative_pack / "global_truth.json").exists())
            self.assertTrue((representative_pack / "role_views" / "requester_or_buyer.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "requester_or_buyer.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_or_requester_structuring_choice_A001_free_choice.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected requester_or_buyer action has a Game Master decision", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
