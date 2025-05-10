# ui_clients.py
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_client_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(0, weight=1)

    form = ttk.LabelFrame(frame, text="Добавление клиента", padding=20)
    form.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
    form.columnconfigure(1, weight=1)
    ttk.Label(form, text="Имя:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    name_e = ttk.Entry(form)
    name_e.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    ttk.Label(form, text="Телефон:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    phone_e = ttk.Entry(form)
    phone_e.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    ttk.Label(form, text="Тип:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    cb_type = ttk.Combobox(form, values=["гость", "покупатель", "постоянный клиент"], state="readonly")
    cb_type.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    def add():
        n, p, t = name_e.get().strip(), phone_e.get().strip(), cb_type.get()
        if not (n and t):
            return messagebox.showerror("Ошибка", "Имя и тип обязательны")
        db.add_client(n, p, t)
        refresh()
        name_e.delete(0, 'end')
        phone_e.delete(0, 'end')
        cb_type.set("")

    ttk.Button(form, text="Добавить", command=add).grid(row=3, column=0, columnspan=2, pady=10)

    # ——— Таблица справа ———
    listf = ttk.LabelFrame(frame, text="Список клиентов", padding=10)
    listf.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    listf.columnconfigure(0, weight=1)
    listf.rowconfigure(0, weight=1)

    cols = ("ID", "Имя", "Тип")
    tree = ttk.Treeview(listf, columns=cols, show="headings", height=12)
    vsb = ttk.Scrollbar(listf, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(listf, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    widths = [50, 200, 150]
    for c, w in zip(cols, widths):
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="center", stretch=False)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    def refresh():
        for iid in tree.get_children(): tree.delete(iid)
        for r in db.get_clients():
            tree.insert("", "end", values=(r["id"], r["name"], r["type"]))

    refresh()
