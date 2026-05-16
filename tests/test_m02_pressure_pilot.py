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
from social_sim.m02_pressure_runner import (  # noqa: E402
    BUYER_ACTION_MENU_ID,
    CLAIM_BOUNDARY,
    VENDOR_ACTION_MENU_ID,
    pressure_citation_flags,
    run_m02_buyer_vendor_pressure_pilot,
    vendor_action_has_pressure_context,
)


VENDOR_TARGET_ROLES = {
    "request_payment_status": "buyer",
    "apply_deadline_pressure": "buyer",
    "signal_service_continuity_risk": "buyer",
    "offer_flexible_timing": "buyer",
    "escalate_vendor_pressure": "buyer",
}

BUYER_TARGET_ROLES = {
    "request_approval": "approver",
    "request_more_evidence": "requester",
    "hold_payment": "accountant",
    "escalate": "approver",
    "mark_approval_inferred": "accountant",
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


class M02RoleStubProvider:
    provider = "stub"
    model = "stub-m02-role-json"

    def __init__(self, role: str, selected_actions: list[str]) -> None:
        self.role = role
        self.selected_actions = selected_actions
        self.calls = 0

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        action_type = self.selected_actions[self.calls]
        self.calls += 1
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        turn = int(extract_fixed_field(request.user_prompt, "turn"))
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        if self.role == "vendor":
            target_role = VENDOR_TARGET_ROLES[action_type]
            source_refs = ["initial_state/case.md", "T001"]
            risk_flags = ["bounded_vendor_pressure_context"] if action_type != "offer_flexible_timing" else []
            private_pressure_refs: list[str] = []
        else:
            target_role = BUYER_TARGET_ROLES[action_type]
            source_refs = ["M001", "A001", "D001"]
            risk_flags = ["vendor_pressure_context", "approval_evidence_gap"]
            private_pressure_refs = ["M001", "A001"]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": target_role,
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the frozen M02 {self.role} action menu while recording vendor pressure context.",
            "payload_summary": f"{self.role.title()} selected {action_type} in the M02 stub pressure pilot with vendor pressure context preserved.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval unresolved"],
            "source_refs": source_refs,
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": risk_flags,
            "private_pressure_refs": private_pressure_refs,
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class M02PressurePilotTest(unittest.TestCase):
    def test_request_payment_status_does_not_turn_generic_delay_text_into_pressure(self) -> None:
        vendor_action = {
            "action_type": "request_payment_status",
            "intent": "Ask for payment status without expedited handling.",
            "payload_summary": "Vendor requested status and mentioned generic delay.",
            "risk_flags": ["vendor_delay"],
        }
        buyer_action = {
            "source_refs": ["A001", "D001", "M001"],
            "risk_flags": ["vendor_dissatisfaction", "payment_delay"],
            "private_pressure_refs": ["A001", "D001", "M001"],
            "intent": "Request approval because the vendor may be dissatisfied by delay.",
            "payload_summary": "Buyer preserved vendor delay context.",
        }

        self.assertFalse(vendor_action_has_pressure_context(vendor_action))
        self.assertEqual(
            pressure_citation_flags(buyer_action, pressure_context_present=vendor_action_has_pressure_context(vendor_action)),
            {
                "source_refs": True,
                "risk_flags": False,
                "private_pressure_refs": False,
                "intent": False,
                "payload_summary": False,
            },
        )

    def test_deadline_pressure_action_allows_pressure_citation_flags(self) -> None:
        vendor_action = {
            "action_type": "apply_deadline_pressure",
            "intent": "Apply a same-day deadline.",
            "payload_summary": "Vendor emphasized urgency.",
            "risk_flags": ["deadline_pressure"],
        }
        buyer_action = {
            "source_refs": ["A001", "D001", "M001"],
            "risk_flags": ["vendor_pressure_context", "approval_evidence_gap"],
            "private_pressure_refs": ["A001", "D001", "M001"],
            "intent": "Request approval while preserving vendor pressure.",
            "payload_summary": "Buyer preserved vendor pressure context.",
        }

        self.assertTrue(vendor_action_has_pressure_context(vendor_action))
        self.assertEqual(
            pressure_citation_flags(buyer_action, pressure_context_present=vendor_action_has_pressure_context(vendor_action)),
            {
                "source_refs": True,
                "risk_flags": True,
                "private_pressure_refs": True,
                "intent": True,
                "payload_summary": True,
            },
        )

    def test_m02_batch_writes_valid_pressure_pilot_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "m02"
            curated_output = tmp_path / "pilot-runs" / "m02"
            run_m02_buyer_vendor_pressure_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                vendor_provider=M02RoleStubProvider(
                    "vendor",
                    [
                        "request_payment_status",
                        "apply_deadline_pressure",
                        "signal_service_continuity_risk",
                        "offer_flexible_timing",
                        "escalate_vendor_pressure",
                    ],
                ),
                buyer_provider=M02RoleStubProvider(
                    "buyer",
                    [
                        "request_approval",
                        "hold_payment",
                        "request_more_evidence",
                        "escalate",
                        "mark_approval_inferred",
                    ],
                ),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "M02")
            self.assertEqual(aggregate["protocol_ref"], "protocols/multi-role/m02-buyer-vendor-pressure-pilot-v0.1.md")
            self.assertEqual(aggregate["scenario_id"], "S04")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["vendor_action_menu_id"], VENDOR_ACTION_MENU_ID)
            self.assertEqual(aggregate["buyer_action_menu_id"], BUYER_ACTION_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in M02")
            self.assertEqual(
                aggregate["vendor_selected_action_counts"],
                {
                    "apply_deadline_pressure": 1,
                    "escalate_vendor_pressure": 1,
                    "offer_flexible_timing": 1,
                    "request_payment_status": 1,
                    "signal_service_continuity_risk": 1,
                },
            )
            self.assertEqual(
                aggregate["buyer_selected_action_counts"],
                {
                    "escalate": 1,
                    "hold_payment": 1,
                    "mark_approval_inferred": 1,
                    "request_approval": 1,
                    "request_more_evidence": 1,
                },
            )
            self.assertEqual(
                aggregate["paired_vendor_buyer_path_counts"],
                {
                    "apply_deadline_pressure -> hold_payment": 1,
                    "escalate_vendor_pressure -> mark_approval_inferred": 1,
                    "offer_flexible_timing -> escalate": 1,
                    "request_payment_status -> request_approval": 1,
                    "signal_service_continuity_risk -> request_more_evidence": 1,
                },
            )
            self.assertEqual(aggregate["vendor_parser_summary"]["total_attempts"], 5)
            self.assertEqual(aggregate["buyer_parser_summary"]["total_attempts"], 5)
            self.assertEqual(aggregate["vendor_parser_summary"]["total_retries"], 0)
            self.assertEqual(aggregate["buyer_parser_summary"]["total_retries"], 0)
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(
                aggregate["pressure_citation_summary"],
                {
                    "buyer_cited_vendor_action_or_message_in_source_refs": 5,
                    "buyer_included_vendor_pressure_in_risk_flags": 3,
                    "buyer_included_vendor_pressure_in_private_pressure_refs": 3,
                    "buyer_referenced_pressure_in_intent": 3,
                    "buyer_referenced_pressure_in_payload_summary": 3,
                },
            )
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 5)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual({action["proposed_by"] for action in actions}, {"vendor", "buyer"})
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002"})
            self.assertTrue((representative_pack / "action_menus" / "vendor.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "buyer.json").exists())
            self.assertTrue((representative_pack / "parser_results" / "vendor.json").exists())
            self.assertTrue((representative_pack / "parser_results" / "buyer.json").exists())
            self.assertTrue((representative_pack / "proposal_attempts" / "vendor.jsonl").exists())
            self.assertTrue((representative_pack / "proposal_attempts" / "buyer.jsonl").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "vendor_A001_pressure.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_A002_pressure_response.md").exists())
            self.assertTrue((representative_pack / "llm_outputs" / "vendor_A001_pressure.json").exists())
            self.assertTrue((representative_pack / "llm_outputs" / "buyer_A002_pressure_response.json").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected vendor action matches action menu", validation_output)
            self.assertIn("PASS: selected buyer action matches action menu", validation_output)
            self.assertIn("PASS: selected vendor action has a Game Master decision", validation_output)
            self.assertIn("PASS: selected buyer action has a Game Master decision", validation_output)
            self.assertIn("PASS: multi-role role artifacts validate: buyer, vendor", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("M02 is a pressure pilot, not a multi-role baseline", summary)
            self.assertIn("no pressure-causation claim", summary)

    def test_committed_exp_0001_representative_pack_remains_valid(self) -> None:
        pack_dir = (
            ROOT
            / "results"
            / "org-payment"
            / "exp-0001-buyer-only-baseline"
            / "representative-evidence-packs"
            / "s04"
            / "request_approval-run-001"
        )
        if not pack_dir.exists():
            self.skipTest("committed EXP-0001 representative pack not generated yet")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_committed_m01_representative_pack_remains_valid(self) -> None:
        pack_dir = (
            ROOT
            / "pilot-runs"
            / "org-payment"
            / "m01-buyer-approver-pilot-0001"
            / "representative-evidence-packs"
            / "buyer-request_approval_approver-approve_payment-run-001"
        )
        if not pack_dir.exists():
            self.skipTest("committed M01 representative pack not generated yet")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
