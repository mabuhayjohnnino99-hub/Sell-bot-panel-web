import sqlite3
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

ADMIN_TOKEN = "SELLBOT-SECRET-KEY"

BASE = Path(__file__).resolve().parent.parent
DB = BASE / "database.db"
env = Environment(loader=FileSystemLoader(BASE / "templates"))

def handler(request):
    token = request.get("query", {}).get("token")
    if token != ADMIN_TOKEN:
        return {
            "statusCode": 302,
            "headers": {"Location": "/login"}
        }

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
