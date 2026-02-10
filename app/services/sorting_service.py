"""Service for sorting (moving) images into category folders."""

import shutil
from pathlib import Path

# Output directory (project root / sorted-images)
SORTED_DIR = Path(__file__).resolve().parent.parent.parent / "sorted-images"


def sort_image(image_path: Path, category_name: str) -> None:
    """Move an image into sorted-images/<category_name>/.

    Creates the category subdirectory if it doesn't exist.
    If a file with the same name already exists in the target directory,
    a numeric suffix is appended to avoid overwriting.
    """
    category_dir = SORTED_DIR / category_name
    category_dir.mkdir(parents=True, exist_ok=True)

    destination = category_dir / image_path.name

    # Handle filename collisions
    if destination.exists():
        stem = image_path.stem
        suffix = image_path.suffix
        counter = 1
        while destination.exists():
            destination = category_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.move(str(image_path), str(destination))
