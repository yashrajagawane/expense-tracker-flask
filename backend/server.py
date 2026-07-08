"""
ASGI bridge: exposes the Flask expense-tracker app to uvicorn (managed by
supervisor). All routes are mounted under /api because the platform ingress
routes preview-URL /api/* → port 8001.
"""
import os
import sys

# Ensure the Flask app is on the path
EXPENSE_APP_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "expense_tracker")
if EXPENSE_APP_DIR not in sys.path:
    sys.path.insert(0, EXPENSE_APP_DIR)

# Force URL prefix so all Flask routes live under /api
os.environ.setdefault("URL_PREFIX", "/api")
os.environ.setdefault("SECRET_KEY", "ledger-dev-secret")

from asgiref.wsgi import WsgiToAsgi  # noqa: E402
from app import app as flask_app  # noqa: E402

app = WsgiToAsgi(flask_app)
