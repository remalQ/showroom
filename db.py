#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""!
@file db.py
@brief Database connection and schema initialization for Auto Showroom.
"""
import sqlite3
from sqlite3 import Connection, Cursor

DB_NAME: str = "autosalon.db"


def connect() -> Connection:
    """!
    \brief Create a new database connection.

    Sets row factory to sqlite3.Row for named column access.

    \return An open sqlite3.Connection object.
    """
    conn: Connection = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """!
    \brief Initialize database schema and perform migrations.

    Creates tables if they do not exist and adds new columns when missing.
    """
    conn: Connection = connect()
    cur: Cursor = conn.cursor()

    # --- Create tables if not exists ---
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category_id INTEGER,
            price REAL,
            FOREIGN KEY(category_id) REFERENCES categories(id)
        )
        """
    )
    cur.execute(
        """
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
        """
    )
    cur.execute(
        """
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
        """
    )
    cur.execute(
        """
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
        """
    )

    # --- Perform migrations: add missing columns ---
    def _add_column(table: str, column_def: str) -> None:
        """!
        \brief Add a column to a table if it does not exist.

        \param[in] table Name of the table.
        \param[in] column_def Column definition SQL (name and type).
        """
        name = column_def.split()[0]
        cur.execute(f"PRAGMA table_info({table})")
        existing = {row['name'] for row in cur.fetchall()}
        if name not in existing:
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column_def}")

    _add_column("clients", "type TEXT DEFAULT 'гость'")
    _add_column("employees", "department TEXT DEFAULT 'продаж'")
    _add_column("products", "used INTEGER DEFAULT 0")
    _add_column("products", "published INTEGER DEFAULT 0")

    conn.commit()
    conn.close()


# --- CRUD operations ---

def add_client(name: str, phone: str, client_type: str) -> None:
    """!
    \brief Insert a new client record.

    \param[in] name Client full name.
    \param[in] phone Contact phone number.
    \param[in] client_type Type/category of client.
    """
    sql = "INSERT INTO clients (name, phone, type) VALUES (?, ?, ?)"
    with connect() as conn:
        conn.execute(sql, (name, phone, client_type))


def get_clients() -> list[sqlite3.Row]:
    """!
    \brief Retrieve all clients.

    \return List of sqlite3.Row objects with columns id, name, type.
    """
    sql = "SELECT id, name, type FROM clients"
    with connect() as conn:
        return conn.execute(sql).fetchall()


def add_employee(name: str, department: str) -> None:
    """!
    \brief Insert a new employee.

    \param[in] name Employee full name.
    \param[in] department Department name.
    """
    sql = "INSERT INTO employees (name, department) VALUES (?, ?)"
    with connect() as conn:
        conn.execute(sql, (name, department))


def get_employees(dept: str | None = None) -> list[sqlite3.Row]:
    """!
    \brief Retrieve employees, optionally filtered by department.

    \param[in] dept Department name filter.
    \return List of sqlite3.Row objects with columns id, name, department.
    """
    sql = "SELECT id, name, department FROM employees"
    params: tuple = ()
    if dept:
        sql += " WHERE department = ?"
        params = (dept,)
    with connect() as conn:
        return conn.execute(sql, params).fetchall()


def add_category(name: str) -> None:
    """!
    \brief Add a product category if not exists.

    \param[in] name Category name.
    """
    sql = "INSERT OR IGNORE INTO categories (name) VALUES (?)"
    with connect() as conn:
        conn.execute(sql, (name,))


def get_categories() -> list[sqlite3.Row]:
    """!
    \brief Get all product categories.

    \return List of sqlite3.Row objects with columns id, name.
    """
    sql = "SELECT id, name FROM categories"
    with connect() as conn:
        return conn.execute(sql).fetchall()


def add_product(
    name: str,
    category_id: int,
    price: float,
    used: bool = False
) -> None:
    """!
    \brief Insert a new product record.

    \param[in] name Product name.
    \param[in] category_id Foreign key to categories.
    \param[in] price Product price.
    \param[in] used Flag indicating if product is used.
    """
    sql = (
        "INSERT INTO products (name, category_id, price, used) VALUES (?, ?, ?, ?)"
    )
    with connect() as conn:
        conn.execute(sql, (name, category_id, price, int(used)))


def update_product(price: float, prod_id: int) -> None:
    """!
    \brief Update price for a product.

    \param[in] price New product price.
    \param[in] prod_id Product ID.
    """
    sql = "UPDATE products SET price = ? WHERE id = ?"
    with connect() as conn:
        conn.execute(sql, (price, prod_id))


def publish_product(prod_id: int, published: bool = True) -> None:
    """!
    \brief Set published flag for a product.

    \param[in] prod_id Product ID.
    \param[in] published Boolean to publish (True) or unpublish (False).
    """
    sql = "UPDATE products SET published = ? WHERE id = ?"
    with connect() as conn:
        conn.execute(sql, (int(published), prod_id))


def search_products(
    cat_id: int | None = None,
    model_query: str = "",
    min_price: float | None = None,
    max_price: float | None = None
) -> list[sqlite3.Row]:
    """!
    \brief Search products by filters.

    \param[in] cat_id Category ID filter.
    \param[in] model_query Substring match for product name.
    \param[in] min_price Minimum price filter.
    \param[in] max_price Maximum price filter.
    \return List of sqlite3.Row matching products.
    """
    sql = (
        "SELECT p.id, p.name, c.name AS category,"
        " p.price, p.used, p.published"
        " FROM products p"
        " JOIN categories c ON p.category_id = c.id"
        " WHERE p.name LIKE ?"
    )
    params: list = [f"%{model_query}%"]
    if cat_id is not None:
        sql += " AND p.category_id = ?"
        params.append(cat_id)
    if min_price is not None:
        sql += " AND p.price >= ?"
        params.append(min_price)
    if max_price is not None:
        sql += " AND p.price <= ?"
        params.append(max_price)

    with connect() as conn:
        return conn.execute(sql, tuple(params)).fetchall()


def get_used_products() -> list[sqlite3.Row]:
    """!
    \brief Retrieve only used products.

    \return Filtered list where used=1.
    """
    return [row for row in search_products() if row["used"] == 1]


def get_new_products() -> list[sqlite3.Row]:
    """!
    \brief Retrieve only new products.

    \return Filtered list where used=0.
    """
    return [row for row in search_products() if row["used"] == 0]


def add_request(
    client_id: int,
    emp_id: int,
    service: str,
    date: str,
    status: str
) -> None:
    """!
    \brief Insert maintenance/service request.

    \param[in] client_id Foreign key to clients.
    \param[in] emp_id Foreign key to employees.
    \param[in] service Description of service.
    \param[in] date Date string (ISO format recommended).
    \param[in] status Current request status.
    """
    sql = (
        "INSERT INTO requests"
        " (client_id, employee_id, service, date, status)"
        " VALUES (?, ?, ?, ?, ?)"
    )
    with connect() as conn:
        conn.execute(sql, (client_id, emp_id, service, date, status))


def get_requests() -> list[sqlite3.Row]:
    """!
    \brief Retrieve all service requests.

    \return List of all requests.
    """
    sql = "SELECT * FROM requests"
    with connect() as conn:
        return conn.execute(sql).fetchall()


def add_sale(
    prod_id: int,
    client_id: int,
    emp_id: int,
    date: str,
    price: float,
    contract: str
) -> None:
    """!
    \brief Record a sale transaction.

    \param[in] prod_id Product ID sold.
    \param[in] client_id Client ID.
    \param[in] emp_id Employee ID who made sale.
    \param[in] date Date of sale.
    \param[in] price Final sale price.
    \param[in] contract Contract document reference.
    """
    sql = (
        "INSERT INTO sales"
        " (product_id, client_id, employee_id, date, price, contract)"
        " VALUES (?, ?, ?, ?, ?, ?)"
    )
    with connect() as conn:
        conn.execute(sql, (prod_id, client_id, emp_id, date, price, contract))


def get_sales() -> list[sqlite3.Row]:
    """!
    \brief Retrieve all sales records.

    \return List of sales.
    """
    sql = "SELECT * FROM sales"
    with connect() as conn:
        return conn.execute(sql).fetchall()


def add_tradein(
    new_prod_id: int,
    old_details: str,
    client_id: int,
    emp_id: int,
    date: str,
    price_diff: float
) -> None:
    """!
    \brief Record a trade-in transaction.

    \param[in] new_prod_id New product ID.
    \param[in] old_details Description of old item.
    \param[in] client_id Client ID.
    \param[in] emp_id Employee ID.
    \param[in] date Date of trade-in.
    \param[in] price_diff Price difference credited.
    """
    sql = (
        "INSERT INTO tradeins"
        " (new_product_id, old_details, client_id, employee_id, date, price_diff)"
        " VALUES (?, ?, ?, ?, ?, ?)"
    )
    with connect() as conn:
        conn.execute(sql, (new_prod_id, old_details, client_id, emp_id, date, price_diff))


def get_tradeins() -> list[sqlite3.Row]:
    """!
    \brief Retrieve all trade-in transactions.

    \return List of trade-ins.
    """
    sql = "SELECT * FROM tradeins"
    with connect() as conn:
        return conn.execute(sql).fetchall()