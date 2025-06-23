import tkinter as tk
from tkinter import ttk, messagebox

from models.employee import Employee
from models.pharmacy import Pharmacy
from services.map_service import MapService

class EmployeeTab(ttk.Frame):
    def __init__(self, parent, map_widget, overview_tab):
        super().__init__(parent)
        self.map_service = MapService(map_widget)
        self.overview_tab = overview_tab
        self.selected_index: int | None = None

        form = ttk.Frame(self)
        form.pack(fill="x", padx=4, pady=4)
        for col, text in enumerate(("Imię", "Nazwisko", "Miasto", "Apteka")):
            ttk.Label(form, text=text).grid(row=0, column=col * 2, sticky="e")

        self.entry_first = ttk.Entry(form, width=12)
        self.entry_last  = ttk.Entry(form, width=12)
        self.entry_city  = ttk.Entry(form, width=12)
        self.combo_phar = ttk.Combobox(form, state="readonly", width=14)

        self.entry_first.grid(row=0, column=1)
        self.entry_last.grid(row=0, column=3)
        self.entry_city.grid(row=0, column=5)
        self.combo_phar.grid(row=0, column=7)

        self.btn_add_save = ttk.Button(form, text="Dodaj", command=self._save)
        self.btn_add_save.grid(row=0, column=8, padx=2)

        self.listbox = tk.Listbox(self, height=10)
        self.listbox.pack(fill="both", expand=True, padx=4)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        bar = ttk.Frame(self)
        bar.pack(fill="x", padx=4, pady=3)
        ttk.Button(bar, text="Usuń",    command=self._delete).pack(side="left")
        ttk.Button(bar, text="Wyczyść", command=self._clear).pack(side="right")

        self.refresh()

    def refresh(self):
        self.combo_phar["values"] = [p.name for p in Pharmacy.all()]
        if self.combo_phar.get() not in self.combo_phar["values"]:
            self.combo_phar.set("")
        self.listbox.delete(0, tk.END)
        for emp in Employee.all():
            self.listbox.insert(tk.END, emp.full_name())

    def _save(self):
        first = self.entry_first.get().strip()
        last  = self.entry_last.get().strip()
        city  = self.entry_city.get().strip()
        phar  = self.combo_phar.get().strip()

        if not all([first, last, city, phar]):
            messagebox.showwarning("Błąd", "Wszystkie pola są wymagane")
            return

        if self.selected_index is None:
            emp = Employee(first, last, city, phar)
        else:
            emp = Employee.all()[self.selected_index]
            if emp.marker:
                self.map_service.remove_marker(emp.marker)
            emp.update(first, last, city, phar)

        emp.marker = self.map_service.add_marker(*emp.coordinates, label=emp.full_name())
        self.refresh()
        self.overview_tab.refresh()
        self._clear()

    def _on_select(self, _event):
        sel = self.listbox.curselection()
        if not sel:
            return
        self.selected_index = sel[0]
        emp = Employee.all()[self.selected_index]
        self.entry_first.delete(0, tk.END); self.entry_first.insert(0, emp.first_name)
        self.entry_last.delete(0, tk.END);  self.entry_last.insert(0, emp.last_name)
        self.entry_city.delete(0, tk.END);  self.entry_city.insert(0, emp.city)
        self.combo_phar.set(emp.assigned_pharmacy)
        self.btn_add_save.config(text="Zapisz")

    def _delete(self):
        sel = self.listbox.curselection()
        if not sel:
            return
        emp = Employee.all().pop(sel[0])
        if emp.marker:
            self.map_service.remove_marker(emp.marker)
        self.refresh()
        self.overview_tab.refresh()
        self._clear()

    def _clear(self):
        for entry in (self.entry_first, self.entry_last, self.entry_city):
            entry.delete(0, tk.END)
        self.combo_phar.set("")
        self.btn_add_save.config(text="Dodaj")
        self.selected_index = None