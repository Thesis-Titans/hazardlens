# HazardLens API

Backend REST API for official Philippine hazard lookups, spatial queries, and evidence generation. Built with FastAPI, Pydantic, SQLAlchemy 2, and PostgreSQL + PostGIS.

## Development Setup

```bash
# From repository root
cd api

# Install dependencies with uv (or standard pip)
uv sync --extra dev

# Run development server
uv run uvicorn app.main:app --reload --port 8000
```

## Verification Commands

Before opening a pull request or pushing changes, verify that the following checks pass:

```bash
# Linting
uv run ruff check .

# Formatting check
uv run ruff format --check .

# Unit & contract tests
uv run pytest
```
