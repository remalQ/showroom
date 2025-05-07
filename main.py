import tkinter as tk
from tkinter import ttk
import db
from ui_clients import build_client_tab
from ui_employees import build_employee_tab
from ui_requests import build_request_tab
from ui_products import build_product_tab

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')
def main():
    db.init_db()

    root = tk.Tk()
    root.title("Автосалон")
    center_window(root, 900, 600)

    style = ttk.Style()
    style.theme_use("clam")  # или "default", "vista", "alt"

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Вкладки
    tabs = {}
    for name in ["Клиенты", "Сотрудники", "Заявки", "Товары"]:
        tabs[name] = ttk.Frame(notebook)
        notebook.add(tabs[name], text=name)

    # Подключение интерфейсов
    build_client_tab(tabs["Клиенты"])
    build_employee_tab(tabs["Сотрудники"])
    build_request_tab(tabs["Заявки"])
    build_product_tab(tabs["Товары"])

    root.mainloop()

if __name__ == "__main__":
    main()
