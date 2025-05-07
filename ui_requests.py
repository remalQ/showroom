import tkinter as tk
from tkinter import ttk, messagebox
import db
from scrollable_tab import make_scrollable_tab


def build_request_tab(tab):
    frame = make_scrollable_tab(tab)

    form = ttk.LabelFrame(frame, text="Создание заявки", padding=20)
    form.grid(row=0, column=0)

    clients = db.get_clients()
    employees = db.get_employees()

    client_dict = {f"{name} (ID: {id})": id for id, name in clients}
    employee_dict = {f"{name} (ID: {id})": id for id, name in employees}

    ttk.Label(form, text="Клиент:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    client_combo = ttk.Combobox(form, values=list(client_dict.keys()), width=30)
    client_combo.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(form, text="Сотрудник:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    employee_combo = ttk.Combobox(form, values=list(employee_dict.keys()), width=30)
    employee_combo.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(form, text="Услуга:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    service_entry = ttk.Entry(form, width=30)
    service_entry.grid(row=2, column=1, padx=10, pady=10)

    ttk.Label(form, text="Дата (ГГГГ-ММ-ДД):").grid(row=3, column=0, padx=10, pady=10, sticky="e")
    date_entry = ttk.Entry(form, width=30)
    date_entry.grid(row=3, column=1, padx=10, pady=10)

    ttk.Label(form, text="Статус:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
    status_entry = ttk.Entry(form, width=30)
    status_entry.grid(row=4, column=1, padx=10, pady=10)

    def on_add():
        try:
            client_id = client_dict[client_combo.get()]
            employee_id = employee_dict[employee_combo.get()]
            service = service_entry.get()
            date = date_entry.get()
            status = status_entry.get()

            if not all([service, date, status]):
                raise ValueError("Все поля должны быть заполнены")

            db.add_request(client_id, employee_id, service, date, status)
            messagebox.showinfo("Успешно", "Заявка добавлена")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    ttk.Button(form, text="Добавить заявку", command=on_add).grid(
        row=5, column=0, columnspan=2, pady=20
    )
