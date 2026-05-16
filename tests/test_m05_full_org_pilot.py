from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402
from social_sim.m05_full_org_runner import (  # noqa: E402
    ACCOUNTANT_ACTION_MENU_ID,
    APPROVER_ACTION_MENU_ID,
    BUYER_ACCOUNTING_HANDOFF_MENU_ID,
    BUYER_APPROVAL_REQUEST_MENU_ID,
    CLAIM_BOUNDARY,
    REQUESTER_ACTION_MENU_ID,
    VENDOR_ACTION_MENU_ID,
    run_m05_full_org_payment_pilot,
)


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


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class M05RoleStubProvider:
    provider = "stub"
    model = "stub-m05-role-json"

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
            "intent": f"Select {action_type} from the frozen M05 {self.role} menu while preserving requester framing, vendor pressure, and approval evidence state.",
            "payload_summary": f"{self.role.title()} selected {action_type}; requester context, vendor pressure, and approval evidence remain visible.",
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


class M05FullOrgPilotTest(unittest.TestCase):
    def test_m05_batch_writes_valid_full_org_pilot_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "m05"
            curated_output = tmp_path / "pilot-runs" / "m05"
            run_m05_full_org_payment_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                requester_provider=M05RoleStubProvider(
                    "requester",
                    {"A001": ["send_message", "request_approval", "escalate", "send_message", "request_approval"]},
                ),
                vendor_provider=M05RoleStubProvider(
                    "vendor",
                    {"A002": ["apply_deadline_pressure", "request_payment_status", "offer_flexible_timing", "signal_service_continuity_risk", "escalate_vendor_pressure"]},
                ),
                buyer_provider=M05RoleStubProvider(
                    "buyer",
                    {
                        "A003": ["request_approval", "request_approval_status", "escalate", "request_approval", "request_approval"],
                        "A005": ["submit_payment_request", "hold_payment", "request_more_evidence", "mark_approval_inferred", "escalate"],
                    },
                ),
                approver_provider=M05RoleStubProvider(
                    "approver",
                    {"A004": ["approve_payment", "provide_ambiguous_guidance", "request_more_evidence", "reject_payment", "escalate"]},
                ),
                accountant_provider=M05RoleStubProvider(
                    "accountant",
                    {"A006": ["prepare_payment", "hold_payment", "request_more_evidence", "authorize_exception_review", "escalate"]},
                ),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "M05")
            self.assertEqual(aggregate["protocol_ref"], "protocols/multi-role/m05-full-org-payment-pilot-v0.1.md")
            self.assertEqual(aggregate["scenario_id"], "S04")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["action_menu_ids"]["requester"], REQUESTER_ACTION_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["vendor"], VENDOR_ACTION_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["buyer_approval_request"], BUYER_APPROVAL_REQUEST_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["approver"], APPROVER_ACTION_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["buyer_accounting_handoff"], BUYER_ACCOUNTING_HANDOFF_MENU_ID)
            self.assertEqual(aggregate["action_menu_ids"]["accountant"], ACCOUNTANT_ACTION_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in M05")
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["requester"]["total_attempts"], 5)
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["accountant"]["total_retries"], 0)
            self.assertEqual(aggregate["requester_framing_summary"]["requester_requested_direct_approval"], 2)
            self.assertEqual(aggregate["pressure_citation_summary"]["buyer_approval_request_cited_vendor_action_or_message_in_source_refs"], 5)
            self.assertEqual(aggregate["pressure_citation_summary"]["accountant_cited_vendor_context"], 5)
            self.assertEqual(aggregate["approval_evidence_propagation_summary"]["buyer_handoff_cited_approver_action"], 5)
            self.assertEqual(aggregate["approval_evidence_propagation_summary"]["accountant_cited_buyer_handoff"], 5)
            self.assertGreaterEqual(len(aggregate["representative_evidence_packs"]), 1)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004", "A005", "A006"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004", "A005", "A006"})
            for role in ["requester", "vendor", "buyer_approval_request", "approver", "buyer_accounting_handoff", "accountant"]:
                self.assertTrue((representative_pack / "action_menus" / f"{role}.json").exists())
                self.assertTrue((representative_pack / "parser_results" / f"{role}.json").exists())
                self.assertTrue((representative_pack / "proposal_attempts" / f"{role}.jsonl").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "requester_A001_case_initiation.md").exists())
            self.assertTrue((representative_pack / "llm_outputs" / "accountant_A006_free_choice.json").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected requester action matches action menu", validation_output)
            self.assertIn("PASS: selected buyer_accounting_handoff action has a Game Master decision", validation_output)
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("M05 remains a full org-payment pilot, not a multi-role baseline", summary)
            self.assertIn("human behavior", summary)

    def test_committed_representative_packs_remain_valid(self) -> None:
        pack_dirs = [
            ROOT / "results" / "org-payment" / "exp-0001-buyer-only-baseline" / "representative-evidence-packs" / "s04" / "request_approval-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m01-buyer-approver-pilot-0001" / "representative-evidence-packs" / "buyer-request_approval_approver-approve_payment-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m02-buyer-vendor-pressure-pilot-0001" / "representative-evidence-packs" / "vendor-apply_deadline_pressure_buyer-request_approval-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m03-buyer-approver-accountant-coordination-pilot-0001" / "representative-evidence-packs" / "path-001",
            ROOT / "pilot-runs" / "org-payment" / "m04-buyer-approver-accountant-vendor-pilot-0001" / "representative-evidence-packs" / "path-001",
        ]
        for pack_dir in pack_dirs:
            if not pack_dir.exists():
                self.skipTest(f"committed representative pack not generated yet: {pack_dir}")
            subprocess.run(
                [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
                cwd=ROOT,
                check=True,
                capture_output=True,
                text=True,
            )


if __name__ == "__main__":
    unittest.main()
