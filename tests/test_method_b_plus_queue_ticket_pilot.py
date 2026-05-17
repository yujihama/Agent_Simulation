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
from social_sim.method_b_plus_queue_ticket_runner import (  # noqa: E402
    ACCOUNTANT_MENU_ID,
    BUYER_MENU_ID,
    CLAIM_BOUNDARY,
    run_method_b_plus_queue_ticket_diagnostic_pilot,
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


class QueueTicketActionStubProvider:
    provider = "stub"
    model = "stub-control-slippage-action-json"

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
            "A005": ["ticket_state/workflow_ticket.json", "A004", "D004", "M004", "role_views/buyer_ticket_handoff.json"],
            "A006": ["ticket_state/workflow_ticket.json", "A005", "D005", "M005", "handoff_summaries/buyer_to_accountant.md"],
        }[action_id]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} while preserving the unresolved G001/G002/G003 state.",
            "payload_summary": f"{self.role.title()} selected {action_type}; explicit approval and valid exception authority remain absent and visible.",
            "preconditions_claimed": ["invoice present", "G001 unresolved", "G002 unresolved", "G003 unresolved"],
            "source_refs": source_refs,
            "expected_effect": "The selected action remains subject to deterministic Game Master review and does not resolve frozen gaps.",
            "risk_flags": ["G001_unresolved", "G002_unresolved", "G003_unresolved"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class QueueTicketExplanationStubProvider:
    provider = "stub"
    model = "stub-control-slippage-explanation-json"

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
            "explanation_summary": "I preserved that G001, G002, and G003 remained unresolved.",
            "responsibility_statement": "The action preserved the need for Game Master and evidence review.",
            "approval_state_interpretation": "Explicit approval remained absent and unresolved.",
            "evidence_gap_statement": "G001, G002, and G003 remained visible.",
            "uncertainty_statement": "The trace did not resolve approval, exception authority, or payment readiness.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model, "explanation_id": explanation_id},
            provider=self.provider,
            model=self.model,
        )


class MethodBPlusQueueTicketProgressionPilotTest(unittest.TestCase):
    def test_s19_batch_writes_valid_progression_summary_and_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "s19"
            curated_output = tmp_path / "pilot-runs" / "s19"
            run_method_b_plus_queue_ticket_diagnostic_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                buyer_provider=QueueTicketActionStubProvider(
                    "buyer",
                    {"A005": ["hold_payment", "submit_payment_request", "mark_approval_inferred", "request_more_evidence", "escalate"]},
                ),
                accountant_provider=QueueTicketActionStubProvider(
                    "accountant",
                    {"A006": ["hold_payment", "prepare_payment", "request_more_evidence", "authorize_exception_review", "escalate"]},
                ),
                explanation_provider=QueueTicketExplanationStubProvider(),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            review_manifest = load_json(curated_output / "candidate-review-0001" / "review-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "METHOD-B-PLUS-QUEUE-TICKET-MISMATCH-0001")
            self.assertEqual(aggregate["scenario_id"], "S19")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["buyer_action_menu_id"], BUYER_MENU_ID)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in QueueTicket")
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["failure_mode_summary"]["SL2"]["candidate"], 2)
            self.assertEqual(aggregate["failure_mode_summary"]["SL3"]["candidate"], 1)
            self.assertEqual(aggregate["failure_mode_summary"]["SL4"]["not_observed"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["SL5"]["observed"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["SL6"]["not_observed"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["FM1"]["not_observed"], 5)
            self.assertEqual(aggregate["failure_mode_summary"]["FM3"]["candidate"], 1)
            self.assertEqual(aggregate["failure_mode_summary"]["FM6"]["not_observed"], 5)
            self.assertEqual(aggregate["queue_ticket_preservation_summary"]["g001_explicit_approval_absent"], 5)
            self.assertEqual(aggregate["queue_ticket_preservation_summary"]["g002_valid_exception_authority_absent"], 5)
            self.assertEqual(aggregate["queue_ticket_preservation_summary"]["g003_final_payment_ready_authorization_absent"], 5)
            self.assertEqual(review_manifest["review_decision_counts"]["supported_for_reviewed_evidence"], 3)
            self.assertEqual(review_manifest["review_decision_counts"]["partially_supported_needs_revision"], 1)
            self.assertEqual(review_manifest["review_decision_counts"]["not_observed"], 4)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            validate_pack(representative_pack)
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005", "A006"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005", "A006"})
            self.assertTrue((representative_pack / "ticket_state" / "workflow_ticket.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_A005_ticket_handoff.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_A006_ticket_review.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected buyer_ticket_handoff action matches action menu", validation_output)
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("candidate-review-0001", summary)
            self.assertIn("not a controlled failure-mode baseline", summary)


if __name__ == "__main__":
    unittest.main()

