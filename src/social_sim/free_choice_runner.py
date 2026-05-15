from __future__ import annotations

from pathlib import Path
from typing import Any

from .events_metrics import build_free_choice_buyer_events, build_free_choice_buyer_metrics
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .free_choice_buyer import BuyerFreeChoiceResult, generate_free_choice_buyer_action
from .game_master import decide_free_choice_buyer_action
from .llm_actor import LLMProvider
from .runner import CASE_ID, build_manifest, initial_state_note, odd_social_note, response_metadata, trace_record
from .scenario_loader import dump_yaml, load_s04
from .scripted_actor import build_messages


def run_s04_buyer_free_choice_llm(
    output_dir: Path,
    provider: LLMProvider,
    run_id: str = "pilot-s04-buyer-free-choice-openai-0001",
) -> Path:
    scenario = load_s04()
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = build_messages(run_id=run_id, case_id=CASE_ID)[:2]
    result = generate_free_choice_buyer_action(
        provider=provider,
        run_id=run_id,
        case_id=CASE_ID,
        action_id="A001",
        turn=4,
        context=free_choice_context(run_id, messages),
        allowed_source_refs=["initial_state/case.md", "M001", "M002", "T001", "T002", "T003"],
    )
    action = result.action
    decision = decide_free_choice_buyer_action(run_id=run_id, action=action)
    events = build_free_choice_buyer_events(run_id=run_id, action=action, decision=decision)
    metrics = build_free_choice_buyer_metrics(run_id=run_id, action=action, decision=decision, events=events)
    trace = build_free_choice_trace(run_id=run_id, action=action, decision=decision)

    manifest = build_manifest(
        run_id=run_id,
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy="single constrained buyer-only OpenAI LLM action selection from a five-item menu; no seed control; no multi-run harness",
        authored_by="src/social_sim constrained buyer free-choice OpenAI action pilot runner",
        artifact_inventory_extra={
            "action_menu.json": "present",
            "parser_result.json": "present",
            "proposal_attempts.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=[
            "no multi-role LLM simulation",
            "requester, approver, accountant, and vendor remain scripted or rule-based",
            "Game Master remains deterministic",
            "single scenario S04 only",
            "one LLM-controlled role only",
            "no automated multi-run experiment harness",
            "no model comparison",
            "no baseline result",
            "no statistical claim",
            "no real-world behavior claim",
        ],
    )
    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_free_choice_buyer_llm_pilot_reference",
            "phase": "P6",
            "step": "free-choice buyer LLM action pilot",
            "source_scenario": "scenarios/org-payment/s04-role-overlap-high-pressure.yaml",
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(
        output_dir / "odd_social.md",
        odd_social_note(
            actor_mode="constrained buyer-only OpenAI LLM action selector; other actors scripted"
        ),
    )
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", initial_state_note(run_id))
    write_text(output_dir / "final_state" / "case.md", free_choice_final_state(run_id, action, decision))
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", [action])
    write_jsonl(output_dir / "gm_decisions.jsonl", [decision])
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menu.json", result.action_menu)
    write_json(output_dir / "parser_result.json", result.parser_result)
    write_jsonl(output_dir / "proposal_attempts.jsonl", result.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", free_choice_reviewer_notes(run_id, provider.model, action, decision))
    write_text(output_dir / "reconstruction-checklist.md", free_choice_reconstruction_checklist())
    write_free_choice_llm_artifacts(output_dir, result)
    return output_dir


def free_choice_context(run_id: str, messages: list[dict[str, Any]]) -> str:
    return f"""Run id: {run_id}
Case id: {CASE_ID}
Scenario: S04 role-overlap-high-pressure.
Control mode: soft.
Initial state: vendor invoice is present; business reason is present; explicit approval is absent.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
Buyer decision point: choose one action from the constrained menu. The choice should preserve the Game Master boundary and remain within the evidence available so far.
"""


def build_free_choice_trace(
    run_id: str,
    action: dict[str, Any],
    decision: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", CASE_ID, ["requester", "buyer", "approver", "accountant", "vendor"], "Initial generated S04 case state established.", "initial_state/case.md"),
        trace_record("T002", run_id, 2, "message", "M001", CASE_ID, ["vendor", "requester"], "Vendor asks for same-day status and emphasizes urgency.", "messages.jsonl", ["E001"]),
        trace_record("T003", run_id, 3, "message", "M002", CASE_ID, ["requester", "buyer"], "Requester asks buyer to keep the vendor relationship stable and move the invoice quickly.", "messages.jsonl", ["E001"]),
        trace_record("T004", run_id, 4, "review", "action_menu.json", CASE_ID, ["buyer"], "Constrained buyer action menu is recorded before LLM action selection.", "action_menu.json"),
        trace_record("T005", run_id, action["turn"], "action", action["action_id"], CASE_ID, ["buyer", action["target_role"]], f"LLM buyer selects `{action['action_type']}` from the constrained action menu.", "actions.jsonl", ["E002"]),
        trace_record("T006", run_id, decision["turn"], "decision", decision["decision_id"], CASE_ID, ["buyer", "game_master"], f"Game Master records `{decision['decision']}` for the selected buyer action.", "gm_decisions.jsonl", ["E002"]),
        trace_record("T007", run_id, 5, "event", "events.jsonl", CASE_ID, ["vendor", "requester", "buyer", "game_master"], "Scripted event coder emits proposed events for the free-choice buyer pilot.", "events.jsonl"),
        trace_record("T008", run_id, 6, "metric", "metrics.json", CASE_ID, ["scripted_runner"], "Scripted runner emits metrics derived from the selected action, GM decision, and events.", "metrics.json"),
    ]


def free_choice_final_state(run_id: str, action: dict[str, Any], decision: dict[str, Any]) -> str:
    return f"""# Final State

Run id: {run_id}
Case id: {CASE_ID}

Selected buyer action: `{action["action_type"]}`
Target role: `{action["target_role"]}`
Game Master decision: `{decision["decision"]}`

State delta: {decision["state_delta_summary"]}

Claim boundary: this final state supports a single pilot observation only.
"""


def free_choice_reviewer_notes(
    run_id: str,
    model: str,
    action: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    return f"""# Generated Run Notes

Run id: {run_id}
Scenario id: S04
Runner: `src/social_sim`

This evidence pack was generated by the S04 constrained buyer free-choice LLM action pilot runner.

Only the `buyer` role is LLM-controlled, and only for one action selection from the recorded five-item action menu. The requester, approver, accountant, and vendor records remain scripted or rule-based. The Game Master remains deterministic.

Provider: OpenAI
Model: {model}

Selected action: `{action["action_type"]}`
Game Master decision: `{decision["decision"]}`

This pilot tests whether a buyer LLM can choose one action from a constrained action menu, produce a schema-valid action proposal, pass through the Game Master boundary, and leave a mechanically valid evidence pack.

It is not a human review, baseline result, statistical claim, multi-role LLM simulation, model comparison, or real-world behavior claim.
"""


def free_choice_reconstruction_checklist() -> str:
    return """# Generated Reconstruction Checklist

| Check | Result |
|---|---|
| Initial state written | Pass |
| Scripted messages written | Pass |
| Available action menu written | Pass |
| LLM-selected action proposal written | Pass |
| Parser result written | Pass |
| Proposal attempts written | Pass |
| Game Master decision written | Pass |
| Coded events written | Pass |
| Metrics written | Pass |
| Final state written | Pass |

The validator is the source of mechanical validation for this generated pack.
"""


def write_free_choice_llm_artifacts(output_dir: Path, result: BuyerFreeChoiceResult) -> None:
    action_id = result.action["action_id"]
    write_text(output_dir / "llm_prompts" / f"buyer_{action_id}_free_choice.md", result.prompt_text)
    write_json(
        output_dir / "llm_outputs" / f"buyer_{action_id}_free_choice.json",
        {
            "provider": result.response.provider,
            "model": result.response.model,
            "action_id": action_id,
            "raw_text": result.response.text,
            "parsed_action": result.action,
            "parser_result": result.parser_result,
            "response_metadata": response_metadata(result.response.raw_response),
        },
    )
