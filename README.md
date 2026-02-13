# Image Sorter App

I need to sort some images, and instead of doing it manually spending more time creating this script is totally the way to go.

## Features

- **Category management** — create, rename, and remove categories with validation
- **Visual sorting** — displays each image full-size so you can pick a category
- **Keyboard shortcuts** — press `1`–`9` or `0` for the first 10 categories
- **Custom folders** — choose any input/output directory via Browse buttons
- **Persistent settings** — categories and folder paths remembered between sessions
- **Auto-organized output** — images moved into `<output>/<category>/` folders

## Download

Grab the latest `ImageSorter.exe` from the [Releases](../../releases) page — no Python installation needed.

## Requirements (source only)

- Python 3.10+
- [Pillow](https://pypi.org/project/Pillow/) (for image display)
- tkinter (ships with Python on most platforms)

## Setup (source)

```bash
# (Optional) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Run the app**
   ```bash
   python main.py
   ```
   Or use the standalone `ImageSorter.exe` from Releases.

2. **Set folders** *(optional)* — use the Browse buttons to pick custom input/output directories
   > ⚠ **Images are MOVED, not copied! Keep a backup!**

3. **Create categories** — on first launch you'll be asked to set up categories
   Use the format `image-category-name` (lowercase letters and hyphens only)
   Examples: `nature-photos`, `city-views`, `black-and-white`

4. **Sort images** — each image is shown one at a time; click a category button or press a number key to sort it

5. **Results** — sorted images are moved into `<output-folder>/<category>/`

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1` – `9` | Sort into category 1–9 |
| `0` | Sort into category 10 |

## Project Structure

```
image-sorter-app/
├── main.py                        # Entry point
├── images/                        # Default input folder
├── sorted-images/                 # Default output folder (created at runtime)
├── app/
│   ├── models/
│   │   └── category.py            # Category dataclass + validation
│   ├── services/
│   │   ├── category_service.py    # Category CRUD + JSON persistence
│   │   ├── image_service.py       # Image file listing
│   │   ├── sorting_service.py     # Move images to sorted folders
│   │   └── settings_service.py    # Folder path settings persistence
│   ├── gui/
│   │   ├── app.py                 # Main window + screen routing
│   │   ├── category_screen.py     # Category management + folder settings UI
│   │   └── sorting_screen.py      # Image display + sorting UI
│   └── data/
│       ├── categories.json        # Persisted categories (runtime)
│       └── settings.json          # Persisted folder paths (runtime)
├── .gitignore
├── requirements.txt
└── README.md
```

## Category Name Format

Categories must follow the `image-category-name` format:
- **Lowercase** letters and numbers only
- Separated by **hyphens** (`-`)
- No spaces, underscores, or special characters

✅ `nature-photos`, `dogs`, `black-and-white`
❌ `Nature Photos`, `foo_bar`, `My Category!`

## Building the Executable

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ImageSorter" --clean main.py
```

The executable will be at `dist/ImageSorter.exe`.
