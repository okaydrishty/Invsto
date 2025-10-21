# Invsto (FastAPI + Prisma)

A small FastAPI project that imports historical OHLCV data into a Postgres database using Prisma (Prisma Client for Python) and exposes a simple API to read/write the data and to calculate a moving-average-crossover strategy performance.

## What this repository contains

- `main.py` — FastAPI app declaration and router inclusion.
- `routers/data.py` — API routes for:
  - GET `/data` — list database `Post` records.
  - POST `/data` — create a new `Post` record.
  - GET `/strategy/performance` — compute strategy performance using stored records.
- `database.py` — small script to import `data.csv` into the Prisma `Post` model.
- `func.py` — strategy helper functions: moving averages, signal generation, performance calculation.
- `models.py` — Pydantic models for request/response validation.
- `prisma/schema.prisma` — Prisma schema (Post model + Postgres datasource and generator).
- `data.csv` — sample OHLCV data used by `database.py`.
- `dockerfile`, `docker-compose.yaml` — Docker setup to run Postgres and the API.
- `requirements.txt` — Python dependencies.
- `test_api.py` — pytest-based API tests using FastAPI's TestClient.
- `.env` — local environment variables (DATABASE_URL, POSTGRES credentials).

## Quick architecture summary

The app stores OHLCV time series rows in a Postgres `Post` model (id, datetime, open, high, low, close, volume). The API uses Prisma to access the DB. The strategy endpoint loads records from Prisma into a pandas DataFrame, computes moving averages, generates signals, and returns basic performance metrics (cumulative return, total trades, win rate).

## Requirements

- Python 3.8+
- PostgreSQL (or `docker-compose` provided)
- Prisma CLI (optional if using Docker image that runs `prisma` commands)

Python dependencies are listed in `requirements.txt` (FastAPI, uvicorn, prisma, pydantic, pandas, numpy, yfinance, pytest).

## Setup & Run (local, without Docker)

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Ensure Postgres is running and `.env` contains a valid `DATABASE_URL`. 

4. Generate Prisma client & run migrations (requires `prisma` installed and in PATH):

```powershell
prisma generate
prisma migrate dev --name init
```

5. Import the sample data into the database (this runs the `database.py` script which reads `data.csv` and writes rows into Prisma):

```powershell
python database.py
```

6. Run the FastAPI app:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://127.0.0.1:8000 and interactive docs at http://127.0.0.1:8000/docs.

## Running with Docker (recommended for easy DB + API orchestration)

1. Ensure Docker Desktop is running.
2. Start services with docker-compose (runs Postgres and builds the API image):

```powershell
docker compose up --build
```

Notes about the Dockerfile:
- The Dockerfile installs Python deps, runs `prisma generate` and `prisma migrate dev`, then executes `python database.py` to seed the DB. This assumes the DB is reachable from the build stage which is not true when building multi-container setups; the docker-compose service `api` depends on `db` at runtime but not during image build. For a robust containerized workflow, prefer seeding the DB at runtime (entrypoint) or use `docker compose run` after the DB is up.

## API Endpoints

- GET /data
  - Returns: list of `Post` objects (id, datetime, open, high, low, close, volume).
- POST /data
  - Request body: open, high, low, close, volume (see `models.PostCreate` for schema).
  - Returns: created `Post` with `id` and `datetime`.
- GET /strategy/performance
  - Returns: { strategy: "Moving Average Crossover", performance: { cumulative_return, total_trades, win_rate } }
  - Calculation: loads all records, computes 20- and 50-period moving averages, generates buy/sell signals where short_ma crosses long_ma, and computes simple strategy returns.

## Tests

Run the test suite (pytest):

```powershell
pytest -q
```

Notes about tests:
- `test_api.py` uses FastAPI's TestClient hitting `main.app`. Tests will succeed only when the Prisma client can connect to a configured database and the DB contains data. The tests attempt to POST new rows and inspect responses.

## Code walkthrough & important details

- `main.py` — creates FastAPI app and includes the router from `routers/data.py`.

- `routers/data.py` — uses Prisma for DB access. Each route creates a `Prisma()` instance and calls `connect()`/`disconnect()` per request. This is simple but not optimal for production (prefer a single shared Prisma client instance reused across requests to avoid connection overhead).

- `database.py` — reads `data.csv`, coerces `datetime`, and iterates rows to create `post` records in Prisma.
  - It calls `db.connect()` synchronously (Prisma client is sync here because `interface = "sync"` in schema generator). It also does no batching.

- `func.py` — contains:
  - calculate_moving_averages(df, short_window=20, long_window=50)
  - generate_signals(df)
  - calculate_performance(df)
  These functions operate on pandas DataFrames and return computed DataFrames or performance dict.

- `models.py` — Pydantic models for request and response. Note: `PostResponse` repeats some fields and also defines `Config.from_attributes = True` to support model creation from attributes.

- Prisma schema (`prisma/schema.prisma`) defines `Post` with Decimal fields for prices. The generator is set to `prisma-client-py` with `interface = "sync"`.







