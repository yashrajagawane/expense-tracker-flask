"# 💸 Ledger — Personal Expense Tracker

A **modern, full-stack personal finance app** built with **Flask + SQLite + SQLAlchemy** and a hand-crafted server-rendered UI (Jinja2 + vanilla JS + Chart.js). Track your income and expenses, set monthly budgets, visualise where your money goes, and export everything to CSV — all in one clean, responsive dashboard with dark & light themes.

> All amounts are displayed in **Indian Rupees (₹)**.

---

## ✨ Highlights

- 🔐 **Authentication** — Sign up, log in, log out. Passwords hashed with Werkzeug (`pbkdf2:sha256`). Server-side sessions via Flask-Login.
- 📊 **Dashboard** — Total income, total expenses, current balance, transaction count, monthly budget progress and recent activity, all at a glance.
- 💰 **Transactions** — Full CRUD across **13 categories** (Food, Shopping, Transport, Bills, Medical, Education, Travel, Entertainment, Salary, Freelance, Business, Investment, Other) with type (income / expense), amount, date, description.
- 🔎 **History** — Searchable, filterable (category + type), paginated transaction table.
- 📈 **Reports** — Chart.js visualisations:
  - Monthly **Income vs Expense** (last 6 months, bar chart)
  - **Expenses by Category** (doughnut chart)
- 🎯 **Budget** — Set a monthly cap; see spent / remaining / % used with a colour-coded progress bar (green → amber → red).
- 👤 **Profile** — Update name, email, and password anytime.
- 📤 **CSV Export** — One-click download of every transaction.
- 🎨 **UI/UX** — Sidebar navigation, modern cards, subtle animations, custom typography (Bricolage Grotesque + Inter + JetBrains Mono), responsive down to mobile, and a persistent **dark / light theme toggle**.
- 🛡️ **Security** — CSRF protection on every POST form (Flask-WTF), server-side form validation, HTTP-only session cookies, `SameSite=Lax`.
- 💬 **Flash messages** — Toast-style success / error / info notifications with auto-dismiss.

---

## 🧱 Tech Stack

| Layer      | Technology                                          |
| ---------- | --------------------------------------------------- |
| Language   | **Python 3.11+**                                    |
| Web        | **Flask 3.0**                                       |
| Auth       | **Flask-Login** + Werkzeug password hashing         |
| ORM        | **Flask-SQLAlchemy** (SQLAlchemy 2.x)               |
| Database   | **SQLite** (file-based, zero-config)                |
| Forms/CSRF | **Flask-WTF** + WTForms                             |
| Frontend   | Jinja2 templates + vanilla JS + **Chart.js 4** (CDN) + **Font Awesome 6** (CDN) |
| Fonts      | Bricolage Grotesque, Inter, JetBrains Mono (Google Fonts) |

---

## 📁 Project Structure

```
expense_tracker/
│
├── app.py               # Flask app factory, all routes, demo seed
├── models.py            # SQLAlchemy models: User, Transaction, Budget
├── config.py            # Configuration (SECRET_KEY, DB URI, CSRF, prefix)
├── requirements.txt     # Python dependencies
├── README.md
│
├── templates/           # Jinja2 templates
│   ├── base.html            # Shared layout: sidebar + flash + theme
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── transactions.html    # List + filters + pagination
│   ├── transaction_form.html# Add / edit
│   ├── reports.html         # Chart.js charts
│   ├── budget.html
│   └── profile.html
│
├── static/
│   ├── css/style.css        # Full design system
│   └── js/main.js           # Theme toggle, flash auto-dismiss
│
└── instance/
    └── expense_tracker.db   # Auto-created on first run
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11** or newer
- **pip** and **venv** (bundled with Python)

### 1. Clone / navigate to the folder

```bash
cd expense_tracker
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python app.py
```

Then open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser.

The SQLite database and demo user are auto-created on first launch — no migrations, no seed scripts to run manually.

---

## 🔑 Demo Account

A pre-populated demo user is seeded on first startup so you can preview everything instantly:

| Field    | Value              |
| -------- | ------------------ |
| Email    | `demo@demo.com`    |
| Password | `demo123`          |

The demo comes with **8 sample transactions** (₹3,000 income, ₹540 expenses across multiple categories) and a **₹1,500 monthly budget** — enough to see every chart, filter, and card populated.

Or create your own account at **`/signup`**.

---

## 🧭 Routes / Pages

| Path                          | Method    | Description                              |
| ----------------------------- | --------- | ---------------------------------------- |
| `/`                           | GET       | Home — redirects to dashboard or login   |
| `/signup`                     | GET, POST | Create a new account                     |
| `/login`                      | GET, POST | Log in                                   |
| `/logout`                     | GET       | Log out (auth required)                  |
| `/dashboard`                  | GET       | Overview cards + recent activity + budget|
| `/transactions`               | GET       | Paginated table with search & filters    |
| `/transactions/new`           | GET, POST | Add a transaction                        |
| `/transactions/<id>/edit`     | GET, POST | Edit a transaction                       |
| `/transactions/<id>/delete`   | POST      | Delete a transaction (CSRF-guarded)      |
| `/reports`                    | GET       | Chart.js visualisations                  |
| `/budget`                     | GET, POST | View & set current month's budget        |
| `/profile`                    | GET, POST | Update name / email / password           |
| `/export.csv`                 | GET       | Download all transactions as CSV         |
| `/health`                     | GET       | JSON health probe (`{\"status\":\"ok\"}`)    |

---

## 🗄️ Database Schema

Three simple SQLAlchemy models — all foreign-keyed to `User` with cascading deletes.

### `User`
| Column         | Type       | Notes                            |
| -------------- | ---------- | -------------------------------- |
| id             | Integer PK |                                  |
| name           | String(80) | Required                         |
| email          | String(120)| Unique, indexed                  |
| password_hash  | String(256)| Werkzeug hash (never plain text) |
| created_at     | DateTime   | UTC                              |

### `Transaction`
| Column       | Type        | Notes                             |
| ------------ | ----------- | --------------------------------- |
| id           | Integer PK  |                                   |
| user_id      | FK → users  | Indexed                           |
| amount       | Float       | Always positive                   |
| category     | String(50)  | One of 13 predefined categories   |
| date         | Date        |                                   |
| description  | String(255) |                                   |
| type         | String(10)  | `income` or `expense`             |
| created_at   | DateTime    | UTC                               |

### `Budget`
| Column   | Type        | Notes                                     |
| -------- | ----------- | ----------------------------------------- |
| id       | Integer PK  |                                           |
| user_id  | FK → users  |                                           |
| year     | Integer     |                                           |
| month    | Integer     | 1–12                                      |
| amount   | Float       |                                           |
|          |             | **Unique** on (`user_id`, `year`, `month`)|

---

## ⚙️ Configuration

All configuration is centralised in `config.py` and can be overridden with environment variables — no need to edit code for local vs. production.

| Env var         | Default                                | Purpose                                                  |
| --------------- | -------------------------------------- | -------------------------------------------------------- |
| `SECRET_KEY`    | `dev-secret-change-me-in-prod`         | Signs session cookies & CSRF tokens — **set in prod!**   |
| `DATABASE_URL`  | `sqlite:///instance/expense_tracker.db`| SQLAlchemy DB URI (works with Postgres, MySQL, etc.)     |
| `URL_PREFIX`    | *(empty)*                              | Mount the app under a path prefix (e.g. `/api`). Leave empty for local run. |

### Example: production launch

```bash
export SECRET_KEY=\"$(python -c 'import secrets; print(secrets.token_hex(32))')\"
export DATABASE_URL=\"postgresql+psycopg://user:pwd@localhost/ledger\"
python app.py
```

---

## 🎨 Design System

Deliberately built to avoid the generic \"AI-slop\" look:

- **Palette:** warm cream (`#f5f2eb`) + deep charcoal (`#0e1116`) + a signature **lime accent** (`#c8f45c`) reserved for balance & brand.
- **Semantic colours:** emerald green for income (`#4ade80`), coral for expense (`#fb7185`), amber for budget warnings.
- **Typography:** Bricolage Grotesque (display headings) · Inter (body) · JetBrains Mono (all numbers, giving the ledger its fintech feel).
- **Motion:** staggered card entrance animations, smooth width transitions on progress bars, transform-based button hover lifts.
- **Dark mode:** true dark surfaces (not just inverted colours), lime becomes the primary CTA, choice is persisted in `localStorage`.

---

## 🛡️ Security Notes

- Passwords are **never stored in plain text** — `werkzeug.security.generate_password_hash` uses `pbkdf2:sha256` by default.
- Every `POST` form includes a hidden `csrf_token` validated server-side by Flask-WTF.
- All routes that mutate data or read user-specific info are wrapped in `@login_required`.
- `SESSION_COOKIE_SAMESITE = \"Lax\"` protects against basic CSRF via cross-site navigation.
- Server-side validation of amounts, dates, categories, and transaction types — the client-side attrs are only hints.
- In production, **always set a strong `SECRET_KEY`** via env var and put the app behind HTTPS.

---

## 🧪 Testing the App

Once running, walk through this smoke test:

1. Open the app → auto-redirects to `/login`.
2. Sign in with `demo@demo.com` / `demo123` — you land on the **dashboard** populated with 4 stat cards, a budget progress bar and recent activity.
3. Click **Transactions** in the sidebar. Try:
   - Searching for \"salary\"
   - Filtering by category \"Food\"
   - Filtering by type \"Income\"
4. Click **Add** → create a new transaction — it appears in the table with a success toast.
5. Click ✏️ on any row to edit; 🗑️ to delete (with confirm dialog).
6. Open **Reports** — both charts render with the demo data.
7. Open **Budget** — change the amount to ₹2,000 and watch the progress bar re-scale.
8. Toggle the sidebar **Dark / Light** button — the theme flips and persists on refresh.
9. Click **Export CSV** — a `transactions.csv` downloads with all rows.
10. **Logout** — you're bounced back to `/login`.

---

## 📦 Requirements

```
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Flask-WTF==1.2.1
WTForms==3.1.2
Werkzeug==3.0.3
```

---

## 🗺️ Roadmap Ideas

- 🔁 **Recurring transactions** (auto-log rent, salary, subscriptions)
- 🌐 **Multi-currency** support with per-user default
- 📥 **CSV import** to bulk-load history from other trackers
- 🔗 **Shareable read-only monthly summary link** (great for splitting with family / accountant)
- 📧 **Email alerts** when you cross budget thresholds (via SendGrid / Resend)
- 📅 **Date-range filter** on the transactions page
- 🎯 **Per-category budgets** in addition to the overall monthly cap
- 📱 **Progressive Web App (PWA)** — install-to-home-screen on Android/iOS

---

## 🤝 Contributing

This is a small, self-contained project — perfect for hacking on. To contribute:

1. Fork the repo.
2. Create a feature branch: `git checkout -b feature/awesome-thing`.
3. Follow the existing code style (PEP-8, small commented functions, no over-engineering).
4. Add / update tests if you introduce new logic.
5. Open a PR.

---

## 📄 License

Released under the **MIT License** — do whatever you want, just don't blame the author if you accidentally track your rupees a bit too accurately. 🙃

---

## 🙋 FAQ

**Q: Can I use this for real money tracking?**
A: Yes — it's fully functional. Just remember to set a strong `SECRET_KEY` and run behind HTTPS.

**Q: How do I reset the database?**
A: Delete `instance/expense_tracker.db` and restart the app. It will be recreated with a fresh demo user.

**Q: Can I change the currency from ₹?**
A: Every currency symbol lives in the Jinja templates (search for `₹`). Swap it globally in seconds — a future release will expose this as a per-user setting.

**Q: Why Flask over Django / FastAPI?**
A: For a small personal app, Flask + Jinja hits the sweet spot: everything renders server-side (no build step, no JS framework required), the whole app fits in one `app.py` you can read in ten minutes, and SQLite gives you zero-config persistence. FastAPI would add async & typed schemas but requires a separate frontend; Django would be overkill for three tables and eight pages.

---

Made with ❤️ and a lot of chai. Happy tracking!
"
