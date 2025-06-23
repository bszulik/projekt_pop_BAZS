import tkinter as tk
from tkinter import ttk

from models.pharmacy import Pharmacy
from models.customer import Customer
from models.employee import Employee

class OverviewTab(ttk.Frame):
    def __init__(self, parent, map_widget):
        super().__init__(parent)
        self.map_widget = map_widget

        self.tree = ttk.Treeview(self, columns=("type", "name"), show="tree headings")
        self.tree.heading("#0",   text="Obiekt")
        self.tree.heading("type", text="Typ")
        self.tree.heading("name", text="Nazwa / Imię")
        self.tree.pack(fill="both", expand=True)

        self.tree.bind("<Double-1>", self._jump)
        ttk.Button(self, text="Odśwież", command=self.refresh).pack(pady=4)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for ph in Pharmacy.all():
            pid = self.tree.insert("", "end", text=f"{ph.name} ({ph.city})",
                                   values=("Apteka", ph.name))
            cid = self.tree.insert(pid, "end", text="Klienci")
            for cust in Customer.all():
                if cust.assigned_pharmacy == ph.name:
                    self.tree.insert(cid, "end", text="",
                                     values=("Klient", cust.full_name()))
            eid = self.tree.insert(pid, "end", text="Pracownicy")
            for emp in Employee.all():
                if emp.assigned_pharmacy == ph.name:
                    self.tree.insert(eid, "end", text="",
                                     values=("Pracownik", emp.full_name()))

    def _jump(self, _event):
        item = self.tree.focus()
        if not item:
            return
        typ, name = self.tree.item(item, "values")
        if typ == "Apteka":
            ph = next(p for p in Pharmacy.all() if p.name == name)
            self._center_map(*ph.coordinates, zoom=10)
        elif typ == "Klient":
            cust = next(c for c in Customer.all() if c.full_name() == name)
            self._center_map(*cust.coordinates, zoom=12)
        elif typ == "Pracownik":
            emp = next(e for e in Employee.all() if e.full_name() == name)
            self._center_map(*emp.coordinates, zoom=12)

    def _center_map(self, lat: float, lon: float, zoom: int):
        self.map_widget.set_position(lat, lon)
        self.map_widget.set_zoom(zoom)