#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_requests.py
@brief Module to build and manage the service requests tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import db
from scrollable_tab import make_scrollable_tab


def build_request_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the service request management interface.

    Creates a scrollable frame containing a form to add new requests
    and a table listing existing requests.

    \param[in] parent The parent frame where the request tab is placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    # Configure two columns: form (fixed) and list (expandable)
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    # Single row expandable for the list
    container.rowconfigure(0, weight=1)

    # --- Request form ---
    form_frame = ttk.LabelFrame(
        container,
        text='Добавление заявки',
        padding=20
    )
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    form_frame.columnconfigure(1, weight=1)

    ttk.Label(form_frame, text='Клиент:').grid(
        row=0, column=0, sticky='e', padx=5, pady=5
    )
    combo_client = ttk.Combobox(
        form_frame,
        state='readonly'
    )
    combo_client.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Сотрудник:').grid(
        row=1, column=0, sticky='e', padx=5, pady=5
    )
    combo_employee = ttk.Combobox(
        form_frame,
        state='readonly'
    )
    combo_employee.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Услуга:').grid(
        row=2, column=0, sticky='e', padx=5, pady=5
    )
    entry_service = ttk.Entry(form_frame)
    entry_service.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Дата (ГГГГ-ММ-ДД):').grid(
        row=3, column=0, sticky='e', padx=5, pady=5
    )
    entry_date = ttk.Entry(form_frame)
    entry_date.grid(row=3, column=1, sticky='ew', padx=5, pady=5)
    # Pre-fill with today's date
    entry_date.insert(0, datetime.now().date().isoformat())

    ttk.Label(form_frame, text='Статус:').grid(
        row=4, column=0, sticky='e', padx=5, pady=5
    )
    entry_status = ttk.Entry(form_frame)
    entry_status.grid(row=4, column=1, sticky='ew', padx=5, pady=5)

    def add_request_callback() -> None:
        """
        \brief Handle adding a new service request.

        Validates form fields, inserts a new request into the database,
        and refreshes the requests list.
        """
        try:
            client_id = int(combo_client.get().split(':')[0])
            employee_id = int(combo_employee.get().split(':')[0])
            service = entry_service.get().strip()
            date_str = entry_date.get().strip()
            status = entry_status.get().strip()

            if not (service and date_str and status):
                raise ValueError('Все поля обязательны')
            # Validate date format
            datetime.fromisoformat(date_str)

            db.add_request(
                client_id,
                employee_id,
                service,
                date_str,
                status
            )
            messagebox.showinfo('Успех', 'Заявка добавлена')

            entry_service.delete(0, tk.END)
            entry_status.delete(0, tk.END)
            _refresh()
        except Exception as err:
            messagebox.showerror('Ошибка', str(err))

    ttk.Button(
        form_frame,
        text='Добавить заявку',
        command=add_request_callback
    ).grid(row=5, column=0, columnspan=2, pady=15)

    # --- Requests list ---
    list_frame = ttk.LabelFrame(
        container,
        text='Список заявок',
        padding=20
    )
    list_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    columns = ('ID', 'Клиент', 'Сотрудник', 'Услуга', 'Дата', 'Статус')
    tree = ttk.Treeview(
        list_frame,
        columns=columns,
        show='headings',
        height=12
    )
    vsb = ttk.Scrollbar(list_frame, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(list_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    col_widths = [50, 120, 120, 180, 100, 100]
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center', stretch=False)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    def _refresh() -> None:
        """
        \brief Refresh client/employee combos and the requests treeview.
        """
        # Load clients and employees
        clients = [f"{r['id']}:{r['name']}" for r in db.get_clients()]
        employees = [f"{r['id']}:{r['name']}" for r in db.get_employees()]
        combo_client['values'] = clients
        combo_employee['values'] = employees

        # Populate treeview
        for item in tree.get_children():
            tree.delete(item)
        for req in db.get_requests():
            tree.insert(
                '',
                tk.END,
                values=(
                    req['id'],
                    req['client_id'],
                    req['employee_id'],
                    req['service'],
                    req['date'],
                    req['status']
                )
            )

    # Initial load
    _refresh()