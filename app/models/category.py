"""Category model and validation."""

import re
from dataclasses import dataclass

# Pattern: lowercase letters/numbers separated by hyphens
# e.g. "nature-photos", "city-views", "dogs"
CATEGORY_NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class Category:
    """Represents an image sorting category."""

    name: str

    def to_dict(self) -> dict:
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(name=data["name"])


def validate_category_name(name: str) -> str | None:
    """Validate a category name.

    Returns an error message string if invalid, or None if valid.

    Valid format: lowercase letters/numbers separated by single hyphens.
    Examples: 'nature-photos', 'city-views', 'dogs', 'black-and-white'
    """
    if not name:
        return "Category name cannot be empty."

    if not CATEGORY_NAME_PATTERN.match(name):
        return (
            "Invalid format. Use lowercase letters and numbers separated by hyphens.\n"
            "Examples: 'nature-photos', 'city-views', 'dogs'"
        )

    return None
