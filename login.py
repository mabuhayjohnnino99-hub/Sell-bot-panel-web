from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from urllib.parse import parse_qs

ADMIN_USER = "admin"
ADMIN_PASS = "12345"
ADMIN_TOKEN = "SELLBOT-SECRET-KEY"

BASE = Path(__file__).resolve().parent.parent
env = Environment(loader=FileSystemLoader(BASE / "templates"))

def handler(request):
    if request.get("method") == "POST":
        body = parse_qs(request.get("body", ""))
        user = body.get("username", [""])[0]
        pw = body.get("password", [""])[0]

        if user == ADMIN_USER and pw == ADMIN_PASS:
            return {
                "statusCode": 302,
                "headers": {
                    "Location": f"/?token={ADMIN_TOKEN}"
                }
            }

    html = env.get_template("login.html").render()
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/html"},
        "body": html
    }
