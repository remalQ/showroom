# autosalon_gui.py
import tkinter as tk
from tkinter import ttk
from db import init_db

class AutoSalonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Автосалон")
        self.geometry("900x600")
        self.configure(bg='#f0f0f0')

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)

        from ui_clients import build_client_tab
        from ui_employees import build_employee_tab
        from ui_requests import build_request_tab

        self.client_tab = ttk.Frame(self.tabs)
        self.employee_tab = ttk.Frame(self.tabs)
        self.request_tab = ttk.Frame(self.tabs)

        self.tabs.add(self.client_tab, text="Клиенты")
        self.tabs.add(self.employee_tab, text="Сотрудники")
        self.tabs.add(self.request_tab, text="Заявки")

        build_client_tab(self.client_tab)
        build_employee_tab(self.employee_tab)
        build_request_tab(self.request_tab)
