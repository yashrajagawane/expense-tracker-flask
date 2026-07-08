# 💸 Ledger — Personal Expense Tracker

A full-stack personal finance app built with **Flask + SQLite + SQLAlchemy**, with a server-rendered UI (Jinja2 + vanilla JS + Chart.js). Track income and expenses, set monthly budgets, visualize spending, and export to CSV — all in a clean, responsive dashboard with dark/light themes.

> All amounts are displayed in **Indian Rupees (₹)**.

🔗 **Live Demo:** [https://your-deployed-url-here.com](https://your-deployed-url-here.com) <!-- Replace with your actual deployment URL -->

**Demo login:** `demo@demo.com` / `demo123`

---

## Screenshots

<!-- Add screenshots or a GIF here, e.g.:
![Dashboard](docs/screenshots/dashboard.png)
![Reports](docs/screenshots/reports.png)
-->

---

## Features

- **Authentication** — Signup/login/logout, passwords hashed with `pbkdf2:sha256`, server-side sessions via Flask-Login
- **Dashboard** — Income, expenses, balance, transaction count, budget progress, recent activity
- **Transactions** — Full CRUD, 13 categories, income/expense type, amount, date, description
- **History** — Searchable, filterable (category + type), paginated table
- **Reports** — Chart.js: Income vs Expense (6-month bar chart), Expenses by Category (doughnut chart)
- **Budget** — Monthly cap with color-coded progress (green → amber → red)
- **Profile** — Update name, email, password
- **CSV Export** — One-click download of all transactions
- **Theme** — Persistent dark/light toggle
- **Security** — CSRF protection (Flask-WTF), server-side validation, HttpOnly cookies, `SameSite=Lax`

---

## Tech Stack

| Layer      | Technology                                                     |
| ---------- | ---------------------------------------------------------------|
| Language   | Python 3.11+                                                   |
| Web        | Flask 3.0                                                      |
| Auth       | Flask-Login + Werkzeug                                         |
| ORM        | Flask-SQLAlchemy (SQLAlchemy 2.x)                               |
| Database   | SQLite                                                          |
| Forms/CSRF | Flask-WTF + WTForms                                             |
| Frontend   | Jinja2 + vanilla JS + Chart.js 4 (CDN) + Font Awesome 6 (CDN)  |
| Fonts      | Bricolage Grotesque, Inter, JetBrains Mono                      |

---

## Quick Start

```bash
git clone https://github.com/your-username/ledger.git
cd ledger

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**. The SQLite database and demo user are auto-created on first run — no migrations needed.

---

## Project Structure

```
expense_tracker/
├── app.py                    # Flask app, routes, demo seed
├── models.py                 # User, Transaction, Budget
├── config.py                 # SECRET_KEY, DB URI, CSRF, prefix
├── requirements.txt
├── templates/
│   ├── base.html
│   ├── login.html / signup.html
│   ├── dashboard.html
│   ├── transactions.html
│   ├── transaction_form.html
│   ├── reports.html
│   ├── budget.html
│   └── profile.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── instance/
    └── expense_tracker.db    # auto-created
```

---

## Routes

| Path                         | Method    | Description                          |
| ---------------------------- | --------- | ------------------------------------- |
| `/`                          | GET       | Redirects to dashboard or login       |
| `/signup`                    | GET, POST | Create account                        |
| `/login`                     | GET, POST | Log in                                |
| `/logout`                    | GET       | Log out                               |
| `/dashboard`                 | GET       | Overview cards + recent activity      |
| `/transactions`              | GET       | Paginated table, search & filters     |
| `/transactions/new`          | GET, POST | Add transaction                       |
| `/transactions/<id>/edit`    | GET, POST | Edit transaction                      |
| `/transactions/<id>/delete`  | POST      | Delete transaction (CSRF-guarded)     |
| `/reports`                   | GET       | Chart.js visualizations               |
| `/budget`                    | GET, POST | View/set current month's budget       |
| `/profile`                   | GET, POST | Update name/email/password            |
| `/export.csv`                | GET       | Download all transactions as CSV      |
| `/health`                    | GET       | JSON health check                     |

---

## Database Schema

**User** — `id`, `name`, `email` (unique), `password_hash`, `created_at`

**Transaction** — `id`, `user_id` (FK), `amount`, `category` (1 of 13), `date`, `description`, `type` (`income`/`expense`), `created_at`

**Budget** — `id`, `user_id` (FK), `year`, `month`, `amount` — unique on (`user_id`, `year`, `month`)

All tables cascade-delete with their parent `User`.

---

## Configuration

Set via environment variables — no code changes needed for prod:

| Env var        | Default                                 | Purpose                             |
| -------------- | ---------------------------------------- | ------------------------------------ |
| `SECRET_KEY`   | `dev-secret-change-me-in-prod`          | Signs sessions & CSRF tokens         |
| `DATABASE_URL` | `sqlite:///instance/expense_tracker.db` | DB URI (Postgres/MySQL compatible)  |
| `URL_PREFIX`   | *(empty)*                                | Mount under a path prefix, e.g. `/api` |

**Production example:**

```bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export DATABASE_URL="postgresql+psycopg://user:pwd@localhost/ledger"
python app.py
```

---

## Design

- **Palette:** cream (`#f5f2eb`), charcoal (`#0e1116`), lime accent (`#c8f45c`)
- **Semantic:** emerald for income (`#4ade80`), coral for expense (`#fb7185`), amber for budget warnings
- **Type:** Bricolage Grotesque (headings), Inter (body), JetBrains Mono (numbers)
- **Dark mode:** true dark surfaces, persisted in `localStorage`

---

## Security

- Passwords hashed with `pbkdf2:sha256`, never stored plain
- CSRF token on every POST form (Flask-WTF)
- `@login_required` on all data-mutating/user-specific routes
- `SESSION_COOKIE_SAMESITE = "Lax"`
- Server-side validation of amounts, dates, categories, types
- Always set a strong `SECRET_KEY` and use HTTPS in production

---

## Requirements

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.2
Werkzeug==3.0.3
```

---

## Roadmap

- [ ] Recurring transactions (rent, salary, subscriptions)
- [ ] Multi-currency support
- [ ] CSV import
- [ ] Shareable read-only monthly summary link
- [ ] Email alerts on budget thresholds
- [ ] Date-range filter on transactions page
- [ ] Per-category budgets
- [ ] PWA (install-to-home-screen)

---

## Contributing

1. Fork the repo
2. `git checkout -b feature/awesome-thing`
3. Follow PEP-8, keep functions small and commented
4. Add/update tests for new logic
5. Open a PR

---

## FAQ

**Can I use this for real money tracking?**
Yes. Just set a strong `SECRET_KEY` and run behind HTTPS.

**How do I reset the database?**
Delete `instance/expense_tracker.db` and restart — it recreates with a fresh demo user.

**Can I change the currency from ₹?**
Yes, search templates for `₹` and swap it. A per-user currency setting is planned.

**Why Flask over Django/FastAPI?**
For a small app with three tables and eight pages, Flask + Jinja renders everything server-side with no build step and no separate frontend — the whole app fits in one readable `app.py`.

---

## License

MIT — do what you want, just don't blame the author if you track your rupees a bit too accurately. 🙃
