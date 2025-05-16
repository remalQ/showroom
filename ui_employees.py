#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_employees.py
@brief Module to build and manage the Employees tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk, messagebox

import db
from scrollable_tab import make_scrollable_tab


def build_employee_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the employee management interface.

    Builds a scrollable frame containing a form to add new employees
    and a table listing existing employees.

    \param[in] parent The parent frame where the employee tab is placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)

    # --- Form to add a new employee ---
    form_frame = ttk.LabelFrame(
        container,
        text='Добавление сотрудника',
        padding=20
    )
    form_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
    form_frame.columnconfigure(1, weight=1)

    ttk.Label(form_frame, text='Имя:').grid(
        row=0, column=0, sticky='e', padx=5, pady=5
    )
    entry_name = ttk.Entry(form_frame)
    entry_name.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

    ttk.Label(form_frame, text='Отдел:').grid(
        row=1, column=0, sticky='e', padx=5, pady=5
    )
    combobox_dept = ttk.Combobox(
        form_frame,
        values=['продаж', 'маркетинг'],
        state='readonly'
    )
    combobox_dept.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

    def add_employee_callback() -> None:
        """
        \brief Handle adding a new employee via the form inputs.

        Validates input fields, inserts a new employee into the database,
        and refreshes the employee list.
        """
        name = entry_name.get().strip()
        department = combobox_dept.get()

        if not name or not department:
            messagebox.showerror('Ошибка', 'Заполните все поля')
            return

        db.add_employee(name, department)
        _refresh_employee_list()

        entry_name.delete(0, tk.END)
        combobox_dept.set('')

    add_button = ttk.Button(
        form_frame,
        text='Добавить',
        command=add_employee_callback
    )
    add_button.grid(row=2, column=0, columnspan=2, pady=10)

    # --- Table listing existing employees ---
    list_frame = ttk.LabelFrame(
        container,
        text='Список сотрудников',
        padding=10
    )
    list_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    columns = ('ID', 'Имя', 'Отдел')
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

    column_widths = [50, 200, 150]
    for col, width in zip(columns, column_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center', stretch=False)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    def _refresh_employee_list() -> None:
        """
        \brief Reload and display all employees in the treeview.
        """
        for item in tree.get_children():
            tree.delete(item)

        for row in db.get_employees():
            tree.insert(
                '',
                tk.END,
                values=(row['id'], row['name'], row['department'])
            )

    _refresh_employee_list()