"""Service for managing app settings (folder paths)."""

import json
from pathlib import Path

# Persist settings alongside categories
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Defaults — relative to project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_INPUT_DIR = str(_PROJECT_ROOT / "images")
DEFAULT_OUTPUT_DIR = str(_PROJECT_ROOT / "sorted-images")


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_settings() -> dict:
    """Load settings from disk. Returns defaults if file doesn't exist."""
    defaults = {
        "input_dir": DEFAULT_INPUT_DIR,
        "output_dir": DEFAULT_OUTPUT_DIR,
    }

    if not SETTINGS_FILE.exists():
        return defaults

    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Merge with defaults so new keys are always present
        return {**defaults, **data}
    except (json.JSONDecodeError, KeyError):
        return defaults


def save_settings(settings: dict) -> None:
    """Persist settings to disk."""
    _ensure_data_dir()
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)


def get_input_dir() -> Path:
    """Return the configured input directory as a Path."""
    p = Path(get_settings()["input_dir"])
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_output_dir() -> Path:
    """Return the configured output directory as a Path."""
    return Path(get_settings()["output_dir"])


def set_input_dir(path: str) -> None:
    """Update the input directory."""
    settings = get_settings()
    settings["input_dir"] = path
    save_settings(settings)


def set_output_dir(path: str) -> None:
    """Update the output directory."""
    settings = get_settings()
    settings["output_dir"] = path
    save_settings(settings)
