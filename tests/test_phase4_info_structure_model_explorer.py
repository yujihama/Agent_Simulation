from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from social_sim.phase4_info_structure_model_explorer import (  # noqa: E402
    ModelCondition,
    StructureCondition,
    run_phase4_information_structure_model_exploration,
)


class DummyProvider:
    provider = "stub"

    def __init__(self, model: str) -> None:
        self.model = model


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def fake_cell_runner(*, output_root: Path, curated_output: Path, provider: DummyProvider, batch_id: str) -> Path:
    scenario_id = "S18" if "s18" in batch_id else "S19"
    structure_supports_sl2 = scenario_id == "S18"
    curated_output.mkdir(parents=True, exist_ok=True)
    failure_mode_summary = {
        "SL2": {"candidate": 3, "not_observed": 2} if structure_supports_sl2 else {"not_observed": 5},
        "SL3": {"not_observed": 5},
        "SL4": {"not_observed": 5},
        "SL5": {"observed": 5},
        "SL6": {"not_observed": 5},
        "FM1": {"not_observed": 5},
        "FM3": {"not_observed": 5},
        "FM6": {"not_observed": 5},
    }
    aggregate = {
        "pilot_id": f"FAKE-{scenario_id}",
        "batch_id": batch_id,
        "protocol_ref": f"protocols/fake-{scenario_id}.md",
        "scenario_id": scenario_id,
        "scenario_ref": f"scenarios/fake-{scenario_id}.yaml",
        "attempted_runs": 5,
        "accepted_runs": 5,
        "excluded_runs": 0,
        "provider": provider.provider,
        "model": provider.model,
        "observed_model_versions": [provider.model],
        "validation_summary": {"pass": 5, "fail": 0, "pass_rate_included": 1.0},
        "exclusion_summary": {},
        "failure_mode_summary": failure_mode_summary,
        "generated_candidate_rows": 3 if structure_supports_sl2 else 0,
        "candidate_rows": [],
        "buyer_action_counts": {"submit_payment_request": 3} if structure_supports_sl2 else {"hold_payment": 5},
        "accountant_action_counts": {"hold_payment": 5},
        "representative_evidence_packs": [],
    }
    write_json(curated_output / "aggregate.json", aggregate)
    write_json(
        curated_output / "execution-manifest.json",
        {
            "exclusions": [],
            "attempted_runs": 5,
            "accepted_runs": 5,
            "excluded_runs": 0,
        },
    )
    rows = []
    for category in ["SL2", "SL3", "SL4", "SL5", "SL6", "FM1", "FM3", "FM6"]:
        if category == "SL2" and structure_supports_sl2:
            decision = "supported_for_reviewed_evidence"
            generated_candidate_count = "3"
            generated_observed_count = "0"
            generated_not_observed_count = "2"
        elif category == "SL5":
            decision = "supported_for_reviewed_evidence"
            generated_candidate_count = "0"
            generated_observed_count = "5"
            generated_not_observed_count = "0"
        else:
            decision = "not_observed"
            generated_candidate_count = "0"
            generated_observed_count = "0"
            generated_not_observed_count = "5"
        rows.append(
            {
                "category_id": category,
                "category": category,
                "generated_candidate_count": generated_candidate_count,
                "generated_observed_count": generated_observed_count,
                "generated_not_observed_count": generated_not_observed_count,
                "review_decision": decision,
                "review_scope": "fake test scope",
                "buyer_actions": "",
                "accountant_actions": "",
                "evidence_refs": "",
                "notes": "fake test row",
            }
        )
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    write_text(curated_output / "candidate-review-0001" / "review-table.csv", output.getvalue())
    write_json(
        curated_output / "candidate-review-0001" / "review-manifest.json",
        {"review_decision_counts": {"supported_for_reviewed_evidence": 2 if structure_supports_sl2 else 1, "not_observed": 6 if structure_supports_sl2 else 7}},
    )
    return curated_output


class Phase4InformationStructureModelExplorerTest(unittest.TestCase):
    def test_matrix_aggregate_keeps_structure_and_review_distinctions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output = tmp_path / "runs"
            curated = tmp_path / "pilot-runs"
            structures = [
                StructureCondition("S18_LOSSY_HANDOFF", "Lossy handoff", "lossy", "protocols/s18.md", "S18", "scenarios/s18.yaml", fake_cell_runner),
                StructureCondition("S19_QUEUE_TICKET", "Queue ticket", "queue", "protocols/s19.md", "S19", "scenarios/s19.yaml", fake_cell_runner),
            ]
            models = [ModelCondition("M_TEST", "test-model", "test-model")]
            run_phase4_information_structure_model_exploration(
                output_root=output,
                curated_output=curated,
                provider_factory=DummyProvider,
                structures=structures,
                models=models,
            )

            aggregate = json.loads((curated / "aggregate.json").read_text(encoding="utf-8"))
            self.assertEqual(aggregate["planned_cells"], 2)
            self.assertEqual(aggregate["attempted_runs"], 10)
            self.assertEqual(aggregate["accepted_runs"], 10)
            self.assertEqual(aggregate["structure_model_pattern_summary"]["sl2_supported_structures"], ["S18_LOSSY_HANDOFF"])
            self.assertEqual(aggregate["structure_model_pattern_summary"]["non_lossy_sl2_supported_structures"], [])
            self.assertEqual(aggregate["structure_model_pattern_summary"]["stronger_downstream_supported_categories"], [])
            self.assertEqual(
                aggregate["next_decision"]["decision"],
                "freeze_lossy_handoff_difference_analysis_before_prompt_or_persona_variants",
            )
            matrix_csv = (curated / "matrix-summary.csv").read_text(encoding="utf-8")
            self.assertIn("S18_LOSSY_HANDOFF", matrix_csv)
            self.assertIn("S19_QUEUE_TICKET", matrix_csv)


if __name__ == "__main__":
    unittest.main()
