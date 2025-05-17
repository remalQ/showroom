#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""!
@file ui_products.py
@brief Module to build and manage the products and categories tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db
from scrollable_tab import make_scrollable_tab


def fmt_price(amount: float) -> str:
    """!
    \brief Format a numeric price into a human-readable string.

    Rounds to nearest integer and adds thousand separators.

    \param[in] amount Price value as float.
    \return Formatted price string, e.g. "1 234 руб.".
    """
    rounded = int(round(amount))
    formatted = f"{rounded:,}".replace(",", " ")
    return f"{formatted} руб."


def build_product_tab(parent: ttk.Frame) -> None:
    """!
    \brief Construct the products and categories management interface.

    Creates a scrollable frame with:
      - Category addition form.
      - Product addition form.
      - Table listing existing products.

    \param[in] parent The parent frame where the products tab is placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    # Configure grid: left column for forms, right for table
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=0)
    container.rowconfigure(1, weight=1)

    # --- Category management ---
    category_frame = ttk.LabelFrame(
        container,
        text='Категории',
        padding=20
    )
    category_frame.grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky='nsew'
    )
    category_frame.columnconfigure(1, weight=1)

    ttk.Label(
        category_frame,
        text='Название категории:'
    ).grid(row=0, column=0, sticky='e', padx=5, pady=5)
    category_entry = ttk.Entry(category_frame)
    category_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    def add_category_callback() -> None:
        """!
        \brief Handle adding a new product category.
        """
        name = category_entry.get().strip()
        if not name:
            messagebox.showerror('Ошибка', 'Введите название категории')
            return
        db.add_category(name)
        messagebox.showinfo('Успех', 'Категория добавлена')
        category_entry.delete(0, tk.END)
        _refresh()

    ttk.Button(
        category_frame,
        text='Добавить категорию',
        command=add_category_callback
    ).grid(row=1, column=0, columnspan=2, pady=10)

    # --- Product management ---
    product_frame = ttk.LabelFrame(
        container,
        text='Товары',
        padding=20
    )
    product_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
    product_frame.columnconfigure(1, weight=1)

    ttk.Label(
        product_frame,
        text='Категория:'
    ).grid(row=0, column=0, sticky='e', padx=5, pady=5)
    category_combo = ttk.Combobox(
        product_frame,
        state='readonly'
    )
    category_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        product_frame,
        text='Название:'
    ).grid(row=1, column=0, sticky='e', padx=5, pady=5)
    name_entry = ttk.Entry(product_frame)
    name_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        product_frame,
        text='Цена:'
    ).grid(row=2, column=0, sticky='e', padx=5, pady=5)
    price_entry = ttk.Entry(product_frame)
    price_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    used_var = tk.BooleanVar()
    ttk.Checkbutton(
        product_frame,
        text='Подержанный',
        variable=used_var
    ).grid(row=3, column=0, columnspan=2, pady=5)

    def add_product_callback() -> None:
        """!
        \brief Handle adding a new product to the database.
        """
        category_name = category_combo.get()
        product_name = name_entry.get().strip()
        price_text = price_entry.get().strip()
        used = used_var.get()

        if not (category_name and product_name and price_text):
            messagebox.showerror('Ошибка', 'Все поля обязательны')
            return
        try:
            price_val = float(price_text)
        except ValueError:
            messagebox.showerror('Ошибка', 'Неверный формат цены')
            return
        db.add_product(
            product_name,
            category_map[category_name],
            price_val,
            used
        )
        messagebox.showinfo('Успех', 'Товар добавлен')
        name_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        category_combo.set('')
        used_var.set(False)
        _refresh()

    ttk.Button(
        product_frame,
        text='Добавить товар',
        command=add_product_callback
    ).grid(row=4, column=0, columnspan=2, pady=10)

    # --- Products list ---
    list_frame = ttk.LabelFrame(
        container,
        text='Список товаров',
        padding=20
    )
    list_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    columns = ('ID', 'Категория', 'Название', 'Цена', 'Подерж.', 'Опубл.')
    tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show='headings',
        height=12
    )
    vsb = ttk.Scrollbar(
        list_frame,
        orient='vertical',
        command=tree.yview
    )
    hsb = ttk.Scrollbar(
        list_frame,
        orient='horizontal',
        command=tree.xview
    )
    tree.configure(
        yscrollcommand=vsb.set,
        xscrollcommand=hsb.set
    )

    col_widths = [50, 120, 200, 100, 80, 80]
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center', stretch=False)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    def _refresh() -> None:
        """!
        \brief Refresh categories and product list from the database.
        """
        nonlocal category_map
        # Update categories
        categories = db.get_categories()
        names = [row['name'] for row in categories]
        category_map = {row['name']: row['id'] for row in categories}
        category_combo['values'] = names

        # Update product table
        for item in tree.get_children():
            tree.delete(item)
        for row in db.search_products():
            tree.insert(
                '',
                tk.END,
                values=(
                    row['id'],
                    row['category'],
                    row['name'],
                    fmt_price(row['price']),
                    'Да' if row['used'] else 'Нет',
                    'Да' if row['published'] else 'Нет'
                )
            )

    # Initialize map and load data
    category_map: dict[str, int] = {}
    _refresh()
