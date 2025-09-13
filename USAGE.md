**Usage Guide (No‑Docker Friendly)**

This guide shows how to run the CRM locally without Docker, plus an optional Docker path if you later want one‑command startup.

**Overview**
- Backend: FastAPI + SQLModel (runs on `http://localhost:8000`)
- Frontend: React + Vite + TypeScript (runs on `http://localhost:5173`)
- DB: Use SQLite locally (no extra install). Postgres is used in Docker/production.

**Prerequisites**
- Python 3.10+ (3.11 recommended). Check: `python3 --version`
- Node.js 18+ (20 recommended). Check: `node -v`

If you need Node: https://nodejs.org/en/download

**1) Backend without Docker (SQLite)**
- Create a virtualenv and install dependencies:
  - macOS/Linux:
    - `cd backend`
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install --upgrade pip`
    - `pip install -r requirements.txt`
  - Windows (PowerShell):
    - `cd backend`
    - `py -m venv .venv`
    - `.\.venv\Scripts\Activate.ps1`
    - `python -m pip install --upgrade pip`
    - `pip install -r requirements.txt`

- Configure environment (use SQLite dev DB):
  - `cp .env.example .env`
  - Open `backend/.env` and set:
    - `DB_URL=sqlite:///./dev.db?check_same_thread=false`
    - `JWT_SECRET=your-dev-secret` (any random string)
    - `AES_KEY_HEX=` (leave empty for now; export requires this and is optional in local dev)

- Start the API:
  - `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
  - Open health: `http://localhost:8000/health`
  - Open docs: `http://localhost:8000/docs`

- Seed sample data (in a new terminal, with venv activated):
  - `cd backend && source .venv/bin/activate` (Windows: activate venv as above)
  - `python -m app.scripts.seed`
  - Creates: Admin `admin@example.com` (pwd `admin123`), Brokers `broker1@example.com` / `broker2@example.com` (pwd `broker123`), plus one example deal & task for broker1.

Notes
- Alembic migrations are configured but not required for SQLite dev — the app auto-creates tables; use Alembic for Postgres/production.
- Redis is optional locally (refresh-token blacklist is skipped if Redis not available).

**2) Frontend without Docker**
- Install deps and start dev server:
  - `cd frontend`
  - `npm install`
  - Ensure API base is correct (Vite env):
    - `echo "VITE_API_BASE=http://localhost:8000/api" > .env` (or set in your shell)
  - `npm run dev`
  - Open: `http://localhost:5173`

- Login
  - Go to `/login`
  - Use Broker demo account: `broker1@example.com` / `broker123`
  - Or Admin: `admin@example.com` / `admin123`

- Try features
  - Kanban: Home page shows deals by stage. Use the stage buttons on each card to transition (writes ActivityLog).
  - Stats: `/stats` page calls `/api/stats/summary`.
  - Register: `/register` visible to Admin — creates users via API.

**3) Exports & Offline Viewer (optional, demo)**
- Server exports are AES-256-GCM–encrypted SQLite bundles. In Docker, they are written under `/data/exports` (volume). For local dev (no Docker), the hardcoded path isn’t writable by default.
- Recommended: test exports in Docker (see next section). If you still want local export, change the path in `backend/app/api/routes/exports.py`:
  - Replace `EXPORT_DIR = Path("/data/exports")` with `EXPORT_DIR = Path("./exports")` and create the folder.
  - Set a 64-hex AES key in `backend/.env`: `AES_KEY_HEX=$(openssl rand -hex 32)`
  - Restart API, then call `POST /api/exports/run` as Admin. Download with `GET /api/exports/{id}/download`.
- Offline viewer (`/offline`) currently demonstrates AES-GCM decryption flow; wiring to actually read the decrypted SQLite (via sql.js/duckdb-wasm) is a next step.

**4) (Optional) Run with Docker**
If you later want to use Docker Desktop for a one-command stack:
- Install Docker Desktop: https://www.docker.com/products/docker-desktop/
- From repository root:
  - `cp .env.example .env`
  - `cp backend/.env.example backend/.env`
  - Set in `backend/.env`: `JWT_SECRET=your-dev-secret` and a 64-hex `AES_KEY_HEX` (e.g. `openssl rand -hex 32`).
  - `docker compose up --build`
  - API: `http://localhost:8000/docs`, Frontend: `http://localhost:5173`
  - Initialize DB (inside the `api` container):
    - `docker compose exec api bash -lc "alembic revision --autogenerate -m 'init' && alembic upgrade head"`
  - Seed: `docker compose exec api python -m app.scripts.seed`

**5) Troubleshooting**
- Port already in use
  - Change ports (`--port` for API) or stop the other process.
- Python version errors (e.g. `TypeError: unsupported operand type(s) for |: ...`)
  - Use Python 3.10+; or keep this repo (already updated) which avoids `|` unions needing 3.10.
- Missing deps (e.g. `ModuleNotFoundError: email_validator`)
  - Re-run: `pip install -r backend/requirements.txt`
- CORS blocked in browser
  - API allows `http://localhost:5173` by default; if you use a different frontend origin, add it in `backend/.env` under `CORS_ORIGINS`.
- Export path errors (permission denied)
  - Prefer Docker for exports. For local: change export path to a writable folder as described above.
- Redis not running
  - Local dev works without Redis. Revocation/refresh safeguards are reduced — OK for local.

**6) Admin & RBAC self-check**
- Login as `broker1@example.com` → only sees their own Deal/Task on Kanban/Tasks.
- Transition a deal stage in Kanban → `ActivityLog` records old/new stage + user.
- Stats endpoints `/api/stats/summary`, `/api/stats/funnel` return numbers.

**7) Where to change config**
- Backend env: `backend/.env` (JWT secret, DB URL, CORS, Redis, AES key)
- Frontend env: `frontend/.env` (`VITE_API_BASE`)

If you want, I can further simplify with a `make dev` script for one‑line startup on macOS/Linux.

