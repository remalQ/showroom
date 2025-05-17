#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""!
@file main.py
@brief Entry point and main window layout for the Auto Showroom application.
"""

import tkinter as tk
from tkinter import ttk

import db
from ui_clients import build_client_tab
from ui_employees import build_employee_tab
from ui_pricelist import build_pricelist_tab
from ui_sales import build_sales_tab
from ui_tradein import build_tradein_tab
from ui_products import build_product_tab
from ui_requests import build_request_tab
from ui_forecast import build_forecast_tab


# Global default window size
DEFAULT_WIDTH: int = 900  # pixels
DEFAULT_HEIGHT: int = 650  # pixels


def center_window(win: tk.Tk) -> None:
    """!
    \brief Center the given window on the screen.

    \param[in] win The tkinter window instance to center.
    """
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x_coord = (screen_width - DEFAULT_WIDTH) // 2
    y_coord = (screen_height - DEFAULT_HEIGHT) // 2
    win.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}+{x_coord}+{y_coord}")



def open_section(
    root: tk.Tk,
    title: str,
    builder: callable,
    modal: bool = True
) -> None:
    """!
    \brief Open a new child window with consistent size and style.

    \param[in] root The parent tkinter root or Toplevel.
    \param[in] title The title for the new window.
    \param[in] builder A function that builds UI elements inside the window.
    \param[in] modal If True, make the window modal.
    """
    win = tk.Toplevel(root)
    win.title(title)
    center_window(win)

    if modal:
        win.transient(root)
        win.grab_set()

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    builder(frame)


def main() -> None:
    """!
    \brief Initialize the database and create the main application window with navigation.
    """
    db.init_db()

    root = tk.Tk()
    root.title("Автосалон")
    center_window(root)

    # Setup ttk styles
    style = ttk.Style(root)
    try:
        style.theme_use("vista")
    except tk.TclError:
        style.theme_use("default")

    style.configure(
        "TFrame", background="#f7f9fa"
    )
    style.configure(
        "TLabelframe", background="#f7f9fa", font=("Segoe UI", 11, "bold")
    )
    style.configure(
        "TLabel", background="#f7f9fa", font=("Segoe UI", 10)
    )
    style.configure(
        "Heading.TLabel", font=("Segoe UI", 12, "bold")
    )
    style.configure(
        "TButton",
        font=("Segoe UI", 10, "bold"),
        padding=(8, 4),
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", "#0050b3"), ("!active", "#0078d7")],
        foreground=[("!disabled", "#4d8fe2")],
    )
    style.configure(
        "Treeview",
        font=("Segoe UI", 10),
        rowheight=26,
        background="white",
        fieldbackground="white",
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#e1e5ea",
    )
    style.map(
        "Treeview.Heading",
        background=[("active", "#d0d4da")],
    )

    # Main layout: navigation + preview
    container = ttk.Frame(root)
    container.pack(fill="both", expand=True)
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    nav = ttk.Frame(container, padding=10)
    nav.grid(row=0, column=0, sticky="ns")

    preview = ttk.Frame(container, padding=10, relief="groove")
    preview.grid(row=0, column=1, sticky="nsew")

    def clear_preview() -> None:
        """!
        \brief Clear the preview area and display a placeholder message.
        """
        for child in preview.winfo_children():
            child.destroy()

        message = ttk.Label(
            preview,
            text="Наведи на кнопку,\nчтобы увидеть предпросмотр",
            justify="center"
        )
        message.pack(expand=True)

    def show_preview(builder_func: callable) -> None:
        """!
        \brief Render a preview of the section UI without opening a new window.

        \param[in] builder_func The UI builder function to render into the preview frame.
        """
        for child in preview.winfo_children():
            child.destroy()

        subframe = ttk.Frame(preview)
        subframe.pack(fill="both", expand=True)
        builder_func(subframe)

    sections = [
        ("Клиенты", "Клиенты", build_client_tab),
        ("Сотрудники", "Сотрудники", build_employee_tab),
        ("Прайс-лист", "Прайс-лист", build_pricelist_tab),
        ("Прогноз выручки", "Прогноз", build_forecast_tab),
        ("Продажи", "Управление продажами", build_sales_tab),
        ("Trade-IN", "Trade-IN", build_tradein_tab),
        ("Товары/Каталог", "Каталог товаров", build_product_tab),
        ("Заявки", "Заявки", build_request_tab),
    ]

    for text, title, builder_func in sections:
        button = ttk.Button(
            nav,
            text=text,
            command=lambda bf=builder_func, t=title: open_section(root, t, bf)
        )
        button.pack(fill="x", pady=6)
        button.bind(
            "<Enter>", lambda e, bf=builder_func: show_preview(bf)
        )
        button.bind(
            "<Leave>", lambda e: clear_preview()
        )

    clear_preview()
    root.mainloop()


if __name__ == "__main__":
    main()