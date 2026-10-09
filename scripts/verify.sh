#!/usr/bin/env bash
# HazardLens Hermetic Verification Script
# Enforces exact verification checks defined in AGENTS.md.
# Exits with non-zero status if any check fails.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="${REPO_ROOT}/api"
WEB_DIR="${REPO_ROOT}/web"

BOLD='\033[1m'
GREEN='\033[0;32m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BOLD}${CYAN}====================================================${NC}"
echo -e "${BOLD}${CYAN}      HazardLens Pre-PR Verification Suite          ${NC}"
echo -e "${BOLD}${CYAN}====================================================${NC}"

# Detect Python runner for api/
run_backend() {
    if command -v uv >/dev/null 2>&1 && [ -f "${API_DIR}/uv.lock" ]; then
        (cd "${API_DIR}" && uv run "$@")
    elif [ -x "${API_DIR}/.venv/bin/pytest" ]; then
        (cd "${API_DIR}" && "${API_DIR}/.venv/bin/$@")
    else
        (cd "${API_DIR}" && "$@")
    fi
}

# 1. Backend Checks
echo -e "\n${BOLD}>>> [1/6] Backend: Linting (ruff check)${NC}"
run_backend ruff check .
echo -e "${GREEN}✓ Backend linting passed${NC}"

echo -e "\n${BOLD}>>> [2/6] Backend: Formatting Check (ruff format --check)${NC}"
run_backend ruff format --check .
echo -e "${GREEN}✓ Backend formatting check passed${NC}"

echo -e "\n${BOLD}>>> [3/6] Backend: Unit & Contract Tests (pytest)${NC}"
run_backend pytest -v
echo -e "${GREEN}✓ Backend tests passed${NC}"

# 2. Frontend Checks
echo -e "\n${BOLD}>>> [4/6] Frontend: Linting (npm run lint)${NC}"
(cd "${WEB_DIR}" && npm run lint)
echo -e "${GREEN}✓ Frontend linting passed${NC}"

echo -e "\n${BOLD}>>> [5/6] Frontend: Type Check (npx tsc --noEmit)${NC}"
(cd "${WEB_DIR}" && npx tsc --noEmit)
echo -e "${GREEN}✓ Frontend type check passed${NC}"

echo -e "\n${BOLD}>>> [6/6] Frontend: Production Bundle Build (npm run build)${NC}"
(cd "${WEB_DIR}" && npm run build)
echo -e "${GREEN}✓ Frontend production build passed${NC}"

echo -e "\n${BOLD}${GREEN}====================================================${NC}"
echo -e "${BOLD}${GREEN}  All verification checks passed hermetically!      ${NC}"
echo -e "${BOLD}${GREEN}====================================================${NC}"
