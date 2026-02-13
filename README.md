# Tickets API (Clean Architecture)

API CRUD para gestion de Users y Tickets con FastAPI, SQLAlchemy 2.0 y Alembic. Documentacion OpenAPI disponible en /docs.

## Estructura

- app/: API, servicios, repositorios, modelos y esquemas.
- alembic/: migraciones.
- tests/: tests de integracion con httpx.

## Endpoints

- /users
- /tickets
- /health

## Requisitos

- Python 3.11.
- SQLite.
- Docker y Docker Compose (opcional).

## Guia de ejecucion sin Docker

1) Crea y activa un entorno virtual:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

2) Instala dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3) Configura variables de entorno:

```bash
cp .env.example .env
```

Edita `.env` para apuntar a tu SQLite local, por ejemplo:

```
DATABASE_URL=sqlite:///./tickets.db
```

4) Ejecuta migraciones:

```bash
alembic upgrade head
```

5) Levanta la API:

```bash
uvicorn app.main:app --reload
```

6) Abre la documentacion:

```text
http://localhost:8000/docs
```

## Guia de ejecucion con Docker

1) Copia el archivo de variables de entorno:

```bash
cp .env.example .env
```

2) Levanta los servicios:

```bash
docker compose up --build -d
```

3) Ejecuta migraciones:

```bash
docker compose exec api alembic upgrade head
```

4) Abre la documentacion:

```text
http://localhost:8000/docs
```

## Tests

```bash
docker compose exec api pytest
```
