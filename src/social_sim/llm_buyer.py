from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .action_parser import ActionParseError, load_action_schema, parse_action_proposal
from .llm_actor import LLMProvider, LLMRequest, LLMResponse


ROOT = Path(__file__).resolve().parents[2]
PROMPT_TEMPLATE = ROOT / "prompts" / "org-payment" / "buyer-action-proposal-v0.1.md"


@dataclass(frozen=True)
class BuyerActionResult:
    action: dict[str, Any]
    prompt_text: str
    response: LLMResponse


SYSTEM_PROMPT = """You are a controlled buyer actor in a research simulation.
Produce exactly one schema-valid JSON action proposal for the preselected buyer decision point.
Do not choose a different action type, target role, turn, or identity field. Do not simulate other roles.
Do not bypass the Game Master. Do not make claims outside the provided scenario context."""


def generate_buyer_action(
    *,
    provider: LLMProvider,
    run_id: str,
    case_id: str,
    action_id: str,
    turn: int,
    target_role: str,
    action_type: str,
    context: str,
    allowed_source_refs: list[str],
    attempts: int = 2,
) -> BuyerActionResult:
    schema = load_action_schema()
    expected_fields = {
        "action_id": action_id,
        "run_id": run_id,
        "turn": turn,
        "proposed_by": "buyer",
        "target_role": target_role,
        "action_type": action_type,
        "case_id": case_id,
        "human_authored": False,
    }
    prompt_text = render_prompt(
        run_id=run_id,
        case_id=case_id,
        action_id=action_id,
        turn=turn,
        target_role=target_role,
        action_type=action_type,
        context=context,
        allowed_source_refs=allowed_source_refs,
        schema=schema,
    )

    last_error: ActionParseError | None = None
    for attempt in range(1, attempts + 1):
        user_prompt = prompt_text
        if last_error is not None:
            user_prompt += (
                "\n\nPrevious output failed local validation: "
                f"{last_error}. Return corrected JSON only."
            )
        response = provider.complete_json(
            LLMRequest(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=user_prompt,
                schema_name="action_proposal_v0_1",
                schema=schema,
            )
        )
        try:
            action = parse_action_proposal(
                response.text,
                expected_fields=expected_fields,
                allowed_source_refs=set(allowed_source_refs),
                schema=schema,
            )
            return BuyerActionResult(action=action, prompt_text=user_prompt, response=response)
        except ActionParseError as exc:
            last_error = exc

    raise ActionParseError(f"LLM action proposal failed validation after {attempts} attempts: {last_error}")


def render_prompt(
    *,
    run_id: str,
    case_id: str,
    action_id: str,
    turn: int,
    target_role: str,
    action_type: str,
    context: str,
    allowed_source_refs: list[str],
    schema: dict[str, Any],
) -> str:
    text = PROMPT_TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "{{action_id}}": action_id,
        "{{run_id}}": run_id,
        "{{turn}}": str(turn),
        "{{target_role}}": target_role,
        "{{action_type}}": action_type,
        "{{case_id}}": case_id,
        "{{allowed_source_refs}}": "\n".join(f"- {ref}" for ref in allowed_source_refs),
        "{{context}}": context,
        "{{schema_json}}": json.dumps(schema, indent=2),
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)
    return text
