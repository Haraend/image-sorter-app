"""Main application window — manages screen transitions."""

import tkinter as tk

from app.gui.category_screen import CategoryScreen
from app.gui.sorting_screen import SortingScreen


class ImageSorterApp(tk.Tk):
    """Root window that switches between category management and sorting."""

    def __init__(self):
        super().__init__()

        self.title("Image Sorter")
        self.geometry("850x700")
        self.minsize(600, 500)
        self.configure(bg="#1e1e2e")

        # Center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 850) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")

        self._current_screen = None
        self._show_category_screen()

    def _clear_screen(self):
        """Remove the current screen."""
        if self._current_screen is not None:
            self._current_screen.destroy()
            self._current_screen = None

    def _show_category_screen(self):
        self._clear_screen()
        self._current_screen = CategoryScreen(
            self,
            on_continue_callback=self._show_sorting_screen,
        )
        self._current_screen.configure(bg="#1e1e2e")
        self._current_screen.pack(fill="both", expand=True)

    def _show_sorting_screen(self):
        self._clear_screen()
        self._current_screen = SortingScreen(
            self,
            on_back_callback=self._show_category_screen,
        )
        self._current_screen.pack(fill="both", expand=True)
