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
from social_sim.method_b_plus_responsibility_runner import (  # noqa: E402
    ACCOUNTANT_ACTION_MENU_ID,
    APPROVER_ACTION_MENU_ID,
    BUYER_ACCOUNTING_HANDOFF_MENU_ID,
    BUYER_APPROVAL_REQUEST_MENU_ID,
    CLAIM_BOUNDARY,
    run_bc32_coordination_pilot,
)


TARGET_ROLES_BY_ACTION_ID = {
    "A001": {
        "request_approval": "approver",
        "request_approval_status": "approver",
        "request_more_evidence": "requester",
        "escalate": "approver",
    },
    "A002": {
        "approve_payment": "buyer",
        "reject_payment": "buyer",
        "request_more_evidence": "buyer",
        "provide_ambiguous_guidance": "buyer",
        "escalate": "buyer",
    },
    "A003": {
        "submit_payment_request": "accountant",
        "request_more_evidence": "requester",
        "hold_payment": "accountant",
        "escalate": "approver",
        "mark_approval_inferred": "accountant",
    },
    "A004": {
        "prepare_payment": "buyer",
        "hold_payment": "buyer",
        "request_more_evidence": "buyer",
        "escalate": "approver",
        "authorize_exception_review": "approver",
    },
}


SOURCE_REFS_BY_ACTION_ID = {
    "A001": ["initial_state/case.md", "M001", "M002", "T001"],
    "A002": ["A001", "D001", "M001", "M002", "T005"],
    "A003": ["A001", "D001", "A002", "D002", "M003", "T009"],
    "A004": ["A002", "D002", "A003", "D003", "M004", "T012"],
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


class BC32ActionStubProvider:
    provider = "stub"
    model = "stub-bc32-action-json"

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
        explicit_note = "explicit approval remains absent and the role boundary is preserved"
        if action_type in {"submit_payment_request", "mark_approval_inferred", "prepare_payment"}:
            explicit_note = "this action moves payment handling forward while explicit approval remains absent"
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} while keeping decision ownership visible.",
            "payload_summary": f"{self.role.title()} selected {action_type}; {explicit_note}.",
            "preconditions_claimed": ["invoice present", "explicit approval absent", "role boundary visible"],
            "source_refs": SOURCE_REFS_BY_ACTION_ID[action_id],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["explicit_approval_absent", "decision_owner_boundary_visible"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class BC32ExplanationStubProvider(BC32ActionStubProvider):
    model = "stub-bc32-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        if "- `explanation_id`:" not in request.user_prompt:
            return super().complete_json(request)
        explanation_id = extract_fixed_field(request.user_prompt, "explanation_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        role = extract_fixed_field(request.user_prompt, "role")
        action_id = extract_fixed_field(request.user_prompt, "explains_action_id")
        explanation = {
            "explanation_id": explanation_id,
            "run_id": run_id,
            "turn": "11",
            "role": role,
            "explains_action_id": action_id,
            "human_authored": False,
            "source_refs": [action_id, "D002", "D003"],
            "explanation_summary": "I preserved that explicit approval was missing or unresolved in the trace.",
            "responsibility_statement": "The handoff kept the approver, buyer, accountant, and Game Master boundaries visible.",
            "approval_state_interpretation": "Explicit approval was absent unless A002 was approve_payment.",
            "evidence_gap_statement": "The approval evidence gap remained visible.",
            "uncertainty_statement": "The trace did not resolve every ownership question.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model, "explanation_id": explanation_id},
            provider=self.provider,
            model=self.model,
        )


class MethodBPlusResponsibilityBoundaryPilotTest(unittest.TestCase):
    def test_bc32_batch_writes_valid_responsibility_boundary_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "bc32"
            curated_output = tmp_path / "pilot-runs" / "bc32"
            buyer = BC32ExplanationStubProvider(
                "buyer",
                {
                    "A001": ["request_approval_status", "request_approval", "escalate", "request_more_evidence", "request_approval_status"],
                    "A003": ["hold_payment", "submit_payment_request", "mark_approval_inferred", "request_more_evidence", "escalate"],
                },
            )
            approver = BC32ExplanationStubProvider(
                "approver",
                {"A002": ["provide_ambiguous_guidance", "request_more_evidence", "escalate", "reject_payment", "approve_payment"]},
            )
            accountant = BC32ExplanationStubProvider(
                "accountant",
                {"A004": ["hold_payment", "prepare_payment", "request_more_evidence", "authorize_exception_review", "prepare_payment"]},
            )

            run_bc32_coordination_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                buyer_provider=buyer,
                approver_provider=approver,
                accountant_provider=accountant,
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "METHOD-B-PLUS-BC32-RESPONSIBILITY-BOUNDARY-0001")
            self.assertEqual(aggregate["scenario_id"], "S15")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["buyer_approval_request_menu_id"], BUYER_APPROVAL_REQUEST_MENU_ID)
            self.assertEqual(aggregate["approver_action_menu_id"], APPROVER_ACTION_MENU_ID)
            self.assertEqual(aggregate["buyer_accounting_handoff_menu_id"], BUYER_ACCOUNTING_HANDOFF_MENU_ID)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_ACTION_MENU_ID)
            self.assertEqual(manifest["scenario_ref"], "scenarios/org-payment/s15-responsibility-boundary-stress.yaml")
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertGreaterEqual(aggregate["failure_mode_summary"]["FM2"].get("candidate", 0), 1)
            self.assertGreaterEqual(aggregate["generated_candidate_rows"], 1)
            self.assertIn("buyer_handoff_cites_approver_or_decision", aggregate["responsibility_boundary_summary"])

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            explanations = load_jsonl(representative_pack / "post_hoc_explanations.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004"})
            self.assertEqual({item["explanation_id"] for item in explanations}, {"X001", "X002", "X003"})
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_X001_A003_post_hoc_explanation.md").exists())
            self.assertTrue((representative_pack / "llm_outputs" / "accountant_X003_A004_post_hoc_explanation.json").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected buyer_approval_request action matches action menu", validation_output)
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            candidate_table = (curated_output / "event-candidate-table.csv").read_text(encoding="utf-8")
            self.assertIn("responsibility_diffusion", candidate_table)
            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate/not-observed accounting only", summary)
            self.assertIn("do not support any failure-mode finding before review", summary)


if __name__ == "__main__":
    unittest.main()
