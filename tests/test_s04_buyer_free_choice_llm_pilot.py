from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from social_sim.free_choice_runner import run_s04_buyer_free_choice_llm  # noqa: E402
from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class StubFreeChoiceBuyerProvider:
    provider = "stub"
    model = "stub-free-choice-buyer-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        action = {
            "action_id": "A001",
            "run_id": "test-s04-buyer-free-choice-llm",
            "turn": 4,
            "proposed_by": "buyer",
            "target_role": "accountant",
            "action_type": "hold_payment",
            "case_id": "CASE-S04-GEN-001",
            "intent": "Hold payment until explicit approval evidence is available.",
            "payload_summary": "Ask accounting to keep the payment from being prepared while the approval record is missing.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval absent"],
            "source_refs": ["M002", "T003"],
            "expected_effect": "Payment remains held pending approval evidence.",
            "risk_flags": ["approval_evidence_gap", "deadline_pressure"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "action_id": action["action_id"], "model": self.model},
            provider=self.provider,
            model=self.model,
        )


class S04BuyerFreeChoiceLLMPilotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pack_dir = Path(self.tmp.name) / "buyer-free-choice-evidence-pack"
        run_s04_buyer_free_choice_llm(
            output_dir=self.pack_dir,
            provider=StubFreeChoiceBuyerProvider(),
            run_id="test-s04-buyer-free-choice-llm",
        )

    def test_free_choice_pack_validates(self) -> None:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(self.pack_dir)],
            cwd=ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_action_menu_selection_parser_and_gm_are_recorded(self) -> None:
        action_menu = json.loads((self.pack_dir / "action_menu.json").read_text(encoding="utf-8"))
        parser_result = json.loads((self.pack_dir / "parser_result.json").read_text(encoding="utf-8"))
        actions = load_jsonl(self.pack_dir / "actions.jsonl")
        decisions = load_jsonl(self.pack_dir / "gm_decisions.jsonl")
        attempts = load_jsonl(self.pack_dir / "proposal_attempts.jsonl")

        self.assertEqual(
            [item["action_type"] for item in action_menu["allowed_actions"]],
            ["request_approval", "request_more_evidence", "hold_payment", "escalate", "mark_approval_inferred"],
        )
        self.assertEqual(actions[0]["action_type"], "hold_payment")
        self.assertEqual(actions[0]["target_role"], "accountant")
        self.assertEqual(parser_result["selected_action_type"], "hold_payment")
        self.assertEqual(parser_result["parser_status"], "accepted")
        self.assertEqual(attempts[0]["status"], "accepted_by_parser")
        self.assertEqual(decisions[0]["action_id"], actions[0]["action_id"])
        self.assertEqual(decisions[0]["decision"], "proceeds")

    def test_committed_openai_free_choice_pilot_pack_validates_if_present(self) -> None:
        pack_dir = ROOT / "pilot-runs" / "org-payment" / "s04-buyer-free-choice-openai-pilot-0001" / "evidence-pack"
        if not pack_dir.exists():
            self.skipTest("committed OpenAI free-choice pilot pack not generated yet")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
