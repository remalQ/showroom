# main.py
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import db

from ui_clients   import build_client_tab
from ui_employees import build_employee_tab
from ui_pricelist import build_pricelist_tab
from ui_sales     import build_sales_tab
from ui_tradein   import build_tradein_tab
from ui_products  import build_product_tab
from ui_requests  import build_request_tab

def center_window(win, w, h):
    sw, sh = win.winfo_screenwidth(), win.winfo_screenheight()
    x, y = (sw - w)//2, (sh - h)//2
    win.geometry(f"{w}x{h}+{x}+{y}")

def open_section(root, title, builder, modal=True):
    win = tk.Toplevel(root)
    win.title(title)
    center_window(win, 900, 650)
    if modal:
        win.transient(root); win.grab_set()
    container = ttk.Frame(win, padding=20)
    container.pack(fill="both", expand=True)
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    builder(container)

def main():
    db.init_db()

    root = tk.Tk()
    root.title("Автосалон")
    center_window(root, 300, 400)

    # --------- СТИЛИ ---------
    style = ttk.Style(root)
    style.theme_use('clam')
    style.configure('TFrame',    background='#f0f0f0')
    style.configure('TLabel',    background='#f0f0f0', font=('Segoe UI',10))
    style.configure('Heading.TLabel', font=('Segoe UI',12,'bold'))
    style.configure('TButton',   font=('Segoe UI',10), padding=6)
    style.configure('TLabelframe', background='#f0f0f0', font=('Segoe UI',10,'bold'))
    style.configure('Treeview',  font=('Segoe UI',10), rowheight=24)
    style.configure('Treeview.Heading', font=('Segoe UI',11,'bold'))

    # --------- Навигация ---------
    nav = ttk.Frame(root, padding=10)
    nav.pack(side="left", fill="y")
    buttons = [
        ("Клиенты",           lambda: open_section(root,"Клиенты",           build_client_tab)),
        ("Сотрудники",        lambda: open_section(root,"Сотрудники",        build_employee_tab)),
        ("Прайс-лист",        lambda: open_section(root,"Прайс-лист",        build_pricelist_tab)),
        ("Продажи",           lambda: open_section(root,"Управление продажами", build_sales_tab)),
        ("Trade-IN",          lambda: open_section(root,"Trade-IN",          build_tradein_tab)),
        ("Товары/Каталог",    lambda: open_section(root,"Каталог товаров",   build_product_tab)),
        ("Заявки",            lambda: open_section(root,"Заявки",            build_request_tab)),
    ]
    for txt, cmd in buttons:
        ttk.Button(nav, text=txt, command=cmd).pack(fill="x", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
