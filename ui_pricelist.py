# ui_pricelist.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_pricelist_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=1)

    # Фильтры
    filt = ttk.LabelFrame(frame, text="Поиск", padding=20)
    filt.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    filt.columnconfigure(1, weight=1)

    ttk.Label(filt, text="Марка:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
    cats = db.get_categories()
    cat_names = [name for _,name in cats]
    cat_map = {name:cid for cid,name in cats}
    cb_cat = ttk.Combobox(filt, values=cat_names, state="readonly")
    cb_cat.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(filt, text="Модель:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
    model_q = ttk.Entry(filt); model_q.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(filt, text="Цена от:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
    price_min = ttk.Entry(filt); price_min.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    ttk.Label(filt, text="до:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
    price_max = ttk.Entry(filt); price_max.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

    def on_search():
        try:
            cid = cat_map.get(cb_cat.get(), None)
            mn = float(price_min.get()) if price_min.get() else None
            mx = float(price_max.get()) if price_max.get() else None
        except ValueError:
            return messagebox.showerror("Ошибка","Неверный формат цены")
        rows = db.search_products(cid, model_q.get(), mn, mx)
        for i in tree.get_children(): tree.delete(i)
        for r in rows:
            tree.insert("",tk.END,values=(
                r["id"], r["category"], r["name"], r["price"],
                "✔" if r["published"] else "", "Да" if r["used"] else "Нет"
            ))

    ttk.Button(filt, text="Поиск", command=on_search).grid(row=4, column=0, columnspan=2, pady=10)

    # Результаты с кнопками обновления/публикации
    res = ttk.LabelFrame(frame, text="Результаты", padding=20)
    res.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    res.columnconfigure(0, weight=1)

    cols = ("ID","Марка","Модель","Цена","Опублик.","Подерж.")
    tree = ttk.Treeview(res, columns=cols, show="headings")
    for c in cols:
        tree.heading(c,text=c); tree.column(c,anchor="center")
    tree.grid(row=0,column=0,sticky="nsew")

    def on_update():
        sel = tree.selection()
        if not sel: return
        pid = tree.item(sel[0])["values"][0]
        top = tk.Toplevel(frame)
        top.title("Обновить цену")
        ttk.Label(top,text="Новая цена:").pack(padx=10,pady=5)
        e = ttk.Entry(top); e.pack(padx=10,pady=5)
        def do():
            try:
                p = float(e.get())
                db.update_product(p,pid)
                messagebox.showinfo("OK","Цена обновлена"); top.destroy(); on_search()
            except:
                messagebox.showerror("Ошибка","Неверный формат")
        ttk.Button(top,text="Сохранить",command=do).pack(pady=10)
    def on_publish():
        sel = tree.selection()
        if not sel: return
        pid = tree.item(sel[0])["values"][0]
        db.publish_product(pid, True)
        messagebox.showinfo("OK","Опубликовано"); on_search()

    btnf = ttk.Frame(res); btnf.grid(row=1,column=0,pady=10)
    ttk.Button(btnf,text="Обновить цену", command=on_update).pack(side="left", padx=5)
    ttk.Button(btnf,text="Опубликовать",  command=on_publish).pack(side="left", padx=5)
