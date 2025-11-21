# Development setup (local)

This document explains how to run the project locally for development. It assumes you are on Linux (Ubuntu) and have Python 3.10+, Node.js and npm installed.

## Backend (Django)

1. Enter backend folder and create virtualenv

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Prepare environment variables

- Copy the example and edit if needed:

```bash
cp .env.example .env
# then fill values in backend/.env if you want (e.g. DJANGO_SECRET)
```

- Load the `.env` into your shell for the current session (simple method):

```bash
set -a; source backend/.env; set +a
```

Or export individual vars (temporary):

```bash
export DJANGO_DEBUG=1
export DJANGO_SECRET='dev-secret-local'
```

4. Run migrations and start server

```bash
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver 0.0.0.0:8000
```

Notes:
- If `MYSQL_HOST` is set in env, Django will try to connect to MySQL. If `MYSQL_HOST` is empty/not set, Django will use a local `db.sqlite3` (fallback) for development.

## Frontend (Vite + React)

1. Install dependencies and run dev server

```bash
cd frontend
npm install
npm run dev
```

2. Vite proxies `/api` to the backend (see `vite.config.mjs`). Open the printed URL (usually http://localhost:5173).

## Quick verification

- Backend health endpoint: `http://localhost:8000/api/health/`
- Frontend dev URL: printed by Vite (commonly `http://localhost:5173`)

## Troubleshooting

- If migrations fail with MySQL connection errors, either set valid `MYSQL_*` environment variables, or leave `MYSQL_HOST` empty to use sqlite fallback.
- If ports are in use, stop the process occupying them (e.g. `lsof -i :8000`) or change the port.
- Do not commit `.env` with real secrets. Use `.env.example` as template.

## Optional: Docker / docker-compose

You can containerize the services with Docker; if you want I can add a `docker-compose.yml` to run backend + frontend + db.
