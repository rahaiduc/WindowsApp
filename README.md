# WindowApp — Window sales API

REST API built with **FastAPI** to manage the catalog of a window-carpentry
business: PVC, aluminium, wood and mixed-material windows. Supports sliding,
casement, tilt-and-turn, fixed and pivot types, with single, double, triple,
tempered or laminated glazing.

> Note: domain field names are kept in Spanish (`ventanas`, `codigo`,
> `tipo_ventana`, `material`, `precio_base`, ...) because they belong to the
> business model. The application chrome (docs, comments, validation messages
> in this README) is in English.

## Stack

- **FastAPI** + **Uvicorn**
- **SQLAlchemy 2.0** (async) + **asyncpg**
- **PostgreSQL 16**
- **Alembic** (async migrations)
- **Pydantic v2** + **pydantic-settings**
- **Docker** + **docker-compose**

## Project layout

```
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── core/config.py
│   ├── models/        # Ventana + enums
│   ├── schemas/       # Pydantic v2
│   ├── crud/          # async operations
│   └── routers/       # /api/v1/ventanas
├── alembic/           # async environment + initial migration
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Endpoints

All endpoints are mounted under the `/api/v1` prefix.

| Method | Path | Description |
|---|---|---|
| GET | `/ventanas` | List with optional filters (`tipo_ventana`, `material`, `precio_min`, `precio_max`, `disponible`, `skip`, `limit`) |
| GET | `/ventanas/{id}` | Retrieve one |
| POST | `/ventanas` | Create (code must be unique) |
| PUT | `/ventanas/{id}` | Partial update |
| DELETE | `/ventanas/{id}` | Delete |
| GET | `/` | Healthcheck |

Interactive docs:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Getting started — option A (Docker, recommended)

```bash
cp .env.example .env
docker compose up --build
```

`docker compose` automatically applies migrations with `alembic upgrade head`
and starts uvicorn with `--reload`.

API at <http://localhost:8000> — Postgres at `localhost:5432`.

To stop:

```bash
docker compose down          # keeps the volume
docker compose down -v       # also drops the database volume
```

## Getting started — option B (local, without Docker)

Requires Python 3.12+ and a reachable PostgreSQL instance.

```bash
python -m venv .venv
.venv\Scripts\activate                 # Windows PowerShell
# source .venv/bin/activate            # Linux / macOS
pip install -r requirements.txt
cp .env.example .env                   # adjust DATABASE_URL if needed
alembic upgrade head
uvicorn app.main:app --reload
```

## Migrations — Alembic

```bash
# Apply all migrations
alembic upgrade head

# Revert the last one
alembic downgrade -1

# Generate a new migration from model changes
alembic revision --autogenerate -m "describe the change"
```

> Inside Docker: `docker compose exec app alembic <command>`.

## Usage example

```bash
curl -X POST http://localhost:8000/api/v1/ventanas \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "VEN-PVC-001",
    "nombre": "Sliding PVC window, white, 120x100",
    "tipo_ventana": "corredera",
    "material": "pvc",
    "tipo_vidrio": "doble",
    "color": "blanco",
    "ancho_cm": 120,
    "alto_cm": 100,
    "precio_base": 189.90,
    "descripcion": "Climalit 4/12/4",
    "stock": 25,
    "disponible": true
  }'

curl "http://localhost:8000/api/v1/ventanas?material=pvc&precio_max=300"
```
