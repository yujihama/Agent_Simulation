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
from social_sim.scenario_sweep_runner import run_buyer_scenario_sweep  # noqa: E402


TARGET_ROLES = {
    "request_approval": "approver",
    "request_more_evidence": "requester",
    "hold_payment": "accountant",
    "escalate": "approver",
    "mark_approval_inferred": "accountant",
}

ACTION_BY_SCENARIO = {
    "s01": "request_approval",
    "s02": "request_more_evidence",
    "s03": "escalate",
    "s04": "hold_payment",
    "s05": "request_approval",
    "s06": "mark_approval_inferred",
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


class ScenarioSweepProvider:
    provider = "stub"
    model = "stub-scenario-sweep-json"

    def complete_json(self, request: LLMRequest) -> LLMResponse:
        run_id = extract_fixed_field(request.user_prompt, "run_id")
        action_id = extract_fixed_field(request.user_prompt, "action_id")
        case_id = extract_fixed_field(request.user_prompt, "case_id")
        scenario_key = re.search(r"buyer-sweep-(s\d\d)-run", run_id)
        if scenario_key is None:
            raise AssertionError(f"unexpected run_id: {run_id}")
        action_type = ACTION_BY_SCENARIO[scenario_key.group(1)]
        action = {
            "action_id": action_id,
            "run_id": run_id,
            "turn": 4,
            "proposed_by": "buyer",
            "target_role": TARGET_ROLES[action_type],
            "action_type": action_type,
            "case_id": case_id,
            "intent": f"Select {action_type} from the constrained scenario sweep action menu.",
            "payload_summary": f"Buyer selected {action_type} in the stub S01-S06 sweep.",
            "preconditions_claimed": ["invoice present", "business reason present", "explicit approval absent"],
            "source_refs": ["M002", "T003"],
            "expected_effect": "The selected action remains subject to deterministic Game Master review.",
            "risk_flags": ["approval_evidence_gap"],
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


class BuyerScenarioSweepPilotTest(unittest.TestCase):
    def test_sweep_writes_valid_runs_and_scenario_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            raw_output = tmp_path / "runs" / "buyer-sweep"
            curated_output = tmp_path / "pilot-runs" / "buyer-sweep"
            run_buyer_scenario_sweep(
                output_root=raw_output,
                curated_output=curated_output,
                provider=ScenarioSweepProvider(),
                count_per_scenario=1,
                batch_id="pilot-buyer-sweep",
            )

            aggregate = load_json(curated_output / "aggregate.json")
            self.assertEqual(aggregate["provider"], "stub")
            self.assertEqual(aggregate["model"], "stub-scenario-sweep-json")
            self.assertEqual(aggregate["scenario_ids"], ["S01", "S02", "S03", "S04", "S05", "S06"])
            self.assertEqual(aggregate["count_per_scenario"], 1)
            self.assertEqual(aggregate["run_count"], 6)
            self.assertEqual(aggregate["claim_boundary"], "pilot_observation_only")
            self.assertEqual(aggregate["action_menu_id"], "org_payment_buyer_constrained_action_menu_v0.1")

            summaries = {item["scenario_id"]: item for item in aggregate["scenario_summaries"]}
            self.assertEqual(summaries["S01"]["selected_action_type_counts"], {"request_approval": 1})
            self.assertEqual(summaries["S06"]["selected_action_type_counts"], {"mark_approval_inferred": 1})
            self.assertEqual(
                summaries["S06"]["gm_decisions_by_selected_action"],
                {"mark_approval_inferred": {"blocked": 1}},
            )
            self.assertEqual(summaries["S05"]["control_mode"], "monitored")
            self.assertEqual(summaries["S06"]["control_mode"], "hard")

            run_ids = [record["run_id"] for record in aggregate["runs"]]
            self.assertIn("pilot-buyer-sweep-s01-run-001", run_ids)
            self.assertIn("pilot-buyer-sweep-s06-run-001", run_ids)
            self.assertEqual(len(aggregate["representative_evidence_packs"]), 6)
            for representative in aggregate["representative_evidence_packs"]:
                self.assertTrue((curated_output / representative["evidence_pack"] / "manifest.json").exists())
                self.assertTrue((curated_output / representative["validation_output"]).exists())

            summary = (curated_output / "summary.md").read_text(encoding="utf-8")
            self.assertIn("Across this small buyer-only scenario sweep pilot", summary)
            self.assertIn("does not claim that scenario differences are statistically significant", summary)
            self.assertIn("| `S01` |", summary)
            self.assertIn("| `S06` |", summary)

    def test_committed_scenario_sweep_representative_pack_validates_if_present(self) -> None:
        pack_dir = (
            ROOT
            / "pilot-runs"
            / "org-payment"
            / "buyer-only-scenario-sweep-pilot-0001"
            / "representative-evidence-packs"
            / "s01"
            / "request_approval-run-001"
        )
        if not pack_dir.exists():
            self.skipTest("committed buyer-only scenario sweep pilot pack not generated yet")
        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )


if __name__ == "__main__":
    unittest.main()
