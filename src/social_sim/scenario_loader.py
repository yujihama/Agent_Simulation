from __future__ import annotations

from pathlib import Path
from typing import Any


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
    root = root or repo_root()
    return load_yaml(root / "scenarios" / "org-payment" / "s04-role-overlap-high-pressure.yaml")
