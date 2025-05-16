#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_tradein.py
@brief Module to build and manage the Trade-IN tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import db
from scrollable_tab import make_scrollable_tab


def build_tradein_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the Trade-IN interface.

    Creates a scrollable form for executing vehicle trade-ins, collecting
    new product selection, old vehicle details, client and employee IDs,
    and price difference.

    \param[in] parent The parent frame where the Trade-IN tab is placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    container.columnconfigure(0, weight=1)

    tradein_frame = ttk.LabelFrame(
        container,
        text='Trade-IN',
        padding=20
    )
    tradein_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    tradein_frame.columnconfigure(1, weight=1)

    # --- Новый автомобиль ---
    ttk.Label(
        tradein_frame,
        text='Новый (ID:название):'
    ).grid(row=0, column=0, sticky='e', padx=5, pady=5)

    new_list = [f"{row['id']}:{row['name']}" for row in db.get_new_products()]
    new_product_combo = ttk.Combobox(
        tradein_frame,
        values=new_list,
        state='readonly'
    )
    new_product_combo.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    # --- Старые детали ---
    ttk.Label(
        tradein_frame,
        text='Старое (описание):'
    ).grid(row=1, column=0, sticky='e', padx=5, pady=5)
    old_details_entry = ttk.Entry(tradein_frame)
    old_details_entry.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    # --- Клиент и сотрудник ---
    ttk.Label(
        tradein_frame,
        text='Клиент ID:'
    ).grid(row=2, column=0, sticky='e', padx=5, pady=5)
    client_id_entry = ttk.Entry(tradein_frame)
    client_id_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(
        tradein_frame,
        text='Сотрудник ID:'
    ).grid(row=3, column=0, sticky='e', padx=5, pady=5)
    employee_id_entry = ttk.Entry(tradein_frame)
    employee_id_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

    # --- Разница в цене ---
    ttk.Label(
        tradein_frame,
        text='Разница в цене:'
    ).grid(row=4, column=0, sticky='e', padx=5, pady=5)
    price_diff_entry = ttk.Entry(tradein_frame)
    price_diff_entry.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

    def submit_tradein() -> None:
        """
        \brief Handle the Trade-IN submission.

        Validates and converts form inputs, stores the record in the database,
        and notifies the user of success or error.
        """
        try:
            new_product_id = int(new_product_combo.get().split(':')[0])
            client_id = int(client_id_entry.get())
            employee_id = int(employee_id_entry.get())
            price_diff = float(price_diff_entry.get())

            db.add_tradein(
                new_product_id,
                old_details_entry.get().strip(),
                client_id,
                employee_id,
                datetime.now().isoformat(),
                price_diff
            )
            messagebox.showinfo('Успех', 'Trade-IN оформлен')
        except Exception as error:
            messagebox.showerror('Ошибка', str(error))

    submit_button = ttk.Button(
        tradein_frame,
        text='Оформить',
        command=submit_tradein
    )
    submit_button.grid(row=5, column=0, columnspan=2, pady=10)