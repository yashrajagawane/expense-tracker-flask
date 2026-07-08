"""
Expense Tracker — Flask + SQLite + SQLAlchemy.

Run locally:
    pip install -r requirements.txt
    python app.py
    # then open http://127.0.0.1:5000

When deployed behind a URL prefix (e.g. "/api"), set URL_PREFIX env var.
"""
from __future__ import annotations

import csv
import io
from calendar import month_name
from collections import defaultdict
from datetime import date, datetime
from functools import wraps

from flask import (
    Flask, Response, abort, flash, redirect, render_template, request, url_for,
)
from flask_login import (
    LoginManager, current_user, login_required, login_user, logout_user,
)
from flask_wtf import CSRFProtect
from sqlalchemy import func

from config import Config
from models import CATEGORIES, Budget, Transaction, User, db


# ----------------------------------------------------------------------
# App factory
# ----------------------------------------------------------------------
def create_app() -> Flask:
    prefix = Config.URL_PREFIX or ""
    static_url = f"{prefix}/static" if prefix else "/static"

    app = Flask(
        __name__,
        static_url_path=static_url,
        static_folder="static",
        template_folder="templates",
    )
    app.config.from_object(Config)
    if prefix:
        app.config["APPLICATION_ROOT"] = prefix

    # Trust reverse-proxy headers so Flask sees the correct scheme/host
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    CSRFProtect(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):  # noqa: ANN001
        return db.session.get(User, int(user_id))

    # Register routes on the app. If a prefix is required, we use a lightweight
    # blueprint. Otherwise routes are registered directly.
    register_routes(app, prefix)

    with app.app_context():
        db.create_all()
        _seed_demo_user()

    return app


# ----------------------------------------------------------------------
# Demo user seeding (idempotent)
# ----------------------------------------------------------------------
def _seed_demo_user() -> None:
    if User.query.filter_by(email="demo@demo.com").first():
        return
    u = User(name="Demo User", email="demo@demo.com")
    u.set_password("demo123")
    db.session.add(u)
    db.session.flush()

    today = date.today()
    samples = [
        (2500, "Salary", "income", "Monthly salary", today.replace(day=1)),
        (500, "Freelance", "income", "Side project", today.replace(day=5)),
        (120, "Food", "expense", "Groceries", today.replace(day=3)),
        (45, "Transport", "expense", "Fuel", today.replace(day=4)),
        (200, "Bills", "expense", "Internet + Electricity", today.replace(day=6)),
        (60, "Entertainment", "expense", "Movie night", today.replace(day=8)),
        (85, "Shopping", "expense", "Clothing", today.replace(day=10)),
        (30, "Medical", "expense", "Pharmacy", today.replace(day=12)),
    ]
    for amt, cat, ttype, desc, dt in samples:
        db.session.add(Transaction(
            user_id=u.id, amount=amt, category=cat, type=ttype,
            description=desc, date=dt,
        ))
    db.session.add(Budget(user_id=u.id, year=today.year, month=today.month, amount=1500))
    db.session.commit()


# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
def register_routes(app: Flask, prefix: str) -> None:  # noqa: C901
    p = prefix or ""

    def R(rule: str) -> str:
        """Prefix helper for @app.route strings."""
        return f"{p}{rule}"

    # ---- auth --------------------------------------------------------
    @app.route(R("/"), endpoint="index")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route(R("/signup"), methods=["GET", "POST"], endpoint="signup")
    def signup():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            pwd = request.form.get("password") or ""
            if not name or not email or len(pwd) < 6:
                flash("Please fill all fields (password ≥ 6 chars).", "error")
            elif User.query.filter_by(email=email).first():
                flash("An account with that email already exists.", "error")
            else:
                u = User(name=name, email=email)
                u.set_password(pwd)
                db.session.add(u)
                db.session.commit()
                login_user(u)
                flash("Welcome aboard!", "success")
                return redirect(url_for("dashboard"))
        return render_template("signup.html")

    @app.route(R("/login"), methods=["GET", "POST"], endpoint="login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))
        if request.method == "POST":
            email = (request.form.get("email") or "").strip().lower()
            pwd = request.form.get("password") or ""
            u = User.query.filter_by(email=email).first()
            if u and u.check_password(pwd):
                login_user(u)
                flash("Logged in.", "success")
                return redirect(url_for("dashboard"))
            flash("Invalid credentials.", "error")
        return render_template("login.html")

    @app.route(R("/logout"), endpoint="logout")
    @login_required
    def logout():
        logout_user()
        flash("Logged out.", "info")
        return redirect(url_for("login"))

    # ---- dashboard ---------------------------------------------------
    @app.route(R("/dashboard"), endpoint="dashboard")
    @login_required
    def dashboard():
        uid = current_user.id
        totals = _totals(uid)
        recent = (Transaction.query.filter_by(user_id=uid)
                  .order_by(Transaction.date.desc(), Transaction.id.desc())
                  .limit(6).all())
        today = date.today()
        budget = Budget.query.filter_by(
            user_id=uid, year=today.year, month=today.month
        ).first()
        month_spent = _month_expense(uid, today.year, today.month)
        budget_amount = budget.amount if budget else 0
        budget_used_pct = round((month_spent / budget_amount) * 100, 1) if budget_amount else 0
        return render_template(
            "dashboard.html",
            totals=totals,
            recent=recent,
            budget_amount=budget_amount,
            month_spent=month_spent,
            budget_used_pct=min(budget_used_pct, 999),
            budget_remaining=max(budget_amount - month_spent, 0),
        )

    # ---- transactions list ------------------------------------------
    @app.route(R("/transactions"), endpoint="transactions")
    @login_required
    def transactions():
        uid = current_user.id
        q = (request.args.get("q") or "").strip()
        cat = request.args.get("category") or ""
        ttype = request.args.get("type") or ""
        page = max(int(request.args.get("page", 1)), 1)
        per_page = 10

        query = Transaction.query.filter_by(user_id=uid)
        if q:
            query = query.filter(Transaction.description.ilike(f"%{q}%"))
        if cat:
            query = query.filter_by(category=cat)
        if ttype in ("income", "expense"):
            query = query.filter_by(type=ttype)

        query = query.order_by(Transaction.date.desc(), Transaction.id.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return render_template(
            "transactions.html",
            transactions=pagination.items,
            pagination=pagination,
            categories=CATEGORIES,
            q=q, cat=cat, ttype=ttype,
        )

    # ---- add / edit / delete transaction ----------------------------
    @app.route(R("/transactions/new"), methods=["GET", "POST"], endpoint="new_transaction")
    @login_required
    def new_transaction():
        if request.method == "POST":
            t = _tx_from_form(request.form)
            if isinstance(t, str):
                flash(t, "error")
            else:
                t.user_id = current_user.id
                db.session.add(t)
                db.session.commit()
                flash("Transaction added.", "success")
                return redirect(url_for("transactions"))
        return render_template(
            "transaction_form.html", categories=CATEGORIES, tx=None,
            form_action=url_for("new_transaction"), heading="Add Transaction",
        )

    @app.route(R("/transactions/<int:tx_id>/edit"), methods=["GET", "POST"], endpoint="edit_transaction")
    @login_required
    def edit_transaction(tx_id: int):
        tx = db.session.get(Transaction, tx_id)
        if not tx or tx.user_id != current_user.id:
            abort(404)
        if request.method == "POST":
            updated = _tx_from_form(request.form, existing=tx)
            if isinstance(updated, str):
                flash(updated, "error")
            else:
                db.session.commit()
                flash("Transaction updated.", "success")
                return redirect(url_for("transactions"))
        return render_template(
            "transaction_form.html", categories=CATEGORIES, tx=tx,
            form_action=url_for("edit_transaction", tx_id=tx.id),
            heading="Edit Transaction",
        )

    @app.route(R("/transactions/<int:tx_id>/delete"), methods=["POST"], endpoint="delete_transaction")
    @login_required
    def delete_transaction(tx_id: int):
        tx = db.session.get(Transaction, tx_id)
        if not tx or tx.user_id != current_user.id:
            abort(404)
        db.session.delete(tx)
        db.session.commit()
        flash("Transaction deleted.", "info")
        return redirect(url_for("transactions"))

    # ---- reports (Chart.js data) ------------------------------------
    @app.route(R("/reports"), endpoint="reports")
    @login_required
    def reports():
        uid = current_user.id
        monthly = _monthly_series(uid)
        cat_expense = _category_expense(uid)
        return render_template(
            "reports.html",
            monthly_labels=[m["label"] for m in monthly],
            monthly_income=[m["income"] for m in monthly],
            monthly_expense=[m["expense"] for m in monthly],
            cat_labels=list(cat_expense.keys()),
            cat_values=list(cat_expense.values()),
        )

    # ---- budget ------------------------------------------------------
    @app.route(R("/budget"), methods=["GET", "POST"], endpoint="budget")
    @login_required
    def budget():
        uid = current_user.id
        today = date.today()
        b = Budget.query.filter_by(user_id=uid, year=today.year, month=today.month).first()
        if request.method == "POST":
            try:
                amt = float(request.form.get("amount") or 0)
                if amt < 0:
                    raise ValueError
            except ValueError:
                flash("Enter a valid amount.", "error")
                return redirect(url_for("budget"))
            if b:
                b.amount = amt
            else:
                b = Budget(user_id=uid, year=today.year, month=today.month, amount=amt)
                db.session.add(b)
            db.session.commit()
            flash("Budget saved.", "success")
            return redirect(url_for("budget"))

        spent = _month_expense(uid, today.year, today.month)
        amount = b.amount if b else 0
        pct = round((spent / amount) * 100, 1) if amount else 0
        return render_template(
            "budget.html",
            budget_amount=amount, spent=spent,
            remaining=max(amount - spent, 0),
            pct=min(pct, 999),
            month_label=f"{month_name[today.month]} {today.year}",
        )

    # ---- profile -----------------------------------------------------
    @app.route(R("/profile"), methods=["GET", "POST"], endpoint="profile")
    @login_required
    def profile():
        u = current_user
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            new_pwd = request.form.get("password") or ""
            if not name or not email:
                flash("Name and email are required.", "error")
                return redirect(url_for("profile"))
            existing = User.query.filter_by(email=email).first()
            if existing and existing.id != u.id:
                flash("Email already in use.", "error")
                return redirect(url_for("profile"))
            u.name = name
            u.email = email
            if new_pwd:
                if len(new_pwd) < 6:
                    flash("Password must be ≥ 6 characters.", "error")
                    return redirect(url_for("profile"))
                u.set_password(new_pwd)
            db.session.commit()
            flash("Profile updated.", "success")
            return redirect(url_for("profile"))
        return render_template("profile.html", user=u)

    # ---- CSV export --------------------------------------------------
    @app.route(R("/export.csv"), endpoint="export_csv")
    @login_required
    def export_csv():
        rows = (Transaction.query.filter_by(user_id=current_user.id)
                .order_by(Transaction.date.desc()).all())
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["Date", "Type", "Category", "Description", "Amount"])
        for t in rows:
            w.writerow([t.date.isoformat(), t.type, t.category, t.description, t.amount])
        return Response(
            buf.getvalue(),
            mimetype="text/csv",
            headers={"Content-Disposition": "attachment; filename=transactions.csv"},
        )

    # ---- health check (used by preview URL healthchecks) ------------
    @app.route(R("/health"), endpoint="health")
    def health():
        return {"status": "ok"}


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------
def _totals(user_id: int) -> dict:
    income = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(
        user_id=user_id, type="income").scalar() or 0
    expense = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter_by(
        user_id=user_id, type="expense").scalar() or 0
    count = Transaction.query.filter_by(user_id=user_id).count()
    return {
        "income": round(income, 2),
        "expense": round(expense, 2),
        "balance": round(income - expense, 2),
        "count": count,
    }


def _month_expense(user_id: int, year: int, month: int) -> float:
    total = db.session.query(func.coalesce(func.sum(Transaction.amount), 0)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "expense",
        func.strftime("%Y", Transaction.date) == f"{year:04d}",
        func.strftime("%m", Transaction.date) == f"{month:02d}",
    ).scalar() or 0
    return round(total, 2)


def _monthly_series(user_id: int, months: int = 6) -> list[dict]:
    """Return last N months income/expense buckets (oldest-first)."""
    today = date.today()
    buckets = []
    for i in range(months - 1, -1, -1):
        y = today.year
        m = today.month - i
        while m <= 0:
            m += 12
            y -= 1
        buckets.append({"year": y, "month": m,
                        "label": f"{month_name[m][:3]} {str(y)[-2:]}",
                        "income": 0.0, "expense": 0.0})

    rows = Transaction.query.filter_by(user_id=user_id).all()
    for t in rows:
        for b in buckets:
            if t.date.year == b["year"] and t.date.month == b["month"]:
                b[t.type] += t.amount
                break
    for b in buckets:
        b["income"] = round(b["income"], 2)
        b["expense"] = round(b["expense"], 2)
    return buckets


def _category_expense(user_id: int) -> dict:
    rows = (db.session.query(Transaction.category, func.sum(Transaction.amount))
            .filter_by(user_id=user_id, type="expense")
            .group_by(Transaction.category).all())
    out = defaultdict(float)
    for cat, total in rows:
        out[cat] = round(total, 2)
    return dict(out)


def _tx_from_form(form, existing: Transaction | None = None):
    """Validate + build/update a Transaction from form data.

    Returns the Transaction on success or an error string on failure.
    """
    try:
        amount = float(form.get("amount") or 0)
    except ValueError:
        return "Amount must be a number."
    if amount <= 0:
        return "Amount must be greater than 0."

    category = form.get("category") or ""
    if category not in CATEGORIES:
        return "Invalid category."

    ttype = form.get("type")
    if ttype not in ("income", "expense"):
        return "Type must be income or expense."

    try:
        dt = datetime.strptime(form.get("date") or "", "%Y-%m-%d").date()
    except ValueError:
        return "Invalid date."

    description = (form.get("description") or "").strip()[:255]

    tx = existing or Transaction()
    tx.amount = amount
    tx.category = category
    tx.type = ttype
    tx.date = dt
    tx.description = description
    return tx


# ----------------------------------------------------------------------
# App instance (imported by uvicorn/ASGI wrapper AND by `python app.py`)
# ----------------------------------------------------------------------
app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
