from __future__ import annotations

import json
import shutil
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from scripts.validate_evidence_pack import validate_pack

from .evidence_pack_writer import write_json, write_text
from .free_choice_buyer import ACTION_MENU_DOC
from .free_choice_runner import run_s04_buyer_free_choice_llm
from .llm_actor import LLMProvider


DEFAULT_REPEATED_BATCH_ID = "pilot-s04-buyer-free-choice-repeat-0001"
PROMPT_TEMPLATE_REF = "prompts/org-payment/buyer-free-choice-action-v0.1.md"


@dataclass(frozen=True)
class RepeatedRunRecord:
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
    validation_report: str


def run_s04_buyer_free_choice_batch(
    *,
    output_root: Path,
    curated_output: Path,
    provider: LLMProvider,
    count: int = 5,
    batch_id: str = DEFAULT_REPEATED_BATCH_ID,
) -> Path:
    if count < 1:
        raise ValueError("count must be at least 1")
    require_new_or_empty(output_root, "output_root")
    require_new_or_empty(curated_output, "curated_output")
    output_root.mkdir(parents=True, exist_ok=True)
    curated_output.mkdir(parents=True, exist_ok=True)

    records: list[RepeatedRunRecord] = []
    for index in range(1, count + 1):
        run_id = f"{batch_id}-run-{index:03d}"
        run_root = output_root / f"run-{index:03d}"
        pack_dir = run_root / "evidence-pack"
        run_s04_buyer_free_choice_llm(
            output_dir=pack_dir,
            provider=provider,
            run_id=run_id,
            batch_execution=True,
        )
        report = validate_pack(pack_dir)
        report_text = report.as_markdown()
        write_text(run_root / "validation-output.md", report_text)
        records.append(read_run_record(index=index, run_id=run_id, pack_dir=pack_dir, validation_report=report_text))

    representatives = copy_representative_packs(records=records, curated_output=curated_output)

    aggregate = build_aggregate(
        batch_id=batch_id,
        count=count,
        provider=provider,
        records=records,
        representatives=representatives,
    )
    write_json(curated_output / "aggregate.json", aggregate)
    write_text(curated_output / "summary.md", render_summary(aggregate))
    return curated_output


def require_new_or_empty(path: Path, label: str) -> None:
    if path.exists() and any(path.iterdir()):
        raise ValueError(f"{label} must be new or empty: {path}")


def read_run_record(index: int, run_id: str, pack_dir: Path, validation_report: str) -> RepeatedRunRecord:
    parser_result = load_json(pack_dir / "parser_result.json")
    attempts = load_jsonl(pack_dir / "proposal_attempts.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    rejected_attempt_count = sum(1 for attempt in attempts if attempt.get("status") != "accepted_by_parser")
    return RepeatedRunRecord(
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
        validation_report=validation_report,
    )


def copy_representative_packs(
    *,
    records: list[RepeatedRunRecord],
    curated_output: Path,
) -> list[dict[str, str]]:
    selected: dict[str, RepeatedRunRecord] = {}
    for record in records:
        selected.setdefault(record.selected_action_type, record)

    representatives: list[dict[str, str]] = []
    for action_type, record in sorted(selected.items()):
        directory_name = f"{action_type}-run-{record.index:03d}"
        pack_path = Path("representative-evidence-packs") / directory_name
        validation_path = Path("representative-validation-outputs") / f"{directory_name}.md"
        shutil.copytree(record.pack_dir, curated_output / pack_path)
        validation_report = validate_pack(curated_output / pack_path).as_markdown()
        write_text(curated_output / validation_path, validation_report)
        representatives.append(
            {
                "selected_action_type": action_type,
                "run_id": record.run_id,
                "evidence_pack": pack_path.as_posix(),
                "validation_output": validation_path.as_posix(),
            }
        )
    return representatives


def build_aggregate(
    batch_id: str,
    count: int,
    provider: LLMProvider,
    records: list[RepeatedRunRecord],
    representatives: list[dict[str, str]],
) -> dict[str, Any]:
    selected_counts = Counter(record.selected_action_type for record in records)
    gm_decisions: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        gm_decisions[record.selected_action_type][record.gm_decision] += 1

    return {
        "batch_id": batch_id,
        "provider": provider.provider,
        "model": provider.model,
        "scenario_id": "S04",
        "actor_setup": "buyer_only_llm",
        "other_roles": "scripted_or_rule_based",
        "game_master": "deterministic_menu_aware_rules",
        "action_menu_id": ACTION_MENU_DOC["menu_id"],
        "prompt_template_ref": PROMPT_TEMPLATE_REF,
        "run_count": count,
        "claim_boundary": "pilot_observation_only",
        "selected_action_type_counts": dict(sorted(selected_counts.items())),
        "parser_summary": {
            "runs_with_parser_acceptance": sum(1 for record in records if record.parser_status == "accepted"),
            "total_attempts": sum(record.attempt_count for record in records),
            "total_rejected_or_invalid_attempts": sum(record.rejected_attempt_count for record in records),
            "runs_with_retries": sum(1 for record in records if record.attempt_count > 1),
        },
        "gm_decisions_by_selected_action": {
            action_type: dict(sorted(counter.items())) for action_type, counter in sorted(gm_decisions.items())
        },
        "representative_evidence_packs_by_selected_action": representatives,
        "runs": [
            {
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


def render_summary(aggregate: dict[str, Any]) -> str:
    lines = [
        "# S04 Buyer Free-Choice Repeated Pilot Summary",
        "",
        f"Batch id: `{aggregate['batch_id']}`",
        f"Provider: `{aggregate['provider']}`",
        f"Model: `{aggregate['model']}`",
        "Scenario id: `S04`",
        f"Actor setup: `{aggregate['actor_setup']}`",
        f"Other roles: `{aggregate['other_roles']}`",
        f"Game Master: `{aggregate['game_master']}`",
        f"Action menu id: `{aggregate['action_menu_id']}`",
        f"Prompt template: [{aggregate['prompt_template_ref']}](../../../{aggregate['prompt_template_ref']})",
        f"Run count: {aggregate['run_count']}",
        "Claim boundary: pilot observation only",
        "",
        "Across this small repeated S04 buyer free-choice pilot set, the buyer selected the following actions under fixed artificial conditions.",
        "",
        "This summary does not claim that buyers generally behave this way, that humans would choose these actions, that S04 proves approval safety or failure rates, or that this is a statistically meaningful behavioral distribution.",
        "",
        "## Selected Action Counts",
        "",
        "| action_type | count |",
        "|---|---:|",
    ]
    for action_type, count in aggregate["selected_action_type_counts"].items():
        lines.append(f"| `{action_type}` | {count} |")

    parser = aggregate["parser_summary"]
    lines.extend(
        [
            "",
            "## Parser Summary",
            "",
            f"- Runs with parser acceptance: {parser['runs_with_parser_acceptance']}",
            f"- Total attempts: {parser['total_attempts']}",
            f"- Total rejected or invalid attempts: {parser['total_rejected_or_invalid_attempts']}",
            f"- Runs with retries: {parser['runs_with_retries']}",
            "",
            "## Game Master Decisions By Selected Action",
            "",
            "| selected action_type | GM decision | count |",
            "|---|---|---:|",
        ]
    )
    for action_type, decisions in aggregate["gm_decisions_by_selected_action"].items():
        for decision, count in decisions.items():
            lines.append(f"| `{action_type}` | `{decision}` | {count} |")

    lines.extend(
        [
            "",
            "## Run Summary",
            "",
            "| run_id | selected action_type | parser attempts | rejected attempts | GM decision | validation |",
            "|---|---|---:|---:|---|---|",
        ]
    )
    for record in aggregate["runs"]:
        lines.append(
            "| "
            f"`{record['run_id']}` | "
            f"`{record['selected_action_type']}` | "
            f"{record['attempt_count']} | "
            f"{record['rejected_attempt_count']} | "
            f"`{record['gm_decision']}` | "
            f"{record['validation_status']} |"
        )

    lines.extend(
        [
            "",
            "## Representative Evidence",
            "",
            "| selected action_type | run_id | evidence pack | validation output |",
            "|---|---|---|---|",
        ]
    )
    for representative in aggregate["representative_evidence_packs_by_selected_action"]:
        lines.append(
            "| "
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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
