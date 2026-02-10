"""Sorting screen — display images one-by-one with category buttons."""

import tkinter as tk
from tkinter import messagebox
from pathlib import Path

from PIL import Image, ImageTk

from app.services import category_service, image_service, sorting_service


class SortingScreen(tk.Frame):
    """Screen that shows images one at a time for the user to sort."""

    def __init__(self, master, on_back_callback):
        super().__init__(master, bg="#1e1e2e")
        self.on_back = on_back_callback
        self.images: list[Path] = []
        self.current_index: int = 0
        self._photo_ref = None  # prevent garbage collection

        self._build_ui()
        self._load_images()

    def _build_ui(self):
        # ── Top bar ──
        top_bar = tk.Frame(self, bg="#1e1e2e")
        top_bar.pack(fill="x", padx=20, pady=(15, 5))

        back_btn = tk.Button(
            top_bar,
            text="← Edit Categories",
            font=("Segoe UI", 10),
            bg="#374151",
            fg="#e0e0e0",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.on_back,
        )
        back_btn.pack(side="left")

        self.progress_label = tk.Label(
            top_bar,
            text="",
            font=("Segoe UI", 11),
            fg="#888",
            bg="#1e1e2e",
        )
        self.progress_label.pack(side="right")

        # ── Image display ──
        self.image_frame = tk.Frame(self, bg="#2a2a3d", highlightthickness=1, highlightbackground="#3a3a5c")
        self.image_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.image_label = tk.Label(self.image_frame, bg="#2a2a3d")
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

        self.filename_label = tk.Label(
            self,
            text="",
            font=("Segoe UI", 10),
            fg="#aaa",
            bg="#1e1e2e",
        )
        self.filename_label.pack(pady=(0, 5))

        # ── Category buttons container ──
        self.btn_frame = tk.Frame(self, bg="#1e1e2e")
        self.btn_frame.pack(padx=20, pady=(5, 15), fill="x")

        # ── "All done" label (hidden initially) ──
        self.done_label = tk.Label(
            self,
            text="✅  All images sorted!",
            font=("Segoe UI", 20, "bold"),
            fg="#34d399",
            bg="#1e1e2e",
        )

    def _load_images(self):
        self.images = image_service.get_image_list()
        self.current_index = 0

        if not self.images:
            self._show_no_images()
            return

        self._build_category_buttons()
        self._show_current_image()

    def _build_category_buttons(self):
        # Clear previous buttons
        for widget in self.btn_frame.winfo_children():
            widget.destroy()

        categories = category_service.get_categories()
        # Keys 1-9 then 0 for the 10th
        key_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

        # Create a grid of buttons, 5 per row
        for i, cat in enumerate(categories):
            key = key_labels[i] if i < 10 else ""
            label_text = f"[{key}]  {cat.name}" if key else cat.name

            btn = tk.Button(
                self.btn_frame,
                text=label_text,
                font=("Segoe UI", 11),
                bg="#7c3aed",
                fg="white",
                activebackground="#6d28d9",
                activeforeground="white",
                relief="flat",
                cursor="hand2",
                command=lambda name=cat.name: self._sort_current(name),
            )
            row, col = divmod(i, 5)
            btn.grid(row=row, column=col, padx=4, pady=4, sticky="ew", ipady=5)

        # Make columns share width evenly
        for col in range(5):
            self.btn_frame.columnconfigure(col, weight=1)

        # Bind keyboard shortcuts
        self._bind_keys(categories)

    def _bind_keys(self, categories):
        """Bind number keys 1-9 and 0 to the first 10 categories."""
        root = self.winfo_toplevel()

        # Unbind previous
        for k in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            root.unbind(f"<Key-{k}>")

        key_map = {
            "1": 0, "2": 1, "3": 2, "4": 3, "5": 4,
            "6": 5, "7": 6, "8": 7, "9": 8, "0": 9,
        }

        for key, index in key_map.items():
            if index < len(categories):
                cat_name = categories[index].name
                root.bind(
                    f"<Key-{key}>",
                    lambda e, name=cat_name: self._sort_current(name),
                )

    def _show_current_image(self):
        if self.current_index >= len(self.images):
            self._show_done()
            return

        image_path = self.images[self.current_index]
        total = len(self.images)

        self.progress_label.config(
            text=f"Image {self.current_index + 1} of {total}"
        )
        self.filename_label.config(text=image_path.name)

        # Load & resize image to fit the frame
        try:
            pil_image = Image.open(image_path)
            pil_image.thumbnail((700, 500), Image.LANCZOS)
            self._photo_ref = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self._photo_ref, text="")
        except Exception as e:
            self.image_label.config(
                image="",
                text=f"⚠ Cannot display image:\n{e}",
                font=("Segoe UI", 12),
                fg="#f87171",
            )
            self._photo_ref = None

    def _sort_current(self, category_name: str):
        if self.current_index >= len(self.images):
            return

        image_path = self.images[self.current_index]

        try:
            sorting_service.sort_image(image_path, category_name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sort image:\n{e}")
            return

        self.current_index += 1
        self._show_current_image()

    def _show_no_images(self):
        self.image_label.config(
            image="",
            text="No images found in the images/ folder.\n\nAdd images and restart the app.",
            font=("Segoe UI", 14),
            fg="#fbbf24",
        )
        self.filename_label.config(text="")
        self.progress_label.config(text="0 images")

    def _show_done(self):
        self.image_label.config(image="", text="")
        self._photo_ref = None
        self.filename_label.config(text="")
        self.progress_label.config(text="Done")

        # Hide image frame & buttons, show done label
        self.image_frame.pack_forget()
        self.btn_frame.pack_forget()
        self.filename_label.pack_forget()
        self.done_label.pack(expand=True)

        # Unbind keys
        root = self.winfo_toplevel()
        for k in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]:
            root.unbind(f"<Key-{k}>")
