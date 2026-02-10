"""Service for managing categories (CRUD + persistence)."""

import json
from pathlib import Path

from app.models.category import Category, validate_category_name

# Path to the persisted categories file
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CATEGORIES_FILE = DATA_DIR / "categories.json"


def _ensure_data_dir() -> None:
    """Create the data directory if it doesn't exist."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_categories() -> list[Category]:
    """Load categories from disk. Returns empty list if none exist."""
    if not CATEGORIES_FILE.exists():
        return []

    try:
        with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Category.from_dict(item) for item in data]
    except (json.JSONDecodeError, KeyError):
        return []


def save_categories(categories: list[Category]) -> None:
    """Persist the full category list to disk."""
    _ensure_data_dir()
    with open(CATEGORIES_FILE, "w", encoding="utf-8") as f:
        json.dump([cat.to_dict() for cat in categories], f, indent=2)


def add_category(name: str) -> str | None:
    """Add a new category. Returns error message or None on success."""
    error = validate_category_name(name)
    if error:
        return error

    categories = get_categories()
    if any(cat.name == name for cat in categories):
        return f"Category '{name}' already exists."

    categories.append(Category(name=name))
    save_categories(categories)
    return None


def remove_category(name: str) -> str | None:
    """Remove a category by name. Returns error message or None on success."""
    categories = get_categories()
    updated = [cat for cat in categories if cat.name != name]

    if len(updated) == len(categories):
        return f"Category '{name}' not found."

    save_categories(updated)
    return None


def rename_category(old_name: str, new_name: str) -> str | None:
    """Rename a category. Returns error message or None on success."""
    error = validate_category_name(new_name)
    if error:
        return error

    categories = get_categories()

    if any(cat.name == new_name for cat in categories):
        return f"Category '{new_name}' already exists."

    found = False
    for cat in categories:
        if cat.name == old_name:
            cat.name = new_name
            found = True
            break

    if not found:
        return f"Category '{old_name}' not found."

    save_categories(categories)
    return None
