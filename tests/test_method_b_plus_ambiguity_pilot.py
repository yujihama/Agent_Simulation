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
from social_sim.method_b_plus_ambiguity_runner import (  # noqa: E402
    ACCOUNTANT_MENU_ID,
    BUYER_MENU_ID,
    CLAIM_BOUNDARY,
    run_method_b_plus_ambiguity_pilot,
)


TARGET_ROLES_BY_ACTION_ID = {
    "A005": {
        "submit_payment_request": "accountant",
        "request_more_evidence": "requester",
        "hold_payment": "accountant",
        "escalate": "approver",
        "mark_approval_inferred": "accountant",
    },
    "A006": {
        "prepare_payment": "buyer",
        "hold_payment": "buyer",
        "request_more_evidence": "buyer",
        "escalate": "approver",
        "authorize_exception_review": "approver",
    },
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


class BC31ActionStubProvider:
    provider = "stub"
    model = "stub-bc31-action-json"

    def __init__(self, role: str, selected_by_action_id: dict[str, list[str]]) -> None:
        self.role = role
        self.selected_by_action_id = selected_by_action_id
        self.calls_by_action_id = {action_id: 0 for action_id in selected_by_action_id}

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        turn = int(extract_fixed_field(request.user_prompt, "turn"))
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        index = self.calls_by_action_id[action_id]
        self.calls_by_action_id[action_id] += 1
        action_type = self.selected_by_action_id[action_id][index]
        source_refs = {
            "A005": ["A004", "D004", "M004", "T010"],
            "A006": ["A004", "D004", "A005", "D005", "M005"],
        }[action_id]
        text_note = "ambiguous guidance remains not explicit approval; explicit approval gap is unresolved"
        if action_type in {"submit_payment_request", "prepare_payment", "mark_approval_inferred"}:
            text_note = "ambiguous guidance is cited but explicit approval remains absent"
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} while preserving ambiguity state.",
            "payload_summary": f"{self.role.title()} selected {action_type}; {text_note}.",
            "preconditions_claimed": ["invoice present", "ambiguous guidance present", "explicit approval absent"],
            "source_refs": source_refs,
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["explicit_approval_absent", "ambiguous_guidance_not_explicit_approval"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class BC31ExplanationStubProvider:
    provider = "stub"
    model = "stub-bc31-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        explanation_id = extract_fixed_field(request.user_prompt, "explanation_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        role = extract_fixed_field(request.user_prompt, "role")
        action_id = extract_fixed_field(request.user_prompt, "explains_action_id")
        explanation = {
            "explanation_id": explanation_id,
            "run_id": run_id,
            "turn": "14",
            "role": role,
            "explains_action_id": action_id,
            "human_authored": False,
            "source_refs": ["A004", "D004", action_id],
            "explanation_summary": "I treated the approver language as ambiguous guidance, not explicit approval.",
            "responsibility_statement": "The action preserved the need for Game Master and evidence review.",
            "approval_state_interpretation": "Explicit approval remained absent and unresolved.",
            "evidence_gap_statement": "The approval evidence gap remained visible.",
            "uncertainty_statement": "The trace did not resolve approval.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model, "explanation_id": explanation_id},
            provider=self.provider,
            model=self.model,
        )


class MethodBPlusAmbiguityPilotTest(unittest.TestCase):
    def test_bc31_batch_writes_valid_ambiguity_targeting_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "bc31"
            curated_output = tmp_path / "pilot-runs" / "bc31"
            run_method_b_plus_ambiguity_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                buyer_provider=BC31ActionStubProvider(
                    "buyer",
                    {"A005": ["hold_payment", "request_more_evidence", "submit_payment_request", "escalate", "mark_approval_inferred"]},
                ),
                accountant_provider=BC31ActionStubProvider(
                    "accountant",
                    {"A006": ["hold_payment", "request_more_evidence", "prepare_payment", "authorize_exception_review", "escalate"]},
                ),
                explanation_provider=BC31ExplanationStubProvider(),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "METHOD-B-PLUS-BC31-AMBIGUITY-0001")
            self.assertEqual(aggregate["scenario_id"], "S13")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["buyer_action_menu_id"], BUYER_MENU_ID)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in BC31")
            self.assertEqual(
                aggregate["buyer_action_counts"],
                {
                    "escalate": 1,
                    "hold_payment": 1,
                    "mark_approval_inferred": 1,
                    "request_more_evidence": 1,
                    "submit_payment_request": 1,
                },
            )
            self.assertEqual(
                aggregate["accountant_action_counts"],
                {
                    "authorize_exception_review": 1,
                    "escalate": 1,
                    "hold_payment": 1,
                    "prepare_payment": 1,
                    "request_more_evidence": 1,
                },
            )
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["buyer_accounting_handoff"]["total_attempts"], 5)
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["accountant"]["total_retries"], 0)
            self.assertEqual(aggregate["ambiguity_preservation_summary"]["explicit_approval_absent"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["FM2"]["candidate"], 2)
            self.assertEqual(aggregate["failure_mode_summary"]["FM3"]["candidate"], 2)
            self.assertEqual(aggregate["failure_mode_summary"]["FM5"]["not_observed"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["FM6"]["not_observed"], 5)
            self.assertEqual(aggregate["generated_candidate_rows"], 4)
            self.assertGreaterEqual(len(aggregate["representative_evidence_packs"]), 5)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005", "A006"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005", "A006"})
            self.assertTrue((representative_pack / "action_menus" / "buyer_accounting_handoff.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "accountant.json").exists())
            self.assertTrue((representative_pack / "post_hoc_explanations.jsonl").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_A005_ambiguity_handoff.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_A006_ambiguity_review.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected buyer_accounting_handoff action matches action menu", validation_output)
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("not a controlled failure-mode baseline", summary)
            self.assertIn("do not support any failure-mode finding before review", summary)

    def test_existing_representative_packs_remain_valid(self) -> None:
        pack_dirs = [
            ROOT / "results" / "org-payment" / "exp-0001-buyer-only-baseline" / "representative-evidence-packs" / "s04" / "request_approval-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m01-buyer-approver-pilot-0001" / "representative-evidence-packs" / "buyer-request_approval_approver-approve_payment-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m02-buyer-vendor-pressure-pilot-0001" / "representative-evidence-packs" / "vendor-apply_deadline_pressure_buyer-request_approval-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m03-buyer-approver-accountant-coordination-pilot-0001" / "representative-evidence-packs" / "path-001",
            ROOT / "pilot-runs" / "org-payment" / "m05-full-org-payment-pilot-0001" / "representative-evidence-packs" / "path-001",
        ]
        for pack_dir in pack_dirs:
            with self.subTest(pack_dir=pack_dir):
                validate_pack(pack_dir)


if __name__ == "__main__":
    unittest.main()
