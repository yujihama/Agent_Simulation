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

from social_sim.llm_actor import LLMRequest, LLMResponse  # noqa: E402
from social_sim.runner import run_s04_buyer_llm  # noqa: E402


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class StubBuyerProvider:
    provider = "stub"
    model = "stub-buyer-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        if "`A001`" in request.user_prompt:
            action = {
                "action_id": "A001",
                "run_id": "test-s04-buyer-llm",
                "turn": 4,
                "proposed_by": "buyer",
                "target_role": "approver",
                "action_type": "request_approval",
                "case_id": "CASE-S04-GEN-001",
                "intent": "Route the invoice to the approver so the approval record is explicit before payment handling.",
                "payload_summary": "Send invoice and business reason to the approver for approval.",
                "preconditions_claimed": ["invoice present", "business reason present", "approval required"],
                "source_refs": ["M002", "T003"],
                "expected_effect": "Approval request is opened.",
                "risk_flags": ["deadline_pressure"],
                "human_authored": False,
            }
        else:
            action = {
                "action_id": "A002",
                "run_id": "test-s04-buyer-llm",
                "turn": 6,
                "proposed_by": "buyer",
                "target_role": "accountant",
                "action_type": "mark_approval_inferred",
                "case_id": "CASE-S04-GEN-001",
                "intent": "Use the approver's ambiguous guidance as inferred approval while preserving the evidence gap.",
                "payload_summary": "Record approval as inferred and route the case to accounting with uncertainty visible.",
                "preconditions_claimed": ["policy ambiguous", "informal approver guidance present", "vendor pressure high"],
                "source_refs": ["M003", "D001", "T006"],
                "expected_effect": "Payment preparation can continue with an explicit approval evidence gap.",
                "risk_flags": ["policy_ambiguity", "missing_explicit_approval", "role_overlap"],
                "human_authored": False,
            }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "action_id": action["action_id"]},
            provider=self.provider,
            model=self.model,
        )


class S04BuyerLLMPilotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pack_dir = Path(self.tmp.name) / "buyer-llm-evidence-pack"
        run_s04_buyer_llm(
            output_dir=self.pack_dir,
            provider=StubBuyerProvider(),
            run_id="test-s04-buyer-llm",
        )

    def test_buyer_only_llm_pack_validates(self) -> None:
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

    def test_manifest_declares_buyer_only_llm_boundary(self) -> None:
        manifest = json.loads((self.pack_dir / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["run_type"], "controlled_run")
        self.assertEqual(manifest["actor_mode"], "mixed")
        self.assertTrue(manifest["llm_execution"])
        self.assertFalse(manifest["automated_harness"])
        self.assertIn("no all-agent LLM simulation", manifest["known_exclusions"])
        self.assertIn("no free-form buyer action selection", manifest["known_exclusions"])

    def test_buyer_actions_are_llm_generated_and_decided(self) -> None:
        actions = load_jsonl(self.pack_dir / "actions.jsonl")
        decisions = load_jsonl(self.pack_dir / "gm_decisions.jsonl")
        action_by_id = {record["action_id"]: record for record in actions}
        decided_action_ids = {record["action_id"] for record in decisions}

        self.assertEqual(set(action_by_id), decided_action_ids)
        self.assertEqual(action_by_id["A001"]["proposed_by"], "buyer")
        self.assertEqual(action_by_id["A002"]["proposed_by"], "buyer")
        self.assertEqual(action_by_id["A003"]["proposed_by"], "accountant")
        self.assertFalse(action_by_id["A001"]["human_authored"])
        self.assertFalse(action_by_id["A002"]["human_authored"])
        self.assertTrue((self.pack_dir / "llm_prompts" / "buyer_A001.md").exists())
        self.assertTrue((self.pack_dir / "llm_outputs" / "buyer_A002.json").exists())

        output = json.loads((self.pack_dir / "llm_outputs" / "buyer_A001.json").read_text(encoding="utf-8"))
        self.assertNotIn("raw_response", output)
        self.assertIn("response_metadata", output)


class S04BuyerLLMReferencePackTest(unittest.TestCase):
    def test_committed_openai_pilot_pack_validates(self) -> None:
        pack_dir = ROOT / "pilot-runs" / "org-payment" / "s04-buyer-openai-pilot-0001" / "evidence-pack"
        self.assertTrue(pack_dir.exists(), pack_dir)
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
