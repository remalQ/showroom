# ui_employees.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_employee_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=1)

    form = ttk.LabelFrame(frame, text="Сотрудник", padding=20)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name = ttk.Entry(form); name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Отдел:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    deps = ["продаж","маркетинг"]
    dept = ttk.Combobox(form, values=deps, state="readonly")
    dept.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    def add():
        n, d = name.get().strip(), dept.get()
        if not (n and d):
            return messagebox.showerror("Ошибка","Все поля обязательны")
        db.add_employee(n,d)
        messagebox.showinfo("OK","Сотрудник добавлен")
        name.delete(0,'end'); dept.set("")

    ttk.Button(form, text="Добавить", command=add).grid(row=2, column=0, columnspan=2, pady=15)

    listf = ttk.LabelFrame(frame, text="Список сотрудников", padding=20)
    listf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    listf.columnconfigure(0, weight=1)

    tree = ttk.Treeview(listf, columns=("ID","Имя","Отдел"), show="headings")
    for col in ("ID","Имя","Отдел"):
        tree.heading(col,text=col); tree.column(col,anchor="center")
    tree.grid(row=0, column=0, sticky="nsew")
    for r in db.get_employees():
        tree.insert("",tk.END,values=(r["id"],r["name"],r["department"]))
