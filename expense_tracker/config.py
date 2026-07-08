"""Application configuration."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    """Base config used by the Flask app."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me-in-prod")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'expense_tracker.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # If deployed behind a path prefix (e.g. "/api"), set URL_PREFIX so all
    # routes and static files are mounted correctly. Empty for local run.
    URL_PREFIX = os.environ.get("URL_PREFIX", "")

    WTF_CSRF_TIME_LIMIT = None  # tokens don't expire during long forms
    # Disable referer-based origin check (still keeps token check). Needed when
    # running behind a reverse proxy that rewrites scheme/host.
    WTF_CSRF_SSL_STRICT = False
    SESSION_COOKIE_SAMESITE = "Lax"
