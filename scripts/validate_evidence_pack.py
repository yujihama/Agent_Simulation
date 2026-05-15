#!/usr/bin/env python3
"""Validate a mechanically generated evidence pack.

This is a validation skeleton for protocol and schema work. It validates
JSON, JSONL, YAML, selected JSON Schema constraints, and cross-record references.
It does not execute agents, call providers, run a multi-run harness, or compute
baseline results. Evidence packs may record prior LLM execution when declared in
their manifest.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


class ValidationError(Exception):
    pass


@dataclass
class ValidationReport:
    pack_dir: Path
    checks: list[str]

    def add(self, message: str) -> None:
        self.checks.append(message)

    def as_markdown(self) -> str:
        lines = [
            "# Evidence Pack Validation Output",
            "",
            f"Evidence pack: `{self.pack_dir.as_posix()}`",
            "",
            "Result: PASS",
            "",
            "## Checks",
            "",
        ]
        lines.extend(f"- PASS: {check}" for check in self.checks)
        lines.extend(
            [
                "",
                "## Boundary",
                "",
                "This validation is mechanical. It does not execute LLMs, run a multi-run experiment harness, produce baseline results, or support statistical claims.",
            ]
        )
        return "\n".join(lines) + "\n"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValidationError(f"{path}: invalid JSON: {exc}") from exc


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValidationError(f"{path}:{lineno}: invalid JSONL: {exc}") from exc
        if not isinstance(value, dict):
            raise ValidationError(f"{path}:{lineno}: JSONL record must be an object")
        records.append(value)
    if not records:
        raise ValidationError(f"{path}: JSONL file is empty")
    return records


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise ValidationError("PyYAML is required for YAML validation") from exc
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - PyYAML exception types vary
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc


def schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return True


def resolve_ref(root_schema: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValidationError(f"unsupported schema ref: {ref}")
    node: Any = root_schema
    for part in ref[2:].split("/"):
        node = node[part]
    if not isinstance(node, dict):
        raise ValidationError(f"schema ref does not point to an object: {ref}")
    return node


def validate_schema(value: Any, schema: dict[str, Any], path: str = "$", root_schema: dict[str, Any] | None = None) -> list[str]:
    root_schema = root_schema or schema
    errors: list[str] = []

    if "$ref" in schema:
        return validate_schema(value, resolve_ref(root_schema, schema["$ref"]), path, root_schema)

    if "oneOf" in schema:
        matches = [validate_schema(value, option, path, root_schema) for option in schema["oneOf"]]
        if sum(1 for result in matches if not result) != 1:
            errors.append(f"{path}: expected exactly one matching schema")
        return errors

    if "anyOf" in schema:
        matches = [validate_schema(value, option, path, root_schema) for option in schema["anyOf"]]
        if not any(not result for result in matches):
            errors.append(f"{path}: expected at least one matching schema")
        return errors

    if "allOf" in schema:
        for option in schema["allOf"]:
            errors.extend(validate_schema(value, option, path, root_schema))

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}")

    if "type" in schema:
        expected_types = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(schema_type_matches(value, expected) for expected in expected_types):
            errors.append(f"{path}: expected type {expected_types!r}")
            return errors

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: value below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: value above maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: array shorter than {schema['minItems']}")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_schema(item, schema["items"], f"{path}[{index}]", root_schema))

    if isinstance(value, dict):
        required = schema.get("required", [])
        for field in required:
            if field not in value:
                errors.append(f"{path}: missing required field {field!r}")
        properties = schema.get("properties", {})
        for field, field_schema in properties.items():
            if field in value:
                errors.extend(validate_schema(value[field], field_schema, f"{path}.{field}", root_schema))
        if schema.get("additionalProperties") is False:
            extras = sorted(set(value) - set(properties))
            for field in extras:
                errors.append(f"{path}: unexpected field {field!r}")
        elif isinstance(schema.get("additionalProperties"), dict):
            for field, item in value.items():
                if field not in properties:
                    errors.extend(validate_schema(item, schema["additionalProperties"], f"{path}.{field}", root_schema))

    return errors


def schema(name: str) -> dict[str, Any]:
    return load_json(SCHEMA_DIR / name)


def assert_schema(value: Any, schema_name: str, label: str) -> None:
    schema_doc = schema(schema_name)
    errors = validate_schema(value, schema_doc)
    if errors:
        raise ValidationError(f"{label} failed {schema_name}:\n" + "\n".join(errors))


def by_id(records: list[dict[str, Any]], key: str, label: str) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = record.get(key)
        if not isinstance(record_id, str) or not record_id:
            raise ValidationError(f"{label}: missing id field {key}")
        if record_id in result:
            raise ValidationError(f"{label}: duplicate id {record_id}")
        result[record_id] = record
    return result


def require_pack_artifacts(pack_dir: Path, manifest: dict[str, Any]) -> None:
    inventory = manifest.get("artifact_inventory", {})
    for artifact, status in inventory.items():
        if status != "present":
            continue
        path = pack_dir / artifact
        if not path.exists():
            raise ValidationError(f"manifest marks {artifact!r} present, but it is missing")


def check_ref(ref: str, ids: dict[str, set[str]], pack_dir: Path) -> bool:
    if ref in ids["all"]:
        return True
    if ref.endswith(".jsonl") and (pack_dir / ref).exists():
        return True
    if ref.endswith(".json") and (pack_dir / ref).exists():
        return True
    if ref.endswith(".md") and (pack_dir / ref).exists():
        return True
    if "/" in ref and (pack_dir / ref).exists():
        return True
    return False


def validate_pack(pack_dir: Path) -> ValidationReport:
    pack_dir = pack_dir.resolve()
    try:
        display_pack_dir = pack_dir.relative_to(ROOT)
    except ValueError:
        display_pack_dir = pack_dir
    report = ValidationReport(pack_dir=display_pack_dir, checks=[])

    manifest = load_json(pack_dir / "manifest.json")
    assert_schema(manifest, "run-manifest.schema.json", "manifest.json")
    report.add("manifest.json validates against run-manifest.schema.json")

    if not isinstance(manifest.get("llm_execution"), bool):
        raise ValidationError("manifest llm_execution must be an explicit boolean")
    if manifest.get("automated_harness") is not False:
        raise ValidationError("single-pack validation requires automated_harness=false")
    report.add("manifest declares explicit LLM execution status and no automated harness")

    require_pack_artifacts(pack_dir, manifest)
    report.add("manifest artifact inventory matches files on disk")

    scenario = load_yaml(pack_dir / "scenario.yaml")
    if not isinstance(scenario, dict) or scenario.get("id") != manifest["scenario_id"]:
        raise ValidationError("scenario.yaml id must match manifest scenario_id")
    scenario_ref = ROOT / manifest["scenario_ref"]
    odd_ref = ROOT / manifest["odd_social_ref"]
    if not scenario_ref.exists():
        raise ValidationError(f"scenario_ref does not exist: {scenario_ref}")
    if not odd_ref.exists():
        raise ValidationError(f"odd_social_ref does not exist: {odd_ref}")
    load_yaml(scenario_ref)
    report.add("scenario YAML files parse and scenario id matches manifest")

    actions = load_jsonl(pack_dir / "actions.jsonl")
    decisions = load_jsonl(pack_dir / "gm_decisions.jsonl")
    trace = load_jsonl(pack_dir / "trace.jsonl")
    events = load_jsonl(pack_dir / "events.jsonl")
    messages = load_jsonl(pack_dir / "messages.jsonl")
    metrics = load_json(pack_dir / "metrics.json")

    for record in actions:
        assert_schema(record, "action-proposal.schema.json", f"action {record.get('action_id')}")
    for record in decisions:
        assert_schema(record, "gm-decision.schema.json", f"decision {record.get('decision_id')}")
    for record in trace:
        assert_schema(record, "trace-record.schema.json", f"trace {record.get('trace_id')}")
    for record in events:
        assert_schema(record, "event-record.schema.json", f"event {record.get('event_id')}")
    assert_schema(metrics, "metrics-record.schema.json", "metrics.json")
    report.add("JSON and JSONL records validate against contract schemas")

    run_id = manifest["run_id"]
    for label, records in [
        ("actions", actions),
        ("gm decisions", decisions),
        ("trace", trace),
        ("events", events),
    ]:
        for record in records:
            if record.get("run_id") != run_id:
                raise ValidationError(f"{label}: run_id mismatch in {record}")
    if metrics.get("run_id") != run_id:
        raise ValidationError("metrics.json run_id mismatch")
    for metric in metrics.get("metrics", []):
        if "run_id" in metric and metric["run_id"] != run_id:
            raise ValidationError(f"metric {metric['metric_id']} run_id does not match envelope")
        if "metrics_version" in metric and metric["metrics_version"] != metrics["metrics_version"]:
            raise ValidationError(f"metric {metric['metric_id']} metrics_version does not match envelope")
    report.add("run_id and metrics envelope inheritance are consistent")

    action_by_id = by_id(actions, "action_id", "actions")
    decision_by_id = by_id(decisions, "decision_id", "gm_decisions")
    trace_by_id = by_id(trace, "trace_id", "trace")
    event_by_id = by_id(events, "event_id", "events")
    message_by_id = by_id(messages, "message_id", "messages")
    ids = {
        "actions": set(action_by_id),
        "decisions": set(decision_by_id),
        "trace": set(trace_by_id),
        "events": set(event_by_id),
        "messages": set(message_by_id),
    }
    ids["all"] = set().union(*ids.values())

    for decision in decisions:
        if decision["action_id"] not in action_by_id:
            raise ValidationError(f"decision {decision['decision_id']} references missing action {decision['action_id']}")
        for ref in decision.get("evidence_refs", []):
            if not check_ref(ref, ids, pack_dir):
                raise ValidationError(f"decision {decision['decision_id']} has unknown evidence ref {ref}")

    for action in actions:
        for ref in action.get("source_refs", []):
            if not check_ref(ref, ids, pack_dir):
                raise ValidationError(f"action {action['action_id']} has unknown source ref {ref}")
    report.add("action proposal source references resolve")

    decided_action_ids = {decision["action_id"] for decision in decisions}
    undecided_action_ids = sorted(set(action_by_id) - decided_action_ids)
    if undecided_action_ids:
        raise ValidationError(
            "current action proposals require Game Master decisions; "
            f"missing decision for action_id(s): {', '.join(undecided_action_ids)}"
        )
    report.add("every current action proposal has a corresponding Game Master decision")

    for event in events:
        if event["turn_end"] < event["turn_start"]:
            raise ValidationError(f"event {event['event_id']} has turn_end before turn_start")
        for ref in event.get("source_refs", []):
            if not check_ref(ref, ids, pack_dir):
                raise ValidationError(f"event {event['event_id']} has unknown source ref {ref}")

    for record in trace:
        for ref in record.get("event_refs", []):
            if ref not in event_by_id:
                raise ValidationError(f"trace {record['trace_id']} references missing event {ref}")
        if not (record["record_ref"] in ids["all"] or check_ref(record["record_ref"], ids, pack_dir)):
            raise ValidationError(f"trace {record['trace_id']} has unknown record_ref {record['record_ref']}")

    for metric in metrics.get("metrics", []):
        for event_id in metric.get("source_event_ids", []):
            if event_id not in event_by_id:
                raise ValidationError(f"metric {metric['metric_id']} references missing event {event_id}")
        for ref in metric.get("source_record_refs", []):
            if not check_ref(ref, ids, pack_dir):
                raise ValidationError(f"metric {metric['metric_id']} has unknown source record ref {ref}")
    report.add("cross-references among actions, decisions, trace, events, and metrics resolve")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a non-LLM evidence pack.")
    parser.add_argument("evidence_pack", type=Path, help="Path to an evidence-pack directory")
    parser.add_argument("--report", type=Path, help="Optional markdown report path")
    args = parser.parse_args()

    try:
        report = validate_pack(args.evidence_pack)
    except ValidationError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    text = report.as_markdown()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
