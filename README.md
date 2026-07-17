<div align="center">

# 💸 Ledger

### A personal expense tracker that actually feels good to use

*Flask · SQLite · SQLAlchemy · Chart.js — server-rendered, zero build step, ready in 2 minutes*

[![Python](https://img.shields.io/badge/Python-3.11+-c8f45c?style=flat-square&logo=python&logoColor=black)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-0e1116?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.x-d71f00?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlalchemy.org/)
[![License](https://img.shields.io/badge/License-MIT-4ade80?style=flat-square)](#-license)
[![Status](https://img.shields.io/badge/status-active-fb7185?style=flat-square)](#)

**[🚀 Live Demo](https://your-deployed-url-here.com)** · **[🖼️ Preview](#-preview)** · **[📖 Routes](#-routes)** · **[🗄️ Schema](#-database-schema)** · **[🤝 Contributing](#-contributing)**

</div>

---

> [!TIP]
> **Try it instantly** — no signup needed. Log in with `demo@demo.com` / `demo123` on the [live demo](https://your-deployed-url-here.com) and see a fully populated dashboard, charts, and budget in one click.

## 📑 Table of Contents

- [Preview](#-preview)
- [Why Ledger?](#why-ledger)
- [What's Inside](#-whats-inside)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Project Structure](#-project-structure)
- [Routes](#-routes)
- [Database Schema](#-database-schema)
- [Configuration](#-configuration)
- [Design Language](#-design-language)
- [Security](#-security)

---

## 🖼️ Preview

<div align="center">

| Dashboard | Transactions |
|:---:|:---:|
| ![Dashboard](docs/screenshots/dashboard.png) | ![Transactions](docs/screenshots/transactions.png) |
| Income, expenses, and balance at a glance, plus budget progress | Full CRUD table with search, filters, and pagination |

| Reports | Budget |
|:---:|:---:|
| ![Reports](docs/screenshots/reports.png) | ![Budget](docs/screenshots/budget.png) |
| Income-vs-expense bar chart and category doughnut chart | Monthly spending cap with color-coded progress |

</div>

> 📸 Drop your own captures into `docs/screenshots/` using the filenames above (recommended: **1280×800px, PNG**) and they'll render automatically here. Good pages to capture: `/dashboard`, `/transactions`, `/reports`, `/budget`.

<br>

## Why Ledger?

Most expense trackers are either bloated SaaS products or bare-bones scripts. Ledger sits in between — **a real, full-stack app you can read end to end in ten minutes**, with the polish (dark mode, charts, CSV export) you'd expect from something you'd actually use every day to track your ₹.

<br>

## ✨ What's Inside

<table>
<tr>
<td width="50%" valign="top">

**🔐 Auth & Security**
- Signup / login / logout
- Passwords hashed (`pbkdf2:sha256`)
- CSRF protection on every form
- Session cookies, `SameSite=Lax`

**📊 Dashboard**
- Income, expenses, balance at a glance
- Budget progress bar
- Recent activity feed

**💰 Transactions**
- Full CRUD, 13 categories
- Income / expense typing
- Search, filter, pagination

</td>
<td width="50%" valign="top">

**📈 Reports**
- Income vs Expense (6-month bar chart)
- Expenses by Category (doughnut chart)
- Powered by Chart.js 4

**🎯 Budgets**
- Monthly cap per user
- Color-coded progress: 🟢 → 🟡 → 🔴

**🎨 Experience**
- Persistent dark / light theme
- Toast notifications
- Responsive down to mobile

</td>
</tr>
</table>

<br>

## 🧱 Tech Stack

| Layer      | Technology                                                     |
| :--------- | :--------------------------------------------------------------|
| Language   | Python 3.11+                                                   |
| Web        | Flask 3.0                                                      |
| Auth       | Flask-Login + Werkzeug                                         |
| ORM        | Flask-SQLAlchemy (SQLAlchemy 2.x)                               |
| Database   | SQLite (Postgres/MySQL-ready via env var)                       |
| Forms/CSRF | Flask-WTF + WTForms                                             |
| Frontend   | Jinja2 · vanilla JS · Chart.js 4 · Font Awesome 6               |
| Fonts      | Bricolage Grotesque · Inter · JetBrains Mono                    |

<br>

## 🏗️ Architecture

```mermaid
flowchart LR
    B[Browser] -->|"HTML forms + fetch()"| F[Flask App<br/>app.py routes]
    F --> J[Jinja2 Templates<br/>+ static CSS/JS]
    F --> Auth[Flask-Login session<br/>+ Flask-WTF CSRF]
    F --> ORM[Flask-SQLAlchemy ORM]
    ORM --> DB[(SQLite<br/>Postgres/MySQL-ready)]
```

Everything is server-rendered — no separate frontend build, no API layer to keep in sync. A request comes in, Flask authenticates the session, SQLAlchemy reads/writes the database, and Jinja2 renders the response directly.

<br>

## 🚀 Quick Start

```bash
git clone https://github.com/your-username/ledger.git
cd ledger

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** — the database and demo user are created automatically. No migrations, no seed scripts.

<br>

## 📁 Project Structure

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
├── docs/
│   └── screenshots/           # Drop preview images here (see Preview section)
└── instance/
    └── expense_tracker.db    # auto-created
```

<br>

## 🧭 Routes

| Path                         | Method    | Description                          |
| :---------------------------- | :--------- | :------------------------------------ |
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

<br>

## 🗄️ Database Schema

```
User ──┬── Transaction  (amount, category, date, type, description)
       └── Budget       (year, month, amount — unique per user/month)
```

All child tables cascade-delete with their parent `User`. Full column details:

<details>
<summary><b>Click to expand column-level schema</b></summary>
<br>

**User** — `id`, `name`, `email` (unique), `password_hash`, `created_at`

**Transaction** — `id`, `user_id` (FK), `amount`, `category` (1 of 13), `date`, `description`, `type` (`income`/`expense`), `created_at`

**Budget** — `id`, `user_id` (FK), `year`, `month`, `amount` — unique on (`user_id`, `year`, `month`)

</details>

<br>

## ⚙️ Configuration

Set via environment variables — no code changes needed for prod:

| Env var        | Default                                 | Purpose                             |
| :------------- | :---------------------------------------- | :------------------------------------ |
| `SECRET_KEY`   | `dev-secret-change-me-in-prod`          | Signs sessions & CSRF tokens         |
| `DATABASE_URL` | `sqlite:///instance/expense_tracker.db` | DB URI (Postgres/MySQL compatible)  |
| `URL_PREFIX`   | *(empty)*                                | Mount under a path prefix, e.g. `/api` |

```bash
# production example
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
export DATABASE_URL="postgresql+psycopg://user:pwd@localhost/ledger"
python app.py
```

<br>

## 🎨 Design Language

<div align="center">

`#f5f2eb` cream · `#0e1116` charcoal · `#c8f45c` lime accent
`#4ade80` income · `#fb7185` expense · amber budget warnings

</div>

Typography pairs **Bricolage Grotesque** for headings, **Inter** for body text, and **JetBrains Mono** for every number on the screen — giving the whole app a fintech feel. Dark mode uses true dark surfaces (not just inverted colors) and persists via `localStorage`.

<br>

## 🛡️ Security

- Passwords hashed with `pbkdf2:sha256` — never stored plain
- CSRF token on every POST form (Flask-WTF)
- `@login_required` on all data-mutating/user-specific routes
- `SESSION_COOKIE_SAMESITE = "Lax"`
- Server-side validation of amounts, dates, categories, types
- ⚠️ Always set a strong `SECRET_KEY` and use HTTPS in production

<br>

## 🗺️ Roadmap

- [ ] Recurring transactions (rent, salary, subscriptions)
- [ ] Multi-currency support
- [ ] CSV import
- [ ] Shareable read-only monthly summary link
- [ ] Email alerts on budget thresholds
- [ ] Date-range filter on transactions page
- [ ] Per-category budgets
- [ ] PWA (install-to-home-screen)

<br>

## 🙋 FAQ

<details>
<summary><b>Can I use this for real money tracking?</b></summary>
<br>
Yes. Just set a strong <code>SECRET_KEY</code> and run behind HTTPS.
</details>

<details>
<summary><b>How do I reset the database?</b></summary>
<br>
Delete <code>instance/expense_tracker.db</code> and restart — it recreates with a fresh demo user.
</details>

<details>
<summary><b>Can I change the currency from ₹?</b></summary>
<br>
Yes — search templates for <code>₹</code> and swap it. A per-user currency setting is planned.
</details>

<details>
<summary><b>Why Flask over Django / FastAPI?</b></summary>
<br>
For a small app with three tables and eight pages, Flask + Jinja renders everything server-side with no build step and no separate frontend — the whole app fits in one readable <code>app.py</code>.
</details>

<br>

## 🤝 Contributing

1. Fork the repo
2. `git checkout -b feature/awesome-thing`
3. Follow PEP-8, keep functions small and commented
4. Add/update tests for new logic
5. Open a PR

<br>

## 📄 License

Released under the **MIT License** — do whatever you want, just don't blame the author if you accidentally track your rupees a bit too accurately. 🙃

<br>

<div align="center">

Made with ❤️ and a lot of chai

</div>
