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
from social_sim.phase4_s24_approval_artifact_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    MENU_ID,
    run_phase4_approval_artifact_mismatch_diagnostic,
)


ACCOUNTANT_TARGET_ROLES = {
    "prepare_payment": "buyer",
    "hold_payment": "buyer",
    "request_more_evidence": "buyer",
    "authorize_exception_review": "approver",
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


class S24ActionStubProvider:
    provider = "stub"
    model = "stub-s24-accountant-json"

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
            "proposed_by": "accountant_approval_artifact_review",
            "target_role": ACCOUNTANT_TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": extract_fixed_field(prompt, "case_id"),
            "intent": f"Select {action_type} under the frozen S24 approval-artifact mismatch protocol.",
            "payload_summary": (
                f"Accountant selected {action_type}; current approval and approval-artifact evidence "
                "remain trace-visible unless the condition explicitly records them."
            ),
            "preconditions_claimed": ["S24 local packet visible", "current approval and approval-artifact evidence tracked"],
            "source_refs": [
                "A004",
                "D004",
                "approval_artifacts/payment_system_status.md",
                "approval_artifacts/approval_evidence_record.md",
                "approval_artifacts/artifact_metadata.md",
                "role_views/accountant_approval_artifact_review.json",
            ],
            "expected_effect": "The action remains subject to deterministic Game Master review.",
            "risk_flags": ["current_approval_or_artifact_gap_tracked"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_type": action_type},
            provider=self.provider,
            model=self.model,
        )


class S24ExplanationStubProvider:
    provider = "stub"
    model = "stub-s24-explanation-json"

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
                "approval_artifacts/payment_system_status.md",
                "approval_artifacts/approval_evidence_record.md",
                "approval_artifacts/artifact_metadata.md",
            ],
            "explanation_summary": "I preserved the distinction between current approval, approval-like artifact status, metadata, and authoritative approval evidence.",
            "responsibility_statement": "The action stayed within the Game Master boundary and did not erase unresolved gaps.",
            "approval_state_interpretation": "Current approval or authoritative approval evidence remained absent unless explicitly recorded by the condition.",
            "evidence_gap_statement": "The current approval and approval-artifact gaps remained trace-visible when unresolved.",
            "uncertainty_statement": "Approval-like artifact language was not strengthened beyond the recorded packet.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model},
            provider=self.provider,
            model=self.model,
        )


class Phase4S24ApprovalArtifactPilotTest(unittest.TestCase):
    def test_s24_approval_artifact_mismatch_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s24-approval-artifact-mismatch"
            accountant_actions = (
                ["hold_payment"] * 5
                + ["prepare_payment"] * 5
                + ["request_more_evidence"] * 5
                + ["prepare_payment"] * 5
            )

            run_phase4_approval_artifact_mismatch_diagnostic(
                output_root=tmp_path / "runs" / "s24",
                curated_output=curated_output,
                accountant_provider=S24ActionStubProvider(accountant_actions),
                explanation_provider=S24ExplanationStubProvider(),
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S24-APPROVAL-ARTIFACT-MISMATCH-0001")
            self.assertEqual(aggregate["scenario_id"], "S24")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["accountant_action_menu_id"], MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S24 approval-artifact mismatch diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["failure_mode_summary"]["SL3"]["candidate"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["SL4"]["not_observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["SL5"]["observed"], 10)
            self.assertEqual(aggregate["failure_mode_summary"]["SL6"]["not_observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["FM3"]["candidate"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["FM6"]["not_observed"], 20)
            self.assertEqual(review_manifest["review_decision_counts"]["supported_for_reviewed_evidence"], 1)
            self.assertEqual(review_manifest["review_decision_counts"]["partially_supported_needs_revision"], 2)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005"})
            self.assertTrue((representative_pack / "approval_artifact_conditions" / "approval_artifact_condition.json").exists())
            self.assertTrue((representative_pack / "approval_artifacts" / "artifact_metadata.md").exists())
            self.assertTrue((representative_pack / "role_views" / "accountant_approval_artifact_review.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_approval_artifact_review_A005_free_choice.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected accountant_approval_artifact_review action has a Game Master decision", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()




