# ui_tradein.py
import tkinter as tk
from tkinter import ttk, messagebox
import db
from datetime import datetime
from scrollable_tab import make_scrollable_tab

def build_tradein_tab(parent):
    frame = make_scrollable_tab(parent)
    frame.columnconfigure(0, weight=1)

    tf = ttk.LabelFrame(frame, text="Trade-IN", padding=20)
    tf.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    tf.columnconfigure(1, weight=1)

    # Новый авто
    ttk.Label(tf,text="Новый (ID:название):").grid(row=0,column=0,sticky="e",padx=5,pady=5)
    new_list = [f"{r['id']}:{r['name']}" for r in db.get_new_products()]
    cbn = ttk.Combobox(tf,values=new_list,state="readonly"); cbn.grid(row=0,column=1,sticky="ew")
    # Старое описание
    ttk.Label(tf,text="Старое (описание):").grid(row=1,column=0,sticky="e",padx=5,pady=5)
    old = ttk.Entry(tf); old.grid(row=1,column=1,sticky="ew",padx=5,pady=5)
    # Клиент / сотрудник
    ttk.Label(tf,text="Клиент ID:").grid(row=2,column=0,sticky="e",padx=5,pady=5)
    enc = ttk.Entry(tf); enc.grid(row=2,column=1,sticky="ew")
    ttk.Label(tf,text="Сотрудник ID:").grid(row=3,column=0,sticky="e",padx=5,pady=5)
    ene = ttk.Entry(tf); ene.grid(row=3,column=1,sticky="ew")
    ttk.Label(tf,text="Разница в цене:").grid(row=4,column=0,sticky="e",padx=5,pady=5)
    diff = ttk.Entry(tf); diff.grid(row=4,column=1,sticky="ew",padx=5,pady=5)

    def do_tradein():
        try:
            npid = int(cbn.get().split(":")[0])
            cl, em = int(enc.get()), int(ene.get())
            pdiff = float(diff.get())
            db.add_tradein(npid, old.get().strip(), cl, em, datetime.now().isoformat(), pdiff)
            messagebox.showinfo("OK","Trade-IN оформлен")
        except Exception as ex:
            messagebox.showerror("Ошибка",str(ex))

    ttk.Button(tf,text="Оформить",command=do_tradein).grid(row=5,column=0,columnspan=2,pady=10)
