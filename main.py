import tkinter as tk
from tkinter import ttk
import tkintermapview

from tabs.pharmacies_tab import PharmacyTab
from tabs.customers_tab import CustomersTab
from tabs.emploies_tab import EmployeeTab
from tabs.overview_tab import OverviewTab

def main() -> None:
    root = tk.Tk()
    root.title("System zarządzania aptekami")
    root.geometry("1400x850")
    root.minsize(1100, 700)

    map_widget = tkintermapview.TkinterMapView(root, width=1400, height=500)
    map_widget.pack(fill="x")
    map_widget.set_position(52.2297, 21.0122)
    map_widget.set_zoom(6)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    tab_over = OverviewTab(notebook, map_widget)
    tab_phar = PharmacyTab(notebook, map_widget)
    tab_cust = CustomersTab(notebook, map_widget, tab_over)
    tab_emp  = EmployeeTab(notebook, map_widget, tab_over)

    tab_phar.dependents = [tab_cust, tab_emp, tab_over]

    notebook.add(tab_phar, text="Apteki")
    notebook.add(tab_cust, text="Klienci")
    notebook.add(tab_emp, text="Pracownicy")
    notebook.add(tab_over, text="Przegląd")

    root.mainloop()

if __name__ == "__main__":
    main()