# Timetable Backend

## Tech Stack

- Python 3.11+ / Django 5 + Django REST Framework
- PostgreSQL 14+
- `django-environ` for configuration
- Optional dev tools: `black`, `isort`, `flake8`, `pytest`, `pre-commit`

---

## TL;DR (Quickstart)

```bash
# 1) Clone / init your repo, then in project root:
python -m venv .env
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install --upgrade pip

# 2) Install deps
pip install django djangorestframework psycopg[binary] django-environ
pip install -r requirements.txt

# 3) Start Postgres (Docker recommended)
docker compose up -d  # requires docker-compose.yml provided below

# 4) Migrate and create admin
python manage.py migrate
python manage.py createsuperuser

# 5) Seed pilot dataset (Phase‑1 scope)
python manage.py seed_pilot

# 6) Run the server
python manage.py runserver
# open http://127.0.0.1:8000/admin
```

---

## Configuration

### Settings split
- `config/settings/base.py` – shared config (DB, DRF, middleware, TEMPLATES).
- `config/settings/local.py` – dev overrides (`DEBUG=True`, `ALLOWED_HOSTS=["*"]`).
- `config/__init__.py` sets default: `config.settings.local`.

**Ensure** in `manage.py`:
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
```

### Required Django settings (snippets)

Create **`.env`** in the project root:

```dotenv
DEBUG=True
SECRET_KEY=dev-please-change
ALLOWED_HOSTS=["*"]

DB_NAME=timetable
DB_USER=ttuser
DB_PASSWORD=ttpass
DB_HOST=localhost
DB_PORT=5432
```

> The code uses `django-environ` to read this file in `config/settings/base.py`.


**Database (PostgreSQL):**
```python
DATABASES = {
  "default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": env("DB_NAME"),
    "USER": env("DB_USER"),
    "PASSWORD": env("DB_PASSWORD"),
    "HOST": env("DB_HOST"),
    "PORT": env("DB_PORT"),
  }
}
```

**Templates (admin requires this):**
```python
TEMPLATES = [
  {
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
      "context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
      ],
    },
  },
]
```

### Local Postgres

```bash
# create db + user (adjust if your local Postgres uses a password prompt)
psql -U postgres -c "CREATE USER ttuser WITH PASSWORD 'ttpass';"
psql -U postgres -c "CREATE DATABASE timetable OWNER ttuser;"
```

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## Project Structure

```
timetable-backend/
├─ config/
│  ├─ settings/
│  │  ├─ __init__.py
│  │  ├─ base.py       # common settings
│  │  ├─ local.py      # dev
│  │  └─ prod.py       # prod
│  ├─ __init__.py      # sets DJANGO_SETTINGS_MODULE to local by default
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ accounts/           # RBAC (future)
├─ catalog/            # tenant, term, dept, room, timeslot, course, offering, section
├─ people/             # instructor, student, enrollment
├─ constraintsapp/     # admin rules, blocked slots, professor availability, student preferences
├─ scheduling/         # timetable_run, assignment
├─ auditlog/           # event log (future)
├─ mediaapp/           # file/audio metadata (optional)
├─ seeds/              # management command: seed_pilot
├─ scripts/            # one-off scripts (optional)
├─ manage.py
└─ .env                # environment variables (local only)
```

---