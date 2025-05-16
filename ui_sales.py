#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_sales.py
@brief Module to build and manage the sales tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import db
from scrollable_tab import make_scrollable_tab


def build_sales_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the interface for selling new and used vehicles.

    Creates a scrollable frame with separate sections for processing sales
    of used and new products, including inputs for product selection,
    client and employee IDs, and sale price.

    \param[in] parent The parent frame where the sales tab will be embedded.
    \return None
    """
    container = make_scrollable_tab(parent)
    # Configure two equal-width columns
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)

    # --- Used product sale section ---
    used_frame = ttk.LabelFrame(
        container,
        text='Продажа подержанного',
        padding=20
    )
    used_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    used_frame.columnconfigure(1, weight=1)

    ttk.Label(
        used_frame,
        text='Выбрать авто:'
    ).grid(row=0, column=0, sticky='e', padx=5, pady=5)
    used_list = [f"{row['id']}:{row['name']}" for row in db.get_used_products()]
    combobox_used = ttk.Combobox(
        used_frame,
        values=used_list,
        state='readonly'
    )
    combobox_used.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        used_frame,
        text='Клиент ID:'
    ).grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_client_used = ttk.Entry(used_frame)
    entry_client_used.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        used_frame,
        text='Сотрудник ID:'
    ).grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_employee_used = ttk.Entry(used_frame)
    entry_employee_used.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        used_frame,
        text='Цена:'
    ).grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_price_used = ttk.Entry(used_frame)
    entry_price_used.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    def sell_used_callback() -> None:
        """
        \brief Process the sale of a used product.

        Validates input, writes sale record to the database,
        and notifies the user.
        """
        try:
            product_id = int(combobox_used.get().split(':')[0])
            client_id = int(entry_client_used.get())
            employee_id = int(entry_employee_used.get())
            price = float(entry_price_used.get())
            db.add_sale(
                product_id,
                client_id,
                employee_id,
                datetime.now().isoformat(),
                price,
                'подержанный'
            )
            messagebox.showinfo('Успех', 'Товар продан')
            # Clear inputs
            combobox_used.set('')
            entry_client_used.delete(0, tk.END)
            entry_employee_used.delete(0, tk.END)
            entry_price_used.delete(0, tk.END)
        except Exception as err:
            messagebox.showerror('Ошибка', str(err))

    ttk.Button(
        used_frame,
        text='Продать',
        command=sell_used_callback
    ).grid(row=4, column=0, columnspan=2, pady=10)

    # --- New product sale section ---
    new_frame = ttk.LabelFrame(
        container,
        text='Продажа нового',
        padding=20
    )
    new_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    new_frame.columnconfigure(1, weight=1)

    new_list = [f"{row['id']}:{row['name']}" for row in db.get_new_products()]
    combobox_new = ttk.Combobox(
        new_frame,
        values=new_list,
        state='readonly'
    )
    combobox_new.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        new_frame,
        text='Клиент ID:'
    ).grid(row=1, column=0, sticky='e', padx=5, pady=5)
    entry_client_new = ttk.Entry(new_frame)
    entry_client_new.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        new_frame,
        text='Сотрудник ID:'
    ).grid(row=2, column=0, sticky='e', padx=5, pady=5)
    entry_employee_new = ttk.Entry(new_frame)
    entry_employee_new.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        new_frame,
        text='Цена:'
    ).grid(row=3, column=0, sticky='e', padx=5, pady=5)
    entry_price_new = ttk.Entry(new_frame)
    entry_price_new.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    def sell_new_callback() -> None:
        """
        \brief Process the sale of a new product.

        Validates input, writes sale record to the database,
        and notifies the user.
        """
        try:
            product_id = int(combobox_new.get().split(':')[0])
            client_id = int(entry_client_new.get())
            employee_id = int(entry_employee_new.get())
            price = float(entry_price_new.get())
            db.add_sale(
                product_id,
                client_id,
                employee_id,
                datetime.now().isoformat(),
                price,
                'новый'
            )
            messagebox.showinfo('Успех', 'Товар продан')
            # Clear inputs
            combobox_new.set('')
            entry_client_new.delete(0, tk.END)
            entry_employee_new.delete(0, tk.END)
            entry_price_new.delete(0, tk.END)
        except Exception as err:
            messagebox.showerror('Ошибка', str(err))

    ttk.Button(
        new_frame,
        text='Продать',
        command=sell_new_callback
    ).grid(row=4, column=0, columnspan=2, pady=10)