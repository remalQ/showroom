import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab


def build_employee_tab(tab):
    frame = make_scrollable_tab(tab)

    form = ttk.LabelFrame(frame, text="Добавление сотрудника", padding=20)
    form.grid(row=0, column=0)

    ttk.Label(form, text="Имя:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    name_entry = ttk.Entry(form, width=30)
    name_entry.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form, text="Должность:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    position_entry = ttk.Entry(form, width=30)
    position_entry.grid(row=1, column=1, padx=10, pady=10)

    def on_add():
        name = name_entry.get()
        position = position_entry.get()
        if name and position:
            db.add_employee(name, position)
            messagebox.showinfo("Успешно", "Сотрудник добавлен")
            name_entry.delete(0, tk.END)
            position_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Ошибка", "Заполните все поля")

    ttk.Button(form, text="Добавить сотрудника", command=on_add).grid(
        row=2, column=0, columnspan=2, pady=20
    )
