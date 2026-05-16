from __future__ import annotations

from pathlib import Path
from typing import Any


ORG_PAYMENT_SCENARIO_FILES = {
    "S01": "s01-clear-policy-low-pressure.yaml",
    "S02": "s02-ambiguous-policy-low-pressure.yaml",
    "S03": "s03-ambiguous-policy-high-pressure.yaml",
    "S04": "s04-role-overlap-high-pressure.yaml",
    "S05": "s05-audit-intervention.yaml",
    "S06": "s06-hard-control.yaml",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to load scenario YAML") from exc
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected YAML object: {path}")
    return data


def dump_yaml(data: dict[str, Any]) -> str:
    try:
        import yaml  # type: ignore
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to write scenario YAML") from exc
    return yaml.safe_dump(data, sort_keys=False)


def load_s04(root: Path | None = None) -> dict[str, Any]:
    return load_org_payment_scenario("S04", root=root)


def org_payment_scenario_path(scenario_id: str, root: Path | None = None) -> Path:
    scenario_id = scenario_id.upper()
    if scenario_id not in ORG_PAYMENT_SCENARIO_FILES:
        raise ValueError(f"unknown org-payment scenario_id: {scenario_id}")
    root = root or repo_root()
    return root / "scenarios" / "org-payment" / ORG_PAYMENT_SCENARIO_FILES[scenario_id]


def org_payment_scenario_ref(scenario_id: str) -> str:
    return f"scenarios/org-payment/{ORG_PAYMENT_SCENARIO_FILES[scenario_id.upper()]}"


def load_org_payment_scenario(scenario_id: str, root: Path | None = None) -> dict[str, Any]:
    scenario = load_yaml(org_payment_scenario_path(scenario_id, root=root))
    expected_id = scenario_id.upper()
    if scenario.get("id") != expected_id:
        raise ValueError(f"scenario file id mismatch: expected {expected_id}, got {scenario.get('id')}")
    return scenario


def load_org_payment_scenarios(root: Path | None = None) -> list[dict[str, Any]]:
    return [load_org_payment_scenario(scenario_id, root=root) for scenario_id in ORG_PAYMENT_SCENARIO_FILES]
