import tkinter as tk
from tkinter import ttk, messagebox

from models.pharmacy import Pharmacy
from services.map_service import MapService

class PharmacyTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)
        self.map_service = MapService(map_widget)
        self.dependents: list = []
        self.sel: int | None = None

        frm = ttk.Frame(self)
        frm.pack(fill="x", padx=4, pady=4)
        ttk.Label(frm, text="Nazwa").grid(row=0, column=0, sticky="e")
        ttk.Label(frm, text="Miasto").grid(row=0, column=2, sticky="e")

        self.e_name = ttk.Entry(frm, width=15)
        self.e_name.grid(row=0, column=1)
        self.e_city = ttk.Entry(frm, width=15)
        self.e_city.grid(row=0, column=3)

        self.btn = ttk.Button(frm, text="Dodaj", command=self._save)
        self.btn.grid(row=0, column=4, padx=4)

        self.lb = tk.Listbox(self, height=10)
        self.lb.pack(fill="both", expand=True, padx=4)
        self.lb.bind("<<ListboxSelect>>", self._pick)

        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        self.refresh()

    def refresh(self):
        self.lb.delete(0, tk.END)
        for ph in Pharmacy.all():
            self.lb.insert(tk.END, f"{ph.name} ({ph.city})")
        for dep in self.dependents:
            if hasattr(dep, "refresh"):
                dep.refresh()

    def _save(self):
        name = self.e_name.get().strip()
        city = self.e_city.get().strip()
        if not (name and city):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.sel is None:
            ph = Pharmacy(name, city)
        else:
            ph = Pharmacy.all()[self.sel]
            if ph.marker:
                self.map_service.remove_marker(ph.marker)
            ph.update(name, city)

        ph.marker = self.map_service.add_marker(*ph.coordinates, label=ph.name)
        self.refresh()
        self._clear()

    def _pick(self, _):
        sel = self.lb.curselection()
        if not sel:
            return
        self.sel = sel[0]
        ph = Pharmacy.all()[self.sel]
        self.e_name.delete(0, tk.END)
        self.e_name.insert(0, ph.name)
        self.e_city.delete(0, tk.END)
        self.e_city.insert(0, ph.city)
        self.btn.config(text="Zapisz")

    def _delete(self):
        sel = self.lb.curselection()
        if not sel:
            return
        ph = Pharmacy.all().pop(sel[0])
        if ph.marker:
            self.map_service.remove_marker(ph.marker)
        self.refresh()
        self._clear()

    def _clear(self):
        self.e_name.delete(0, tk.END)
        self.e_city.delete(0, tk.END)
        self.btn.config(text="Dodaj")
        self.sel = None
