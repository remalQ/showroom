import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab


def build_product_tab(tab):
    frame = make_scrollable_tab(tab)

    # --- Добавление товара ---
    add_frame = ttk.LabelFrame(frame, text="Добавление товара", padding=20)
    add_frame.grid(row=0, column=0, padx=20, pady=10)

    categories = db.get_categories()
    category_dict = {name: id for id, name in categories}

    ttk.Label(add_frame, text="Наименование:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = ttk.Entry(add_frame, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(add_frame, text="Категория:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    category_combo = ttk.Combobox(add_frame, values=list(category_dict.keys()), width=30)
    category_combo.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(add_frame, text="Цена:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    price_entry = ttk.Entry(add_frame, width=30)
    price_entry.grid(row=2, column=1, padx=10, pady=10)

    def add_product():
        try:
            name = name_entry.get()
            category = category_combo.get()
            price = float(price_entry.get())
            if not name or category not in category_dict:
                raise ValueError("Неверные данные")

            db.add_product(name, category_dict[category], price)
            messagebox.showinfo("Успешно", "Товар добавлен")
            name_entry.delete(0, tk.END)
            price_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    ttk.Button(add_frame, text="Добавить товар", command=add_product).grid(
        row=3, column=0, columnspan=2, pady=20
    )

    # --- Поиск товара ---
    search_frame = ttk.LabelFrame(frame, text="Поиск товаров", padding=20)
    search_frame.grid(row=1, column=0, padx=20, pady=10)

    ttk.Label(search_frame, text="Поиск по названию:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.grid(row=0, column=1, padx=10, pady=10)

    results_box = tk.Listbox(search_frame, width=70)
    results_box.grid(row=2, column=0, columnspan=2, pady=10)

    def do_search():
        query = search_entry.get()
        results = db.search_products(query)
        results_box.delete(0, tk.END)
        for name, category, price in results:
            results_box.insert(tk.END, f"{name} | {category} | {price:.2f} руб.")

    ttk.Button(search_frame, text="Найти", command=do_search).grid(
        row=1, column=0, columnspan=2, pady=10
    )
