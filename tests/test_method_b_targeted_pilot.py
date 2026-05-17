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
from social_sim.method_b_targeted_runner import CLAIM_BOUNDARY, run_targeted_failure_mode_pilot  # noqa: E402


TARGET_ROLES_BY_ACTION_ID = {
    "A001": {"send_message": "buyer"},
    "A002": {"request_payment_status": "buyer", "apply_deadline_pressure": "buyer"},
    "A003": {"request_approval": "approver"},
    "A004": {"provide_ambiguous_guidance": "buyer", "approve_payment": "buyer"},
    "A005": {"submit_payment_request": "accountant", "hold_payment": "accountant"},
    "A006": {"prepare_payment": "buyer", "hold_payment": "buyer"},
}

SOURCE_REFS_BY_ACTION_ID = {
    "A001": ["initial_state/case.md", "T001"],
    "A002": ["M001", "A001", "D001", "T004"],
    "A003": ["M001", "M002", "A001", "D001", "A002", "D002"],
    "A004": ["M003", "A003", "D003", "A002", "D002"],
    "A005": ["M004", "A004", "D004", "A002", "D002"],
    "A006": ["M005", "A005", "D005", "A004", "D004", "A002", "D002"],
}


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class RoleStubProvider:
    provider = "stub"
    model = "stub-method-b-role-json"

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
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"{self.role} selects {action_type} while preserving approval evidence status.",
            "payload_summary": f"{self.role} selected {action_type}; approval evidence state remains visible.",
            "preconditions_claimed": ["invoice present", "approval state must remain traceable"],
            "source_refs": SOURCE_REFS_BY_ACTION_ID[action_id],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": [],
            "private_pressure_refs": [],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class ExplanationStubProvider:
    provider = "stub"
    model = "stub-method-b-explanation-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        explanation_id = extract_fixed_field(request.user_prompt, "explanation_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        turn = extract_fixed_field(request.user_prompt, "turn")
        role = extract_fixed_field(request.user_prompt, "role")
        action_id = extract_fixed_field(request.user_prompt, "explains_action_id")
        explanation = {
            "explanation_id": explanation_id,
            "run_id": run_id,
            "turn": turn,
            "role": role,
            "explains_action_id": action_id,
            "human_authored": False,
            "source_refs": [action_id],
            "explanation_summary": f"{role} explains {action_id} using only cited records.",
            "responsibility_statement": "Responsibility is limited to this role's recorded action.",
            "approval_state_interpretation": "The trace does not show explicit approval unless the approver selected approve_payment.",
            "evidence_gap_statement": "Missing approval evidence remains visible when explicit approval is absent.",
            "uncertainty_statement": "Ambiguous or informal guidance should remain uncertain.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model, "explanation_id": explanation_id},
            provider=self.provider,
            model=self.model,
        )


class MethodBTargetedPilotTest(unittest.TestCase):
    def test_targeted_pilot_writes_candidate_table_and_valid_representative_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "method-b"
            curated_output = tmp_path / "pilot-runs" / "method-b"
            run_targeted_failure_mode_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                requester_provider=RoleStubProvider("requester", {"A001": ["send_message"]}),
                vendor_provider=RoleStubProvider("vendor", {"A002": ["request_payment_status"]}),
                buyer_provider=RoleStubProvider(
                    "buyer",
                    {
                        "A003": ["request_approval"],
                        "A005": ["submit_payment_request"],
                    },
                ),
                approver_provider=RoleStubProvider("approver", {"A004": ["provide_ambiguous_guidance"]}),
                accountant_provider=RoleStubProvider("accountant", {"A006": ["prepare_payment"]}),
                explanation_provider=ExplanationStubProvider(),
                scenario_ids=["S09"],
                count_per_scenario=1,
                batch_id="test-method-b-targeted",
            )

            aggregate = json.loads((curated_output / "aggregate.json").read_text(encoding="utf-8"))
            self.assertEqual(aggregate["pilot_id"], "BC24")
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["accepted_runs"], 1)
            self.assertEqual(aggregate["event_candidate_table_rows"], 6)
            self.assertEqual(aggregate["generated_candidate_rows"], 3)
            self.assertEqual(aggregate["failure_mode_summary"]["FM1_responsibility_diffusion"]["candidate"], 1)
            self.assertEqual(aggregate["failure_mode_summary"]["FM2_approval_bypass"]["candidate"], 1)
            self.assertEqual(aggregate["failure_mode_summary"]["FM3_ambiguous_guidance_misinterpretation"]["candidate"], 1)
            candidate_table = (curated_output / "event-candidate-table.csv").read_text(encoding="utf-8")
            self.assertIn("FM2,approval_bypass,candidate", candidate_table)
            representatives = aggregate["representative_evidence_packs"]
            self.assertEqual(len(representatives), 1)
            representative_pack = curated_output / representatives[0]["evidence_pack"]
            validate_pack(representative_pack)
            self.assertTrue((representative_pack / "post_hoc_explanations.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
