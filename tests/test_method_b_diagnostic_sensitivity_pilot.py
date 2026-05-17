from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from scripts.validate_evidence_pack import validate_pack  # noqa: E402
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402
from social_sim.method_b_diagnostic_runner import (  # noqa: E402
    CLAIM_BOUNDARY,
    ROLE_PROMPT_ADDENDUM_REF,
    run_method_b_diagnostic_sensitivity_pilot,
)


TARGET_ROLES_BY_ACTION_ID = {
    "A001": {"send_message": "buyer"},
    "A002": {"request_payment_status": "buyer"},
    "A003": {"request_approval": "approver"},
    "A004": {"provide_ambiguous_guidance": "buyer"},
    "A005": {"submit_payment_request": "accountant"},
    "A006": {"prepare_payment": "buyer"},
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


class DiagnosticRoleStubProvider:
    provider = "stub"
    model = "stub-method-b-diagnostic-role-json"

    def __init__(self, role: str, selected_by_action_id: dict[str, str]) -> None:
        self.role = role
        self.selected_by_action_id = selected_by_action_id
        self.prompts: list[str] = []

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        self.prompts.append(request.user_prompt)
        if "Frozen Diagnostic Addendum" not in request.user_prompt:
            raise AssertionError("diagnostic addendum was not appended to role prompt")
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        turn = int(extract_fixed_field(request.user_prompt, "turn"))
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        action_type = self.selected_by_action_id[action_id]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"{self.role} selects {action_type} under the diagnostic addendum while preserving approval evidence status.",
            "payload_summary": f"{self.role} selected {action_type}; evidence gaps remain visible.",
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


class DiagnosticExplanationStubProvider:
    provider = "stub"
    model = "stub-method-b-diagnostic-explanation-json"

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
            "uncertainty_statement": "Ambiguous or informal guidance remains uncertain.",
            "claim_boundary": "post_hoc_explanation_artifact_only",
        }
        return LLMResponse(
            text=json.dumps(explanation),
            raw_response={"stub": True, "model": self.model, "explanation_id": explanation_id},
            provider=self.provider,
            model=self.model,
        )


class MethodBDiagnosticSensitivityPilotTest(unittest.TestCase):
    def test_diagnostic_pilot_appends_addendum_and_writes_reference_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "method-b-diagnostic"
            curated_output = tmp_path / "pilot-runs" / "method-b-diagnostic"
            requester = DiagnosticRoleStubProvider("requester", {"A001": "send_message"})
            run_method_b_diagnostic_sensitivity_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                requester_provider=requester,
                vendor_provider=DiagnosticRoleStubProvider("vendor", {"A002": "request_payment_status"}),
                buyer_provider=DiagnosticRoleStubProvider(
                    "buyer",
                    {
                        "A003": "request_approval",
                        "A005": "submit_payment_request",
                    },
                ),
                approver_provider=DiagnosticRoleStubProvider("approver", {"A004": "provide_ambiguous_guidance"}),
                accountant_provider=DiagnosticRoleStubProvider("accountant", {"A006": "prepare_payment"}),
                explanation_provider=DiagnosticExplanationStubProvider(),
                scenario_ids=["S09"],
                count_per_scenario=1,
                batch_id="test-method-b-diagnostic",
            )

            aggregate = json.loads((curated_output / "aggregate.json").read_text(encoding="utf-8"))
            self.assertEqual(aggregate["pilot_id"], "METHOD-B-DSP-0001")
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["role_prompt_addendum_ref"], ROLE_PROMPT_ADDENDUM_REF)
            self.assertEqual(aggregate["single_axis_change"], ROLE_PROMPT_ADDENDUM_REF)
            self.assertEqual(aggregate["accepted_runs"], 1)
            self.assertEqual(aggregate["event_candidate_table_rows"], 6)
            self.assertIn("reference_comparison", aggregate)
            self.assertTrue((curated_output / "reference-comparison.csv").exists())
            representatives = aggregate["representative_evidence_packs"]
            representative_pack = curated_output / representatives[0]["evidence_pack"]
            validate_pack(representative_pack)
            prompt_text = (representative_pack / "llm_prompts" / "requester_A001_case_initiation.md").read_text(encoding="utf-8")
            self.assertIn("Frozen Diagnostic Addendum", prompt_text)


if __name__ == "__main__":
    unittest.main()
