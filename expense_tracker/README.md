# Ledger — Expense Tracker

A clean, modern full-stack **expense tracker** built with **Flask + SQLite + SQLAlchemy**.

- Authentication (signup / login / logout, hashed passwords, sessions)
- Dashboard: total income, total expenses, current balance, transaction count
- Full CRUD on transactions with 13 built-in categories
- Searchable / filterable / paginated transaction history
- Reports (Chart.js): last-6-month income vs expense, category donut
- Monthly budget with progress bar
- Profile: update name, email, password
- Dark & light modes, responsive design, sidebar navigation
- CSRF protection (Flask-WTF), flash messages, CSV export

## Project structure

```
expense_tracker/
├── app.py              # Flask app & routes
├── models.py           # SQLAlchemy models: User, Transaction, Budget
├── config.py           # Configuration
├── requirements.txt
├── templates/          # Jinja2 templates
├── static/             # CSS + JS
├── instance/           # SQLite DB (auto-created)
└── README.md
```

## Run locally

```bash
cd expense_tracker
python -m venv .venv && source .venv/bin/activate      # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000**

## Demo account

A demo user is auto-seeded on first run:

- **Email:** `demo@demo.com`
- **Password:** `demo123`

## Notes

- The DB file lives at `instance/expense_tracker.db` and is created on first run.
- Set `SECRET_KEY` env var in production.
- To deploy behind a URL prefix (reverse proxy), set `URL_PREFIX=/your-prefix`.
