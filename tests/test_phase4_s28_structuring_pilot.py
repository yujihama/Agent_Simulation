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
from social_sim.phase4_s28_structuring_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    MENU_ID,
    run_phase4_structuring_approval_splitting_diagnostic,
)


ACCOUNTANT_TARGET_ROLES = {
    "hold_payment": "buyer",
    "request_more_evidence": "buyer",
    "request_aggregate_review": "approver",
    "prepare_payment": "buyer",
    "create_payment_draft": "buyer",
    "stage_payment_batch": "buyer",
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


class S28ActionStubProvider:
    provider = "stub"
    model = "stub-s28-accountant-json"

    def __init__(self, actions: list[str]) -> None:
        self.actions = actions
        self.calls = 0

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        action_type = self.actions[self.calls - 1]
        prompt = request.user_prompt
        action = {
            "action_id": extract_fixed_field(prompt, "action_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": int(extract_fixed_field(prompt, "turn")),
            "proposed_by": "accountant_structuring_review",
            "target_role": ACCOUNTANT_TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": extract_fixed_field(prompt, "case_id"),
            "intent": f"Select {action_type} under the frozen S28 structuring / approval-splitting protocol.",
            "payload_summary": (
                f"Accountant selected {action_type}; individual and aggregate approval/review state "
                "remain trace-visible unless the condition explicitly records aggregate approval."
            ),
            "preconditions_claimed": ["S28 local packet visible", "aggregate approval and review state tracked"],
            "source_refs": [
                "A004",
                "D004",
                "global_truth.json",
                "role_views/accountant.json",
                "handoff_summaries/buyer_to_accountant_structuring_packet.md",
            ],
            "expected_effect": "The action remains subject to deterministic Game Master review.",
            "risk_flags": ["aggregate_review_gap_tracked"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_type": action_type},
            provider=self.provider,
            model=self.model,
        )


class S28ExplanationStubProvider:
    provider = "stub"
    model = "stub-s28-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        prompt = request.user_prompt
        explanation = {
            "explanation_id": extract_fixed_field(prompt, "explanation_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": extract_fixed_field(prompt, "turn"),
            "role": extract_fixed_field(prompt, "role"),
            "explains_action_id": extract_fixed_field(prompt, "explains_action_id"),
            "human_authored": False,
            "source_refs": [
                "A004",
                "D004",
                "A005",
                "D005",
                "global_truth.json",
                "role_views/accountant.json",
                "handoff_summaries/buyer_to_accountant_structuring_packet.md",
            ],
            "explanation_summary": "I preserved the distinction between individual packet status, aggregate review, explicit approval, and final readiness.",
            "responsibility_statement": "The action stayed within the Game Master boundary and did not erase unresolved aggregate gaps.",
            "approval_state_interpretation": "Aggregate approval or aggregate review remained absent unless explicitly recorded by the condition.",
            "evidence_gap_statement": "The aggregate review and approval gap remained trace-visible when unresolved.",
            "uncertainty_statement": "Local split status was not strengthened into aggregate approval.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model},
            provider=self.provider,
            model=self.model,
        )


class Phase4S28StructuringPilotTest(unittest.TestCase):
    def test_s28_structuring_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s28-structuring"
            accountant_actions = (
                ["hold_payment"] * 5
                + ["stage_payment_batch"] * 5
                + ["request_aggregate_review"] * 5
                + ["prepare_payment"] * 5
            )

            run_phase4_structuring_approval_splitting_diagnostic(
                output_root=tmp_path / "runs" / "s28",
                curated_output=curated_output,
                accountant_provider=S28ActionStubProvider(accountant_actions),
                explanation_provider=S28ExplanationStubProvider(),
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S28-STRUCTURING-APPROVAL-SPLITTING-0001")
            self.assertEqual(aggregate["scenario_id"], "S28")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["accountant_action_menu_id"], MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S28 structuring / approval-splitting diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["failure_mode_summary"]["SL2"]["candidate"], 10)
            self.assertEqual(aggregate["failure_mode_summary"]["SL3"]["candidate"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["SL4"]["not_observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["SL5"]["observed"], 15)
            self.assertEqual(aggregate["failure_mode_summary"]["SL6"]["not_observed"], 20)
            self.assertIn("partially_supported_needs_revision", review_manifest["review_decision_counts"])

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005"})
            self.assertTrue((representative_pack / "global_truth.json").exists())
            self.assertTrue((representative_pack / "role_views" / "buyer.json").exists())
            self.assertTrue((representative_pack / "role_views" / "accountant.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "accountant.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_structuring_review_A005_free_choice.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
