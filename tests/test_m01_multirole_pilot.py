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
from social_sim.multirole_runner import (  # noqa: E402
    APPROVER_ACTION_MENU_ID,
    BUYER_ACTION_MENU_ID,
    CLAIM_BOUNDARY,
    run_m01_buyer_approver_pilot,
)


BUYER_TARGET_ROLES = {
    "request_approval": "approver",
    "request_approval_status": "approver",
    "escalate": "approver",
}

APPROVER_TARGET_ROLES = {
    "approve_payment": "buyer",
    "reject_payment": "buyer",
    "request_more_evidence": "buyer",
    "provide_ambiguous_guidance": "buyer",
    "escalate": "buyer",
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


class M01RoleStubProvider:
    provider = "stub"
    model = "stub-m01-role-json"

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
        target_roles = BUYER_TARGET_ROLES if self.role == "buyer" else APPROVER_TARGET_ROLES
        source_refs = ["M002", "T003"] if self.role == "buyer" else ["A001", "D001", "T006"]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": turn,
            "proposed_by": self.role,
            "target_role": target_roles[action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the frozen M01 {self.role} action menu.",
            "payload_summary": f"{self.role.title()} selected {action_type} in the M01 stub pilot.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval unresolved"],
            "source_refs": source_refs,
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["approval_evidence_gap"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "model": self.model, "action_id": action_id},
            provider=self.provider,
            model=self.model,
        )


class M01MultiRolePilotTest(unittest.TestCase):
    def test_m01_batch_writes_valid_multirole_pilot_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "m01"
            curated_output = tmp_path / "pilot-runs" / "m01"
            run_m01_buyer_approver_pilot(
                output_root=raw_output,
                curated_output=curated_output,
                buyer_provider=M01RoleStubProvider(
                    "buyer",
                    ["request_approval", "request_approval", "request_approval_status", "escalate", "request_approval"],
                ),
                approver_provider=M01RoleStubProvider(
                    "approver",
                    [
                        "approve_payment",
                        "provide_ambiguous_guidance",
                        "request_more_evidence",
                        "escalate",
                        "approve_payment",
                    ],
                ),
            )

            aggregate = load_json(curated_output / "aggregate.json")
            manifest = load_json(curated_output / "execution-manifest.json")
            self.assertEqual(aggregate["pilot_id"], "M01")
            self.assertEqual(aggregate["protocol_ref"], "protocols/multi-role/multi-role-pilot-v0.1.md")
            self.assertEqual(aggregate["scenario_id"], "S04")
            self.assertEqual(aggregate["attempted_runs"], 5)
            self.assertEqual(aggregate["accepted_runs"], 5)
            self.assertEqual(aggregate["excluded_runs"], 0)
            self.assertEqual(aggregate["claim_boundary"], CLAIM_BOUNDARY)
            self.assertEqual(aggregate["buyer_action_menu_id"], BUYER_ACTION_MENU_ID)
            self.assertEqual(aggregate["approver_action_menu_id"], APPROVER_ACTION_MENU_ID)
            self.assertEqual(manifest["replacement_policy"], "excluded runs are not replaced in M01")
            self.assertEqual(
                aggregate["buyer_selected_action_counts"],
                {"escalate": 1, "request_approval": 3, "request_approval_status": 1},
            )
            self.assertEqual(
                aggregate["approver_selected_action_counts"],
                {
                    "approve_payment": 2,
                    "escalate": 1,
                    "provide_ambiguous_guidance": 1,
                    "request_more_evidence": 1,
                },
            )
            self.assertEqual(
                aggregate["paired_buyer_approver_path_counts"],
                {
                    "escalate -> escalate": 1,
                    "request_approval -> approve_payment": 2,
                    "request_approval -> provide_ambiguous_guidance": 1,
                    "request_approval_status -> request_more_evidence": 1,
                },
            )
            self.assertEqual(aggregate["buyer_parser_summary"]["total_attempts"], 5)
            self.assertEqual(aggregate["approver_parser_summary"]["total_attempts"], 5)
            self.assertEqual(aggregate["buyer_parser_summary"]["total_retries"], 0)
            self.assertEqual(aggregate["approver_parser_summary"]["total_retries"], 0)
            self.assertEqual(aggregate["validation_summary"], {"pass": 5, "fail": 0, "pass_rate_included": 1.0})
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 4)

            representative = aggregate["representative_evidence_packs"][0]
            representative_pack = curated_output / representative["evidence_pack"]
            actions = load_jsonl(representative_pack / "actions.jsonl")
            decisions = load_jsonl(representative_pack / "gm_decisions.jsonl")
            self.assertEqual({action["proposed_by"] for action in actions}, {"buyer", "approver"})
            self.assertEqual({decision["action_id"] for decision in decisions}, {"A001", "A002"})
            self.assertTrue((representative_pack / "parser_results" / "buyer.json").exists())
            self.assertTrue((representative_pack / "parser_results" / "approver.json").exists())
            self.assertTrue((representative_pack / "proposal_attempts" / "buyer.jsonl").exists())
            self.assertTrue((representative_pack / "proposal_attempts" / "approver.jsonl").exists())

            validation_output = (curated_output / representative["validation_output"]).read_text(encoding="utf-8")
            self.assertIn("PASS: selected buyer action matches action menu", validation_output)
            self.assertIn("PASS: selected approver action matches action menu", validation_output)
            self.assertIn("PASS: selected approver action has a Game Master decision", validation_output)

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("M01 is a pilot, not a multi-role baseline", summary)
            self.assertIn("no statistical significance claim", summary)

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


if __name__ == "__main__":
    unittest.main()
