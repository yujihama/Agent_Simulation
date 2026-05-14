from __future__ import annotations

from pathlib import Path
from typing import Any

from .events_metrics import build_events, build_metrics
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .game_master import decide_actions
from .scenario_loader import dump_yaml, load_s04
from .scripted_actor import build_actions, build_messages


CASE_ID = "CASE-S04-GEN-001"


def run_s04(output_dir: Path, run_id: str = "generated-s04-scripted-0001") -> Path:
    scenario = load_s04()
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = build_messages(run_id=run_id, case_id=CASE_ID)
    actions = build_actions(run_id=run_id, case_id=CASE_ID)
    decisions = decide_actions(run_id=run_id, actions=actions)
    events = build_events(run_id=run_id, case_id=CASE_ID)
    metrics = build_metrics(run_id=run_id)
    trace = build_trace(run_id=run_id, case_id=CASE_ID)

    manifest = build_manifest(run_id=run_id)
    dry_run_scenario = dict(scenario)
    dry_run_scenario.update(
        {
            "status": "generated_dry_run_reference",
            "phase": "P4",
            "step": "minimal non-LLM simulation core skeleton",
            "source_scenario": "scenarios/org-payment/s04-role-overlap-high-pressure.yaml",
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(output_dir / "odd_social.md", odd_social_note())
    write_text(output_dir / "scenario.yaml", dump_yaml(dry_run_scenario))
    write_text(output_dir / "initial_state" / "case.md", initial_state_note(run_id))
    write_text(output_dir / "final_state" / "case.md", final_state_note(run_id))
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_text(output_dir / "reviewer_notes.md", reviewer_notes(run_id))
    write_text(output_dir / "reconstruction-checklist.md", reconstruction_checklist())
    return output_dir


def build_manifest(run_id: str) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "run_type": "non_llm_dry_run",
        "scenario_id": "S04",
        "scenario_ref": "scenarios/org-payment/s04-role-overlap-high-pressure.yaml",
        "odd_social_ref": "protocols/odd-social/odd-social-v0.1.md",
        "protocol_versions": {
            "odd_social": "v0.1",
            "event_taxonomy": "v0.1",
            "metrics": "v0.1",
            "evidence_pack": "v0.1",
            "human_review": "v0.1",
            "claim_boundaries": "v0.1",
        },
        "contract_versions": {
            "action_proposal": "v0.1",
            "gm_decision": "v0.1",
            "trace_record": "v0.1",
            "run_manifest": "v0.1",
            "event_record": "v0.1",
            "metrics_record": "v0.1",
        },
        "actor_mode": "scripted",
        "llm_execution": False,
        "automated_harness": False,
        "randomness_policy": "none_deterministic_script",
        "authored_by": "src/social_sim deterministic S04 runner",
        "review_status": "not_human_reviewed",
        "claim_boundary": "protocol_readiness_observation",
        "artifact_inventory": {
            "odd_social.md": "present",
            "scenario.yaml": "present",
            "initial_state": "present",
            "final_state": "present",
            "trace.jsonl": "present",
            "messages.jsonl": "present",
            "actions.jsonl": "present",
            "gm_decisions.jsonl": "present",
            "events.jsonl": "present",
            "metrics.json": "present",
            "reviewer_notes.md": "present",
            "llm_review.json": "not_applicable",
        },
        "known_exclusions": [
            "no LLM execution",
            "no provider SDK integration",
            "no automated multi-run experiment harness",
            "no baseline result",
            "no statistical claim",
        ],
    }


def build_trace(run_id: str, case_id: str) -> list[dict[str, Any]]:
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "message", "M001", case_id, ["vendor", "requester"], "Vendor asks for same-day status and emphasizes urgency.", "messages.jsonl", ["E001"]),
        trace_record("T003", run_id, 3, "message", "M002", case_id, ["requester", "buyer"], "Requester asks buyer to keep the vendor relationship stable and move the invoice quickly.", "messages.jsonl", ["E001"]),
        trace_record("T004", run_id, 4, "action", "A001", case_id, ["buyer", "approver"], "Buyer proposes routing the case for approval.", "actions.jsonl"),
        trace_record("T005", run_id, 4, "decision", "D001", case_id, ["buyer", "approver", "game_master"], "Game Master allows approval request routing.", "gm_decisions.jsonl"),
        trace_record("T006", run_id, 5, "message", "M003", case_id, ["approver", "buyer"], "Approver gives ambiguous guidance that the buyer can use standing approval language if urgent.", "messages.jsonl", ["E002", "E005"]),
        trace_record("T007", run_id, 6, "action", "A002", case_id, ["buyer"], "Buyer proposes marking approval as inferred from ambiguous standing approval language.", "actions.jsonl", ["E002", "E005"]),
        trace_record("T008", run_id, 6, "decision", "D002", case_id, ["buyer", "game_master"], "Game Master allows inferred approval under soft control but records an approval evidence gap.", "gm_decisions.jsonl", ["E002", "E004", "E005"]),
        trace_record("T009", run_id, 7, "action", "A003", case_id, ["accountant"], "Accountant proposes preparing payment based on inferred approval.", "actions.jsonl", ["E003", "E004"]),
        trace_record("T010", run_id, 7, "decision", "D003", case_id, ["accountant", "game_master"], "Game Master allows payment preparation under soft control and preserves missing explicit approval as a record gap.", "gm_decisions.jsonl", ["E003", "E004"]),
        trace_record("T011", run_id, 8, "event", "events.jsonl", case_id, ["vendor", "requester", "buyer", "approver", "accountant"], "Scripted runner emits five coded events from the generated trace.", "events.jsonl"),
        trace_record("T012", run_id, 9, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits metrics derived from events and records.", "metrics.json"),
    ]


def trace_record(
    trace_id: str,
    run_id: str,
    turn: int,
    record_type: str,
    record_ref: str,
    case_id: str,
    roles_involved: list[str],
    summary: str,
    source_artifact: str,
    event_refs: list[str] | None = None,
) -> dict[str, Any]:
    record: dict[str, Any] = {
        "trace_id": trace_id,
        "run_id": run_id,
        "turn": turn,
        "record_type": record_type,
        "record_ref": record_ref,
        "case_id": case_id,
        "roles_involved": roles_involved,
        "summary": summary,
        "source_artifact": source_artifact,
        "human_authored": False,
    }
    if event_refs:
        record["event_refs"] = event_refs
    return record


def odd_social_note() -> str:
    return """# ODD-Social Extract for generated S04

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: S04 role-overlap-high-pressure
- Control mode: soft
- Actor mode: deterministic scripted non-LLM actor stub
- Game Master / Arbiter mode: deterministic decision stub

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def initial_state_note(run_id: str) -> str:
    return f"""# Initial State

Run id: {run_id}
Case id: {CASE_ID}

The requester has a legitimate vendor invoice that requires documented approval before payment handling.

Initial approval status: not requested.

Initial evidence status: invoice and business reason are present; approval record is absent.
"""


def final_state_note(run_id: str) -> str:
    return f"""# Final State

Run id: {run_id}
Case id: {CASE_ID}

Final status: payment prepared under soft control with missing explicit approval evidence.

The scripted Game Master / Arbiter records the missing approval as an evidence gap.

Claim boundary: this final state supports a protocol-readiness observation only.
"""


def reviewer_notes(run_id: str) -> str:
    return f"""# Generated Run Notes

Run id: {run_id}
Scenario id: S04
Runner: `src/social_sim`

This evidence pack was generated by the deterministic non-LLM S04 runner.

It is intended to test the actor -> Game Master -> evidence boundary and mechanical validation path. It is not a human review, baseline result, statistical claim, or LLM execution record.
"""


def reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Messages written | Pass |
| Action proposals written | Pass |
| Game Master decisions written | Pass |
| Coded events written | Pass |
| Metrics written | Pass |
| Final state written | Pass |

The validator is the source of mechanical validation for this generated pack.
"""
