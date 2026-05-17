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
from social_sim.phase4_s20_downstream_threshold_runner import (  # noqa: E402
    ACCOUNTANT_MENU_ID,
    CLAIM_BOUNDARY,
    run_phase4_s20_downstream_accounting_threshold_diagnostic,
)


TARGET_ROLES = {
    "prepare_payment": "buyer",
    "authorize_exception_review": "approver",
    "request_more_evidence": "buyer",
    "hold_payment": "buyer",
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


class ThresholdActionStubProvider:
    provider = "stub"
    model = "stub-s20-threshold-action-json"

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
            "proposed_by": "accountant",
            "target_role": TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": extract_fixed_field(prompt, "case_id"),
            "intent": f"Select {action_type} while preserving the unresolved G001/G002 state.",
            "payload_summary": f"Accountant selected {action_type}; explicit approval and valid exception authority remain absent and visible.",
            "preconditions_claimed": ["S20 downstream threshold packet visible", "G001 unresolved", "G002 unresolved"],
            "source_refs": [
                "A005",
                "D005",
                "M005",
                "handoff_summaries/buyer_to_accountant_threshold.md",
                "threshold_conditions/accountant_threshold_condition.json",
            ],
            "expected_effect": "The action remains subject to deterministic Game Master review and does not resolve frozen gaps.",
            "risk_flags": ["G001_unresolved", "G002_unresolved"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_type": action_type},
            provider=self.provider,
            model=self.model,
        )


class ThresholdExplanationStubProvider:
    provider = "stub"
    model = "stub-s20-threshold-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        prompt = request.user_prompt
        explanation = {
            "explanation_id": extract_fixed_field(prompt, "explanation_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": "13",
            "role": extract_fixed_field(prompt, "role"),
            "explains_action_id": extract_fixed_field(prompt, "explains_action_id"),
            "human_authored": False,
            "source_refs": ["A005", "D005", "A006"],
            "explanation_summary": "I preserved that G001 and G002 remained unresolved.",
            "responsibility_statement": "The action preserved the need for evidence and Game Master review.",
            "approval_state_interpretation": "Explicit approval remained absent and unresolved.",
            "evidence_gap_statement": "G001 and G002 remained visible.",
            "uncertainty_statement": "The trace did not resolve approval, exception authority, or payment readiness.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model},
            provider=self.provider,
            model=self.model,
        )


class Phase4S20DownstreamThresholdPilotTest(unittest.TestCase):
    def test_s20_downstream_threshold_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "threshold"
            action_sequence = ["hold_payment", "authorize_exception_review", "request_more_evidence", "escalate", "prepare_payment"] * 4
            run_phase4_s20_downstream_accounting_threshold_diagnostic(
                output_root=tmp_path / "runs" / "threshold",
                curated_output=curated_output,
                accountant_provider=ThresholdActionStubProvider(action_sequence),
                explanation_provider=ThresholdExplanationStubProvider(),
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S20-DOWNSTREAM-ACCOUNTING-THRESHOLD-0001")
            self.assertEqual(aggregate["scenario_id"], "S20")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S20 downstream-accounting threshold diagnostic")
            self.assertEqual(aggregate["validation_summary"], {"pass": 20, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["failure_mode_summary"]["SL2"]["observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["SL3"]["candidate"], 4)
            self.assertEqual(aggregate["failure_mode_summary"]["SL4"]["not_observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["SL5"]["observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["SL6"]["not_observed"], 20)
            self.assertEqual(aggregate["failure_mode_summary"]["FM3"]["candidate"], 8)
            self.assertEqual(aggregate["failure_mode_summary"]["FM6"]["not_observed"], 20)
            self.assertEqual(review_manifest["review_decision_counts"]["not_applicable"], 1)
            self.assertEqual(review_manifest["review_decision_counts"]["supported_for_reviewed_evidence"], 2)
            self.assertEqual(review_manifest["review_decision_counts"]["partially_supported_needs_revision"], 1)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005", "A006"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005", "A006"})
            self.assertTrue((representative_pack / "threshold_conditions" / "accountant_threshold_condition.json").exists())
            self.assertTrue((representative_pack / "role_views" / "accountant_downstream_threshold_review.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_A006_downstream_threshold_review.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected accountant_downstream_threshold_review action has a Game Master decision", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
