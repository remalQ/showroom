# ui_forecast.py
import tkinter as tk
from tkinter import ttk
import random
from datetime import datetime
from scrollable_tab import make_scrollable_tab

def fmt_price(amount):
    val = int(round(amount))
    s = f"{val:,}".replace(",", " ")
    return f"{s} руб."

def build_forecast_tab(parent):
    frame = make_scrollable_tab(parent)
    # две колонки: левая — контролы, правая — результат и детализация
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    # две строки: строка 0 — таблица, строка 1 — детализация
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    # --- Панель параметров ---
    ctrl = ttk.LabelFrame(frame, text="Параметры прогноза", padding=20)
    ctrl.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nw")
    ttk.Label(ctrl, text="Окно n месяцев:").grid(row=0, column=0, sticky="w", pady=5)
    spin_n = ttk.Spinbox(ctrl, from_=1, to=12, width=5)
    spin_n.set(3)
    spin_n.grid(row=0, column=1, sticky="w", pady=5, padx=5)
    btn = ttk.Button(ctrl, text="Вычислить прогноз")
    btn.grid(row=1, column=0, columnspan=2, pady=15)

    # --- Таблица факта + прогноза ---
    tbl_frame = ttk.LabelFrame(frame, text="Выручка 2025 (факт + прогноз)", padding=10)
    tbl_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    tbl_frame.columnconfigure(0, weight=1)
    tbl_frame.rowconfigure(0, weight=1)

    cols = ("Месяц","Выручка","Тип")
    tree = ttk.Treeview(tbl_frame, columns=cols, show="headings", height=12)
    vsb = ttk.Scrollbar(tbl_frame, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(tbl_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    widths = [100, 120, 100]
    for c,w in zip(cols, widths):
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="center", stretch=False)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    # --- Блок детализации расчётов ---
    det_frame = ttk.LabelFrame(frame, text="Детализация скользящей средней", padding=10)
    det_frame.grid(row=1, column=1, padx=10, pady=(0,10), sticky="nsew")
    det_frame.columnconfigure(0, weight=1)
    det_frame.rowconfigure(0, weight=1)

    txt = tk.Text(det_frame, wrap="none")
    vsb2 = ttk.Scrollbar(det_frame, orient="vertical",   command=txt.yview)
    hsb2 = ttk.Scrollbar(det_frame, orient="horizontal", command=txt.xview)
    txt.configure(yscrollcommand=vsb2.set, xscrollcommand=hsb2.set)
    txt.grid(row=0, column=0, sticky="nsew")
    vsb2.grid(row=0, column=1, sticky="ns")
    hsb2.grid(row=1, column=0, sticky="ew")
    txt.configure(state="disabled", font=("Courier New", 10))

    # --- Функция расчёта и вывода ---
    def on_compute():
        # 1) Генерируем случайную выручку для месяцев до текущего в 2025
        now = datetime.now()
        current = now.month if now.year == 2025 else 6
        actual = [random.uniform(1e6,5e6) for _ in range(1, current)]

        # 2) Строим прогноз (скользящая средняя)
        n = int(spin_n.get())
        values = actual.copy()
        details = []

        for m in range(current, 13):
            window = values[-n:]
            avg = sum(window)/len(window)
            values.append(avg)
            # Формируем строку детали
            months = ["Янв","Фев","Мар","Апр","Май","Июн","Июл","Авг","Сен","Окт","Ноя","Дек"]
            wnd_str = ", ".join(fmt_price(x) for x in window)
            details.append(f"Прогноз на {months[m-1]}: mₜ = ({wnd_str}) / {n} = {fmt_price(avg)}\n")

        # 3) Заполняем таблицу
        for iid in tree.get_children(): tree.delete(iid)
        months_full = ["Январь","Февраль","Март","Апрель","Май","Июнь",
                       "Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"]
        for idx, rev in enumerate(values, start=1):
            typ = "Факт" if idx < current else "Прогноз"
            tree.insert("", "end", values=(months_full[idx-1], fmt_price(rev), typ))

        # 4) Заполняем текст детализации
        txt.configure(state="normal")
        txt.delete("1.0", "end")
        txt.insert("end", "Скользящая средняя (n=%d)\n\n" % n)
        txt.insert("end", "".join(details))
        txt.configure(state="disabled")

    btn.configure(command=on_compute)
    # первый прогон
    on_compute()
