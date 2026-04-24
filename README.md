# Карго жеткізу веб-сайты (Байерлік қызмет)

Django-based web application for cargo delivery workflows with roles, admin panel, and REST API.

## Project Structure

```text
cargo/
├── manage.py
├── requirements.txt
├── README.md
├── Dockerfile
├── docker-compose.yml
├── render.yaml
├── cargo_project/        # Django project config
├── users/                # auth/profile/roles
├── orders/               # order workflow + feedback
├── cargo/                # cargo types/routes/maps/contact
├── templates/
├── static/
├── docs/                 # operational docs
└── load-tests/           # k6 scenarios
```

## Local Setup

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
py -3 -m pip install -r requirements.txt
py -3 manage.py migrate
py -3 manage.py createsuperuser
py -3 manage.py runserver
```

Main URLs:

- Home: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`
- Health: `http://127.0.0.1:8000/health/`

## API

API routes are under `/api/`.

- JWT: `/api/auth/token/`, `/api/auth/token/refresh/`
- Profile: `/api/me/`
- Orders: `/api/orders/`
- Catalog: `/api/cargo-types/`, `/api/routes/`

Detailed reference: `docs/API.md`.

## Testing and Coverage

```powershell
py -3 manage.py test
py -3 -m coverage run manage.py test
py -3 -m coverage report
```

Detailed testing guide: `docs/TESTING.md`.

## Docker

Run locally with Docker:

```powershell
docker compose up --build
```

## CI/CD

GitHub Actions workflow is configured at `.github/workflows/ci.yml`:

- dependency install
- `manage.py check`
- full test run
- coverage report

## Render Deployment

Render blueprint is defined in `render.yaml`.

Required env vars:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `ALLOWED_HOSTS`

Start command runs migrations and launches Gunicorn.

## Monitoring and Logs

- App health endpoint: `/health/`
- Centralized logging configured in `cargo_project/settings.py`
- Runtime logs are written to `logs/cargo.log` and console (Render logs)

## Load Testing

k6 smoke scenario:

```powershell
k6 run .\load-tests\k6-smoke.js
```

Use Render URL target:

```powershell
k6 run -e BASE_URL=https://your-service.onrender.com .\load-tests\k6-smoke.js
```
