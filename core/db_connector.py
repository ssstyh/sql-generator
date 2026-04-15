from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class DatabaseConnector:
    """Day 1 placeholder for database-related configuration access."""

    def __init__(self, config_path: Path | None = None) -> None:
        base_dir = Path(__file__).resolve().parent.parent
        self.config_path = config_path or (base_dir / "config" / "db_config.yaml")

    def load_config(self) -> dict[str, Any]:
        with self.config_path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        return data

    def get_profile(self, profile_name: str | None = None) -> dict[str, Any]:
        config = self.load_config()
        selected_profile = profile_name or config.get("default_profile")
        profiles = config.get("profiles", {})
        if selected_profile not in profiles:
            raise KeyError(f"Database profile not found: {selected_profile}")
        return profiles[selected_profile]
