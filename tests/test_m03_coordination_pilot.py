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
from social_sim.m03_coordination_runner import (  # noqa: E402
    ACCOUNTANT_ACTION_MENU_ID,
    APPROVER_ACTION_MENU_ID,
    BUYER_ACCOUNTING_HANDOFF_MENU_ID,
    BUYER_APPROVAL_REQUEST_MENU_ID,
    CLAIM_BOUNDARY,
    run_m03_coordination_pilot,
)


TARGET_ROLES = {
    "request_approval": "approver",
    "request_approval_status": "approver",
    "escalate": "approver",
    "approve_payment": "buyer",
    "reject_payment": "buyer",
    "request_more_evidence": "requester",
    "hold_payment": "accountant",
    "mark_approval_inferred": "accountant",
    "submit_payment_request": "accountant",
    "prepare_payment": "buyer",
    "authorize_exception_review": "approver",
}

TARGET_ROLES_BY_ACTION_ID = {
    "A001": {
        "request_approval": "approver",
        "request_approval_status": "approver",
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class M03RoleStubProvider:
    provider = "stub"
    model = "stub-m03-role-json"

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
            "A001": ["M001", "M002", "T003"],
            "A002": ["A001", "D001", "M001", "T006"],
            "A003": ["A002", "D002", "M003", "A001", "D001"],
            "A004": ["A003", "D003", "M004", "A002", "D002"],
        }[action_id]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": TARGET_ROLES_BY_ACTION_ID[action_id][action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the frozen M03 {self.role} menu while preserving approval evidence state.",
            "payload_summary": f"{self.role.title()} selected {action_type}; explicit, ambiguous, rejected, or missing approval evidence remains visible.",
            "preconditions_claimed": ["invoice present", "business reason present", "approval evidence must be preserved"],
            "source_refs": source_refs,
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["approval_evidence_gap"] if action_type != "approve_payment" else [],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class M03CoordinationPilotTest(unittest.TestCase):
    def test_m03_batch_writes_valid_coordination_pilot_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "m03"
            curated_output = tmp_path / "pilot-runs" / "m03"
            run_m03_coordination_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                buyer_provider=M03RoleStubProvider(
                    "buyer",
                    {
                        "A001": ["request_approval", "request_approval", "request_approval_status", "escalate", "request_approval"],
                        "A003": ["submit_payment_request", "hold_payment", "request_more_evidence", "escalate", "mark_approval_inferred"],
                    },
                ),
                approver_provider=M03RoleStubProvider(
                    "approver",
                    {
                        "A002": [
                            "approve_payment",
                            "provide_ambiguous_guidance",
                            "request_more_evidence",
                            "escalate",
                            "reject_payment",
                        ]
                    },
                ),
                accountant_provider=M03RoleStubProvider(
                    "accountant",
                    {
                        "A004": [
                            "prepare_payment",
                            "request_more_evidence",
                            "hold_payment",
                            "authorize_exception_review",
                            "escalate",
                        ]
                    },
                ),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "M03")
            self.assertEqual(aggregate["protocol_ref"], "protocols/multi-role/m03-buyer-approver-accountant-coordination-pilot-v0.1.md")
            self.assertEqual(aggregate["scenario_id"], "S04")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["buyer_approval_request_menu_id"], BUYER_APPROVAL_REQUEST_MENU_ID)
            self.assertEqual(aggregate["approver_action_menu_id"], APPROVER_ACTION_MENU_ID)
            self.assertEqual(aggregate["buyer_accounting_handoff_menu_id"], BUYER_ACCOUNTING_HANDOFF_MENU_ID)
            self.assertEqual(aggregate["accountant_action_menu_id"], ACCOUNTANT_ACTION_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in M03")
            self.assertEqual(
                aggregate["buyer_approval_request_action_counts"],
                {"escalate": 1, "request_approval": 3, "request_approval_status": 1},
            )
            self.assertEqual(
                aggregate["approver_action_counts"],
                {
                    "approve_payment": 1,
                    "escalate": 1,
                    "provide_ambiguous_guidance": 1,
                    "reject_payment": 1,
                    "request_more_evidence": 1,
                },
            )
            self.assertEqual(
                aggregate["buyer_accounting_handoff_action_counts"],
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
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["buyer_approval_request"]["total_attempts"], 5)
            self.assertEqual(aggregate["parser_summaries_by_role_turn"]["approver"]["total_retries"], 0)
            self.assertEqual(aggregate["approval_evidence_propagation_summary"]["buyer_handoff_cited_approver_action"], 5)
            self.assertEqual(aggregate["approval_evidence_propagation_summary"]["accountant_cited_buyer_handoff"], 5)
            self.assertEqual(aggregate["coordination_gap_summary"]["explicit_approval_absent_at_accountant_stage"], 4)
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 5)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual([action["action_id"] for action in actions], ["A001", "A002", "A003", "A004"])
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002", "A003", "A004"})
            self.assertTrue((representative_pack / "action_menus" / "buyer_approval_request.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "approver.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "buyer_accounting_handoff.json").exists())
            self.assertTrue((representative_pack / "action_menus" / "accountant.json").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_A001_approval_request.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "approver_A002_free_choice.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "buyer_A003_accounting_handoff.md").exists())
            self.assertTrue((representative_pack / "llm_prompts" / "accountant_A004_free_choice.md").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected buyer_approval_request action matches action menu", validation_output)
            self.assertIn("PASS: selected buyer_accounting_handoff action matches action menu", validation_output)
            self.assertIn("PASS: selected accountant action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("M03 is a coordination pilot, not a multi-role baseline", summary)
            self.assertIn("no human behavior", summary)

    def test_committed_representative_packs_remain_valid(self) -> None:
        pack_dirs = [
            ROOT / "results" / "org-payment" / "exp-0001-buyer-only-baseline" / "representative-evidence-packs" / "s04" / "request_approval-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m01-buyer-approver-pilot-0001" / "representative-evidence-packs" / "buyer-request_approval_approver-approve_payment-run-001",
            ROOT / "pilot-runs" / "org-payment" / "m02-buyer-vendor-pressure-pilot-0001" / "representative-evidence-packs" / "vendor-apply_deadline_pressure_buyer-request_approval-run-001",
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
