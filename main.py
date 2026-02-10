"""Image Sorter App — entry point."""

from app.gui.app import ImageSorterApp


def main():
    app = ImageSorterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
