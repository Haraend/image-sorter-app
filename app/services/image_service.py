"""Service for listing images from the input folder."""

from pathlib import Path

from app.services.settings_service import get_input_dir

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}


def get_image_list() -> list[Path]:
    """Return a sorted list of image file paths from the input directory.

    Only includes files with supported image extensions.
    Returns an empty list if the directory doesn't exist or contains no images.
    """
    images_dir = get_input_dir()

    if not images_dir.exists():
        images_dir.mkdir(parents=True, exist_ok=True)
        return []

    images = [
        f
        for f in images_dir.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    return sorted(images, key=lambda p: p.name.lower())
