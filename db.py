# db.py
import sqlite3

DB_NAME = "autosalon.db"

def connect():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = connect()
    cur = conn.cursor()

    # 1) Создаём все таблицы (если их нет)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT,
            phone TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            category_id INTEGER,
            price REAL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY,
            client_id INTEGER,
            employee_id INTEGER,
            service TEXT,
            date TEXT,
            status TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            product_id INTEGER,
            client_id INTEGER,
            employee_id INTEGER,
            date TEXT,
            price REAL,
            contract TEXT,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS tradeins (
            id INTEGER PRIMARY KEY,
            new_product_id INTEGER,
            old_details TEXT,
            client_id INTEGER,
            employee_id INTEGER,
            date TEXT,
            price_diff REAL,
            FOREIGN KEY(new_product_id) REFERENCES products(id),
            FOREIGN KEY(client_id) REFERENCES clients(id),
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    ''')

    # 2) Миграции — добавляем новые колонки к уже существующим таблицам

    def add_column(table, column_def):
        """Если колонки нет — добавляем её."""
        name = column_def.split()[0]
        cur.execute(f"PRAGMA table_info({table})")
        cols = [r["name"] for r in cur.fetchall()]
        if name not in cols:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")

    # у клиентов: type
    add_column("clients",    "type TEXT DEFAULT 'гость'")
    # у сотрудников: department
    add_column("employees",  "department TEXT DEFAULT 'продаж'")
    # в товарах: used и published
    add_column("products",   "used INTEGER DEFAULT 0")
    add_column("products",   "published INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


# --- дальше ваши CRUD-функции без изменений, но уже с учётом новых колонок ---

# Клиенты
def add_client(name, phone, client_type):
    with connect() as conn:
        conn.execute(
            "INSERT INTO clients (name, phone, type) VALUES (?, ?, ?)",
            (name, phone, client_type)
        )

def get_clients():
    with connect() as conn:
        return conn.execute(
            "SELECT id, name, type FROM clients"
        ).fetchall()


# Сотрудники
def add_employee(name, department):
    with connect() as conn:
        conn.execute(
            "INSERT INTO employees (name, department) VALUES (?, ?)",
            (name, department)
        )

def get_employees(dept=None):
    sql = "SELECT id, name, department FROM employees"
    params = ()
    if dept:
        sql += " WHERE department = ?"
        params = (dept,)
    with connect() as conn:
        return conn.execute(sql, params).fetchall()


# Категории и товары
def add_category(name):
    with connect() as conn:
        conn.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,))

def get_categories():
    with connect() as conn:
        return conn.execute("SELECT id, name FROM categories").fetchall()

def add_product(name, category_id, price, used=False):
    with connect() as conn:
        conn.execute(
            "INSERT INTO products (name, category_id, price, used) VALUES (?, ?, ?, ?)",
            (name, category_id, price, int(used))
        )

def update_product(price, prod_id):
    with connect() as conn:
        conn.execute("UPDATE products SET price = ? WHERE id = ?", (price, prod_id))

def publish_product(prod_id, published=True):
    with connect() as conn:
        conn.execute("UPDATE products SET published = ? WHERE id = ?", (int(published), prod_id))

def search_products(cat_id=None, model_query="", min_price=None, max_price=None):
    sql = '''
        SELECT p.id, p.name, c.name AS category, p.price, p.used, p.published 
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.name LIKE ?
    '''
    params = [f"%{model_query}%"]
    if cat_id:
        sql += " AND p.category_id = ?"
        params.append(cat_id)
    if min_price is not None:
        sql += " AND p.price >= ?"
        params.append(min_price)
    if max_price is not None:
        sql += " AND p.price <= ?"
        params.append(max_price)
    with connect() as conn:
        return conn.execute(sql, params).fetchall()

def get_used_products():
    return [r for r in search_products() if r["used"] == 1]

def get_new_products():
    return [r for r in search_products() if r["used"] == 0]


# Заявки
def add_request(client_id, emp_id, service, date, status):
    with connect() as conn:
        conn.execute(
            "INSERT INTO requests (client_id, employee_id, service, date, status) VALUES (?, ?, ?, ?, ?)",
            (client_id, emp_id, service, date, status)
        )

def get_requests():
    with connect() as conn:
        return conn.execute("SELECT * FROM requests").fetchall()


# Продажи
def add_sale(prod_id, client_id, emp_id, date, price, contract):
    with connect() as conn:
        conn.execute(
            "INSERT INTO sales (product_id, client_id, employee_id, date, price, contract) VALUES (?, ?, ?, ?, ?, ?)",
            (prod_id, client_id, emp_id, date, price, contract)
        )

def get_sales():
    with connect() as conn:
        return conn.execute("SELECT * FROM sales").fetchall()


# Trade-IN
def add_tradein(new_prod_id, old_details, client_id, emp_id, date, price_diff):
    with connect() as conn:
        conn.execute(
            "INSERT INTO tradeins (new_product_id, old_details, client_id, employee_id, date, price_diff) VALUES (?, ?, ?, ?, ?, ?)",
            (new_prod_id, old_details, client_id, emp_id, date, price_diff)
        )

def get_tradeins():
    with connect() as conn:
        return conn.execute("SELECT * FROM tradeins").fetchall()
