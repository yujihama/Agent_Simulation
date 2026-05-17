from __future__ import annotations

import csv
import io
import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from .evidence_pack_writer import write_json, write_text
from .llm_actor import LLMProvider, OpenAIResponsesProvider
from .method_b_plus_lossy_handoff_runner import run_method_b_plus_lossy_handoff_diagnostic_pilot
from .method_b_plus_queue_ticket_runner import run_method_b_plus_queue_ticket_diagnostic_pilot
from .multirole_runner import now_utc
from .phase4_exception_route_runner import run_phase4_exception_route_ambiguity_diagnostic_pilot
from .repeated_runner import require_new_or_empty


DEFAULT_BATCH_ID = "phase4-information-structure-model-exploration-0001"
PILOT_ID = "PHASE4-INFORMATION-STRUCTURE-MODEL-EXPLORATION-0001"
PROTOCOL_REF = "protocols/failure-modes/phase4-information-structure-model-exploration-v0.1.md"
CLAIM_BOUNDARY = "phase4_information_structure_model_exploration_observation_only"
RUNS_PER_CELL = 5
ROOT = Path(__file__).resolve().parents[2]

SLIPPAGE_CATEGORIES = ["SL1", "SL2", "SL3", "SL4", "SL5", "SL6", "FM1", "FM3", "FM6"]


@dataclass(frozen=True)
class ModelCondition:
    condition_id: str
    requested_model: str
    slug: str


@dataclass(frozen=True)
class StructureCondition:
    structure_id: str
    structure_name: str
    slug: str
    protocol_ref: str
    scenario_id: str
    scenario_ref: str
    runner: Callable[..., Path]


MODEL_CONDITIONS = [
    ModelCondition("M_GPT_4_1_MINI", "gpt-4.1-mini", "gpt-4-1-mini"),
    ModelCondition("M_GPT_5_2", "gpt-5.2", "gpt-5-2"),
    ModelCondition("M_GPT_5_4", "gpt-5.4", "gpt-5-4"),
]

STRUCTURE_CONDITIONS = [
    StructureCondition(
        structure_id="S18_LOSSY_HANDOFF",
        structure_name="Lossy handoff",
        slug="s18-lossy-handoff",
        protocol_ref="protocols/failure-modes/method-b-plus-lossy-handoff-diagnostic-v0.1.md",
        scenario_id="S18",
        scenario_ref="scenarios/org-payment/s18-lossy-handoff-control-slippage.yaml",
        runner=run_method_b_plus_lossy_handoff_diagnostic_pilot,
    ),
    StructureCondition(
        structure_id="S19_QUEUE_TICKET",
        structure_name="Queue/ticket state mismatch",
        slug="s19-queue-ticket",
        protocol_ref="protocols/failure-modes/method-b-plus-queue-ticket-state-mismatch-diagnostic-v0.1.md",
        scenario_id="S19",
        scenario_ref="scenarios/org-payment/s19-queue-ticket-state-mismatch-control-slippage.yaml",
        runner=run_method_b_plus_queue_ticket_diagnostic_pilot,
    ),
    StructureCondition(
        structure_id="S20_EXCEPTION_ROUTE",
        structure_name="Exception route ambiguity",
        slug="s20-exception-route",
        protocol_ref="protocols/failure-modes/phase4-exception-route-ambiguity-diagnostic-v0.1.md",
        scenario_id="S20",
        scenario_ref="scenarios/org-payment/s20-exception-route-ambiguity.yaml",
        runner=run_phase4_exception_route_ambiguity_diagnostic_pilot,
    ),
]


def run_phase4_information_structure_model_exploration(
    *,
    output_root: Path,
    curated_output: Path,
    dotenv_path: Path | None = None,
    provider_factory: Callable[[str], LLMProvider] | None = None,
    structures: list[StructureCondition] | None = None,
    models: list[ModelCondition] | None = None,
    batch_id: str = DEFAULT_BATCH_ID,
    write_repo_reflection: bool = True,
) -> Path:
    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    selected_structures = structures or STRUCTURE_CONDITIONS
    selected_models = models or MODEL_CONDITIONS
    make_provider = provider_factory or (lambda model: OpenAIResponsesProvider.from_env(dotenv_path=dotenv_path, model=model))

    cell_results: list[dict[str, Any]] = []
    for structure in selected_structures:
        for model in selected_models:
            cell_results.append(
                run_exploration_cell(
                    output_root=output_root,
                    structure=structure,
                    model=model,
                    provider_factory=make_provider,
                    batch_id=batch_id,
                )
            )

    representatives = copy_matrix_representatives(cell_results=cell_results, curated_output=curated_output)
    completed_at = now_utc()
    aggregate = build_matrix_aggregate(
        batch_id=batch_id,
        started_at=started_at,
        completed_at=completed_at,
        cell_results=cell_results,
        representatives=representatives,
    )
    write_json(curated_output / "aggregate.json", aggregate)
    write_json(curated_output / "execution-manifest.json", build_execution_manifest(aggregate))
    write_text(curated_output / "matrix-summary.csv", render_matrix_summary_csv(aggregate))
    write_text(curated_output / "candidate-summary.csv", render_candidate_summary_csv(aggregate["candidate_review_rows"]))
    write_text(curated_output / "summary.md", render_summary(aggregate))
    write_candidate_review_package(curated_output, aggregate)
    if write_repo_reflection:
        write_text(ROOT / "docs" / "reflections" / "phase4-information-structure-model-exploration-reflection.md", render_reflection(aggregate))
    return curated_output


def run_exploration_cell(
    *,
    output_root: Path,
    structure: StructureCondition,
    model: ModelCondition,
    provider_factory: Callable[[str], LLMProvider],
    batch_id: str,
) -> dict[str, Any]:
    cell_root = output_root / structure.slug / model.slug
    cell_raw = cell_root / "raw"
    cell_curated = cell_root / "curated"
    cell_batch_id = f"{batch_id}-{structure.scenario_id.lower()}-{model.slug}"
    try:
        provider = provider_factory(model.requested_model)
        structure.runner(
            output_root=cell_raw,
            curated_output=cell_curated,
            provider=provider,
            batch_id=cell_batch_id,
        )
        return collect_cell_result(structure=structure, model=model, cell_curated=cell_curated, cell_batch_id=cell_batch_id)
    except Exception as exc:
        return failed_cell_result(
            structure=structure,
            model=model,
            cell_batch_id=cell_batch_id,
            stage="cell_execution",
            detail=str(exc),
        )


def collect_cell_result(
    *,
    structure: StructureCondition,
    model: ModelCondition,
    cell_curated: Path,
    cell_batch_id: str,
) -> dict[str, Any]:
    aggregate = read_json(cell_curated / "aggregate.json")
    manifest = read_json(cell_curated / "execution-manifest.json")
    review_manifest = read_json(cell_curated / "candidate-review-0001" / "review-manifest.json")
    review_rows = read_review_rows(cell_curated / "candidate-review-0001" / "review-table.csv")
    status = classify_cell_status(aggregate, manifest)
    return {
        "structure_id": structure.structure_id,
        "structure_name": structure.structure_name,
        "structure_slug": structure.slug,
        "model_condition_id": model.condition_id,
        "requested_model": model.requested_model,
        "model_slug": model.slug,
        "cell_batch_id": cell_batch_id,
        "cell_status": status,
        "cell_curated_output": cell_curated.as_posix(),
        "protocol_ref": structure.protocol_ref,
        "scenario_id": structure.scenario_id,
        "scenario_ref": structure.scenario_ref,
        "attempted_runs": aggregate.get("attempted_runs", 0),
        "accepted_runs": aggregate.get("accepted_runs", 0),
        "excluded_runs": aggregate.get("excluded_runs", 0),
        "provider": aggregate.get("provider", "not_recorded"),
        "model": aggregate.get("model", model.requested_model),
        "observed_model_versions": aggregate.get("observed_model_versions", []),
        "validation_summary": aggregate.get("validation_summary", {}),
        "exclusion_summary": aggregate.get("exclusion_summary", {}),
        "failure_mode_summary": aggregate.get("failure_mode_summary", {}),
        "generated_candidate_rows": aggregate.get("generated_candidate_rows", 0),
        "candidate_rows": aggregate.get("candidate_rows", []),
        "candidate_review_rows": add_cell_fields(review_rows, structure, model),
        "review_decision_counts": review_manifest.get("review_decision_counts", {}),
        "buyer_action_counts": aggregate.get("buyer_action_counts", {}),
        "accountant_action_counts": aggregate.get("accountant_action_counts", {}),
        "representative_evidence_packs": aggregate.get("representative_evidence_packs", []),
        "source_curated_output": cell_curated,
        "top_level_failure": None,
    }


def failed_cell_result(
    *,
    structure: StructureCondition,
    model: ModelCondition,
    cell_batch_id: str,
    stage: str,
    detail: str,
) -> dict[str, Any]:
    return {
        "structure_id": structure.structure_id,
        "structure_name": structure.structure_name,
        "structure_slug": structure.slug,
        "model_condition_id": model.condition_id,
        "requested_model": model.requested_model,
        "model_slug": model.slug,
        "cell_batch_id": cell_batch_id,
        "cell_status": "provider_failure",
        "cell_curated_output": None,
        "protocol_ref": structure.protocol_ref,
        "scenario_id": structure.scenario_id,
        "scenario_ref": structure.scenario_ref,
        "attempted_runs": 0,
        "accepted_runs": 0,
        "excluded_runs": 0,
        "provider": "not_initialized",
        "model": model.requested_model,
        "observed_model_versions": [],
        "validation_summary": {"pass": 0, "fail": 0},
        "exclusion_summary": {stage: 1},
        "failure_mode_summary": {},
        "generated_candidate_rows": 0,
        "candidate_rows": [],
        "candidate_review_rows": unavailable_review_rows(structure, model, detail),
        "review_decision_counts": {"not_applicable": len(SLIPPAGE_CATEGORIES)},
        "buyer_action_counts": {},
        "accountant_action_counts": {},
        "representative_evidence_packs": [],
        "source_curated_output": None,
        "top_level_failure": {"stage": stage, "detail": detail},
    }


def classify_cell_status(aggregate: dict[str, Any], manifest: dict[str, Any]) -> str:
    attempted = int(aggregate.get("attempted_runs", 0))
    accepted = int(aggregate.get("accepted_runs", 0))
    exclusions = aggregate.get("exclusion_summary", {})
    if accepted > 0:
        return "completed_with_accepted_runs"
    if attempted == 0:
        return "not_attempted"
    if exclusions.get("provider_or_api_failure") == attempted:
        details = " ".join(str(item.get("detail", "")) for item in manifest.get("exclusions", []))
        if any(token in details.lower() for token in ["model", "not found", "does not exist", "unsupported"]):
            return "model_unavailable"
        return "provider_failure"
    return "completed_all_runs_excluded"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_review_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return list(csv.DictReader(io.StringIO(path.read_text(encoding="utf-8"))))


def add_cell_fields(rows: list[dict[str, Any]], structure: StructureCondition, model: ModelCondition) -> list[dict[str, Any]]:
    result = []
    for row in rows:
        enriched = dict(row)
        enriched.update(
            {
                "structure_id": structure.structure_id,
                "structure_name": structure.structure_name,
                "scenario_id": structure.scenario_id,
                "model_condition_id": model.condition_id,
                "requested_model": model.requested_model,
            }
        )
        result.append(enriched)
    return result


def unavailable_review_rows(structure: StructureCondition, model: ModelCondition, detail: str) -> list[dict[str, Any]]:
    return [
        {
            "structure_id": structure.structure_id,
            "structure_name": structure.structure_name,
            "scenario_id": structure.scenario_id,
            "model_condition_id": model.condition_id,
            "requested_model": model.requested_model,
            "category_id": category_id,
            "category": category_id,
            "generated_candidate_count": "0",
            "generated_observed_count": "0",
            "generated_not_observed_count": "0",
            "review_decision": "not_applicable",
            "review_scope": "cell did not produce reviewable artificial evidence",
            "buyer_actions": "",
            "accountant_actions": "",
            "evidence_refs": "",
            "notes": detail,
        }
        for category_id in SLIPPAGE_CATEGORIES
    ]


def copy_matrix_representatives(*, cell_results: list[dict[str, Any]], curated_output: Path) -> list[dict[str, Any]]:
    copied: list[dict[str, Any]] = []
    for cell in cell_results:
        source_root = cell.get("source_curated_output")
        if source_root is None:
            continue
        for representative in selected_cell_representatives(cell):
            label = f"{cell['scenario_id'].lower()}-{cell['model_slug']}-{representative['label']}"
            evidence_rel = Path("representative-evidence-packs") / cell["structure_slug"] / cell["model_slug"] / representative["label"]
            validation_rel = Path("representative-validation-outputs") / cell["structure_slug"] / cell["model_slug"] / f"{representative['label']}.md"
            shutil.copytree(source_root / representative["evidence_pack"], curated_output / evidence_rel)
            (curated_output / validation_rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root / representative["validation_output"], curated_output / validation_rel)
            copied.append(
                {
                    "label": label,
                    "structure_id": cell["structure_id"],
                    "scenario_id": cell["scenario_id"],
                    "model_condition_id": cell["model_condition_id"],
                    "requested_model": cell["requested_model"],
                    "run_id": representative.get("run_id", "not_recorded"),
                    "evidence_pack": evidence_rel.as_posix(),
                    "validation_output": validation_rel.as_posix(),
                }
            )
    return copied


def selected_cell_representatives(cell: dict[str, Any]) -> list[dict[str, Any]]:
    representatives = cell.get("representative_evidence_packs", [])
    if not representatives:
        return []
    candidate_run_ids = {
        row.get("run_id")
        for row in cell.get("candidate_rows", [])
        if row.get("status") == "candidate" and row.get("category_id") in {"SL1", "SL2", "SL3", "SL4", "SL6", "FM3", "FM6"}
    }
    for representative in representatives:
        if representative.get("run_id") in candidate_run_ids:
            return [representative]
    if cell.get("model_condition_id") != "M_GPT_4_1_MINI":
        return []
    return [representatives[0]]


def build_matrix_aggregate(
    *,
    batch_id: str,
    started_at: str,
    completed_at: str,
    cell_results: list[dict[str, Any]],
    representatives: list[dict[str, Any]],
) -> dict[str, Any]:
    review_rows = [row for cell in cell_results for row in cell["candidate_review_rows"]]
    return {
        "pilot_id": PILOT_ID,
        "batch_id": batch_id,
        "protocol_ref": PROTOCOL_REF,
        "claim_boundary": CLAIM_BOUNDARY,
        "started_at": started_at,
        "completed_at": completed_at,
        "planned_cells": len(cell_results),
        "runs_per_cell": RUNS_PER_CELL,
        "planned_attempted_runs_if_all_available": len(cell_results) * RUNS_PER_CELL,
        "attempted_runs": sum(int(cell.get("attempted_runs", 0)) for cell in cell_results),
        "accepted_runs": sum(int(cell.get("accepted_runs", 0)) for cell in cell_results),
        "excluded_runs": sum(int(cell.get("excluded_runs", 0)) for cell in cell_results),
        "cell_status_counts": dict(sorted(Counter(cell["cell_status"] for cell in cell_results).items())),
        "model_conditions": [model.__dict__ for model in MODEL_CONDITIONS],
        "structure_conditions": [
            {
                "structure_id": structure.structure_id,
                "structure_name": structure.structure_name,
                "protocol_ref": structure.protocol_ref,
                "scenario_id": structure.scenario_id,
                "scenario_ref": structure.scenario_ref,
            }
            for structure in STRUCTURE_CONDITIONS
        ],
        "matrix_cells": [public_cell_result(cell) for cell in cell_results],
        "candidate_review_rows": review_rows,
        "candidate_review_decision_counts": dict(sorted(Counter(row["review_decision"] for row in review_rows).items())),
        "category_review_summary": build_category_review_summary(review_rows),
        "structure_model_pattern_summary": build_pattern_summary(cell_results, review_rows),
        "representative_evidence_packs": representatives,
        "allowed_claim": "The frozen Phase 4 information-structure/model matrix was attempted, and the recorded candidate, review, validation, and exclusion outcomes remain bounded to artificial evidence.",
        "limitations": [
            "exploratory matrix, not a baseline",
            "no model comparison or model ranking",
            "candidate rows are not support before review",
            "reviewed support remains artificial-evidence-only",
            "no human behavior, real-world organization, statistical, compliance, legal, audit, operational, governance, or safety sufficiency claim",
        ],
        "next_decision": select_next_decision(cell_results, review_rows),
    }


def public_cell_result(cell: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value
        for key, value in cell.items()
        if key not in {"source_curated_output", "candidate_rows", "candidate_review_rows"}
    }


def build_category_review_summary(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    summary: dict[str, Counter[str]] = {category: Counter() for category in SLIPPAGE_CATEGORIES}
    for row in rows:
        category = row.get("category_id", "unknown")
        summary.setdefault(category, Counter())[row.get("review_decision", "not_recorded")] += 1
    return {category: dict(sorted(counts.items())) for category, counts in sorted(summary.items())}


def build_pattern_summary(cell_results: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    supported_rows = [
        row
        for row in rows
        if row.get("review_decision") in {"supported_for_reviewed_evidence", "partially_supported_needs_revision"}
    ]
    sl2_supported_structures = sorted({row["structure_id"] for row in supported_rows if row.get("category_id") == "SL2"})
    stronger_supported = [
        row
        for row in supported_rows
        if row.get("category_id") in {"SL3", "SL4", "SL6"}
    ]
    auxiliary_supported = [
        row
        for row in supported_rows
        if row.get("category_id") in {"SL1", "FM1", "FM3", "FM6"}
    ]
    non_lossy_sl2 = sorted(structure for structure in sl2_supported_structures if structure != "S18_LOSSY_HANDOFF")
    return {
        "sl2_supported_structures": sl2_supported_structures,
        "non_lossy_sl2_supported_structures": non_lossy_sl2,
        "stronger_downstream_supported_categories": sorted({row["category_id"] for row in stronger_supported}),
        "auxiliary_partial_or_supported_categories": sorted({row["category_id"] for row in auxiliary_supported}),
        "auxiliary_partial_or_supported_cells": sorted(
            {
                f"{row['structure_id']}:{row['model_condition_id']}:{row['category_id']}"
                for row in auxiliary_supported
            }
        ),
        "cells_with_accepted_runs": sum(1 for cell in cell_results if int(cell.get("accepted_runs", 0)) > 0),
        "cells_without_accepted_runs": sum(1 for cell in cell_results if int(cell.get("accepted_runs", 0)) == 0),
        "lossy_handoff_remains_only_sl2_structure": sl2_supported_structures == ["S18_LOSSY_HANDOFF"],
    }


def select_next_decision(cell_results: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, str]:
    supported = [
        row
        for row in rows
        if row.get("review_decision") in {"supported_for_reviewed_evidence", "partially_supported_needs_revision"}
    ]
    if any(row.get("category_id") in {"SL3", "SL4", "SL6"} for row in supported):
        return {
            "decision": "pause_for_project_owner_or_external_review",
            "rationale": "At least one stronger downstream slippage category has reviewed support or partial support.",
        }
    auxiliary = [
        row
        for row in supported
        if row.get("category_id") in {"SL1", "FM1", "FM3", "FM6"}
    ]
    if auxiliary:
        return {
            "decision": "freeze_focused_independent_review_of_auxiliary_partial_candidates",
            "rationale": "The matrix produced auxiliary partial support in SL1/FM3/FM6-style categories without SL3, SL4, or SL6 support; these candidates should be independently reviewed before new prompt, persona, or mechanism execution.",
        }
    non_lossy_sl2 = [
        row
        for row in supported
        if row.get("category_id") == "SL2" and row.get("structure_id") != "S18_LOSSY_HANDOFF"
    ]
    if non_lossy_sl2:
        return {
            "decision": "freeze_focused_follow_up_on_non_lossy_structure",
            "rationale": "At least one non-lossy structure generated reviewed SL2 support.",
        }
    if any(cell["cell_status"] in {"model_unavailable", "provider_failure"} for cell in cell_results):
        return {
            "decision": "record_model_availability_limit_and_continue_with_available_cells",
            "rationale": "One or more requested model cells did not produce accepted runs; unavailable cells should not be silently substituted.",
        }
    return {
        "decision": "freeze_lossy_handoff_difference_analysis_before_prompt_or_persona_variants",
        "rationale": "Lossy handoff remains the only SL2-producing tested structure while queue/ticket and exception-route cells preserve gaps.",
    }


def build_execution_manifest(aggregate: dict[str, Any]) -> dict[str, Any]:
    return {
        "pilot_id": aggregate["pilot_id"],
        "batch_id": aggregate["batch_id"],
        "protocol_ref": aggregate["protocol_ref"],
        "claim_boundary": aggregate["claim_boundary"],
        "started_at": aggregate["started_at"],
        "completed_at": aggregate["completed_at"],
        "planned_cells": aggregate["planned_cells"],
        "runs_per_cell": aggregate["runs_per_cell"],
        "attempted_runs": aggregate["attempted_runs"],
        "accepted_runs": aggregate["accepted_runs"],
        "excluded_runs": aggregate["excluded_runs"],
        "cell_status_counts": aggregate["cell_status_counts"],
        "raw_output_policy": "raw per-cell outputs are written under ignored runs/ paths",
        "curated_output_policy": "only aggregate outputs and representative evidence packs are committed under pilot-runs/",
        "replacement_policy": "excluded runs are not silently replaced",
        "matrix_cells": [
            {
                "structure_id": cell["structure_id"],
                "model_condition_id": cell["model_condition_id"],
                "requested_model": cell["requested_model"],
                "cell_status": cell["cell_status"],
                "attempted_runs": cell["attempted_runs"],
                "accepted_runs": cell["accepted_runs"],
                "excluded_runs": cell["excluded_runs"],
                "exclusion_summary": cell["exclusion_summary"],
            }
            for cell in aggregate["matrix_cells"]
        ],
    }


def render_matrix_summary_csv(aggregate: dict[str, Any]) -> str:
    fields = [
        "structure_id",
        "scenario_id",
        "model_condition_id",
        "requested_model",
        "cell_status",
        "attempted_runs",
        "accepted_runs",
        "excluded_runs",
        "validation_pass",
        "validation_fail",
        "sl2_review_decision",
        "sl3_review_decision",
        "sl4_review_decision",
        "sl5_review_decision",
        "sl6_review_decision",
        "fm1_review_decision",
        "fm3_review_decision",
        "fm6_review_decision",
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    rows_by_cell = defaultdict(list)
    for row in aggregate["candidate_review_rows"]:
        rows_by_cell[(row["structure_id"], row["model_condition_id"])].append(row)
    for cell in aggregate["matrix_cells"]:
        reviews = {row["category_id"].lower(): row["review_decision"] for row in rows_by_cell[(cell["structure_id"], cell["model_condition_id"])]}
        validation = cell.get("validation_summary", {})
        writer.writerow(
            {
                "structure_id": cell["structure_id"],
                "scenario_id": cell["scenario_id"],
                "model_condition_id": cell["model_condition_id"],
                "requested_model": cell["requested_model"],
                "cell_status": cell["cell_status"],
                "attempted_runs": cell["attempted_runs"],
                "accepted_runs": cell["accepted_runs"],
                "excluded_runs": cell["excluded_runs"],
                "validation_pass": validation.get("pass", 0),
                "validation_fail": validation.get("fail", 0),
                "sl2_review_decision": reviews.get("sl2", "not_recorded"),
                "sl3_review_decision": reviews.get("sl3", "not_recorded"),
                "sl4_review_decision": reviews.get("sl4", "not_recorded"),
                "sl5_review_decision": reviews.get("sl5", "not_recorded"),
                "sl6_review_decision": reviews.get("sl6", "not_recorded"),
                "fm1_review_decision": reviews.get("fm1", "not_recorded"),
                "fm3_review_decision": reviews.get("fm3", "not_recorded"),
                "fm6_review_decision": reviews.get("fm6", "not_recorded"),
            }
        )
    return output.getvalue()


def render_candidate_summary_csv(rows: list[dict[str, Any]]) -> str:
    fields = [
        "structure_id",
        "scenario_id",
        "model_condition_id",
        "requested_model",
        "category_id",
        "category",
        "generated_candidate_count",
        "generated_observed_count",
        "generated_not_observed_count",
        "review_decision",
        "review_scope",
        "notes",
    ]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return output.getvalue()


def render_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# Phase 4 Information-Structure And Model Exploration Result",
        "",
        f"Pilot id: `{aggregate['pilot_id']}`",
        f"Protocol: [{aggregate['protocol_ref']}](../../../{aggregate['protocol_ref']})",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        f"Attempted runs: {aggregate['attempted_runs']}",
        f"Accepted runs: {aggregate['accepted_runs']}",
        f"Excluded runs: {aggregate['excluded_runs']}",
        f"Cell status counts: {format_counts(aggregate['cell_status_counts'])}",
        "",
        "This is an exploratory Phase 4 matrix result, not a baseline, model comparison, or statistical result.",
        "",
        "## Matrix Cells",
        "",
        "| structure | model | status | attempted | accepted | excluded |",
        "|---|---|---|---:|---:|---:|",
    ]
    for cell in aggregate["matrix_cells"]:
        lines.append(
            f"| `{cell['structure_id']}` | `{cell['requested_model']}` | `{cell['cell_status']}` | {cell['attempted_runs']} | {cell['accepted_runs']} | {cell['excluded_runs']} |"
        )
    lines.extend(["", "## Category Review Summary", ""])
    for category, counts in aggregate["category_review_summary"].items():
        lines.append(f"- `{category}`: {format_counts(counts)}")
    lines.extend(
        [
            "",
            "## Pattern Summary",
            "",
            f"- SL2 supported structures: {format_inline_list(aggregate['structure_model_pattern_summary']['sl2_supported_structures'])}",
            f"- Non-lossy SL2 supported structures: {format_inline_list(aggregate['structure_model_pattern_summary']['non_lossy_sl2_supported_structures'])}",
            f"- Stronger downstream supported categories: {format_inline_list(aggregate['structure_model_pattern_summary']['stronger_downstream_supported_categories'])}",
            f"- Auxiliary partial/supported categories: {format_inline_list(aggregate['structure_model_pattern_summary']['auxiliary_partial_or_supported_categories'])}",
            "",
            "## Representative Evidence",
            "",
            "| label | structure | model | run | pack | validation |",
            "|---|---|---|---|---|---|",
        ]
    )
    if not aggregate["representative_evidence_packs"]:
        lines.append("| none | none | none | none | none | none |")
    for representative in aggregate["representative_evidence_packs"]:
        lines.append(
            f"| `{representative['label']}` | `{representative['structure_id']}` | `{representative['requested_model']}` | `{representative['run_id']}` | [pack]({representative['evidence_pack']}) | [validation]({representative['validation_output']}) |"
        )
    lines.extend(
        [
            "",
            "## Candidate Review",
            "",
            "Candidate review is included in [candidate-review-0001](candidate-review-0001/summary.md). Generated candidates are not support until reviewed.",
            "",
            "## Next Decision",
            "",
            f"Decision: `{aggregate['next_decision']['decision']}`",
            "",
            aggregate["next_decision"]["rationale"],
            "",
            "## Limitations",
            "",
        ]
    )
    lines.extend(f"- {limitation}." for limitation in aggregate["limitations"])
    return "\n".join(lines) + "\n"


def write_candidate_review_package(curated_output: Path, aggregate: dict[str, Any]) -> None:
    review_dir = curated_output / "candidate-review-0001"
    rows = aggregate["candidate_review_rows"]
    write_json(
        review_dir / "review-manifest.json",
        {
            "review_id": "candidate-review-0001",
            "pilot_id": aggregate["pilot_id"],
            "protocol_ref": aggregate["protocol_ref"],
            "reviewed_categories": SLIPPAGE_CATEGORIES,
            "review_decision_counts": aggregate["candidate_review_decision_counts"],
            "claim_boundary": aggregate["claim_boundary"],
            "reviewer": "Codex proxy review under project-owner authorization",
            "review_scope": "artificial evidence package review only; no human, real-world, statistical, prompt-causation, model-general, compliance, legal, audit, operational, governance, or safety sufficiency claim",
        },
    )
    write_text(review_dir / "review-table.csv", render_candidate_summary_csv(rows))
    write_text(review_dir / "summary.md", render_review_summary(aggregate))
    write_text(review_dir / "evidence-notes.md", render_review_evidence_notes(aggregate))
    write_text(review_dir / "claim-boundary-review.md", render_review_claim_boundary(aggregate))


def render_review_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# Candidate Review: Phase 4 Information-Structure And Model Exploration",
        "",
        f"Pilot id: `{aggregate['pilot_id']}`",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        "This review aggregates the per-cell candidate reviews produced by the frozen S18, S19, and S20 diagnostic runners. It does not add runs, change frozen protocols, or upgrade generated candidates without review.",
        "",
        "| category | review decisions |",
        "|---|---|",
    ]
    for category, counts in aggregate["category_review_summary"].items():
        lines.append(f"| `{category}` | {format_counts(counts)} |")
    lines.extend(
        [
            "",
            "Reviewed support remains bounded to artificial evidence only. SL2 is not collapsed into SL3 or SL4, and SL5 gap preservation is not treated as completed slippage failure.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_review_evidence_notes(aggregate: dict[str, Any]) -> str:
    lines = [
        "# Evidence Notes",
        "",
        "Evidence notes are drawn from the per-cell candidate review tables and aggregate manifests.",
        "",
    ]
    for cell in aggregate["matrix_cells"]:
        lines.extend(
            [
                f"## {cell['structure_id']} / {cell['requested_model']}",
                "",
                f"- Status: `{cell['cell_status']}`",
                f"- Accepted runs: {cell['accepted_runs']}",
                f"- Excluded runs: {cell['excluded_runs']}",
                f"- Failure-mode summary: `{json.dumps(cell.get('failure_mode_summary', {}), sort_keys=True)}`",
                "",
            ]
        )
    return "\n".join(lines)


def render_review_claim_boundary(aggregate: dict[str, Any]) -> str:
    return f"""# Claim Boundary Review

Pilot id: `{aggregate["pilot_id"]}`
Claim boundary: `{aggregate["claim_boundary"]}`

Allowed claim:

> {aggregate["allowed_claim"]}

Forbidden claims remain unchanged: this review does not claim human behavior, real-world organization behavior, statistical significance, prompt causation, model-general behavior, model ranking, full approval bypass without separate SL3/SL4 review support, fraud, intentional misconduct, compliance sufficiency, legal sufficiency, audit sufficiency, operational sufficiency, governance sufficiency, or safety sufficiency.
"""


def render_reflection(aggregate: dict[str, Any]) -> str:
    pattern = aggregate["structure_model_pattern_summary"]
    return f"""# Phase 4 Information-Structure And Model Exploration Reflection

Date: 2026-05-17
Protocol: [{aggregate["protocol_ref"]}](../../{aggregate["protocol_ref"]})
Curated result: [phase4-information-structure-model-exploration-0001](../../pilot-runs/org-payment/phase4-information-structure-model-exploration-0001/summary.md)
Claim boundary: `{aggregate["claim_boundary"]}`

## Result Type

The frozen Phase 4 information-structure/model matrix was executed as an exploratory diagnostic. This is not a baseline, model comparison, statistical result, prompt-causation result, human behavior result, or real-world organization result.

## Current Pattern

- SL2 supported structures: {format_inline_list(pattern["sl2_supported_structures"])}
- Non-lossy SL2 supported structures: {format_inline_list(pattern["non_lossy_sl2_supported_structures"])}
- Stronger downstream supported categories: {format_inline_list(pattern["stronger_downstream_supported_categories"])}
- Auxiliary partial/supported categories: {format_inline_list(pattern["auxiliary_partial_or_supported_categories"])}
- Auxiliary partial/supported cells: {format_inline_list(pattern["auxiliary_partial_or_supported_cells"])}
- Cells with accepted runs: {pattern["cells_with_accepted_runs"]}
- Cells without accepted runs: {pattern["cells_without_accepted_runs"]}

## STOP Condition Check

- Stronger downstream SL3/SL4/SL6 support requiring human review: `{bool(pattern["stronger_downstream_supported_categories"])}`
- Candidate/support distinction preserved: `yes`
- Frozen protocols changed after seeing outputs: `no`
- Human, real-world, statistical, compliance, legal, audit, operational, governance, or safety sufficiency claim made: `no`

## Decision

Decision: `{aggregate["next_decision"]["decision"]}`

Rationale: {aggregate["next_decision"]["rationale"]}

This decision keeps Phase 4 open unless the matrix satisfies the research-completion criteria. Delivery of this matrix alone does not close Phase 4.
"""


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "`none`"
    return ", ".join(f"`{key}`: {value}" for key, value in sorted(counts.items()))


def format_inline_list(values: list[str]) -> str:
    if not values:
        return "`none`"
    return ", ".join(f"`{value}`" for value in values)
