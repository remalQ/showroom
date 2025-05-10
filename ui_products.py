# ui_products.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def fmt_price(amount):
    # Округляем до целых, разделяем пробелами
    val = int(round(amount))
    s = f"{val:,}".replace(",", " ")
    return f"{s} руб."

def build_product_tab(parent):
    frame = make_scrollable_tab(parent)
    # две колонки: левая — формы (фиксированная), правая — список (растягивается)
    frame.columnconfigure(0, weight=0)
    frame.columnconfigure(1, weight=1)
    # две строки: строка 0 — добавление категории, строка 1 — всё остальное
    frame.rowconfigure(0, weight=0)
    frame.rowconfigure(1, weight=1)

    # ——— Добавление категории ———
    cat_frame = ttk.LabelFrame(frame, text="Категории", padding=20)
    cat_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    cat_frame.columnconfigure(1, weight=1)

    ttk.Label(cat_frame, text="Название категории:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    ent_cat = ttk.Entry(cat_frame)
    ent_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    def add_category():
        name = ent_cat.get().strip()
        if not name:
            return messagebox.showerror("Ошибка", "Введите название категории")
        db.add_category(name)
        messagebox.showinfo("ОК", "Категория добавлена")
        ent_cat.delete(0, "end")
        refresh()

    ttk.Button(cat_frame, text="Добавить категорию", command=add_category)\
        .grid(row=1, column=0, columnspan=2, pady=10)

    # ——— Добавление товара ———
    prod_frame = ttk.LabelFrame(frame, text="Товары", padding=20)
    prod_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    prod_frame.columnconfigure(1, weight=1)

    ttk.Label(prod_frame, text="Категория:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    cb_cat = ttk.Combobox(prod_frame, state="readonly")
    cb_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(prod_frame, text="Название:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    ent_name = ttk.Entry(prod_frame)
    ent_name.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(prod_frame, text="Цена:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    ent_price = ttk.Entry(prod_frame)
    ent_price.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    used_var = tk.BooleanVar()
    ttk.Checkbutton(prod_frame, text="Подержанный", variable=used_var)\
        .grid(row=3, column=0, columnspan=2, pady=5)

    def add_product():
        cat = cb_cat.get()
        name = ent_name.get().strip()
        price = ent_price.get().strip()
        used = used_var.get()
        if not (cat and name and price):
            return messagebox.showerror("Ошибка", "Все поля обязательны")
        try:
            price = float(price)
        except ValueError:
            return messagebox.showerror("Ошибка", "Неверный формат цены")
        db.add_product(name, cat_map[cat], price, used)
        messagebox.showinfo("ОК", "Товар добавлен")
        ent_name.delete(0, "end"); ent_price.delete(0, "end")
        cb_cat.set(""); used_var.set(False)
        refresh()

    ttk.Button(prod_frame, text="Добавить товар", command=add_product)\
        .grid(row=4, column=0, columnspan=2, pady=10)

    # ——— Список товаров ———
    list_frame = ttk.LabelFrame(frame, text="Список товаров", padding=20)
    list_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    list_frame.columnconfigure(0, weight=1)
    list_frame.rowconfigure(0, weight=1)

    cols = ("ID", "Категория", "Название", "Цена", "Подерж.", "Опубл.")
    # задаём высоту в 12 строк
    tree = ttk.Treeview(list_frame, columns=cols, show="headings", height=12)
    vsb = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    # жёстко прописываем ширины колонок
    widths = [50, 120, 200, 100, 80, 80]
    for c, w in zip(cols, widths):
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="center", stretch=False)

    tree.grid(row=0, column=0, sticky="nsew")
    vsb.grid(row=0, column=1, sticky="ns")
    hsb.grid(row=1, column=0, sticky="ew")

    def refresh():
        # обновить категории
        categories = db.get_categories()
        names = [r["name"] for r in categories]
        nonlocal cat_map
        cat_map = {r["name"]: r["id"] for r in categories}
        cb_cat["values"] = names

        # обновить дерево товаров
        for iid in tree.get_children():
            tree.delete(iid)
        for r in db.search_products():
            tree.insert("", "end", values=(
                r["id"],
                r["category"],
                r["name"],
                fmt_price(r["price"]),  # <- форматируем цену
                "Да" if r["used"] else "Нет",
                "Да" if r["published"] else "Нет"
            ))

    # первый запуск
    cat_map = {}
    refresh()
