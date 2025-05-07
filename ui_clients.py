import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab

def build_client_tab(tab):
    frame = make_scrollable_tab(tab)

    form = ttk.LabelFrame(frame, text="Добавление клиента", padding=20)
    form.grid(row=0, column=0)

    ttk.Label(form, text="Имя:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = ttk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form, text="Телефон:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    phone_entry = ttk.Entry(form, width=30)
    phone_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_add():
        name = name_entry.get()
        phone = phone_entry.get()
        if name and phone:
            db.add_client(name, phone)
            messagebox.showinfo("Успешно", "Клиент добавлен")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    ttk.Button(form, text="Добавить клиента", command=on_add).grid(
        row=2, column=0, columnspan=2, pady=20
    )
