from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class S04ScriptedRunTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.pack_dir = Path(self.tmp.name) / "generated-evidence-pack"
        env = os.environ.copy()
        env["PYTHONPATH"] = str(SRC)
        subprocess.run(
            [
                sys.executable,
                "-m",
                "social_sim",
                "generate-s04",
                "--output",
                str(self.pack_dir),
            ],
            cwd=ROOT,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_generated_json_jsonl_yaml_and_validator(self) -> None:
        json.loads((self.pack_dir / "manifest.json").read_text(encoding="utf-8"))
        json.loads((self.pack_dir / "metrics.json").read_text(encoding="utf-8"))
        for name in ["trace.jsonl", "messages.jsonl", "actions.jsonl", "gm_decisions.jsonl", "events.jsonl"]:
            self.assertTrue(load_jsonl(self.pack_dir / name), name)

        import yaml  # type: ignore

        scenario = yaml.safe_load((self.pack_dir / "scenario.yaml").read_text(encoding="utf-8"))
        self.assertEqual(scenario["id"], "S04")

        subprocess.run(
            [sys.executable, "scripts/validate_evidence_pack.py", str(self.pack_dir)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )

    def test_every_action_has_gm_decision(self) -> None:
        actions = load_jsonl(self.pack_dir / "actions.jsonl")
        decisions = load_jsonl(self.pack_dir / "gm_decisions.jsonl")
        action_ids = {record["action_id"] for record in actions}
        decided_action_ids = {record["action_id"] for record in decisions}
        self.assertEqual(action_ids, decided_action_ids)

    def test_action_source_refs_resolve(self) -> None:
        ids, paths = self._known_refs()
        actions = load_jsonl(self.pack_dir / "actions.jsonl")
        for action in actions:
            for ref in action["source_refs"]:
                self.assertTrue(ref in ids or ref in paths, ref)

    def test_events_and_metrics_reference_valid_records(self) -> None:
        ids, paths = self._known_refs()
        events = load_jsonl(self.pack_dir / "events.jsonl")
        metrics = json.loads((self.pack_dir / "metrics.json").read_text(encoding="utf-8"))
        event_ids = {record["event_id"] for record in events}

        self.assertEqual({record["review_status"] for record in events}, {"proposed"})
        self.assertEqual(metrics["review_status"], "not_human_reviewed")

        for event in events:
            for ref in event["source_refs"]:
                self.assertTrue(ref in ids or ref in paths, ref)

        for metric in metrics["metrics"]:
            for event_id in metric["source_event_ids"]:
                self.assertIn(event_id, event_ids)
            for ref in metric["source_record_refs"]:
                self.assertTrue(ref in ids or ref in paths, ref)

    def _known_refs(self) -> tuple[set[str], set[str]]:
        id_fields = {
            "trace.jsonl": "trace_id",
            "messages.jsonl": "message_id",
            "actions.jsonl": "action_id",
            "gm_decisions.jsonl": "decision_id",
            "events.jsonl": "event_id",
        }
        ids: set[str] = set()
        for filename, field in id_fields.items():
            ids.update(record[field] for record in load_jsonl(self.pack_dir / filename))

        paths = {
            "trace.jsonl",
            "messages.jsonl",
            "actions.jsonl",
            "gm_decisions.jsonl",
            "events.jsonl",
            "metrics.json",
            "initial_state/case.md",
            "final_state/case.md",
            "reviewer_notes.md",
            "reconstruction-checklist.md",
        }
        return ids, paths


if __name__ == "__main__":
    unittest.main()
