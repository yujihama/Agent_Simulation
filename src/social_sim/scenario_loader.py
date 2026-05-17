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

ORG_PAYMENT_HIGH_FRICTION_SCENARIO_FILES = {
    "S07": "s07-ambiguous-delegated-authority.yaml",
    "S08": "s08-split-responsibility-deadline.yaml",
    "S09": "s09-informal-pre-approval.yaml",
    "S10": "s10-conflicting-policy-and-norm.yaml",
    "S11": "s11-audit-visibility-workaround.yaml",
    "S12": "s12-post-hoc-justification-setting.yaml",
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


def org_payment_scenario_files(include_high_friction: bool = False) -> dict[str, str]:
    files = dict(ORG_PAYMENT_SCENARIO_FILES)
    if include_high_friction:
        files.update(ORG_PAYMENT_HIGH_FRICTION_SCENARIO_FILES)
    return files


def org_payment_scenario_path(scenario_id: str, root: Path | None = None, include_high_friction: bool = False) -> Path:
    scenario_id = scenario_id.upper()
    files = org_payment_scenario_files(include_high_friction=include_high_friction)
    if scenario_id not in files:
        raise ValueError(f"unknown org-payment scenario_id: {scenario_id}")
    root = root or repo_root()
    return root / "scenarios" / "org-payment" / files[scenario_id]


def org_payment_scenario_ref(scenario_id: str, include_high_friction: bool = True) -> str:
    files = org_payment_scenario_files(include_high_friction=include_high_friction)
    return f"scenarios/org-payment/{files[scenario_id.upper()]}"


def load_org_payment_scenario(scenario_id: str, root: Path | None = None, include_high_friction: bool = False) -> dict[str, Any]:
    scenario = load_yaml(org_payment_scenario_path(scenario_id, root=root, include_high_friction=include_high_friction))
    expected_id = scenario_id.upper()
    if scenario.get("id") != expected_id:
        raise ValueError(f"scenario file id mismatch: expected {expected_id}, got {scenario.get('id')}")
    return scenario


def load_org_payment_scenarios(root: Path | None = None) -> list[dict[str, Any]]:
    return [load_org_payment_scenario(scenario_id, root=root) for scenario_id in ORG_PAYMENT_SCENARIO_FILES]
