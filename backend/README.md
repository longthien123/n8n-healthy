Django backend for n8n-health

Setup

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

API

- GET /api/health/  -> {"status": "ok"}
