# ui_sales.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime
from scrollable_tab import make_scrollable_tab

def build_sales_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=1); frame.columnconfigure(1, weight=1)

    # Подержанные
    used = ttk.LabelFrame(frame, text="Продажа подержанного", padding=20)
    used.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
    used.columnconfigure(1,weight=1)
    ttk.Label(used,text="Выбрать авто:").grid(row=0,column=0,sticky="e",padx=5,pady=5)
    used_list = [f"{r['id']}:{r['name']}" for r in db.get_used_products()]
    cb_used = ttk.Combobox(used,values=used_list,state="readonly"); cb_used.grid(row=0,column=1,sticky="ew")
    ttk.Label(used,text="Клиент ID:").grid(row=1,column=0,sticky="e",padx=5,pady=5)
    ent_c = ttk.Entry(used); ent_c.grid(row=1,column=1,sticky="ew")
    ttk.Label(used,text="Сотрудник ID:").grid(row=2,column=0,sticky="e",padx=5,pady=5)
    ent_e = ttk.Entry(used); ent_e.grid(row=2,column=1,sticky="ew")
    ttk.Label(used,text="Цена:").grid(row=3,column=0,sticky="e",padx=5,pady=5)
    ent_pr= ttk.Entry(used); ent_pr.grid(row=3,column=1,sticky="ew")
    def sell_used():
        try:
            pid = int(cb_used.get().split(":")[0])
            cid, eid = int(ent_c.get()), int(ent_e.get())
            price = float(ent_pr.get())
            db.add_sale(pid, cid, eid, datetime.now().isoformat(), price, "подержанный")
            messagebox.showinfo("OK","Продано"); cb_used.set(""); ent_c.delete(0,'end')
            ent_e.delete(0,'end'); ent_pr.delete(0,'end')
        except Exception as ex:
            messagebox.showerror("Ошибка",str(ex))
    ttk.Button(used,text="Продать",command=sell_used).grid(row=4,column=0,columnspan=2,pady=10)

    # Новые
    new = ttk.LabelFrame(frame, text="Продажа нового", padding=20)
    new.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
    new.columnconfigure(1,weight=1)
    new_list = [f"{r['id']}:{r['name']}" for r in db.get_new_products()]
    cb_new = ttk.Combobox(new,values=new_list,state="readonly"); cb_new.grid(row=0,column=1,sticky="ew")
    ttk.Label(new,text="Клиент ID:").grid(row=1,column=0,sticky="e",padx=5,pady=5)
    ent_c2 = ttk.Entry(new); ent_c2.grid(row=1,column=1,sticky="ew")
    ttk.Label(new,text="Сотрудник ID:").grid(row=2,column=0,sticky="e",padx=5,pady=5)
    ent_e2 = ttk.Entry(new); ent_e2.grid(row=2,column=1,sticky="ew")
    ttk.Label(new,text="Цена:").grid(row=3,column=0,sticky="e",padx=5,pady=5)
    ent_pr2= ttk.Entry(new); ent_pr2.grid(row=3,column=1,sticky="ew")
    def sell_new():
        try:
            pid = int(cb_new.get().split(":")[0])
            cid, eid = int(ent_c2.get()), int(ent_e2.get())
            price = float(ent_pr2.get())
            db.add_sale(pid, cid, eid, datetime.now().isoformat(), price, "новый")
            messagebox.showinfo("OK","Продано")
        except Exception as ex:
            messagebox.showerror("Ошибка",str(ex))
    ttk.Button(new,text="Продать",command=sell_new).grid(row=4,column=0,columnspan=2,pady=10)
