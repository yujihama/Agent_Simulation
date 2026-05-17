from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from social_sim.phase4_prompt_persona_variant_runner import (  # noqa: E402
    PromptVariant,
    VariantStructure,
    run_phase4_prompt_persona_variant_diagnostic,
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


def fake_runner_factory(module: types.ModuleType):
    def fake_runner(*, output_root: Path, curated_output: Path, provider: DummyProvider, batch_id: str) -> Path:
        self_text = module.ADDENDUM_TEXT
        scenario_id = "S18" if "s18" in batch_id else "S20"
        sl2_supported = scenario_id == "S18" and "PV1_OPERATIONAL_ROUTER" in self_text
        curated_output.mkdir(parents=True, exist_ok=True)
        pack_dir = curated_output / "representative-evidence-packs" / "path-001"
        write_json(pack_dir / "manifest.json", {"run_id": f"{batch_id}-run-001", "prompt_addendum_ref": module.ADDENDUM_REF})
        write_text(curated_output / "representative-validation-outputs" / "path-001.md", "# Validation\n\nPASS\n")
        aggregate = {
            "pilot_id": f"FAKE-{scenario_id}",
            "batch_id": batch_id,
            "protocol_ref": f"protocols/{scenario_id.lower()}.md",
            "scenario_id": scenario_id,
            "scenario_ref": f"scenarios/{scenario_id.lower()}.yaml",
            "attempted_runs": 5,
            "accepted_runs": 5,
            "excluded_runs": 0,
            "provider": provider.provider,
            "model": provider.model,
            "observed_model_versions": [provider.model],
            "validation_summary": {"pass": 5, "fail": 0, "pass_rate_included": 1.0},
            "exclusion_summary": {},
            "failure_mode_summary": {
                "SL2": {"candidate": 1, "not_observed": 4} if sl2_supported else {"not_observed": 5},
                "SL3": {"not_observed": 5},
                "SL4": {"not_observed": 5},
                "SL5": {"observed": 5},
                "SL6": {"not_observed": 5},
                "FM1": {"not_observed": 5},
                "FM3": {"not_observed": 5},
                "FM6": {"not_observed": 5},
            },
            "generated_candidate_rows": 1 if sl2_supported else 0,
            "candidate_rows": [
                {
                    "category_id": "SL2",
                    "status": "candidate",
                    "run_id": f"{batch_id}-run-001",
                }
            ]
            if sl2_supported
            else [],
            "buyer_action_counts": {"submit_payment_request": 1} if sl2_supported else {"hold_payment": 5},
            "accountant_action_counts": {"hold_payment": 5},
            "representative_evidence_packs": [
                {
                    "label": "path-001",
                    "run_id": f"{batch_id}-run-001",
                    "evidence_pack": "representative-evidence-packs/path-001",
                    "validation_output": "representative-validation-outputs/path-001.md",
                }
            ],
        }
        write_json(curated_output / "aggregate.json", aggregate)
        write_json(curated_output / "execution-manifest.json", {"exclusions": [], "accepted_runs": 5})
        rows = []
        for category in ["SL1", "SL2", "SL3", "SL4", "SL5", "SL6", "FM1", "FM3", "FM6"]:
            if category == "SL2" and sl2_supported:
                decision = "partially_supported_needs_revision"
                generated_candidate_count = "1"
                generated_observed_count = "0"
                generated_not_observed_count = "4"
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
        write_json(curated_output / "candidate-review-0001" / "review-manifest.json", {"review_decision_counts": {}})
        return curated_output

    return fake_runner


class Phase4PromptPersonaVariantRunnerTest(unittest.TestCase):
    def test_variant_matrix_aggregates_reviews_and_restores_base_addendum(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            output = tmp_path / "runs"
            curated = tmp_path / "pilot-runs"
            fake_module = types.ModuleType("fake_phase4_variant_module")
            fake_module.ADDENDUM_TEXT = "base addendum"
            fake_module.ADDENDUM_REF = "prompts/base.md"
            structures = [
                VariantStructure("S18_LOSSY_HANDOFF", "Lossy handoff", "s18", "protocols/s18.md", "S18", "scenarios/s18.yaml", fake_runner_factory(fake_module), fake_module),
                VariantStructure("S20_EXCEPTION_ROUTE", "Exception route", "s20", "protocols/s20.md", "S20", "scenarios/s20.yaml", fake_runner_factory(fake_module), fake_module),
            ]
            variants = [
                PromptVariant("PV1_OPERATIONAL_ROUTER", "Operational router", "pv1", "Variant id: `PV1_OPERATIONAL_ROUTER`"),
            ]

            run_phase4_prompt_persona_variant_diagnostic(
                output_root=output,
                curated_output=curated,
                provider_factory=DummyProvider,
                structures=structures,
                variants=variants,
                write_repo_reflection=False,
            )

            aggregate = json.loads((curated / "aggregate.json").read_text(encoding="utf-8"))
            self.assertEqual(fake_module.ADDENDUM_TEXT, "base addendum")
            self.assertEqual(fake_module.ADDENDUM_REF, "prompts/base.md")
            self.assertEqual(aggregate["planned_cells"], 2)
            self.assertEqual(aggregate["attempted_runs"], 10)
            self.assertEqual(aggregate["accepted_runs"], 10)
            self.assertEqual(aggregate["variant_pattern_summary"]["sl2_supported_cells"], ["S18_LOSSY_HANDOFF:PV1_OPERATIONAL_ROUTER"])
            self.assertEqual(aggregate["variant_pattern_summary"]["stronger_downstream_supported_categories"], [])
            self.assertEqual(aggregate["next_decision"]["decision"], "analyze_prompt_persona_sl2_boundary_before_more_variants")
            self.assertTrue((curated / "candidate-review-0001" / "summary.md").exists())
            self.assertTrue((curated / "representative-evidence-packs" / "s18" / "pv1" / "path-001" / "manifest.json").exists())


if __name__ == "__main__":
    unittest.main()
