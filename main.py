import tkinter as tk
from tkinter import ttk
import tkintermapview

from tabs.pharmacies_tab     import pharmacies_tab
from tabs.customers_tab    import customers_tab
from tabs.emploies_tab  import emploies_tab
from tabs.overview_tab   import overview_tab


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
    tab_wash = PharmacyTab(notebook, map_widget)
    tab_cli  = CustomersTab(notebook,  map_widget, tab_over)
    tab_emp  = EmployeeTab(notebook, map_widget, tab_over)

    tab_wash.dependents = [tab_cli, tab_emp, tab_over]

    notebook.add(tab_wash, text="Apteki")
    notebook.add(tab_cli,  text="Klienci")
    notebook.add(tab_emp,  text="Pracownicy")
    notebook.add(tab_over, text="Przegląd")

    root.mainloop()


if _name_ == "_main_":
    main()