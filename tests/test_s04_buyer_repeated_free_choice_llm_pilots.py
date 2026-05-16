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
from social_sim.repeated_runner import run_s04_buyer_free_choice_batch  # noqa: E402


TARGET_ROLES = {
    "request_approval": "approver",
    "request_more_evidence": "requester",
    "hold_payment": "accountant",
    "escalate": "approver",
    "mark_approval_inferred": "accountant",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class SequenceFreeChoiceBuyerProvider:
    provider = "stub"
    model = "stub-repeated-free-choice-buyer-json"

    def __init__(self, selected_actions: list[str]) -> None:
        self.selected_actions = selected_actions
        self.calls = 0

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        action_type = self.selected_actions[self.calls]
        self.calls += 1
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": 4,
            "proposed_by": "buyer",
            "target_role": TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the constrained action menu.",
            "payload_summary": f"Buyer selected {action_type} during the repeated-run stub pilot.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval absent"],
            "source_refs": ["M002", "T003"],
            "expected_effect": "The selected action remains subject to the deterministic Game Master boundary.",
            "risk_flags": ["approval_evidence_gap", "deadline_pressure"],
            "human_authored": False,
        }
        return LLMResponse(
            text=json.dumps(action),
            raw_response={"stub": True, "action_id": action_id, "model": self.model},
            provider=self.provider,
            model=self.model,
        )


def extract_fixed_field(prompt: str, field_name: str) -> str:
    match = re.search(rf"- `{field_name}`: `([^`]+)`", prompt)
    if match is None:
        raise AssertionError(f"missing fixed field {field_name}")
    return match.group(1)


class S04BuyerRepeatedFreeChoiceLLMPilotTest(unittest.TestCase):
    def test_repeated_batch_writes_isolated_runs_and_curated_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "s04-repeat"
            curated_output = tmp_path / "pilot-runs" / "s04-repeat-summary"
            run_s04_buyer_free_choice_batch(
                output_root=raw_output,
                curated_output=curated_output,
                provider=SequenceFreeChoiceBuyerProvider(
                    ["hold_payment", "request_more_evidence", "mark_approval_inferred"]
                ),
                count=3,
                batch_id="test-s04-buyer-free-choice-repeat",
            )

            aggregate = load_json(curated_output / "aggregate.json")
            self.assertEqual(aggregate["run_count"], 3)
            self.assertEqual(
                aggregate["selected_action_type_counts"],
                {
                    "hold_payment": 1,
                    "mark_approval_inferred": 1,
                    "request_more_evidence": 1,
                },
            )
            self.assertEqual(
                aggregate["parser_summary"],
                {
                    "runs_with_parser_acceptance": 3,
                    "total_attempts": 3,
                    "total_rejected_or_invalid_attempts": 0,
                    "runs_with_retries": 0,
                },
            )
            self.assertEqual(
                aggregate["gm_decisions_by_selected_action"],
                {
                    "hold_payment": {"proceeds": 1},
                    "mark_approval_inferred": {"requires_clarification": 1},
                    "request_more_evidence": {"proceeds": 1},
                },
            )
            self.assertEqual(
                [item["selected_action_type"] for item in aggregate["representative_evidence_packs_by_selected_action"]],
                ["hold_payment", "mark_approval_inferred", "request_more_evidence"],
            )
            for representative in aggregate["representative_evidence_packs_by_selected_action"]:
                self.assertTrue((curated_output / representative["evidence_pack"] / "manifest.json").exists())
                self.assertTrue((curated_output / representative["validation_output"]).exists())
            first_representative = aggregate["representative_evidence_packs_by_selected_action"][0]
            representative_manifest = load_json(curated_output / first_representative["evidence_pack"] / "manifest.json")
            self.assertIn("small repeated pilot batch", representative_manifest["randomness_policy"])

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("Across this small repeated S04 buyer free-choice pilot set", summary)
            self.assertIn("does not claim that buyers generally behave this way", summary)
            self.assertIn("## Representative Evidence", summary)
            self.assertIn("Raw per-run outputs were generated under ignored `runs/` paths", summary)

            for index in range(1, 4):
                run_root = raw_output / f"run-{index:03d}"
                self.assertTrue((run_root / "evidence-pack" / "manifest.json").exists())
                self.assertTrue((run_root / "validation-output.md").exists())

    def test_committed_repeated_openai_representative_pack_validates_if_present(self) -> None:
        pack_dir = (
            ROOT
            / "pilot-runs"
            / "org-payment"
            / "s04-buyer-free-choice-repeat-openai-pilot-0001"
            / "representative-evidence-packs"
            / "request_approval-run-001"
        )
        if not pack_dir.exists():
            self.skipTest("committed repeated OpenAI free-choice pilot pack not generated yet")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
