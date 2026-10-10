# HazardLens Root Makefile
# Provides standardized baseline developer and CI workflows matching AGENTS.md

.PHONY: all help verify verify-backend verify-frontend verify-docs test test-backend lint lint-backend lint-frontend format format-check install dev-db dev-api dev-web docker-up docker-down docker-logs clean

API_DIR = api
WEB_DIR = web

# Python runner resolution matching scripts/verify.sh:
# 1. uv run (if uv is installed and api/uv.lock exists)
# 2. Project virtual environment (if api/.venv/bin/python exists)
# 3. System / PATH executable (fallback)
UV := $(shell command -v uv 2>/dev/null)
HAVE_UV_LOCK := $(wildcard $(API_DIR)/uv.lock)
HAVE_VENV := $(wildcard $(API_DIR)/.venv/bin/python)

ifneq ($(and $(UV),$(HAVE_UV_LOCK)),)
  PY_RUN = uv run
else ifneq ($(HAVE_VENV),)
  PY_RUN = .venv/bin/python -m
else
  PY_RUN = python3 -m
endif

all: help

help:
	@echo "======================================================================"
	@echo "                     HazardLens Developer Commands                    "
	@echo "======================================================================"
	@echo "  make verify           Run full verification suite (backend + frontend + docs)"
	@echo "  make verify-backend   Run backend ruff check, ruff format --check, and pytest"
	@echo "  make verify-frontend  Run frontend eslint, tsc --noEmit, and npm run build"
	@echo "  make verify-docs      Run markdownlint and document link integrity checks"
	@echo ""
	@echo "  make test             Run backend pytest suite"
	@echo "  make lint             Run both backend and frontend linters"
	@echo "  make format           Auto-format backend code with ruff"
	@echo "  make format-check     Check backend code formatting without changes"
	@echo ""
	@echo "  make install          Install all backend and frontend dependencies"
	@echo "  make dev-db           Start PostgreSQL + PostGIS service via Docker Compose"
	@echo "  make dev-api          Start FastAPI development server with hot-reload"
	@echo "  make dev-web          Start Vite frontend development server"
	@echo ""
	@echo "  make docker-up        Start all Docker Compose services (db, api, web)"
	@echo "  make docker-down      Stop Docker Compose services"
	@echo "  make docker-logs      Follow Docker Compose logs"
	@echo "  make clean            Clean local build caches and artifacts"
	@echo "======================================================================"

# --- Verification Suite (AGENTS.md) ---

verify:
	@./scripts/verify.sh all

verify-backend:
	@./scripts/verify.sh backend

verify-frontend:
	@./scripts/verify.sh frontend

verify-docs:
	@./scripts/verify.sh docs

# --- Backend Testing & Quality ---

test: test-backend

test-backend:
	cd $(API_DIR) && $(PY_RUN) pytest -v $(ARGS)

lint: lint-backend lint-frontend

lint-backend:
	cd $(API_DIR) && $(PY_RUN) ruff check .

lint-frontend:
	cd $(WEB_DIR) && npm run lint

format:
	cd $(API_DIR) && $(PY_RUN) ruff format .
	cd $(API_DIR) && $(PY_RUN) ruff check --fix .

format-check:
	cd $(API_DIR) && $(PY_RUN) ruff format --check .

# --- Dependency Management ---

install:
	@echo ">>> Installing backend dependencies..."
	cd $(API_DIR) && (command -v uv >/dev/null 2>&1 && uv sync || pip install -e ".[dev]")
	@echo ">>> Installing frontend dependencies..."
	cd $(WEB_DIR) && npm install

# --- Local Development ---

dev-db:
	docker compose up -d db

dev-api:
	cd $(API_DIR) && $(PY_RUN) uvicorn app.main:app --reload --port 8000

dev-web:
	cd $(WEB_DIR) && npm run dev

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

# --- Housekeeping ---

clean:
	@echo ">>> Cleaning caches and build artifacts..."
	rm -rf $(API_DIR)/.pytest_cache $(API_DIR)/.ruff_cache $(API_DIR)/dist $(API_DIR)/build $(API_DIR)/*.egg-info
	rm -rf $(WEB_DIR)/dist $(WEB_DIR)/.vite $(WEB_DIR)/*.tsbuildinfo
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete"
