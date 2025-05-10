# ui_employees.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_employee_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(0, weight=1)

    # форма слева
    form = ttk.LabelFrame(frame, text="Добавление сотрудника", padding=20)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    form.columnconfigure(1, weight=1)
    ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_e = ttk.Entry(form); name_e.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    ttk.Label(form, text="Отдел:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    cb_dep = ttk.Combobox(form, values=["продаж","маркетинг"], state="readonly")
    cb_dep.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    def add():
        n, d = name_e.get().strip(), cb_dep.get()
        if not (n and d):
            return messagebox.showerror("Ошибка","Заполните все поля")
        db.add_employee(n,d); refresh(); name_e.delete(0,'end'); cb_dep.set("")
    ttk.Button(form, text="Добавить", command=add).grid(row=2, column=0, columnspan=2, pady=10)

    # таблица справа
    listf = ttk.LabelFrame(frame, text="Список сотрудников", padding=10)
    listf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    listf.columnconfigure(0, weight=1)
    listf.rowconfigure(0, weight=1)

    cols = ("ID","Имя","Отдел")
    tree = ttk.Treeview(listf, columns=cols, show="headings", height=12)
    vsb = ttk.Scrollbar(listf, orient="vertical",   command=tree.yview)
    hsb = ttk.Scrollbar(listf, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    widths = [50, 200, 150]
    for c,w in zip(cols, widths):
        tree.heading(c, text=c); tree.column(c, width=w, anchor="center", stretch=False)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    def refresh():
        for iid in tree.get_children(): tree.delete(iid)
        for r in db.get_employees():
            tree.insert("", "end", values=(r["id"], r["name"], r["department"]))

    refresh()
