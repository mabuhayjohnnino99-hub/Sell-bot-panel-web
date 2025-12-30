import sqlite3
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "database.db"
TEMPLATES = BASE / "templates"

env = Environment(loader=FileSystemLoader(TEMPLATES))

def handler(request):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT COUNT(*), SUM(price) FROM sales")
    orders, total = c.fetchone()

    c.execute("SELECT file, price, stock FROM products")
    products = c.fetchall()

    conn.close()

    html = env.get_template("dashboard.html").render(
        orders=orders,
        total=total or 0,
        products=products
    )

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
