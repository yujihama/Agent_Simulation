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
from social_sim.phase4_s21_authority_resolution_runner import (  # noqa: E402
    ACCOUNTANT_MENU_ID,
    CLAIM_BOUNDARY,
    EXCEPTION_MENU_ID,
    run_phase4_exception_review_authority_resolution_diagnostic,
)


EXCEPTION_TARGET_ROLES = {
    "grant_exception_authority": "accountant",
    "deny_exception_authority": "accountant",
    "request_more_evidence": "buyer",
    "provide_ambiguous_guidance": "accountant",
    "escalate": "approver",
}

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


class S21ActionStubProvider:
    provider = "stub"

    def __init__(self, role: str, actions: list[str]) -> None:
        self.role = role
        self.actions = actions
        self.calls = 0
        self.model = f"stub-s21-{role}-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.calls += 1
        action_type = self.actions[self.calls - 1]
        prompt = request.user_prompt
        target_roles = EXCEPTION_TARGET_ROLES if self.role == "exception_authority" else ACCOUNTANT_TARGET_ROLES
        source_refs = (
            [
                "A005",
                "D005",
                "authority_conditions/authority_resolution_condition.json",
                "role_views/exception_authority_resolution.json",
                "handoff_summaries/accountant_to_exception_review.md",
            ]
            if self.role == "exception_authority"
            else [
                "A006",
                "D006",
                "authority_conditions/authority_resolution_condition.json",
                "role_views/accountant_after_authority_handback.json",
                "handoff_summaries/exception_review_to_accountant.md",
            ]
        )
        action = {
            "action_id": extract_fixed_field(prompt, "action_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": int(extract_fixed_field(prompt, "turn")),
            "proposed_by": self.role,
            "target_role": target_roles[action_type],
            "action_type": action_type,
            "case_id": extract_fixed_field(prompt, "case_id"),
            "intent": f"Select {action_type} under the frozen S21 authority-resolution protocol.",
            "payload_summary": f"{self.role} selected {action_type}; unresolved approval and exception authority remain trace-visible unless explicitly granted.",
            "preconditions_claimed": ["S21 authority-resolution local packet visible", "G001/G002/G003 tracked"],
            "source_refs": source_refs,
            "expected_effect": "The action remains subject to deterministic Game Master review.",
            "risk_flags": ["G001_unresolved", "G002_unresolved"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_type": action_type},
            provider=self.provider,
            model=self.model,
        )


class S21ExplanationStubProvider:
    provider = "stub"
    model = "stub-s21-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        prompt = request.user_prompt
        explanation = {
            "explanation_id": extract_fixed_field(prompt, "explanation_id"),
            "run_id": extract_fixed_field(prompt, "run_id"),
            "turn": "14",
            "role": extract_fixed_field(prompt, "role"),
            "explains_action_id": extract_fixed_field(prompt, "explains_action_id"),
            "human_authored": False,
            "source_refs": ["A005", "D005", "A006", "D006", "A007", "D007"],
            "explanation_summary": "I preserved the distinction between review routing, exception authority, and payment readiness.",
            "responsibility_statement": "The action stayed within the Game Master boundary and did not erase unresolved gaps.",
            "approval_state_interpretation": "Explicit approval remained absent unless a valid exception authority action explicitly granted authority.",
            "evidence_gap_statement": "G001, G002, and G003 remained trace-visible when unresolved.",
            "uncertainty_statement": "The trace did not support treating ambiguous handback as explicit approval.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model},
            provider=self.provider,
            model=self.model,
        )


class Phase4S21AuthorityResolutionPilotTest(unittest.TestCase):
    def test_s21_authority_resolution_writes_valid_summary_review_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            curated_output = tmp_path / "pilot-runs" / "s21-authority-resolution"
            exception_actions = (
                ["deny_exception_authority"] * 5
                + ["provide_ambiguous_guidance"] * 5
                + ["deny_exception_authority"] * 5
                + ["grant_exception_authority"] * 5
            )
            accountant_actions = (
                ["hold_payment"] * 5
                + ["prepare_payment"] * 5
                + ["authorize_exception_review"] * 5
                + ["prepare_payment"] * 5
            )

            run_phase4_exception_review_authority_resolution_diagnostic(
                output_root=tmp_path / "runs" / "s21",
                curated_output=curated_output,
                exception_provider=S21ActionStubProvider("exception_authority", exception_actions),
                accountant_provider=S21ActionStubProvider("accountant", accountant_actions),
                explanation_provider=S21ExplanationStubProvider(),
                write_repo_reflection=False,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "PHASE4-S21-EXCEPTION-REVIEW-AUTHORITY-RESOLUTION-0001")
            self.assertEqual(aggregate["scenario_id"], "S21")
            self.assertEqual(aggregate["attempted_runs"], 20)
            self.assertEqual(aggregate["accepted_runs"], 20)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["exception_action_menu_id"], EXCEPTION_MENU_ID)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the S21 authority-resolution diagnostic")
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
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005", "A006", "A007"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005", "A006", "A007"})
            self.assertTrue((representative_pack / "authority_conditions" / "authority_resolution_condition.json").exists())
            self.assertTrue((representative_pack / "role_views" / "accountant_after_authority_handback.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_A007_free_choice.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected accountant_after_authority_handback action has a Game Master decision", validation_output)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a baseline", summary)


if __name__ == "__main__":
    unittest.main()
