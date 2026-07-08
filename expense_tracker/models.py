"""SQLAlchemy models: User, Transaction, Budget."""
from datetime import datetime, date

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

# Allowed transaction categories (kept here so both models & forms share them)
CATEGORIES = [
    "Food", "Shopping", "Transport", "Bills", "Medical", "Education",
    "Travel", "Entertainment", "Salary", "Freelance", "Business",
    "Investment", "Other",
]


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    transactions = db.relationship(
        "Transaction", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    budgets = db.relationship(
        "Budget", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    # --- password helpers ---
    def set_password(self, raw: str) -> None:
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw: str) -> bool:
        return check_password_hash(self.password_hash, raw)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    description = db.Column(db.String(255), default="")
    # 'income' or 'expense'
    type = db.Column(db.String(10), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Budget(db.Model):
    """One budget per (user, year, month)."""
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("user_id", "year", "month", name="uq_user_year_month"),
    )
