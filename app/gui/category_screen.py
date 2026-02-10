"""Category management screen — create, edit, remove categories."""

import tkinter as tk
from tkinter import messagebox, simpledialog

from app.models.category import validate_category_name
from app.services import category_service


class CategoryScreen(tk.Frame):
    """Screen for managing image sorting categories."""

    def __init__(self, master, on_continue_callback):
        super().__init__(master)
        self.on_continue = on_continue_callback
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # ── Title ──
        title = tk.Label(
            self,
            text="Manage Categories",
            font=("Segoe UI", 18, "bold"),
            fg="#e0e0e0",
            bg="#1e1e2e",
        )
        title.pack(pady=(20, 5))

        hint = tk.Label(
            self,
            text='Use format:  image-category-name  (lowercase, hyphens only)',
            font=("Segoe UI", 10),
            fg="#888",
            bg="#1e1e2e",
        )
        hint.pack(pady=(0, 10))

        # ── Add category row ──
        add_frame = tk.Frame(self, bg="#1e1e2e")
        add_frame.pack(pady=5, padx=20, fill="x")

        self.entry = tk.Entry(
            add_frame,
            font=("Segoe UI", 12),
            bg="#2a2a3d",
            fg="#e0e0e0",
            insertbackground="#e0e0e0",
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightcolor="#7c3aed",
            highlightbackground="#3a3a5c",
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))
        self.entry.bind("<Return>", lambda e: self._add_category())

        add_btn = tk.Button(
            add_frame,
            text="＋ Add",
            font=("Segoe UI", 11, "bold"),
            bg="#7c3aed",
            fg="white",
            activebackground="#6d28d9",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._add_category,
        )
        add_btn.pack(side="right", ipady=4, ipadx=10)

        # ── Category list ──
        list_frame = tk.Frame(self, bg="#1e1e2e")
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 12),
            bg="#2a2a3d",
            fg="#e0e0e0",
            selectbackground="#7c3aed",
            selectforeground="white",
            relief="flat",
            bd=0,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # ── Action buttons ──
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=5, padx=20, fill="x")

        rename_btn = tk.Button(
            btn_frame,
            text="✏ Rename",
            font=("Segoe UI", 10),
            bg="#374151",
            fg="#e0e0e0",
            activebackground="#4b5563",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._rename_category,
        )
        rename_btn.pack(side="left", padx=(0, 5), ipady=3, ipadx=8)

        remove_btn = tk.Button(
            btn_frame,
            text="✕ Remove",
            font=("Segoe UI", 10),
            bg="#991b1b",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._remove_category,
        )
        remove_btn.pack(side="left", padx=(0, 5), ipady=3, ipadx=8)

        # ── Continue button ──
        self.continue_btn = tk.Button(
            self,
            text="Continue to Sorting  →",
            font=("Segoe UI", 13, "bold"),
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self._on_continue,
        )
        self.continue_btn.pack(pady=(10, 20), ipady=6, ipadx=20)

    # ── Actions ──

    def _add_category(self):
        name = self.entry.get().strip()
        error = category_service.add_category(name)
        if error:
            messagebox.showwarning("Invalid Category", error)
            return
        self.entry.delete(0, tk.END)
        self._refresh_list()

    def _remove_category(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Select", "Select a category to remove.")
            return
        name = self.listbox.get(selection[0])
        if messagebox.askyesno("Confirm", f"Remove category '{name}'?"):
            category_service.remove_category(name)
            self._refresh_list()

    def _rename_category(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("Select", "Select a category to rename.")
            return
        old_name = self.listbox.get(selection[0])
        new_name = simpledialog.askstring(
            "Rename Category",
            f"Rename '{old_name}' to:\n(format: image-category-name)",
            parent=self,
        )
        if new_name is None:
            return
        new_name = new_name.strip()
        error = category_service.rename_category(old_name, new_name)
        if error:
            messagebox.showwarning("Invalid", error)
            return
        self._refresh_list()

    def _on_continue(self):
        cats = category_service.get_categories()
        if not cats:
            messagebox.showwarning(
                "No Categories",
                "Please add at least one category before continuing.",
            )
            return
        self.on_continue()

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for cat in category_service.get_categories():
            self.listbox.insert(tk.END, cat.name)
