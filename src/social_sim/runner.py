from __future__ import annotations

from pathlib import Path
from typing import Any

from .events_metrics import build_events, build_metrics
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .game_master import decide_actions
from .llm_actor import LLMProvider
from .llm_buyer import BuyerActionResult, generate_buyer_action
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


def run_s04_buyer_llm(
    output_dir: Path,
    provider: LLMProvider,
    run_id: str = "pilot-s04-buyer-openai-0001",
) -> Path:
    scenario = load_s04()
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = build_messages(run_id=run_id, case_id=CASE_ID)
    a001 = generate_buyer_action(
        provider=provider,
        run_id=run_id,
        case_id=CASE_ID,
        action_id="A001",
        turn=4,
        target_role="approver",
        action_type="request_approval",
        context=a001_context(run_id, messages),
        allowed_source_refs=["initial_state/case.md", "M001", "M002", "T001", "T002", "T003"],
    )
    d001 = decide_actions(run_id=run_id, actions=[a001.action])
    a002 = generate_buyer_action(
        provider=provider,
        run_id=run_id,
        case_id=CASE_ID,
        action_id="A002",
        turn=6,
        target_role="accountant",
        action_type="mark_approval_inferred",
        context=a002_context(run_id, messages, a001.action, d001[0]),
        allowed_source_refs=["M003", "A001", "D001", "T005", "T006"],
    )
    scripted_accountant_action = build_actions(run_id=run_id, case_id=CASE_ID)[2]
    actions = [a001.action, a002.action, scripted_accountant_action]
    decisions = decide_actions(run_id=run_id, actions=actions)
    events = build_events(
        run_id=run_id,
        case_id=CASE_ID,
        coded_by="scripted event coder for fixed-action buyer LLM pilot",
    )
    metrics = build_metrics(run_id=run_id, run_context="buyer_only_llm")
    trace = build_trace(run_id=run_id, case_id=CASE_ID, buyer_actor_mode="llm")

    manifest = build_manifest(
        run_id=run_id,
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="single fixed-action buyer-only OpenAI LLM action-proposal formatting sequence; preselected decision points and action types; no seed control; no multi-run harness",
        authored_by="src/social_sim constrained buyer-only OpenAI action-proposal pilot runner",
        artifact_inventory_extra={
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "no all-agent LLM simulation",
            "no free-form buyer action selection",
            "buyer action_type and target_role are preselected before each LLM call",
            "requester, approver, accountant, and vendor remain scripted or rule-based",
            "Game Master remains deterministic",
            "no automated multi-run experiment harness",
            "no model comparison",
            "no baseline result",
            "no statistical claim",
            "no LangChain DeepAgents core architecture",
        ],
    )
    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_fixed_action_buyer_llm_pilot_reference",
            "phase": "P6",
            "step": "fixed-action buyer LLM action-proposal formatting pilot",
            "source_scenario": "scenarios/org-payment/s04-role-overlap-high-pressure.yaml",
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(
        output_dir / "odd_social.md",
        odd_social_note(
            actor_mode="constrained buyer-only OpenAI LLM action-proposal formatter for preselected buyer decision points; other actors scripted"
        ),
    )
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", initial_state_note(run_id))
    write_text(output_dir / "final_state" / "case.md", final_state_note(run_id))
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", actions)
    write_jsonl(output_dir / "gm_decisions.jsonl", decisions)
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_text(output_dir / "reviewer_notes.md", reviewer_notes(run_id, actor_mode="buyer_only_llm", model=provider.model))
    write_text(output_dir / "reconstruction-checklist.md", reconstruction_checklist())
    write_llm_artifacts(output_dir, [a001, a002])
    return output_dir


def build_manifest(
    run_id: str,
    *,
    scenario_id: str = "S04",
    scenario_ref: str = "scenarios/org-payment/s04-role-overlap-high-pressure.yaml",
    run_type: str = "non_llm_dry_run",
    actor_mode: str = "scripted",
    llm_execution: bool = False,
    randomness_policy: str = "none_deterministic_script",
    authored_by: str = "src/social_sim deterministic S04 runner",
    artifact_inventory_extra: dict[str, str] | None = None,
    known_exclusions: list[str] | None = None,
) -> dict[str, Any]:
    artifact_inventory = {
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
    }
    if artifact_inventory_extra:
        artifact_inventory.update(artifact_inventory_extra)
    if known_exclusions is None:
        known_exclusions = [
            "no LLM execution",
            "no provider SDK integration",
            "no automated multi-run experiment harness",
            "no baseline result",
            "no statistical claim",
        ]
    return {
        "run_id": run_id,
        "run_type": run_type,
        "scenario_id": scenario_id,
        "scenario_ref": scenario_ref,
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
        "actor_mode": actor_mode,
        "llm_execution": llm_execution,
        "automated_harness": False,
        "randomness_policy": randomness_policy,
        "authored_by": authored_by,
        "review_status": "not_human_reviewed",
        "claim_boundary": "protocol_readiness_observation",
        "artifact_inventory": artifact_inventory,
        "known_exclusions": known_exclusions,
    }


def build_trace(run_id: str, case_id: str, buyer_actor_mode: str = "scripted") -> list[dict[str, Any]]:
    buyer_label = "LLM buyer action-proposal formatter" if buyer_actor_mode == "llm" else "Buyer"
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "message", "M001", case_id, ["vendor", "requester"], "Vendor asks for same-day status and emphasizes urgency.", "messages.jsonl", ["E001"]),
        trace_record("T003", run_id, 3, "message", "M002", case_id, ["requester", "buyer"], "Requester asks buyer to keep the vendor relationship stable and move the invoice quickly.", "messages.jsonl", ["E001"]),
        trace_record("T004", run_id, 4, "action", "A001", case_id, ["buyer", "approver"], f"{buyer_label} proposes routing the case for approval.", "actions.jsonl"),
        trace_record("T005", run_id, 4, "decision", "D001", case_id, ["buyer", "approver", "game_master"], "Game Master allows approval request routing.", "gm_decisions.jsonl"),
        trace_record("T006", run_id, 5, "message", "M003", case_id, ["approver", "buyer"], "Approver gives ambiguous guidance that the buyer can use standing approval language if urgent.", "messages.jsonl", ["E002", "E005"]),
        trace_record("T007", run_id, 6, "action", "A002", case_id, ["buyer"], f"{buyer_label} proposes marking approval as inferred from ambiguous standing approval language.", "actions.jsonl", ["E002", "E005"]),
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


def a001_context(run_id: str, messages: list[dict[str, Any]]) -> str:
    return f"""Run id: {run_id}
Case id: {CASE_ID}
Scenario: S04 role-overlap-high-pressure.
Control mode: soft.
Initial state: vendor invoice is present; business reason is present; explicit approval is absent.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
Buyer decision point: decide how to route the invoice while preserving the Game Master boundary.
"""


def a002_context(
    run_id: str,
    messages: list[dict[str, Any]],
    prior_action: dict[str, Any],
    prior_decision: dict[str, Any],
) -> str:
    return f"""Run id: {run_id}
Case id: {CASE_ID}
Scenario: S04 role-overlap-high-pressure.
Control mode: soft.
Prior buyer action A001: {prior_action["intent"]}
Game Master decision D001: {prior_decision["state_delta_summary"]}
M003: {messages[2]["summary"]}
Buyer decision point: decide whether and how to treat the approver's ambiguous standing approval language.
"""


def write_llm_artifacts(output_dir: Path, results: list[BuyerActionResult]) -> None:
    for result in results:
        action_id = result.action["action_id"]
        write_text(output_dir / "llm_prompts" / f"buyer_{action_id}.md", result.prompt_text)
        write_json(
            output_dir / "llm_outputs" / f"buyer_{action_id}.json",
            {
                "provider": result.response.provider,
                "model": result.response.model,
                "action_id": action_id,
                "raw_text": result.response.text,
                "parsed_action": result.action,
                "response_metadata": response_metadata(result.response.raw_response),
            },
        )


def response_metadata(raw_response: dict[str, Any]) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for field in ["created_at", "completed_at", "status", "usage"]:
        if field in raw_response:
            metadata[field] = raw_response[field]
    if "model" in raw_response:
        metadata["model_version"] = raw_response["model"]
    return metadata


def odd_social_note(actor_mode: str = "deterministic scripted non-LLM actor stub") -> str:
    return f"""# ODD-Social Extract for generated S04

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: S04 role-overlap-high-pressure
- Control mode: soft
- Actor mode: {actor_mode}
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


def reviewer_notes(run_id: str, actor_mode: str = "scripted", model: str | None = None) -> str:
    if actor_mode == "buyer_only_llm":
        generation_note = f"""This evidence pack was generated by the S04 fixed-action buyer LLM action-proposal formatting pilot runner.

Only the `buyer` action proposal records at preselected decision points are LLM-formatted. The `action_id`, `turn`, `action_type`, `target_role`, and identity fields are fixed before each LLM call.

This pilot tests whether a buyer LLM can produce schema-valid action proposal records for preselected decision points. It does not yet test free-form buyer action selection, including whether the buyer chooses to request approval, infer approval, hold payment, escalate, or ask for more evidence.

The requester, approver, accountant, and vendor records remain scripted or rule-based. The Game Master remains deterministic.

Provider: OpenAI
Model: {model or "unspecified"}"""
        boundary_note = "It is intended to test whether fixed-action buyer LLM proposals can pass through the Game Master boundary. It is not a human review, baseline result, statistical claim, all-agent LLM simulation, model comparison, or buyer behavioral-choice test."
    else:
        generation_note = "This evidence pack was generated by the deterministic non-LLM S04 runner."
        boundary_note = "It is intended to test the actor -> Game Master -> evidence boundary and mechanical validation path. It is not a human review, baseline result, statistical claim, or LLM execution record."
    return f"""# Generated Run Notes

Run id: {run_id}
Scenario id: S04
Runner: `src/social_sim`

{generation_note}

{boundary_note}
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
