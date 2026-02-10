# Image Sorter App

I need to sort some images, and I am too lazy to do it manually. Clearly spending twice the time creating this script is the way to go.

## Features

- **Category management** — create, rename, and remove categories with validation
- **Visual sorting** — displays each image full-size so you can pick a category
- **Keyboard shortcuts** — press `1`–`9` or `0` for the first 10 categories
- **Persistent categories** — saved as JSON, remembered between sessions
- **Auto-organized output** — images moved into `sorted-images/<category>/` folders

## Requirements

- Python 3.10+
- [Pillow](https://pypi.org/project/Pillow/) (for image display)
- tkinter (ships with Python on most platforms)

## Setup

```bash
# (Optional) Create a virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install Pillow
```

## Usage

1. **Add images** — drop your unsorted images into the `images/` folder
2. **Run the app**
   ```bash
   python main.py
   ```
3. **Create categories** — on first launch you'll be asked to set up categories  
   Use the format `image-category-name` (lowercase letters and hyphens only)  
   Examples: `nature-photos`, `city-views`, `black-and-white`
4. **Sort images** — each image is shown one at a time; click a category button or press a number key to sort it
5. **Results** — sorted images are moved into `sorted-images/<category>/`

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1` – `9` | Sort into category 1–9 |
| `0` | Sort into category 10 |

## Project Structure

```
image-sorter-app/
├── main.py                        # Entry point
├── images/                        # Drop unsorted images here
├── sorted-images/                 # Output (created at runtime)
├── app/
│   ├── models/
│   │   └── category.py            # Category dataclass + validation
│   ├── services/
│   │   ├── category_service.py    # Category CRUD + JSON persistence
│   │   ├── image_service.py       # Image file listing
│   │   └── sorting_service.py     # Move images to sorted folders
│   ├── gui/
│   │   ├── app.py                 # Main window + screen routing
│   │   ├── category_screen.py     # Category management UI
│   │   └── sorting_screen.py      # Image display + sorting UI
│   └── data/
│       └── categories.json        # Persisted categories (runtime)
├── .gitignore
└── README.md
```

## Category Name Format

Categories must follow the `image-category-name` format:
- **Lowercase** letters and numbers only
- Separated by **hyphens** (`-`)
- No spaces, underscores, or special characters

✅ `nature-photos`, `dogs`, `black-and-white`  
❌ `Nature Photos`, `foo_bar`, `My Category!`
