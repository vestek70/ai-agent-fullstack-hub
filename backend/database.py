"""
Database module for ai-agent-fullstack-hub.
Provides a local pre-seeded SQLite database simulating enterprise PostgreSQL
with customers, products, orders, order_items, and support_tickets tables.
"""

import sqlite3
import os
import time
from typing import Dict, Any, List

DB_PATH = os.path.join(os.path.dirname(__file__), "agent_hub.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create tables
    cursor.executescript("""
    DROP TABLE IF EXISTS order_items;
    DROP TABLE IF EXISTS orders;
    DROP TABLE IF EXISTS support_tickets;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS products;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        company TEXT NOT NULL,
        country TEXT NOT NULL,
        tier TEXT CHECK(tier IN ('Enterprise', 'Growth', 'Starter')) DEFAULT 'Starter',
        status TEXT CHECK(status IN ('Active', 'Churned', 'Onboarding')) DEFAULT 'Active',
        created_at DATE NOT NULL
    );

    CREATE TABLE products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        rating REAL NOT NULL,
        created_at DATE NOT NULL
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL REFERENCES customers(id),
        order_date DATE NOT NULL,
        status TEXT CHECK(status IN ('Delivered', 'Processing', 'Cancelled', 'Shipped')) DEFAULT 'Delivered',
        total_amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        shipping_city TEXT NOT NULL
    );

    CREATE TABLE order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL REFERENCES orders(id),
        product_id INTEGER NOT NULL REFERENCES products(id),
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL
    );

    CREATE TABLE support_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL REFERENCES customers(id),
        subject TEXT NOT NULL,
        priority TEXT CHECK(priority IN ('Critical', 'High', 'Medium', 'Low')) DEFAULT 'Medium',
        status TEXT CHECK(status IN ('Open', 'In Progress', 'Resolved', 'Closed')) DEFAULT 'Open',
        category TEXT NOT NULL,
        resolution_time_hours REAL
    );
    """)

    # Seed Customers
    customers_data = [
        ("TechNova Systems", "billing@technova.de", "TechNova AG", "Germany", "Enterprise", "Active", "2024-01-15"),
        ("Apex Cloud Inc", "ops@apexcloud.com", "Apex Cloud Solutions", "USA", "Enterprise", "Active", "2024-02-01"),
        ("Nordic Retail Lab", "admin@nordicretail.se", "Nordic Retail Group", "Sweden", "Growth", "Active", "2024-03-10"),
        ("Tokyo AI Dynamics", "contact@tokyoai.co.jp", "Tokyo AI Labs", "Japan", "Enterprise", "Active", "2024-01-20"),
        ("Sao Paulo Fintech", "pagamentos@spfintech.com.br", "SP Fintech Corp", "Brazil", "Growth", "Active", "2024-04-05"),
        ("Bavaria AutoSoft", "it@bavaria-auto.de", "Bavaria Automotive", "Germany", "Enterprise", "Active", "2024-02-14"),
        ("Parisian Luxury Tech", "contact@paris-lux.fr", "Parisian Luxury Digital", "France", "Growth", "Active", "2024-03-22"),
        ("London Algo Trading", "dev@londontrading.co.uk", "London Algo Capital", "UK", "Enterprise", "Active", "2024-01-08"),
        ("Sydney Cloud Works", "hello@sydneycloud.au", "Sydney Cloud Works Pty", "Australia", "Starter", "Active", "2024-05-18"),
        ("CyberShield Israel", "security@cybershield.io", "CyberShield Ltd", "Israel", "Growth", "Active", "2024-02-28"),
        ("Toronto Analytics", "data@toronto-analytics.ca", "Toronto Data Corp", "Canada", "Growth", "Active", "2024-04-12"),
        ("Berlin Green Mobility", "fleet@berlin-green.de", "Berlin Green Mobility GmbH", "Germany", "Starter", "Active", "2024-06-01"),
    ]
    cursor.executemany("""
    INSERT INTO customers (name, email, company, country, tier, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, customers_data)

    # Seed Products
    products_data = [
        ("Agentic AI Gateway Pro", "Software", 1499.00, 500, 4.9, "2024-01-01"),
        ("Vector DB Acceleration Node", "Hardware", 3200.00, 45, 4.8, "2024-01-05"),
        ("Autonomous Workflow Engine", "Software", 899.00, 1000, 4.7, "2024-02-01"),
        ("Enterprise LLM Guardrail Kit", "Security", 1250.00, 200, 4.9, "2024-02-15"),
        ("GPU Cluster Interconnect Switch", "Hardware", 4800.00, 20, 4.9, "2024-01-10"),
        ("Realtime Tool Calling SDK License", "Developer Tools", 499.00, 800, 4.6, "2024-03-01"),
        ("Neural Cache High-Speed Module", "Hardware", 2100.00, 60, 4.7, "2024-03-15"),
        ("Multi-Agent Orchestration Hub", "Software", 1999.00, 350, 4.8, "2024-02-20"),
    ]
    cursor.executemany("""
    INSERT INTO products (name, category, price, stock, rating, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, products_data)

    # Seed Orders
    orders_data = [
        (1, "2024-06-01", "Delivered", 14200.00, "Wire Transfer", "Munich"),
        (2, "2024-06-05", "Delivered", 18500.00, "Credit Card", "San Francisco"),
        (4, "2024-06-12", "Delivered", 16800.00, "Wire Transfer", "Tokyo"),
        (6, "2024-06-15", "Delivered", 12900.00, "Wire Transfer", "Stuttgart"),
        (8, "2024-06-18", "Delivered", 21400.00, "Wire Transfer", "London"),
        (3, "2024-06-22", "Shipped", 4500.00, "Credit Card", "Stockholm"),
        (5, "2024-06-25", "Delivered", 6200.00, "Credit Card", "Sao Paulo"),
        (7, "2024-07-02", "Delivered", 5800.00, "Credit Card", "Paris"),
        (10, "2024-07-05", "Delivered", 8900.00, "Wire Transfer", "Tel Aviv"),
        (11, "2024-07-10", "Processing", 7400.00, "Credit Card", "Toronto"),
        (1, "2024-07-15", "Delivered", 9800.00, "Wire Transfer", "Berlin"),
        (2, "2024-07-20", "Delivered", 11200.00, "Credit Card", "Seattle"),
        (4, "2024-07-28", "Delivered", 14300.00, "Wire Transfer", "Osaka"),
        (12, "2024-08-01", "Processing", 2999.00, "Credit Card", "Berlin"),
        (6, "2024-08-04", "Delivered", 15400.00, "Wire Transfer", "Frankfurt"),
    ]
    cursor.executemany("""
    INSERT INTO orders (customer_id, order_date, status, total_amount, payment_method, shipping_city)
    VALUES (?, ?, ?, ?, ?, ?)
    """, orders_data)

    # Seed Support Tickets
    tickets_data = [
        (1, "Latency optimization for Tool Calling in EU-Central", "High", "Resolved", "Performance", 4.5),
        (2, "Scale Vector DB throughput above 50k QPS", "Critical", "In Progress", "Infrastructure", None),
        (4, "Japanese tokenization enhancement in Hermes 3 model", "Medium", "Resolved", "Model Support", 8.2),
        (6, "Automotive CAN-bus telemetry agent integration", "High", "Open", "Custom Tooling", None),
        (8, "Fix high-frequency query retry limit in SQL connector", "Critical", "Resolved", "Database", 2.1),
        (5, "PIX and local payment gateway webhook timeout", "Medium", "Open", "Billing", None),
        (10, "Post-quantum crypto signature verification failure", "Critical", "Open", "Security", None),
        (11, "Multi-tenant workspace isolation configuration", "Low", "Resolved", "Configuration", 12.0),
    ]
    cursor.executemany("""
    INSERT INTO support_tickets (customer_id, subject, priority, status, category, resolution_time_hours)
    VALUES (?, ?, ?, ?, ?, ?)
    """, tickets_data)

    conn.commit()
    conn.close()
    print("Database initialized successfully at", DB_PATH)

def execute_query(sql: str) -> Dict[str, Any]:
    """Execute a safe SQL SELECT query and return structured data with timing."""
    start_time = time.time()
    clean_sql = sql.strip().rstrip(";")

    # Guard against accidental destructive commands in read tool
    forbidden = ["DROP", "DELETE", "TRUNCATE", "ALTER", "UPDATE", "INSERT INTO"]
    first_word = clean_sql.split()[0].upper() if clean_sql else ""
    if any(keyword in clean_sql.upper() for keyword in ["DROP TABLE", "DELETE FROM", "TRUNCATE TABLE"]):
        return {
            "success": False,
            "error": "Destructive SQL commands are blocked in query execution tool for security.",
            "execution_time_ms": round((time.time() - start_time) * 1000, 2),
            "columns": [],
            "rows": [],
            "row_count": 0
        }

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(clean_sql)
        
        columns = [description[0] for description in cursor.description] if cursor.description else []
        rows = [list(row) for row in cursor.fetchall()]
        conn.close()

        execution_time_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "success": True,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "execution_time_ms": execution_time_ms,
            "query": clean_sql
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "execution_time_ms": round((time.time() - start_time) * 1000, 2),
            "columns": [],
            "rows": [],
            "row_count": 0,
            "query": clean_sql
        }

def get_schema() -> Dict[str, Any]:
    """Inspect tables, columns, types, and sample data for the LLM prompt or UI schema viewer."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    schema_info = {}
    for table in tables:
        cursor.execute(f"PRAGMA table_info({table});")
        columns = [{"name": col[1], "type": col[2], "notnull": bool(col[3]), "pk": bool(col[5])} for col in cursor.fetchall()]
        
        cursor.execute(f"SELECT * FROM {table} LIMIT 2;")
        sample_rows = [list(row) for row in cursor.fetchall()]

        cursor.execute(f"SELECT COUNT(*) FROM {table};")
        count = cursor.fetchone()[0]

        schema_info[table] = {
            "columns": columns,
            "total_rows": count,
            "sample_rows": sample_rows
        }

    conn.close()
    return schema_info

if __name__ == "__main__":
    init_db()
    res = execute_query("SELECT c.name, c.country, SUM(o.total_amount) as total_spent FROM customers c JOIN orders o ON c.id = o.customer_id GROUP BY c.id ORDER BY total_spent DESC LIMIT 5;")
    print("Test Query Columns:", res["columns"])
    print("Test Query Rows:", res["rows"])
