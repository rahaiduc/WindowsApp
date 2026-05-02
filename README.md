# WindowApp — API de venta de ventanas

API REST en **FastAPI** para la gestión del catálogo de ventanas de un negocio
de carpintería de PVC, aluminio, madera y mixta. Soporta tipos corredera,
abatible, oscilobatiente, fija y pivotante, con vidrios simple, doble, triple,
templado o laminado.

## Stack

- **FastAPI** + **Uvicorn**
- **SQLAlchemy 2.0** (async) + **asyncpg**
- **PostgreSQL 16**
- **Alembic** (migraciones async)
- **Pydantic v2** + **pydantic-settings**
- **Docker** + **docker-compose**

## Estructura

```
.
├── app/
│   ├── main.py
│   ├── database.py
│   ├── dependencies.py
│   ├── core/config.py
│   ├── models/        # Ventana + enums
│   ├── schemas/       # Pydantic v2
│   ├── crud/          # operaciones async
│   └── routers/       # /api/v1/ventanas
├── alembic/           # entorno async + migración inicial
├── alembic.ini
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## Endpoints

Todos bajo el prefijo `/api/v1`.

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/ventanas` | Lista con filtros opcionales (`tipo_ventana`, `material`, `precio_min`, `precio_max`, `disponible`, `skip`, `limit`) |
| GET | `/ventanas/{id}` | Detalle |
| POST | `/ventanas` | Crear (código único) |
| PUT | `/ventanas/{id}` | Actualización parcial |
| DELETE | `/ventanas/{id}` | Eliminar |
| GET | `/` | Healthcheck |

Documentación interactiva:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Puesta en marcha — opción A (Docker, recomendado)

```bash
cp .env.example .env
docker compose up --build
```

`docker compose` aplica las migraciones automáticamente con
`alembic upgrade head` y arranca uvicorn con `--reload`.

API en <http://localhost:8000> — Postgres en `localhost:5432`.

Para parar:

```bash
docker compose down          # conserva el volumen
docker compose down -v       # borra también la base de datos
```

## Puesta en marcha — opción B (local sin Docker)

Requiere Python 3.12+ y un Postgres accesible.

```bash
python -m venv .venv
.venv\Scripts\activate                 # Windows PowerShell
# source .venv/bin/activate            # Linux / macOS
pip install -r requirements.txt
cp .env.example .env                   # ajusta DATABASE_URL si es necesario
alembic upgrade head
uvicorn app.main:app --reload
```

## Migraciones — Alembic

```bash
# Aplicar todas las migraciones
alembic upgrade head

# Revertir la última
alembic downgrade -1

# Crear una nueva migración a partir de cambios en los modelos
alembic revision --autogenerate -m "descripcion del cambio"
```

> Dentro de Docker: `docker compose exec app alembic <comando>`.

## Ejemplo de uso

```bash
curl -X POST http://localhost:8000/api/v1/ventanas \
  -H "Content-Type: application/json" \
  -d '{
    "codigo": "VEN-PVC-001",
    "nombre": "Ventana corredera PVC blanca 120x100",
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
