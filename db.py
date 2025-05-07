import sqlite3

DB_NAME = "autosalon.db"

def connect():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        category_id INTEGER,
        price REAL,
        FOREIGN KEY (category_id) REFERENCES categories(id)
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        phone TEXT
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        position TEXT
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY,
        client_id INTEGER,
        employee_id INTEGER,
        service TEXT,
        date TEXT,
        status TEXT,
        FOREIGN KEY (client_id) REFERENCES clients(id),
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )''')

    conn.commit()
    conn.close()

# --- Clients ---
def add_client(name, phone):
    with connect() as conn:
        conn.execute("INSERT INTO clients (name, phone) VALUES (?, ?)", (name, phone))

def get_clients():
    with connect() as conn:
        return conn.execute("SELECT id, name FROM clients").fetchall()

# --- Employees ---
def add_employee(name, position):
    with connect() as conn:
        conn.execute("INSERT INTO employees (name, position) VALUES (?, ?)", (name, position))

def get_employees():
    with connect() as conn:
        return conn.execute("SELECT id, name FROM employees").fetchall()

# --- Requests ---
def add_request(client_id, employee_id, service, date, status):
    with connect() as conn:
        conn.execute(
            "INSERT INTO requests (client_id, employee_id, service, date, status) VALUES (?, ?, ?, ?, ?)",
            (client_id, employee_id, service, date, status)
        )

def get_requests():
    with connect() as conn:
        return conn.execute('''
            SELECT r.id, c.name, e.name, r.service, r.date, r.status
            FROM requests r
            JOIN clients c ON r.client_id = c.id
            JOIN employees e ON r.employee_id = e.id
        ''').fetchall()

# --- Categories ---
def add_category(name):
    with connect() as conn:
        conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))

def get_categories():
    with connect() as conn:
        return conn.execute("SELECT id, name FROM categories").fetchall()

# --- Products ---
def add_product(name, category_id, price):
    with connect() as conn:
        conn.execute(
            "INSERT INTO products (name, category_id, price) VALUES (?, ?, ?)",
            (name, category_id, price)
        )

def search_products(query):
    with connect() as conn:
        return conn.execute('''
            SELECT p.name, c.name, p.price
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.name LIKE ?
        ''', ('%' + query + '%',)).fetchall()