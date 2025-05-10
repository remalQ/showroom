# ui_requests.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import db
from scrollable_tab import make_scrollable_tab

def build_request_tab(parent):
    frame = make_scrollable_tab(parent)
    # две колонки: левая — форма, правая — список (растягивается)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    # одну строку делаем растягивающейся, чтобы список мог занять всё
    frame.rowconfigure(0, weight=1)

    # ——— Форма добавления заявки ———
    form = ttk.LabelFrame(frame, text="Добавление заявки", padding=20)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Клиент:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    cb_client = ttk.Combobox(form, state="readonly")
    cb_client.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Сотрудник:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    cb_emp = ttk.Combobox(form, state="readonly")
    cb_emp.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Услуга:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ent_serv = ttk.Entry(form)
    ent_serv.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Дата (ГГГГ-ММ-ДД):").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    ent_date = ttk.Entry(form)
    ent_date.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
    ent_date.insert(0, datetime.now().date().isoformat())

    ttk.Label(form, text="Статус:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
    ent_status = ttk.Entry(form)
    ent_status.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

    def add_request():
        try:
            cid = int(cb_client.get().split(":")[0])
            eid = int(cb_emp.get().split(":")[0])
            svc = ent_serv.get().strip()
            dt  = ent_date.get().strip()
            st  = ent_status.get().strip()
            if not (svc and dt and st):
                raise ValueError("Все поля обязательны")
            datetime.fromisoformat(dt)  # валидация
            db.add_request(cid, eid, svc, dt, st)
            messagebox.showinfo("ОК", "Заявка добавлена")
            ent_serv.delete(0, "end")
            ent_status.delete(0, "end")
            refresh()
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))

    ttk.Button(form, text="Добавить заявку", command=add_request)\
        .grid(row=5, column=0, columnspan=2, pady=15)

    # ——— Список заявок ———
    list_frame = ttk.LabelFrame(frame, text="Список заявок", padding=20)
    list_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    cols = ("ID", "Клиент", "Сотрудник", "Услуга", "Дата", "Статус")
    # высота 12 строк
    tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
    vsb = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # фиксируем ширины колонок
    widths = [50, 120, 120, 180, 100, 100]
    for c, w in zip(cols, widths):
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="center", stretch=False)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    def refresh():
        # обновляем combobox’ы
        clients   = [f"{r['id']}:{r['name']}" for r in db.get_clients()]
        employees = [f"{r['id']}:{r['name']}" for r in db.get_employees()]
        cb_client['values'] = clients
        cb_emp   ['values'] = employees

        # обновляем Treeview
        for iid in tree.get_children():
            tree.delete(iid)
        for req in db.get_requests():
            tree.insert("", "end", values=(
                req['id'],
                req['client_id'],
                req['employee_id'],
                req['service'],
                req['date'],
                req['status']
            ))

    # первый вызов
    refresh()
