#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""!
@file ui_pricelist.py
@brief Module to build and manage the price list tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db
from scrollable_tab import make_scrollable_tab


def fmt_price(amount: float) -> str:
    """!
    \brief Format a numeric price into human-readable string.

    \param[in] amount The price value.
    \return Formatted string, e.g. "1 234 руб.".
    """
    value = int(round(amount))
    formatted = f"{value:,}".replace(",", " ")
    return f"{formatted} руб."


def build_pricelist_tab(parent: ttk.Frame) -> None:
    """!
    \brief Construct the price list search and management interface.

    Creates filters for category, model, price range, and displays search
    results with options to update price or publish products.

    \param[in] parent The parent frame where the price list tab should be placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    # --- Filter panel ---
    filter_frame = ttk.LabelFrame(
        container,
        text='Поиск',
        padding=20
    )
    filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    filter_frame.columnconfigure(1, weight=1)

    ttk.Label(filter_frame, text='Марка:').grid(
        row=0, column=0, sticky='e', padx=5, pady=5
    )
    categories = db.get_categories()
    cat_names = [name for _, name in categories]
    cat_map = {name: cid for cid, name in categories}
    combobox_category = ttk.Combobox(
        filter_frame,
        values=cat_names,
        state='readonly'
    )
    combobox_category.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(filter_frame, text='Модель:').grid(
        row=1, column=0, sticky='e', padx=5, pady=5
    )
    entry_model = ttk.Entry(filter_frame)
    entry_model.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(filter_frame, text='Цена от:').grid(
        row=2, column=0, sticky='e', padx=5, pady=5
    )
    entry_price_min = ttk.Entry(filter_frame)
    entry_price_min.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(filter_frame, text='до:').grid(
        row=3, column=0, sticky='e', padx=5, pady=5
    )
    entry_price_max = ttk.Entry(filter_frame)
    entry_price_max.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    def search_callback() -> None:
        """!
        \brief Perform product search and update results table.
        """
        try:
            category_id = cat_map.get(combobox_category.get(), None)
            price_min = float(entry_price_min.get()) \
                if entry_price_min.get() else None
            price_max = float(entry_price_max.get()) \
                if entry_price_max.get() else None
        except ValueError:
            messagebox.showerror('Ошибка', 'Неверный формат цены')
            return

        rows = db.search_products(
            category_id,
            entry_model.get(),
            price_min,
            price_max
        )
        _populate_results(rows)

    button_search = ttk.Button(
        filter_frame,
        text='Поиск',
        command=search_callback
    )
    button_search.grid(row=4, column=0, columnspan=2, pady=10)

    # --- Results panel ---
    results_frame = ttk.LabelFrame(
        container,
        text='Результаты',
        padding=20
    )
    results_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    results_frame.columnconfigure(0, weight=1)
    results_frame.rowconfigure(0, weight=1)

    columns = ('ID', 'Марка', 'Модель', 'Цена', 'Опубл.', 'Подерж.')
    tree = ttk.Treeview(
        results_frame,
        columns=columns,
        show='headings',
        height=12
    )
    vsb = ttk.Scrollbar(
        results_frame,
        orient='vertical',
        command=tree.yview
    )
    hsb = ttk.Scrollbar(
        results_frame,
        orient='horizontal',
        command=tree.xview
    )
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    widths = [50, 120, 200, 100, 80, 80]
    for col, width in zip(columns, widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center', stretch=False)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    def _populate_results(rows: list[tk.Event]) -> None:
        """!
        \brief Populate the treeview with search result rows.
        """
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert(
                '',
                tk.END,
                values=(
                    row['id'],
                    row['category'],
                    row['name'],
                    fmt_price(row['price']),
                    '✔' if row['published'] else '',
                    'Да' if row['used'] else 'Нет'
                )
            )

    def update_price_callback() -> None:
        """!
        \brief Open a dialog to update the selected product's price.
        """
        selection = tree.selection()
        if not selection:
            return
        product_id = tree.item(selection[0])['values'][0]

        top = tk.Toplevel(container)
        top.title('Обновить цену')
        ttk.Label(top, text='Новая цена:').pack(padx=10, pady=5)
        entry_new_price = ttk.Entry(top)
        entry_new_price.pack(padx=10, pady=5)

        def save_new_price() -> None:
            try:
                new_price = float(entry_new_price.get())
                db.update_product(new_price, product_id)
                messagebox.showinfo('Успех', 'Цена обновлена')
                top.destroy()
                search_callback()
            except ValueError:
                messagebox.showerror('Ошибка', 'Неверный формат цены')

        ttk.Button(top, text='Сохранить', command=save_new_price).pack(pady=10)

    def publish_product_callback() -> None:
        """!
        \brief Publish the selected product.
        """
        selection = tree.selection()
        if not selection:
            return
        product_id = tree.item(selection[0])['values'][0]
        db.publish_product(product_id, True)
        messagebox.showinfo('Успех', 'Опубликовано')
        search_callback()

    button_frame = ttk.Frame(results_frame)
    button_frame.grid(row=2, column=0, pady=10, sticky='e')
    ttk.Button(
        button_frame,
        text='Обновить цену',
        command=update_price_callback
    ).pack(side='left', padx=5)
    ttk.Button(
        button_frame,
        text='Опубликовать',
        command=publish_product_callback
    ).pack(side='left', padx=5)
