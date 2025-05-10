# ui_clients.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_client_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=1)

    form = ttk.LabelFrame(frame, text="Клиент", padding=20)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    form.columnconfigure(1, weight=1)

    ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name = ttk.Entry(form); name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Телефон:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    phone = ttk.Entry(form); phone.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(form, text="Тип:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    types = ["гость","покупатель","постоянный клиент"]
    client_type = ttk.Combobox(form, values=types, state="readonly")
    client_type.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    def add():
        n, p, t = name.get().strip(), phone.get().strip(), client_type.get()
        if not (n and p and t):
            return messagebox.showerror("Ошибка","Все поля обязательны")
        db.add_client(n,p,t)
        messagebox.showinfo("OK","Клиент добавлен")
        name.delete(0,'end'); phone.delete(0,'end'); client_type.set("")

    ttk.Button(form, text="Добавить", command=add).grid(row=3, column=0, columnspan=2, pady=15)

    listf = ttk.LabelFrame(frame, text="Список клиентов", padding=20)
    listf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    listf.columnconfigure(0, weight=1)

    tree = ttk.Treeview(listf, columns=("ID","Имя","Тип"), show="headings")
    for col in ("ID","Имя","Тип"):
        tree.heading(col,text=col); tree.column(col,anchor="center")
    tree.grid(row=0, column=0, sticky="nsew")
    for r in db.get_clients():
        tree.insert("",tk.END,values=(r["id"],r["name"],r["type"]))
