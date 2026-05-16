from __future__ import annotations

import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import validate_pack

from .evidence_pack_writer import write_json, write_text
from .free_choice_runner import SWEEP_ACTION_MENU_ID, run_buyer_free_choice_llm
from .llm_actor import LLMProvider
from .repeated_runner import PROMPT_TEMPLATE_REF, require_new_or_empty
from .scenario_loader import load_org_payment_scenarios


DEFAULT_SWEEP_BATCH_ID = "pilot-buyer-sweep"


@dataclass(frozen=True)
class SweepRunRecord:
    scenario_id: str
    scenario_name: str
    index: int
    run_id: str
    selected_action_type: str
    selected_target_role: str
    parser_status: str
    attempt_count: int
    rejected_attempt_count: int
    gm_decision: str
    validation_status: str
    pack_dir: Path


def run_buyer_scenario_sweep(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider,
    count_per_scenario: int = 3,
    batch_id: str = DEFAULT_SWEEP_BATCH_ID,
) -> Path:
    if count_per_scenario < 1:
        raise ValueError("count_per_scenario must be at least 1")
    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    scenarios = load_org_payment_scenarios()
    records: list[SweepRunRecord] = []
    for scenario in scenarios:
        scenario_id = scenario["id"]
        scenario_slug = scenario_id.lower()
        for index in range(1, count_per_scenario + 1):
            run_id = f"{batch_id}-{scenario_slug}-run-{index:03d}"
            run_root = output_root / scenario_slug / f"run-{index:03d}"
            pack_dir = run_root / "evidence-pack"
            run_buyer_free_choice_llm(
                output_dir=pack_dir,
                provider=provider,
                scenario=scenario,
                run_id=run_id,
                batch_execution=True,
                action_menu_id=SWEEP_ACTION_MENU_ID,
            )
            report = validate_pack(pack_dir)
            write_text(run_root / "validation-output.md", report.as_markdown())
            records.append(read_sweep_record(scenario=scenario, index=index, run_id=run_id, pack_dir=pack_dir))

    representatives = copy_sweep_representatives(records=records, curated_output=curated_output)
    aggregate = build_sweep_aggregate(
        provider=provider,
        scenarios=scenarios,
        records=records,
        representatives=representatives,
        count_per_scenario=count_per_scenario,
        batch_id=batch_id,
    )
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "summary.md", render_sweep_summary(aggregate))
    return curated_output


def read_sweep_record(
    *,
    scenario: dict[str, Any],
    index: int,
    run_id: str,
    pack_dir: Path,
) -> SweepRunRecord:
    parser_result = load_json(pack_dir / "parser_result.json")
    attempts = load_jsonl(pack_dir / "proposal_attempts.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    rejected_attempt_count = sum(1 for attempt in attempts if attempt.get("status") != "accepted_by_parser")
    return SweepRunRecord(
        scenario_id=scenario["id"],
        scenario_name=scenario["name"],
        index=index,
        run_id=run_id,
        selected_action_type=parser_result["selected_action_type"],
        selected_target_role=parser_result["selected_target_role"],
        parser_status=parser_result["parser_status"],
        attempt_count=parser_result["attempt_count"],
        rejected_attempt_count=rejected_attempt_count,
        gm_decision=decisions[0]["decision"],
        validation_status="PASS",
        pack_dir=pack_dir,
    )


def copy_sweep_representatives(
    *,
    records: list[SweepRunRecord],
    curated_output: Path,
) -> list[dict[str, str]]:
    selected: dict[tuple[str, str], SweepRunRecord] = {}
    first_by_scenario: dict[str, SweepRunRecord] = {}
    for record in records:
        first_by_scenario.setdefault(record.scenario_id, record)
        selected.setdefault((record.scenario_id, record.selected_action_type), record)

    for record in first_by_scenario.values():
        selected.setdefault((record.scenario_id, record.selected_action_type), record)

    representatives: list[dict[str, str]] = []
    for (scenario_id, action_type), record in sorted(selected.items()):
        scenario_slug = scenario_id.lower()
        directory_name = f"{action_type}-run-{record.index:03d}"
        pack_path = Path("representative-evidence-packs") / scenario_slug / directory_name
        validation_path = Path("representative-validation-outputs") / scenario_slug / f"{directory_name}.md"
        shutil.copytree(record.pack_dir, curated_output / pack_path)
        validation_report = validate_pack(curated_output / pack_path).as_markdown()
        write_text(curated_output / validation_path, validation_report)
        representatives.append(
            {
                "scenario_id": scenario_id,
                "selected_action_type": action_type,
                "run_id": record.run_id,
                "evidence_pack": pack_path.as_posix(),
                "validation_output": validation_path.as_posix(),
            }
        )
    return representatives


def build_sweep_aggregate(
    *,
    provider: LLMProvider,
    scenarios: list[dict[str, Any]],
    records: list[SweepRunRecord],
    representatives: list[dict[str, str]],
    count_per_scenario: int,
    batch_id: str,
) -> dict[str, Any]:
    records_by_scenario: dict[str, list[SweepRunRecord]] = defaultdict(list)
    for record in records:
        records_by_scenario[record.scenario_id].append(record)

    scenario_summaries: list[dict[str, Any]] = []
    for scenario in scenarios:
        scenario_id = scenario["id"]
        scenario_records = records_by_scenario[scenario_id]
        selected_counts = Counter(record.selected_action_type for record in scenario_records)
        gm_decisions: dict[str, Counter[str]] = defaultdict(Counter)
        for record in scenario_records:
            gm_decisions[record.selected_action_type][record.gm_decision] += 1
        scenario_summaries.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": scenario["name"],
                "policy_ambiguity": scenario["manipulated_variables"]["policy_ambiguity"],
                "deadline_pressure": scenario["manipulated_variables"]["deadline_pressure"],
                "role_overlap": scenario["manipulated_variables"]["role_overlap"],
                "audit_presence": scenario["manipulated_variables"]["audit_presence"],
                "control_mode": scenario["control_mode"],
                "selected_action_type_counts": dict(sorted(selected_counts.items())),
                "parser_summary": {
                    "runs_with_parser_acceptance": sum(
                        1 for record in scenario_records if record.parser_status == "accepted"
                    ),
                    "total_attempts": sum(record.attempt_count for record in scenario_records),
                    "total_rejected_or_invalid_attempts": sum(
                        record.rejected_attempt_count for record in scenario_records
                    ),
                    "runs_with_retries": sum(1 for record in scenario_records if record.attempt_count > 1),
                },
                "gm_decisions_by_selected_action": {
                    action_type: dict(sorted(counter.items())) for action_type, counter in sorted(gm_decisions.items())
                },
                "validation_summary": {
                    "pass": sum(1 for record in scenario_records if record.validation_status == "PASS"),
                    "fail": sum(1 for record in scenario_records if record.validation_status != "PASS"),
                },
            }
        )

    return {
        "batch_id": batch_id,
        "provider": provider.provider,
        "model": provider.model,
        "scenario_ids": [scenario["id"] for scenario in scenarios],
        "actor_setup": "buyer_only_llm",
        "other_roles": "scripted_or_rule_based",
        "game_master": "deterministic_menu_aware_rules",
        "action_menu_id": SWEEP_ACTION_MENU_ID,
        "prompt_template_ref": PROMPT_TEMPLATE_REF,
        "count_per_scenario": count_per_scenario,
        "run_count": len(records),
        "claim_boundary": "pilot_observation_only",
        "allowed_claim": (
            "Across this small buyer-only scenario sweep pilot, action selections were recorded "
            "for S01-S06 under fixed artificial conditions."
        ),
        "forbidden_claims": [
            "Scenario differences are statistically significant.",
            "S04 causes risky behavior.",
            "Hard control is proven effective.",
            "Human organizations would behave similarly.",
        ],
        "scenario_summaries": scenario_summaries,
        "representative_evidence_packs": representatives,
        "runs": [
            {
                "scenario_id": record.scenario_id,
                "index": record.index,
                "run_id": record.run_id,
                "selected_action_type": record.selected_action_type,
                "selected_target_role": record.selected_target_role,
                "parser_status": record.parser_status,
                "attempt_count": record.attempt_count,
                "rejected_attempt_count": record.rejected_attempt_count,
                "gm_decision": record.gm_decision,
                "validation_status": record.validation_status,
            }
            for record in records
        ],
    }


def render_sweep_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# Buyer-Only Scenario Sweep Pilot Summary",
        "",
        f"Batch id: `{aggregate['batch_id']}`",
        f"Provider: `{aggregate['provider']}`",
        f"Model: `{aggregate['model']}`",
        "Scenario ids: `S01`-`S06`",
        f"Actor setup: `{aggregate['actor_setup']}`",
        f"Other roles: `{aggregate['other_roles']}`",
        f"Game Master: `{aggregate['game_master']}`",
        f"Action menu id: `{aggregate['action_menu_id']}`",
        f"Prompt template: [{aggregate['prompt_template_ref']}](../../../{aggregate['prompt_template_ref']})",
        f"Count per scenario: {aggregate['count_per_scenario']}",
        f"Run count: {aggregate['run_count']}",
        "Claim boundary: pilot observation only",
        "",
        aggregate["allowed_claim"],
        "",
        "This summary does not claim that scenario differences are statistically significant, that S04 causes risky behavior, that hard control is proven effective, or that human organizations would behave similarly.",
        "",
        "## Scenario Summary",
        "",
        "| scenario_id | policy_ambiguity | deadline_pressure | role_overlap | audit_presence | control_mode | selected action counts | GM decision counts | validation |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for scenario in aggregate["scenario_summaries"]:
        lines.append(
            "| "
            f"`{scenario['scenario_id']}` | "
            f"`{scenario['policy_ambiguity']}` | "
            f"`{scenario['deadline_pressure']}` | "
            f"`{scenario['role_overlap']}` | "
            f"`{scenario['audit_presence']}` | "
            f"`{scenario['control_mode']}` | "
            f"{format_counts(scenario['selected_action_type_counts'])} | "
            f"{format_nested_counts(scenario['gm_decisions_by_selected_action'])} | "
            f"PASS {scenario['validation_summary']['pass']} / FAIL {scenario['validation_summary']['fail']} |"
        )

    lines.extend(
        [
            "",
            "## Parser Summary By Scenario",
            "",
            "| scenario_id | accepted runs | attempts | rejected or invalid proposals | runs with retries |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for scenario in aggregate["scenario_summaries"]:
        parser = scenario["parser_summary"]
        lines.append(
            "| "
            f"`{scenario['scenario_id']}` | "
            f"{parser['runs_with_parser_acceptance']} | "
            f"{parser['total_attempts']} | "
            f"{parser['total_rejected_or_invalid_attempts']} | "
            f"{parser['runs_with_retries']} |"
        )

    lines.extend(
        [
            "",
            "## Representative Evidence",
            "",
            "| scenario_id | selected action_type | run_id | evidence pack | validation output |",
            "|---|---|---|---|---|",
        ]
    )
    for representative in aggregate["representative_evidence_packs"]:
        lines.append(
            "| "
            f"`{representative['scenario_id']}` | "
            f"`{representative['selected_action_type']}` | "
            f"`{representative['run_id']}` | "
            f"[pack]({representative['evidence_pack']}) | "
            f"[validation]({representative['validation_output']}) |"
        )

    lines.extend(
        [
            "",
            "Raw per-run outputs were generated under ignored `runs/` paths during validation and are not committed.",
        ]
    )
    return "\n".join(lines) + "\n"


def format_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "`none`"
    return ", ".join(f"`{key}`: {value}" for key, value in sorted(counts.items()))


def format_nested_counts(counts: dict[str, dict[str, int]]) -> str:
    parts: list[str] = []
    for outer_key, inner_counts in sorted(counts.items()):
        inner = ", ".join(f"{key}: {value}" for key, value in sorted(inner_counts.items()))
        parts.append(f"`{outer_key}` -> {inner}")
    return "<br>".join(parts) if parts else "`none`"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
