from __future__ import annotations

import csv
import io
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import ValidationError, validate_pack

from .evidence_pack_writer import write_json, write_jsonl, write_text
from .free_choice_runner import SWEEP_ACTION_MENU_ID, run_buyer_free_choice_llm
from .llm_actor import LLMProvider
from .repeated_runner import PROMPT_TEMPLATE_REF, require_new_or_empty
from .scenario_loader import dump_yaml, load_org_payment_scenarios, org_payment_scenario_ref
from .scenario_sweep_runner import format_counts, format_nested_counts, load_json, load_jsonl


EXPERIMENT_ID = "EXP-0001"
BASELINE_PROTOCOL_ID = "buyer-only-baseline-v0.1"
BASELINE_PROTOCOL_REF = "protocols/baseline/buyer-only-baseline-v0.1.md"
DEFAULT_BASELINE_BATCH_ID = "exp-0001-buyer-only-baseline"
FROZEN_RUNS_PER_SCENARIO = 5
FROZEN_SCENARIO_COUNT = 6
FROZEN_TOTAL_PLANNED_RUNS = FROZEN_RUNS_PER_SCENARIO * FROZEN_SCENARIO_COUNT
RESULT_CLAIM_BOUNDARY = "artificial_organization_buyer_only_baseline"


@dataclass(frozen=True)
class BaselineRunRecord:
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
    model_version: str | None
    pack_dir: Path


@dataclass(frozen=True)
class ExcludedRunRecord:
    scenario_id: str
    scenario_name: str
    index: int
    run_id: str
    exclusion_reason: str
    stage: str
    detail: str


def run_buyer_only_baseline(
    *,
    output_root: Path,
    results_output: Path,
    provider: LLMProvider,
    batch_id: str = DEFAULT_BASELINE_BATCH_ID,
) -> Path:
    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(results_output, "results_output")
    output_root.mkdir(parents=True, exist_ok=True)
    results_output.mkdir(parents=True, exist_ok=True)

    started_at = now_utc()
    scenarios = load_org_payment_scenarios()
    records: list[BaselineRunRecord] = []
    exclusions: list[ExcludedRunRecord] = []

    for scenario in scenarios:
        scenario_id = scenario["id"]
        scenario_slug = scenario_id.lower()
        for index in range(1, FROZEN_RUNS_PER_SCENARIO + 1):
            run_id = f"{batch_id}-{scenario_slug}-run-{index:03d}"
            run_root = output_root / scenario_slug / f"run-{index:03d}"
            pack_dir = run_root / "evidence-pack"
            try:
                run_buyer_free_choice_llm(
                    output_dir=pack_dir,
                    provider=provider,
                    scenario=scenario,
                    run_id=run_id,
                    batch_execution=True,
                    action_menu_id=SWEEP_ACTION_MENU_ID,
                )
                apply_baseline_evidence_context(pack_dir=pack_dir, scenario=scenario, model=provider.model)
                report = validate_pack(pack_dir)
                write_text(run_root / "validation-output.md", report.as_markdown())
                records.append(read_baseline_record(scenario=scenario, index=index, run_id=run_id, pack_dir=pack_dir))
            except ValidationError as exc:
                write_text(run_root / "validation-output.md", failed_validation_markdown(pack_dir, str(exc)))
                exclusions.append(
                    ExcludedRunRecord(
                        scenario_id=scenario_id,
                        scenario_name=scenario["name"],
                        index=index,
                        run_id=run_id,
                        exclusion_reason="validation_failure",
                        stage="validation",
                        detail=str(exc),
                    )
                )
            except Exception as exc:
                exclusions.append(
                    ExcludedRunRecord(
                        scenario_id=scenario_id,
                        scenario_name=scenario["name"],
                        index=index,
                        run_id=run_id,
                        exclusion_reason=classify_exception(exc),
                        stage="generation",
                        detail=str(exc),
                    )
                )

    completed_at = now_utc()
    representatives = copy_baseline_representatives(records=records, results_output=results_output)
    execution_manifest = build_execution_manifest(
        provider=provider,
        started_at=started_at,
        completed_at=completed_at,
        batch_id=batch_id,
        records=records,
        exclusions=exclusions,
    )
    aggregate = build_baseline_aggregate(
        provider=provider,
        scenarios=scenarios,
        records=records,
        exclusions=exclusions,
        representatives=representatives,
        execution_manifest=execution_manifest,
        batch_id=batch_id,
    )

    write_json(results_output / "execution-manifest.json", execution_manifest)
    write_json(results_output / "aggregate.json", aggregate)
    write_text(results_output / "scenario-summary.csv", render_scenario_summary_csv(aggregate))
    write_text(results_output / "summary.md", render_baseline_summary(aggregate))
    return results_output


def apply_baseline_evidence_context(*, pack_dir: Path, scenario: dict[str, Any], model: str) -> None:
    action = load_jsonl(pack_dir / "actions.jsonl")[0]
    decision = load_jsonl(pack_dir / "gm_decisions.jsonl")[0]
    run_id = action["run_id"]
    case_id = action["case_id"]
    scenario_id = scenario["id"]

    manifest = load_json(pack_dir / "manifest.json")
    manifest.update(
        {
            "randomness_policy": (
                "one constrained buyer-only OpenAI LLM action selection from a five-item menu as an "
                "EXP-0001 baseline run; provider randomness is not explicitly seeded; aggregate "
                "reporting is handled in the EXP-0001 result package"
            ),
            "authored_by": "src/social_sim EXP-0001 buyer-only baseline runner",
            "claim_boundary": RESULT_CLAIM_BOUNDARY,
            "known_exclusions": [
                "no multi-role LLM simulation",
                "requester, approver, accountant, and vendor remain scripted or rule-based",
                "Game Master remains deterministic",
                f"single scenario {scenario_id} as one EXP-0001 baseline run",
                "one LLM-controlled role only",
                "no model comparison",
                "no statistical claim",
                "no real-world behavior claim",
                "no human behavior claim",
                "excluded runs are not replaced in EXP-0001",
            ],
        }
    )
    write_json(pack_dir / "manifest.json", manifest)

    baseline_scenario = dict(scenario)
    baseline_scenario.update(
        {
            "status": "generated_buyer_only_baseline_reference",
            "phase": "P7",
            "step": "EXP-0001 buyer-only baseline execution",
            "source_scenario": org_payment_scenario_ref(scenario_id),
        }
    )
    write_text(pack_dir / "scenario.yaml", dump_yaml(baseline_scenario))
    write_text(pack_dir / "final_state" / "case.md", baseline_final_state(run_id, case_id, scenario, action, decision))
    write_text(pack_dir / "reviewer_notes.md", baseline_reviewer_notes(run_id, model, scenario, action, decision))

    events = load_jsonl(pack_dir / "events.jsonl")
    for event in events:
        event["coded_by"] = "scripted event coder for EXP-0001 buyer-only baseline"
    write_jsonl(pack_dir / "events.jsonl", events)

    trace = load_jsonl(pack_dir / "trace.jsonl")
    for record in trace:
        if record.get("trace_id") == "T007":
            record["summary"] = "Scripted event coder emits proposed events for the EXP-0001 buyer-only baseline run."
    write_jsonl(pack_dir / "trace.jsonl", trace)

    metrics = load_json(pack_dir / "metrics.json")
    for metric in metrics.get("metrics", []):
        if metric.get("metric_id") == "MR001":
            metric["known_limitations"] = [
                "single EXP-0001 buyer-only baseline run",
                "aggregate baseline summary is reported separately",
                "no behavioral claim",
            ]
        elif metric.get("metric_id") == "MR002":
            metric["known_limitations"] = ["rule-based Game Master", "single EXP-0001 baseline run"]
        elif metric.get("metric_id") == "MR003":
            metric["known_limitations"] = ["scripted event coding over one LLM action choice"]
        elif metric.get("metric_id") == "MR004":
            metric["value"] = "mechanically_validated_buyer_only_baseline_pack"
            metric["known_limitations"] = ["single EXP-0001 baseline run", "no inter-reviewer reliability"]
    write_json(pack_dir / "metrics.json", metrics)


def read_baseline_record(
    *,
    scenario: dict[str, Any],
    index: int,
    run_id: str,
    pack_dir: Path,
) -> BaselineRunRecord:
    parser_result = load_json(pack_dir / "parser_result.json")
    attempts = load_jsonl(pack_dir / "proposal_attempts.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    llm_output = load_json(pack_dir / "llm_outputs" / "buyer_A001_free_choice.json")
    rejected_attempt_count = sum(1 for attempt in attempts if attempt.get("status") != "accepted_by_parser")
    return BaselineRunRecord(
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
        model_version=llm_output.get("response_metadata", {}).get("model_version"),
        pack_dir=pack_dir,
    )


def baseline_final_state(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    action: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    return f"""# Final State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

Selected buyer action: `{action["action_type"]}`
Target role: `{action["target_role"]}`
Game Master decision: `{decision["decision"]}`

State delta: {decision["state_delta_summary"]}

Claim boundary: this final state supports one EXP-0001 buyer-only baseline run observation only. Aggregate baseline accounting is reported separately.
"""


def baseline_reviewer_notes(
    run_id: str,
    model: str,
    scenario: dict[str, Any],
    action: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    return f"""# Generated Baseline Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Frozen protocol: `protocols/baseline/buyer-only-baseline-v0.1.md`
Runner: `src/social_sim`

This evidence pack is one included EXP-0001 buyer-only baseline run generated under the frozen baseline protocol.

Only the `buyer` role is LLM-controlled, and only for one action selection from the recorded five-item action menu. The requester, approver, accountant, and vendor records remain scripted or rule-based. The Game Master remains deterministic and menu-aware.

Provider: OpenAI
Model: {model}
Control mode: {scenario["control_mode"]}

Selected action: `{action["action_type"]}`
Game Master decision: `{decision["decision"]}`

This pack supports mechanical reconstruction of one baseline run and the aggregate EXP-0001 accounting reported outside the pack.

It is not a human review, statistical significance claim, multi-role LLM simulation, model comparison, real-world behavior claim, or human behavior claim.
"""


def copy_baseline_representatives(
    *,
    records: list[BaselineRunRecord],
    results_output: Path,
) -> list[dict[str, str]]:
    selected: dict[tuple[str, str], BaselineRunRecord] = {}
    first_by_scenario: dict[str, BaselineRunRecord] = {}
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
        shutil.copytree(record.pack_dir, results_output / pack_path)
        validation_report = validate_pack(results_output / pack_path).as_markdown()
        write_text(results_output / validation_path, validation_report)
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


def build_execution_manifest(
    *,
    provider: LLMProvider,
    started_at: str,
    completed_at: str,
    batch_id: str,
    records: list[BaselineRunRecord],
    exclusions: list[ExcludedRunRecord],
) -> dict[str, Any]:
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": BASELINE_PROTOCOL_ID,
        "frozen_protocol_ref": BASELINE_PROTOCOL_REF,
        "batch_id": batch_id,
        "provider": provider.provider,
        "model": provider.model,
        "model_versions_observed": sorted({record.model_version for record in records if record.model_version}),
        "started_at_utc": started_at,
        "completed_at_utc": completed_at,
        "scenario_ids": ["S01", "S02", "S03", "S04", "S05", "S06"],
        "runs_per_scenario": FROZEN_RUNS_PER_SCENARIO,
        "total_planned_runs": FROZEN_TOTAL_PLANNED_RUNS,
        "attempted_runs": FROZEN_TOTAL_PLANNED_RUNS,
        "accepted_runs": len(records),
        "excluded_runs": len(exclusions),
        "failed_runs": len(exclusions),
        "replacement_policy": "excluded runs are not replaced in EXP-0001",
        "actor_setup": "buyer_only_llm",
        "other_roles": "scripted_or_rule_based",
        "game_master": "deterministic_menu_aware_rules",
        "action_menu_id": SWEEP_ACTION_MENU_ID,
        "prompt_template_ref": PROMPT_TEMPLATE_REF,
        "claim_boundary": RESULT_CLAIM_BOUNDARY,
        "exclusions": [exclusion_to_dict(exclusion) for exclusion in exclusions],
    }


def build_baseline_aggregate(
    *,
    provider: LLMProvider,
    scenarios: list[dict[str, Any]],
    records: list[BaselineRunRecord],
    exclusions: list[ExcludedRunRecord],
    representatives: list[dict[str, str]],
    execution_manifest: dict[str, Any],
    batch_id: str,
) -> dict[str, Any]:
    records_by_scenario: dict[str, list[BaselineRunRecord]] = defaultdict(list)
    exclusions_by_scenario: dict[str, list[ExcludedRunRecord]] = defaultdict(list)
    for record in records:
        records_by_scenario[record.scenario_id].append(record)
    for exclusion in exclusions:
        exclusions_by_scenario[exclusion.scenario_id].append(exclusion)

    scenario_summaries: list[dict[str, Any]] = []
    for scenario in scenarios:
        scenario_id = scenario["id"]
        scenario_records = records_by_scenario[scenario_id]
        scenario_exclusions = exclusions_by_scenario[scenario_id]
        selected_counts = Counter(record.selected_action_type for record in scenario_records)
        gm_decisions: dict[str, Counter[str]] = defaultdict(Counter)
        for record in scenario_records:
            gm_decisions[record.selected_action_type][record.gm_decision] += 1
        exclusion_counts = Counter(exclusion.exclusion_reason for exclusion in scenario_exclusions)
        scenario_summaries.append(
            {
                "scenario_id": scenario_id,
                "scenario_name": scenario["name"],
                "policy_ambiguity": scenario["manipulated_variables"]["policy_ambiguity"],
                "deadline_pressure": scenario["manipulated_variables"]["deadline_pressure"],
                "role_overlap": scenario["manipulated_variables"]["role_overlap"],
                "audit_presence": scenario["manipulated_variables"]["audit_presence"],
                "control_mode": scenario["control_mode"],
                "attempted_runs": FROZEN_RUNS_PER_SCENARIO,
                "accepted_runs": len(scenario_records),
                "excluded_runs": len(scenario_exclusions),
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
                    "parser_failures": sum(
                        1 for exclusion in scenario_exclusions if exclusion.exclusion_reason == "parser_failure"
                    ),
                },
                "gm_decisions_by_selected_action": {
                    action_type: dict(sorted(counter.items())) for action_type, counter in sorted(gm_decisions.items())
                },
                "validation_summary": {
                    "pass": sum(1 for record in scenario_records if record.validation_status == "PASS"),
                    "fail": sum(
                        1 for exclusion in scenario_exclusions if exclusion.exclusion_reason == "validation_failure"
                    ),
                },
                "exclusion_summary": dict(sorted(exclusion_counts.items())),
            }
        )

    parser_attempt_distribution = Counter(record.attempt_count for record in records)
    exclusion_counts = Counter(exclusion.exclusion_reason for exclusion in exclusions)
    validation_passes = sum(1 for record in records if record.validation_status == "PASS")
    accepted_runs = len(records)
    attempted_runs = FROZEN_TOTAL_PLANNED_RUNS
    return {
        "experiment_id": EXPERIMENT_ID,
        "protocol_id": BASELINE_PROTOCOL_ID,
        "frozen_protocol_ref": BASELINE_PROTOCOL_REF,
        "batch_id": batch_id,
        "provider": provider.provider,
        "model": provider.model,
        "model_versions_observed": execution_manifest["model_versions_observed"],
        "scenario_ids": [scenario["id"] for scenario in scenarios],
        "actor_setup": "buyer_only_llm",
        "other_roles": "scripted_or_rule_based",
        "game_master": "deterministic_menu_aware_rules",
        "action_menu_id": SWEEP_ACTION_MENU_ID,
        "prompt_template_ref": PROMPT_TEMPLATE_REF,
        "runs_per_scenario": FROZEN_RUNS_PER_SCENARIO,
        "total_planned_runs": attempted_runs,
        "attempted_runs": attempted_runs,
        "accepted_runs": accepted_runs,
        "excluded_runs": len(exclusions),
        "claim_boundary": RESULT_CLAIM_BOUNDARY,
        "allowed_claims": [
            "Under the frozen EXP-0001 artificial organization protocol, buyer-only LLM runs produced the following action selection distribution across S01-S06.",
            "All included runs passed mechanical evidence-pack validation.",
            "These results are bounded to this artificial setup, model, prompt, and deterministic GM.",
        ],
        "forbidden_claims": [
            "Humans would behave this way.",
            "Real organizations would experience this failure rate.",
            "This proves soft/monitored/hard controls work or fail in real companies.",
            "This is a general result about all LLMs.",
            "This is a statistically meaningful behavioral distribution.",
        ],
        "validation_summary": {
            "total_runs_attempted": attempted_runs,
            "total_runs_included": accepted_runs,
            "parser_failures": exclusion_counts.get("parser_failure", 0),
            "validation_failures": exclusion_counts.get("validation_failure", 0),
            "api_or_provider_failures": exclusion_counts.get("provider_or_api_failure", 0),
            "other_generation_failures": sum(
                count
                for reason, count in exclusion_counts.items()
                if reason not in {"parser_failure", "validation_failure", "provider_or_api_failure"}
            ),
            "total_retries": sum(max(record.attempt_count - 1, 0) for record in records),
            "total_rejected_or_invalid_proposals": sum(record.rejected_attempt_count for record in records),
            "validation_pass_rate_included": 1.0 if accepted_runs else 0.0,
        },
        "parser_attempt_distribution": {str(key): value for key, value in sorted(parser_attempt_distribution.items())},
        "exclusion_summary": dict(sorted(exclusion_counts.items())),
        "scenario_summaries": scenario_summaries,
        "representative_evidence_packs": representatives,
        "runs": [record_to_dict(record) for record in records],
        "excluded_run_records": [exclusion_to_dict(exclusion) for exclusion in exclusions],
        "execution_manifest_ref": "execution-manifest.json",
    }


def render_scenario_summary_csv(aggregate: dict[str, Any]) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=[
            "scenario_id",
            "policy_ambiguity",
            "deadline_pressure",
            "role_overlap",
            "audit_presence",
            "control_mode",
            "attempted_runs",
            "accepted_runs",
            "excluded_runs",
            "selected_action_counts",
            "gm_decision_counts",
            "parser_attempts",
            "rejected_or_invalid_proposals",
            "validation_pass",
            "validation_fail",
            "exclusion_summary",
        ],
        lineterminator="\n",
    )
    writer.writeheader()
    for scenario in aggregate["scenario_summaries"]:
        parser = scenario["parser_summary"]
        validation = scenario["validation_summary"]
        writer.writerow(
            {
                "scenario_id": scenario["scenario_id"],
                "policy_ambiguity": scenario["policy_ambiguity"],
                "deadline_pressure": scenario["deadline_pressure"],
                "role_overlap": scenario["role_overlap"],
                "audit_presence": scenario["audit_presence"],
                "control_mode": scenario["control_mode"],
                "attempted_runs": scenario["attempted_runs"],
                "accepted_runs": scenario["accepted_runs"],
                "excluded_runs": scenario["excluded_runs"],
                "selected_action_counts": compact_counts(scenario["selected_action_type_counts"]),
                "gm_decision_counts": compact_nested_counts(scenario["gm_decisions_by_selected_action"]),
                "parser_attempts": parser["total_attempts"],
                "rejected_or_invalid_proposals": parser["total_rejected_or_invalid_attempts"],
                "validation_pass": validation["pass"],
                "validation_fail": validation["fail"],
                "exclusion_summary": compact_counts(scenario["exclusion_summary"]),
            }
        )
    return output.getvalue()


def render_baseline_summary(aggregate: dict[str, Any]) -> str:
    validation = aggregate["validation_summary"]
    lines = [
        "# EXP-0001 Buyer-Only Baseline Result",
        "",
        f"Frozen protocol: [{aggregate['frozen_protocol_ref']}](../../../{aggregate['frozen_protocol_ref']})",
        f"Execution manifest: [execution-manifest.json](execution-manifest.json)",
        f"Provider: `{aggregate['provider']}`",
        f"Model: `{aggregate['model']}`",
        f"Model versions observed: {format_inline_list(aggregate['model_versions_observed'])}",
        "Scenario ids: `S01`-`S06`",
        f"Runs per scenario: {aggregate['runs_per_scenario']}",
        f"Total runs attempted: {aggregate['attempted_runs']}",
        f"Total runs included: {aggregate['accepted_runs']}",
        f"Excluded runs: {aggregate['excluded_runs']}",
        f"Actor setup: `{aggregate['actor_setup']}`",
        f"Other roles: `{aggregate['other_roles']}`",
        f"Game Master: `{aggregate['game_master']}`",
        f"Action menu id: `{aggregate['action_menu_id']}`",
        f"Prompt template: [{aggregate['prompt_template_ref']}](../../../{aggregate['prompt_template_ref']})",
        f"Claim boundary: `{aggregate['claim_boundary']}`",
        "",
        "Under the frozen EXP-0001 artificial organization protocol, buyer-only LLM runs produced the following action selection distribution across S01-S06.",
        "",
    ]
    if validation["validation_failures"] == 0 and aggregate["accepted_runs"] > 0:
        lines.append("All included runs passed mechanical evidence-pack validation.")
        lines.append("")
    lines.extend(
        [
            "These results are bounded to this artificial setup, model, prompt, and deterministic GM.",
            "",
            "## Scenario Summary",
            "",
            "| scenario_id | policy_ambiguity | deadline_pressure | role_overlap | audit_presence | control_mode | attempted | included | excluded | selected action counts | GM decision counts | validation |",
            "|---|---|---|---|---|---|---:|---:|---:|---|---|---|",
        ]
    )
    for scenario in aggregate["scenario_summaries"]:
        lines.append(
            "| "
            f"`{scenario['scenario_id']}` | "
            f"`{scenario['policy_ambiguity']}` | "
            f"`{scenario['deadline_pressure']}` | "
            f"`{scenario['role_overlap']}` | "
            f"`{scenario['audit_presence']}` | "
            f"`{scenario['control_mode']}` | "
            f"{scenario['attempted_runs']} | "
            f"{scenario['accepted_runs']} | "
            f"{scenario['excluded_runs']} | "
            f"{format_counts(scenario['selected_action_type_counts'])} | "
            f"{format_nested_counts(scenario['gm_decisions_by_selected_action'])} | "
            f"PASS {scenario['validation_summary']['pass']} / FAIL {scenario['validation_summary']['fail']} |"
        )

    lines.extend(
        [
            "",
            "## Validation Summary",
            "",
            f"- Total runs attempted: {validation['total_runs_attempted']}",
            f"- Total runs included: {validation['total_runs_included']}",
            f"- Parser failures: {validation['parser_failures']}",
            f"- Validation failures: {validation['validation_failures']}",
            f"- API/provider failures: {validation['api_or_provider_failures']}",
            f"- Other generation failures: {validation['other_generation_failures']}",
            f"- Total retries: {validation['total_retries']}",
            f"- Rejected or invalid proposals: {validation['total_rejected_or_invalid_proposals']}",
            f"- Validation pass rate for included runs: {validation['validation_pass_rate_included']:.2f}",
            "",
            "## Parser Attempt Distribution",
            "",
            "| attempts | included runs |",
            "|---:|---:|",
        ]
    )
    for attempts, count in aggregate["parser_attempt_distribution"].items():
        lines.append(f"| {attempts} | {count} |")

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
            "## Claim Boundary",
            "",
            "- Artificial organization only.",
            "- Buyer-only LLM control only.",
            "- Requester, approver, accountant, and vendor are scripted or rule-based.",
            "- Game Master is deterministic and menu-aware.",
            "- Generated event labels are proposed and not human-reviewed coded evidence.",
            "- No human behavior claim.",
            "- No real-world organization claim.",
            "- No model comparison or general LLM behavior claim.",
            "- No statistical significance claim.",
            "",
            "## Limitations",
            "",
            "- EXP-0001 uses 5 runs per scenario as a preliminary baseline.",
            "- The result is bounded to `gpt-4.1-mini`, the frozen prompt, the frozen action menu, and the deterministic Game Master rules.",
            "- Counts are descriptive baseline accounting only and do not establish causal, statistical, compliance, legal, or real-world organizational conclusions.",
            "- Raw per-run outputs were generated under ignored `runs/` paths and are not committed in full.",
        ]
    )
    return "\n".join(lines) + "\n"


def record_to_dict(record: BaselineRunRecord) -> dict[str, Any]:
    return {
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
        "model_version": record.model_version,
    }


def exclusion_to_dict(exclusion: ExcludedRunRecord) -> dict[str, Any]:
    return {
        "scenario_id": exclusion.scenario_id,
        "index": exclusion.index,
        "run_id": exclusion.run_id,
        "exclusion_reason": exclusion.exclusion_reason,
        "stage": exclusion.stage,
        "detail": exclusion.detail,
    }


def classify_exception(exc: Exception) -> str:
    name = exc.__class__.__name__.lower()
    message = str(exc).lower()
    if "parse" in name or "parser" in message or "schema" in message or "json" in message:
        return "parser_failure"
    if "provider" in name or "api" in message or "openai" in message or "http" in message:
        return "provider_or_api_failure"
    return "generation_failure"


def failed_validation_markdown(pack_dir: Path, detail: str) -> str:
    return "\n".join(
        [
            "# Evidence Pack Validation Output",
            "",
            f"Evidence pack: `{pack_dir.as_posix()}`",
            "",
            "Result: FAIL",
            "",
            "## Failure",
            "",
            detail,
            "",
            "## Boundary",
            "",
            "This validation is mechanical. It does not support statistical claims or real-world behavior claims.",
            "",
        ]
    )


def compact_counts(counts: dict[str, int]) -> str:
    if not counts:
        return "none"
    return "; ".join(f"{key}:{value}" for key, value in sorted(counts.items()))


def compact_nested_counts(counts: dict[str, dict[str, int]]) -> str:
    if not counts:
        return "none"
    return "; ".join(
        f"{outer}->{','.join(f'{inner}:{value}' for inner, value in sorted(inner_counts.items()))}"
        for outer, inner_counts in sorted(counts.items())
    )


def format_inline_list(values: list[str]) -> str:
    if not values:
        return "`not returned`"
    return ", ".join(f"`{value}`" for value in values)


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
