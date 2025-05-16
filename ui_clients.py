#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_clients.py
@brief Module to build and manage the client tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db
from scrollable_tab import make_scrollable_tab


def build_client_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the client management interface.

    This function creates a scrollable frame containing a form to add new clients
    and a table listing existing clients.

    \param[in] parent The parent frame where the client tab should be placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    # --- Form to add a new client ---
    form_frame = ttk.LabelFrame(
        container,
        text='Добавление клиента',
        padding=20
    )
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    form_frame.columnconfigure(1, weight=1)

    ttk.Label(form_frame, text='Имя:').grid(
        row=0, column=0, sticky='e', padx=5, pady=5
    )
    entry_name = ttk.Entry(form_frame)
    entry_name.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Телефон:').grid(
        row=1, column=0, sticky='e', padx=5, pady=5
    )
    entry_phone = ttk.Entry(form_frame)
    entry_phone.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Тип:').grid(
        row=2, column=0, sticky='e', padx=5, pady=5
    )
    combobox_type = ttk.Combobox(
        form_frame,
        values=['гость', 'покупатель', 'постоянный клиент'],
        state='readonly'
    )
    combobox_type.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    def add_client_callback() -> None:
        """
        \brief Handle adding a new client via the form inputs.

        Validates input fields, inserts a new client into the database,
        and refreshes the client list.
        """
        name = entry_name.get().strip()
        phone = entry_phone.get().strip()
        client_type = combobox_type.get()

        if not name or not client_type:
            messagebox.showerror('Ошибка', 'Имя и тип обязательны')
            return

        db.add_client(name, phone, client_type)
        _refresh_client_list()

        entry_name.delete(0, tk.END)
        entry_phone.delete(0, tk.END)
        combobox_type.set('')

    add_button = ttk.Button(
        form_frame,
        text='Добавить',
        command=add_client_callback
    )
    add_button.grid(row=3, column=0, columnspan=2, pady=10)

    # --- Table listing existing clients ---
    list_frame = ttk.LabelFrame(
        container,
        text='Список клиентов',
        padding=10
    )
    list_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    columns = ('ID', 'Имя', 'Тип')
    tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show='headings',
        height=12
    )
    scrollbar_v = ttk.Scrollbar(
        list_frame,
        orient='vertical',
        command=tree.yview
    )
    scrollbar_h = ttk.Scrollbar(
        list_frame,
        orient='horizontal',
        command=tree.xview
    )
    tree.configure(
        yscrollcommand=scrollbar_v.set,
        xscrollcommand=scrollbar_h.set
    )

    column_widths = [50, 200, 150]
    for col, width in zip(columns, column_widths):
        tree.heading(col, text=col)
        tree.column(
            col,
            width=width,
            anchor='center',
            stretch=False
        )

    tree.grid(row=0, column=0, sticky='nsew')
    scrollbar_v.grid(row=0, column=1, sticky='ns')
    scrollbar_h.grid(row=1, column=0, sticky='ew')

    def _refresh_client_list() -> None:
        """
        \brief Reload and display all clients in the treeview.
        """
        for item in tree.get_children():
            tree.delete(item)

        for row in db.get_clients():
            tree.insert(
                '',
                tk.END,
                values=(row['id'], row['name'], row['type'])
            )

    _refresh_client_list()