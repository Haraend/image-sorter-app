"""Service for listing images from the images/ folder."""

from pathlib import Path

# Supported image extensions
SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}

# Root images directory (project root / images)
IMAGES_DIR = Path(__file__).resolve().parent.parent.parent / "images"


def get_image_list() -> list[Path]:
    """Return a sorted list of image file paths from the images/ directory.

    Only includes files with supported image extensions.
    Returns an empty list if the directory doesn't exist or contains no images.
    """
    if not IMAGES_DIR.exists():
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        return []

    images = [
        f
        for f in IMAGES_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in SUPPORTED_EXTENSIONS
    ]

    return sorted(images, key=lambda p: p.name.lower())
