"""Service for managing app settings (folder paths)."""

import json
from pathlib import Path

# Persist settings alongside categories
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SETTINGS_FILE = DATA_DIR / "settings.json"

# Default — current working directory (the folder the user launches from)
DEFAULT_INPUT_DIR = str(Path.cwd())


def _ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_settings() -> dict:
    """Load settings from disk. Returns defaults if file doesn't exist."""
    defaults = {
        "input_dir": DEFAULT_INPUT_DIR,
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
    """Return the output directory — always <input_dir>/sorted."""
    return get_input_dir() / "sorted"


def set_input_dir(path: str) -> None:
    """Update the input directory."""
    settings = get_settings()
    settings["input_dir"] = path
    save_settings(settings)
