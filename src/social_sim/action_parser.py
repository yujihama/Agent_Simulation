from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
ACTION_SCHEMA_PATH = ROOT / "schemas" / "action-proposal.schema.json"


class ActionParseError(ValueError):
    pass


def load_action_schema(path: Path = ACTION_SCHEMA_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_action_proposal(
    text: str,
    *,
    expected_fields: dict[str, Any],
    allowed_source_refs: set[str],
    schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    schema = schema or load_action_schema()
    value = _load_json_object(text)
    if "action_proposal" in value and isinstance(value["action_proposal"], dict):
        value = value["action_proposal"]

    _validate_against_action_schema(value, schema)
    for field, expected in expected_fields.items():
        if value.get(field) != expected:
            raise ActionParseError(f"{field} must be {expected!r}, got {value.get(field)!r}")

    unknown_refs = sorted(set(value.get("source_refs", [])) - allowed_source_refs)
    if unknown_refs:
        raise ActionParseError(f"source_refs include refs outside the allowed prior evidence set: {unknown_refs}")
    return value


def _load_json_object(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ActionParseError("LLM output does not contain a JSON object")
        try:
            value = json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise ActionParseError(f"LLM output is not valid JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise ActionParseError("LLM output must be a JSON object")
    return value


def _validate_against_action_schema(value: dict[str, Any], schema: dict[str, Any]) -> None:
    required = schema.get("required", [])
    missing = [field for field in required if field not in value]
    if missing:
        raise ActionParseError(f"missing required action fields: {missing}")

    properties = schema.get("properties", {})
    if schema.get("additionalProperties") is False:
        extras = sorted(set(value) - set(properties))
        if extras:
            raise ActionParseError(f"unexpected action fields: {extras}")

    for field, field_schema in properties.items():
        if field not in value:
            continue
        _validate_value(value[field], field_schema, field)


def _validate_value(value: Any, schema: dict[str, Any], field: str) -> None:
    if "anyOf" in schema:
        errors: list[str] = []
        for option in schema["anyOf"]:
            try:
                _validate_value(value, option, field)
                return
            except ActionParseError as exc:
                errors.append(str(exc))
        raise ActionParseError(f"{field} does not match any allowed schema: {errors}")

    if "enum" in schema and value not in schema["enum"]:
        raise ActionParseError(f"{field} must be one of {schema['enum']!r}, got {value!r}")

    expected_type = schema.get("type")
    if expected_type == "string" and not isinstance(value, str):
        raise ActionParseError(f"{field} must be a string")
    if expected_type == "integer" and (not isinstance(value, int) or isinstance(value, bool)):
        raise ActionParseError(f"{field} must be an integer")
    if expected_type == "boolean" and not isinstance(value, bool):
        raise ActionParseError(f"{field} must be a boolean")
    if expected_type == "null" and value is not None:
        raise ActionParseError(f"{field} must be null")
    if expected_type == "array":
        if not isinstance(value, list):
            raise ActionParseError(f"{field} must be an array")
        item_schema = schema.get("items", {})
        for index, item in enumerate(value):
            _validate_value(item, item_schema, f"{field}[{index}]")

    if isinstance(value, str) and schema.get("minLength") and len(value) < schema["minLength"]:
        raise ActionParseError(f"{field} is shorter than {schema['minLength']}")
    if isinstance(value, int) and not isinstance(value, bool) and "minimum" in schema and value < schema["minimum"]:
        raise ActionParseError(f"{field} is below minimum {schema['minimum']}")
