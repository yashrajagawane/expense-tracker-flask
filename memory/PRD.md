# Ledger — Expense Tracker · PRD

## Original problem statement
Build a modern full-stack **Expense Tracker** web application.

**Stack requested:** HTML / CSS / JavaScript · Python Flask · SQLite · SQLAlchemy ORM.
Delivered as a clean, modular, responsive project with the specified folder layout.

## Delivered architecture
- **Backend:** Flask 3 + Flask-SQLAlchemy + Flask-Login + Flask-WTF (CSRF), SQLite via SQLAlchemy.
- **Frontend:** Server-rendered Jinja2 templates + vanilla JS + Chart.js (CDN) + Font Awesome (CDN).
- **Deployment shim:** In this container the app is served by the pre-existing uvicorn/supervisor on port 8001 via a thin `asgiref.WsgiToAsgi` bridge (`/app/backend/server.py`). All routes mount under `/api` because the platform ingress routes preview-URL `/api/*` → 8001. Standalone local run (`python app.py`) works without any prefix.

Project layout (as requested):
```
/app/expense_tracker/
├── app.py              # Flask app + all routes + seed
├── models.py           # SQLAlchemy models: User, Transaction, Budget
├── config.py           # Configuration
├── requirements.txt
├── templates/          # base, login, signup, dashboard, transactions, transaction_form, reports, budget, profile
├── static/css/style.css
├── static/js/main.js
├── instance/expense_tracker.db
└── README.md
```

## User personas
- **Individual budget tracker** — wants a simple, private ledger to log income + expenses, see spending patterns, and hit monthly budgets.

## Core requirements (static)
1. Auth: signup, login, logout, password hashing, sessions
2. Dashboard: total income, total expenses, current balance, transaction count
3. Transactions: full CRUD across 13 categories (Food, Shopping, Transport, Bills, Medical, Education, Travel, Entertainment, Salary, Freelance, Business, Investment, Other)
4. Transaction history: searchable/filterable/paginated table
5. Reports: Chart.js — monthly income vs expense + category-wise expenses
6. Budget: monthly cap with progress bar (used / remaining / %)
7. Profile: update name, email, password
8. UI: responsive, sidebar nav, dark & light mode, modern cards, icons, animations
9. Security: password hashing, form validation, CSRF
10. DB models: User, Transaction, Budget (SQLAlchemy)
11. Extras: CSV export, flash messages, pagination

## What's implemented (2026-07-08)
- ✅ All 11 requirement areas above
- ✅ 13 categories exactly as listed
- ✅ Distinctive UI: warm cream + deep ink palette, lime accent for income, coral for expense; Bricolage Grotesque / Inter / JetBrains Mono fonts; grain overlay on auth page; staggered card rise-in animations
- ✅ Auto-seeded demo user with 8 sample transactions and a $1500 monthly budget
- ✅ Dark/light theme toggle persisted in localStorage; charts re-render on theme change
- ✅ CSRF token on every POST form (login, signup, add/edit/delete tx, budget, profile)
- ✅ data-testid attributes on every interactive element
- ✅ Testing agent verified 100% backend & frontend success

## Test / verification status (iteration_1.json)
Passed: health, CSRF, auth guard, demo login, dashboard stats ($3000 / $540 / $2460 / 8), budget block, transactions table + testids, search filter, add transaction, reports charts, budget save, theme toggle, logout, CSV export headers, invalid credential rejection.

Deferred to future iteration (not blocking): exhaustive signup form, edit/delete UI actions, category/type dropdown filters, profile password change re-login, pagination beyond 10 rows, mobile breakpoint.

## Prioritized backlog
- **P1** — Add explicit tests for edit/delete, profile password change round-trip, pagination.
- **P1** — Optional: date-range filter on Transactions page.
- **P2** — Recurring transactions (auto-log monthly salary, rent, etc).
- **P2** — Multi-currency (per-user default currency + FX display).
- **P2** — Data import: upload CSV to bulk-add historical transactions.
- **P3** — Email budget-overrun alerts (SendGrid / Resend).
- **P3** — Shareable read-only monthly summary link.

## Next tasks
- Ship to the user; collect feedback on which P1/P2 to tackle next.
