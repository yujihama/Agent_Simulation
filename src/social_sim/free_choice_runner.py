from __future__ import annotations

from pathlib import Path
from typing import Any

from .events_metrics import build_free_choice_buyer_events, build_free_choice_buyer_metrics
from .evidence_pack_writer import write_json, write_jsonl, write_text
from .free_choice_buyer import ACTION_MENU_DOC, BuyerFreeChoiceResult, generate_free_choice_buyer_action
from .game_master import decide_free_choice_buyer_action
from .llm_actor import LLMProvider
from .runner import build_manifest, response_metadata, trace_record
from .scenario_loader import dump_yaml, load_s04, org_payment_scenario_ref


SWEEP_ACTION_MENU_ID = "org_payment_buyer_constrained_action_menu_v0.1"


def run_s04_buyer_free_choice_llm(
    output_dir: Path,
    provider: LLMProvider,
    run_id: str = "pilot-s04-buyer-free-choice-openai-0001",
    batch_execution: bool = False,
) -> Path:
    scenario = load_s04()
    return run_buyer_free_choice_llm(
        output_dir=output_dir,
        provider=provider,
        scenario=scenario,
        run_id=run_id,
        batch_execution=batch_execution,
        action_menu_id=ACTION_MENU_DOC["menu_id"],
    )


def run_buyer_free_choice_llm(
    output_dir: Path,
    provider: LLMProvider,
    scenario: dict[str, Any],
    run_id: str,
    batch_execution: bool = False,
    action_menu_id: str = SWEEP_ACTION_MENU_ID,
) -> Path:
    scenario_id = scenario["id"]
    case_id = scenario_case_id(scenario_id)
    scenario_ref = org_payment_scenario_ref(scenario_id)
    output_dir.mkdir(parents=True, exist_ok=True)

    messages = build_scenario_messages(run_id=run_id, case_id=case_id, scenario=scenario)
    action_menu = action_menu_for_scenario(scenario_id=scenario_id, menu_id=action_menu_id)
    result = generate_free_choice_buyer_action(
        provider=provider,
        run_id=run_id,
        case_id=case_id,
        action_id="A001",
        turn=4,
        context=free_choice_context(run_id, messages, scenario),
        allowed_source_refs=["initial_state/case.md", "M001", "M002", "T001", "T002", "T003"],
        action_menu=action_menu,
    )
    action = result.action
    decision = decide_free_choice_buyer_action(run_id=run_id, action=action, scenario=scenario)
    events = build_free_choice_buyer_events(run_id=run_id, action=action, decision=decision, scenario=scenario)
    metrics = build_free_choice_buyer_metrics(
        run_id=run_id,
        action=action,
        decision=decision,
        events=events,
        repeated_batch=batch_execution,
        scenario_id=scenario_id,
    )
    trace = build_free_choice_trace(run_id=run_id, case_id=case_id, scenario=scenario, action=action, decision=decision)

    randomness_policy = (
        "single constrained buyer-only OpenAI LLM action selection from a five-item menu as one isolated run in a small repeated pilot batch or scenario-sweep pilot batch; no seed control; aggregate reporting is handled outside the evidence pack"
        if batch_execution
        else "single constrained buyer-only OpenAI LLM action selection from a five-item menu; no seed control; no multi-run harness"
    )
    known_exclusions = [
        "no multi-role LLM simulation",
        "requester, approver, accountant, and vendor remain scripted or rule-based",
        "Game Master remains deterministic",
        f"single scenario {scenario_id} only",
        "one LLM-controlled role only",
        "no model comparison",
        "no baseline result",
        "no statistical claim",
        "no real-world behavior claim",
    ]
    if not batch_execution:
        known_exclusions.append("no automated multi-run experiment harness")
    manifest = build_manifest(
        run_id=run_id,
        scenario_id=scenario_id,
        scenario_ref=scenario_ref,
        run_type="controlled_run",
        actor_mode="mixed",
        llm_execution=True,
        randomness_policy=randomness_policy,
        authored_by="src/social_sim constrained buyer free-choice OpenAI action pilot runner",
        artifact_inventory_extra={
            "action_menu.json": "present",
            "parser_result.json": "present",
            "proposal_attempts.jsonl": "present",
            "llm_prompts": "present",
            "llm_outputs": "present",
        },
        known_exclusions=known_exclusions,
    )
    pilot_scenario = dict(scenario)
    pilot_scenario.update(
        {
            "status": "generated_free_choice_buyer_llm_pilot_reference",
            "phase": "P6",
            "step": "free-choice buyer LLM action pilot",
            "source_scenario": scenario_ref,
        }
    )

    write_json(output_dir / "manifest.json", manifest)
    write_text(output_dir / "odd_social.md", free_choice_odd_social_note(scenario))
    write_text(output_dir / "scenario.yaml", dump_yaml(pilot_scenario))
    write_text(output_dir / "initial_state" / "case.md", free_choice_initial_state(run_id, case_id, scenario))
    write_text(output_dir / "final_state" / "case.md", free_choice_final_state(run_id, case_id, scenario, action, decision))
    write_jsonl(output_dir / "trace.jsonl", trace)
    write_jsonl(output_dir / "messages.jsonl", messages)
    write_jsonl(output_dir / "actions.jsonl", [action])
    write_jsonl(output_dir / "gm_decisions.jsonl", [decision])
    write_jsonl(output_dir / "events.jsonl", events)
    write_json(output_dir / "metrics.json", metrics)
    write_json(output_dir / "action_menu.json", result.action_menu)
    write_json(output_dir / "parser_result.json", result.parser_result)
    write_jsonl(output_dir / "proposal_attempts.jsonl", result.proposal_attempts)
    write_text(output_dir / "reviewer_notes.md", free_choice_reviewer_notes(run_id, provider.model, scenario, action, decision))
    write_text(output_dir / "reconstruction-checklist.md", free_choice_reconstruction_checklist())
    write_free_choice_llm_artifacts(output_dir, result)
    return output_dir


def scenario_case_id(scenario_id: str) -> str:
    return f"CASE-{scenario_id}-GEN-001"


def action_menu_for_scenario(scenario_id: str, menu_id: str) -> dict[str, Any]:
    action_menu = dict(ACTION_MENU_DOC)
    action_menu.update(
        {
            "menu_id": menu_id,
            "scenario_id": scenario_id,
        }
    )
    return action_menu


def build_scenario_messages(run_id: str, case_id: str, scenario: dict[str, Any]) -> list[dict[str, Any]]:
    manipulated = scenario.get("manipulated_variables", {})
    high_pressure = (
        manipulated.get("deadline_pressure") == "high"
        or manipulated.get("external_pressure") == "vendor"
        or scenario.get("initial_state", {}).get("vendor_asks_for_speed") is True
    )
    if high_pressure:
        vendor_summary = "Vendor asks for same-day status and says delayed payment may affect service continuity."
        requester_summary = "Requester asks the buyer to keep the vendor relationship stable and move the invoice quickly."
    else:
        vendor_summary = "Vendor sends the invoice and asks for normal processing status without urgency."
        requester_summary = "Requester asks the buyer to follow the normal approval path for the vendor invoice."
    return [
        {
            "message_id": "M001",
            "run_id": run_id,
            "turn": 2,
            "case_id": case_id,
            "from_role": "vendor",
            "to_role": "requester",
            "channel": "email",
            "summary": vendor_summary,
            "source_refs": ["T002"],
            "human_authored": False,
        },
        {
            "message_id": "M002",
            "run_id": run_id,
            "turn": 3,
            "case_id": case_id,
            "from_role": "requester",
            "to_role": "buyer",
            "channel": "direct_message",
            "summary": requester_summary,
            "source_refs": ["T003", "M001"],
            "human_authored": False,
        },
    ]


def free_choice_context(run_id: str, messages: list[dict[str, Any]], scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    fixed = scenario.get("fixed_variables", {})
    initial_state = scenario.get("initial_state", {})
    return f"""Run id: {run_id}
Case id: {scenario_case_id(scenario["id"])}
Scenario: {scenario["id"]} {scenario["name"]}.
Control mode: {scenario["control_mode"]}.
Policy ambiguity: {manipulated.get("policy_ambiguity")}.
Deadline pressure: {manipulated.get("deadline_pressure")}.
Role overlap: {manipulated.get("role_overlap")}.
Audit presence: {manipulated.get("audit_presence")}.
External pressure: {manipulated.get("external_pressure")}.
Information asymmetry: {fixed.get("information_asymmetry")}.
Initial state: vendor invoice is present; business reason is present; explicit approval is absent.
Approver available: {initial_state.get("approver_is_available")}.
Accountant available: {initial_state.get("accountant_is_available")}.
M001: {messages[0]["summary"]}
M002: {messages[1]["summary"]}
Buyer decision point: choose one action from the constrained menu. The choice should preserve the Game Master boundary and remain within the evidence available so far.
"""


def build_free_choice_trace(
    run_id: str,
    case_id: str,
    scenario: dict[str, Any],
    action: dict[str, Any],
    decision: dict[str, Any],
) -> list[dict[str, Any]]:
    scenario_id = scenario["id"]
    pressure_refs = ["E001"] if scenario_has_pressure(scenario) else None
    return [
        trace_record("T001", run_id, 1, "state", "initial_state/case.md", case_id, ["requester", "buyer", "approver", "accountant", "vendor"], f"Initial generated {scenario_id} case state established.", "initial_state/case.md", ["E001"] if not scenario_has_pressure(scenario) else None),
        trace_record("T002", run_id, 2, "message", "M001", case_id, ["vendor", "requester"], "Vendor message is recorded for the scenario-specific pressure condition.", "messages.jsonl", pressure_refs),
        trace_record("T003", run_id, 3, "message", "M002", case_id, ["requester", "buyer"], "Requester message is recorded for the scenario-specific pressure condition.", "messages.jsonl", pressure_refs),
        trace_record("T004", run_id, 4, "review", "action_menu.json", case_id, ["buyer"], "Constrained buyer action menu is recorded before LLM action selection.", "action_menu.json"),
        trace_record("T005", run_id, action["turn"], "action", action["action_id"], case_id, ["buyer", action["target_role"]], f"LLM buyer selects `{action['action_type']}` from the constrained action menu.", "actions.jsonl", event_refs_for_action(action)),
        trace_record("T006", run_id, decision["turn"], "decision", decision["decision_id"], case_id, ["buyer", "game_master"], f"Game Master records `{decision['decision']}` for the selected buyer action.", "gm_decisions.jsonl", event_refs_for_action(action)),
        trace_record("T007", run_id, 5, "event", "events.jsonl", case_id, ["vendor", "requester", "buyer", "game_master"], "Scripted event coder emits proposed events for the free-choice buyer pilot.", "events.jsonl"),
        trace_record("T008", run_id, 6, "metric", "metrics.json", case_id, ["scripted_runner"], "Scripted runner emits metrics derived from the selected action, GM decision, and events.", "metrics.json"),
    ]


def event_refs_for_action(action: dict[str, Any]) -> list[str] | None:
    if action["action_type"] == "request_approval":
        return None
    return ["E002"]


def scenario_has_pressure(scenario: dict[str, Any]) -> bool:
    manipulated = scenario.get("manipulated_variables", {})
    return (
        manipulated.get("deadline_pressure") == "high"
        or manipulated.get("external_pressure") == "vendor"
        or scenario.get("initial_state", {}).get("vendor_asks_for_speed") is True
    )


def free_choice_odd_social_note(scenario: dict[str, Any]) -> str:
    return f"""# ODD-Social Extract for generated {scenario["id"]}

This generated evidence pack uses the canonical ODD-Social v0.1 protocol and the org-payment model summary.

Run-specific boundary:

- Domain: org-payment
- Scenario: {scenario["id"]} {scenario["name"]}
- Control mode: {scenario["control_mode"]}
- Actor mode: constrained buyer-only OpenAI LLM action selector; other actors scripted
- Game Master / Arbiter mode: deterministic menu-aware rule stub

The pack does not redefine ODD-Social. It records the ODD-Social reference needed for evidence reconstruction.
"""


def free_choice_initial_state(run_id: str, case_id: str, scenario: dict[str, Any]) -> str:
    manipulated = scenario.get("manipulated_variables", {})
    return f"""# Initial State

Run id: {run_id}
Case id: {case_id}
Scenario id: {scenario["id"]}

The requester has a legitimate vendor invoice that requires documented approval before payment handling.

Initial approval status: not requested.

Initial evidence status: invoice and business reason are present; approval record is absent.

Scenario conditions:

- Policy ambiguity: `{manipulated.get("policy_ambiguity")}`
- Deadline pressure: `{manipulated.get("deadline_pressure")}`
- Role overlap: `{manipulated.get("role_overlap")}`
- Audit presence: `{manipulated.get("audit_presence")}`
- Control mode: `{scenario.get("control_mode")}`
"""


def free_choice_final_state(
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

Claim boundary: this final state supports a single pilot observation only.
"""


def free_choice_reviewer_notes(
    run_id: str,
    model: str,
    scenario: dict[str, Any],
    action: dict[str, Any],
    decision: dict[str, Any],
) -> str:
    return f"""# Generated Run Notes

Run id: {run_id}
Scenario id: {scenario["id"]}
Runner: `src/social_sim`

This evidence pack was generated by the constrained buyer free-choice LLM action pilot runner.

Only the `buyer` role is LLM-controlled, and only for one action selection from the recorded five-item action menu. The requester, approver, accountant, and vendor records remain scripted or rule-based. The Game Master remains deterministic.

Provider: OpenAI
Model: {model}
Control mode: {scenario["control_mode"]}

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
