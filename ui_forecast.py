#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@file ui_forecast.py
@brief Module to build and manage the revenue forecast tab in the Auto Showroom UI.
"""

import tkinter as tk
from tkinter import ttk
import random
import math
from datetime import datetime

from scrollable_tab import make_scrollable_tab


def fmt_price(amount: float) -> str:
    """
    \brief Format a numeric amount into a human-readable price string.

    Rounds to nearest integer and adds thousand separators.

    \param[in] amount Value to format.
    \return Formatted string, e.g. "1 234 руб.".
    """
    rounded = int(round(amount))
    formatted = f"{rounded:,}".replace(",", " ")
    return f"{formatted} руб."


def build_forecast_tab(parent: ttk.Frame) -> None:
    """
    \brief Construct the revenue forecast interface.

    Creates a scrollable frame with:
      - Controls to set the moving average window.
      - Table showing actual and forecasted monthly revenue for 2025.
      - Text area detailing the moving average calculations and accuracy metrics.

    \param[in] parent The parent frame where the forecast tab is placed.
    \return None
    """
    container = make_scrollable_tab(parent)
    # Grid: left controls, right upper table and lower details
    container.columnconfigure(0, weight=0)
    container.columnconfigure(1, weight=1)
    container.rowconfigure(0, weight=1)
    container.rowconfigure(1, weight=1)

    # --- Forecast parameters panel ---
    params_frame = ttk.LabelFrame(
        container,
        text='Параметры прогноза',
        padding=20
    )
    params_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nw')
    params_frame.columnconfigure(1, weight=1)

    ttk.Label(
        params_frame,
        text='Окно (месяцев):'
    ).grid(row=0, column=0, sticky='w', pady=5)
    spin_months = ttk.Spinbox(
        params_frame,
        from_=1,
        to=12,
        width=5
    )
    spin_months.set(3)
    spin_months.grid(row=0, column=1, sticky='w', pady=5, padx=5)

    compute_btn = ttk.Button(
        params_frame,
        text='Вычислить прогноз'
    )
    compute_btn.grid(row=1, column=0, columnspan=2, pady=15)

    # --- Actual + forecast table ---
    table_frame = ttk.LabelFrame(
        container,
        text='Выручка 2025 (факт + прогноз)',
        padding=10
    )
    table_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
    table_frame.columnconfigure(0, weight=1)
    table_frame.rowconfigure(0, weight=1)

    columns = ('Месяц', 'Выручка', 'Тип')
    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show='headings',
        height=12
    )
    vsb = ttk.Scrollbar(
        table_frame,
        orient='vertical',
        command=tree.yview
    )
    hsb = ttk.Scrollbar(
        table_frame,
        orient='horizontal',
        command=tree.xview
    )
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    col_widths = [100, 120, 100]
    for col, width in zip(columns, col_widths):
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='center', stretch=False)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    # --- Calculation details and accuracy metrics ---
    detail_frame = ttk.LabelFrame(
        container,
        text='Детализация и точность прогноза',
        padding=10
    )
    detail_frame.grid(row=1, column=1, padx=10, pady=(0, 10), sticky='nsew')
    detail_frame.columnconfigure(0, weight=1)
    detail_frame.rowconfigure(0, weight=1)

    txt = tk.Text(
        detail_frame,
        wrap='none',
        font=('Courier New', 10)
    )
    vsb2 = ttk.Scrollbar(
        detail_frame,
        orient='vertical',
        command=txt.yview
    )
    hsb2 = ttk.Scrollbar(
        detail_frame,
        orient='horizontal',
        command=txt.xview
    )
    txt.configure(yscrollcommand=vsb2.set, xscrollcommand=hsb2.set)

    txt.grid(row=0, column=0, sticky='nsew')
    vsb2.grid(row=0, column=1, sticky='ns')
    hsb2.grid(row=1, column=0, sticky='ew')
    txt.configure(state='disabled')

    def compute_forecast() -> None:
        """
        \brief Generate and display actual and forecast data using moving average,
               and compute accuracy metrics on actual data.

        - Generates random actual revenue for past months of 2025.
        - Computes forecast for remaining months using moving average.
        - Calculates MAE, RMSE, and MAPE for historical forecast.
        - Populates table and detail text.
        """
        now = datetime.now()
        current_month = now.month if now.year == 2025 else 6

        # Actual data
        actual_rev = [random.uniform(1e6, 5e6) for _ in range(1, current_month)]

        # Forecast using moving average
        window = int(spin_months.get())
        values = actual_rev.copy()
        details = []
        months_short = [
            'Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
            'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек'
        ]
        months_full = [
            'Январь','Февраль','Март','Апрель','Май','Июнь',
            'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'
        ]

        # Generate forecast values and detail lines
        for m in range(current_month, 13):
            window_vals = values[-window:]
            avg = sum(window_vals) / len(window_vals)
            values.append(avg)
            wnd_str = ', '.join(fmt_price(v) for v in window_vals)
            details.append(
                f"Прогноз на {months_short[m-1]}: mₜ = ({wnd_str}) / {window} = {fmt_price(avg)}\n"
            )

        # Calculate accuracy metrics on historical data if possible
        if len(actual_rev) > window:
            forecast_hist = []
            for i in range(window, len(actual_rev)):
                wnd = actual_rev[i-window:i]
                forecast_hist.append(sum(wnd) / len(wnd))
            actual_hist = actual_rev[window:]
            errors = [abs(a - f) for a, f in zip(actual_hist, forecast_hist)]
            mae = sum(errors) / len(errors)
            rmse = math.sqrt(sum((a - f)**2 for a, f in zip(actual_hist, forecast_hist)) / len(actual_hist))
            mape = sum(abs((a - f) / a) for a, f in zip(actual_hist, forecast_hist)) / len(actual_hist) * 100
        else:
            mae = rmse = mape = None

        # Populate table
        for iid in tree.get_children():
            tree.delete(iid)
        for idx, rev in enumerate(values, start=1):
            typ = 'Факт' if idx < current_month else 'Прогноз'
            tree.insert('', 'end', values=(months_full[idx-1], fmt_price(rev), typ))

        # Populate detail text
        txt.configure(state='normal')
        txt.delete('1.0', 'end')
        txt.insert('end', f"Скользящая средняя (n={window})\n\n")
        txt.insert('end', ''.join(details))
        txt.insert('end', "\nТочность прогноза (исторические данные):\n")
        if mae is not None:
            txt.insert('end', f"MAE = {fmt_price(mae)}, RMSE = {fmt_price(rmse)}, MAPE = {mape:.1f}%\n")
        else:
            txt.insert('end', "Недостаточно данных для оценки точности (меньше n значений).\n")
        txt.configure(state='disabled')

    compute_btn.configure(command=compute_forecast)
    compute_forecast()