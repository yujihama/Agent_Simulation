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

from scripts.validate_evidence_pack import validate_pack

from social_sim.llm_actor import LLMRequest, LLMResponse
from social_sim.multi_role_sweep_runner import CLAIM_BOUNDARY, PROTOCOL_REF, SCENARIO_IDS, SWEEP_ID, run_multi_role_scenario_sweep_pilot


TARGET_ROLES_BY_ACTION_ID = {
    "A001": {
        "send_message": "buyer",
        "request_approval": "approver",
        "escalate": "approver",
    },
    "A002": {
        "request_payment_status": "buyer",
        "apply_deadline_pressure": "buyer",
        "signal_service_continuity_risk": "buyer",
        "offer_flexible_timing": "buyer",
        "escalate_vendor_pressure": "buyer",
    },
    "A003": {
        "request_approval": "approver",
        "request_approval_status": "approver",
        "escalate": "approver",
    },
    "A004": {
        "approve_payment": "buyer",
        "reject_payment": "buyer",
        "request_more_evidence": "buyer",
        "provide_ambiguous_guidance": "buyer",
        "escalate": "buyer",
    },
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


SOURCE_REFS_BY_ACTION_ID = {
    "A001": ["initial_state/case.md", "T001"],
    "A002": ["M001", "A001", "D001", "T004"],
    "A003": ["M001", "M002", "A001", "D001", "A002", "D002"],
    "A004": ["M003", "A003", "D003", "A002", "D002"],
    "A005": ["M004", "A004", "D004", "A002", "D002"],
    "A006": ["M005", "A005", "D005", "A004", "D004", "A002", "D002"],
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class SweepRoleStubProvider:
    provider = "stub"
    model = "stub-multi-role-sweep-json"

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
        risk_flags = ["vendor_deadline_pressure"] if action_id in {"A003", "A005", "A006"} else []
        if action_id == "A001" and action_type == "escalate":
            risk_flags.append("requester_operational_urgency")
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the frozen scenario sweep {self.role} menu while preserving scenario context.",
            "payload_summary": f"{self.role.title()} selected {action_type}; scenario conditions and approval evidence remain visible.",
            "preconditions_claimed": ["invoice present", "business reason present", "approval evidence must be preserved"],
            "source_refs": SOURCE_REFS_BY_ACTION_ID[action_id],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": risk_flags,
            "private_pressure_refs": ["A002", "D002", "M002"] if action_id in {"A003", "A005", "A006"} else [],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class MultiRoleScenarioSweepTest(unittest.TestCase):
    def test_sweep_writes_valid_scenario_aggregate_and_representatives(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "multi-role-sweep"
            curated_output = tmp_path / "pilot-runs" / "multi-role-sweep"
            run_multi_role_scenario_sweep_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                count_per_scenario=1,
                requester_provider=SweepRoleStubProvider(
                    "requester",
                    {"A001": ["send_message", "request_approval", "escalate", "send_message", "request_approval", "escalate"]},
                ),
                vendor_provider=SweepRoleStubProvider(
                    "vendor",
                    {"A002": ["apply_deadline_pressure", "request_payment_status", "offer_flexible_timing", "signal_service_continuity_risk", "escalate_vendor_pressure", "apply_deadline_pressure"]},
                ),
                buyer_provider=SweepRoleStubProvider(
                    "buyer",
                    {
                        "A003": ["request_approval", "request_approval_status", "escalate", "request_approval", "request_approval", "request_approval_status"],
                        "A005": ["submit_payment_request", "hold_payment", "request_more_evidence", "mark_approval_inferred", "escalate", "submit_payment_request"],
                    },
                ),
                approver_provider=SweepRoleStubProvider(
                    "approver",
                    {"A004": ["approve_payment", "request_more_evidence", "provide_ambiguous_guidance", "reject_payment", "escalate", "approve_payment"]},
                ),
                accountant_provider=SweepRoleStubProvider(
                    "accountant",
                    {"A006": ["prepare_payment", "hold_payment", "request_more_evidence", "authorize_exception_review", "escalate", "prepare_payment"]},
                ),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["sweep_id"], SWEEP_ID)
            self.assertEqual(aggregate["protocol_ref"], PROTOCOL_REF)
            self.assertEqual(aggregate["scenario_set"], SCENARIO_IDS)
            self.assertEqual(aggregate["attempted_runs"], 6)
            self.assertEqual(aggregate["accepted_runs"], 6)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in the multi-role scenario sweep")
            self.assertEqual(aggregate["validation_summary"], {"pass": 6, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 6)
            self.assertIn("action_menu_ids", aggregate)

            for scenario_id in SCENARIO_IDS:
                scenario_item = aggregate["scenarios"][scenario_id]
                self.assertEqual(scenario_item["attempted_runs"], 1)
                self.assertEqual(scenario_item["accepted_runs"], 1)
                self.assertEqual(scenario_item["excluded_runs"], 0)
                self.assertEqual(scenario_item["validation_summary"], {"pass": 1, "fail": 0, "pass_rate_included": 1.0})
                self.assertTrue(scenario_item["full_org_payment_path_counts"])

            for representative in aggregate["representative_evidence_packs"]:
                pack_dir = curated_output / representative["evidence_pack"]
                validate_pack(pack_dir)
                scenario_yaml = (pack_dir / "scenario.yaml").read_text(encoding="utf-8")
                self.assertIn(f"id: {representative['scenario_id']}", scenario_yaml)
                menu = load_json(pack_dir / "action_menus" / "requester.json")
                self.assertEqual(menu["scenario_id"], representative["scenario_id"])
                validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
                self.assertIn("PASS: selected requester action matches action menu", validation_output)
                self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("scenario sweep pilot, not a multi-role baseline", summary)
            self.assertIn("human behavior", summary)


if __name__ == "__main__":
    unittest.main()
