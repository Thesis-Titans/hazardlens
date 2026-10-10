#!/usr/bin/env bash
# HazardLens Unified Bash Verification Script
# Executes the pre-PR verification checks defined in AGENTS.md.
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

# Python runner resolution:
# 1. uv run (if uv is available and api/uv.lock exists)
# 2. Project virtual environment (if api/.venv/bin/<cmd> is executable)
# 3. System / PATH executable (fallback)
run_backend() {
    local cmd="$1"
    shift
    if command -v uv >/dev/null 2>&1 && [ -f "${API_DIR}/uv.lock" ]; then
        (cd "${API_DIR}" && uv run "${cmd}" "$@")
    elif [ -x "${API_DIR}/.venv/bin/${cmd}" ]; then
        (cd "${API_DIR}" && "${API_DIR}/.venv/bin/${cmd}" "$@")
    else
        (cd "${API_DIR}" && "${cmd}" "$@")
    fi
}

check_backend() {
    echo -e "\n${BOLD}>>> [1/7] Backend: Linting (ruff check)${NC}"
    run_backend ruff check .
    echo -e "${GREEN}✓ Backend linting passed${NC}"

    echo -e "\n${BOLD}>>> [2/7] Backend: Formatting Check (ruff format --check)${NC}"
    run_backend ruff format --check .
    echo -e "${GREEN}✓ Backend formatting check passed${NC}"

    echo -e "\n${BOLD}>>> [3/7] Backend: Unit & Contract Tests (pytest)${NC}"
    run_backend pytest -v
    echo -e "${GREEN}✓ Backend tests passed${NC}"
}

check_frontend() {
    echo -e "\n${BOLD}>>> [4/7] Frontend: Linting (npm run lint)${NC}"
    (cd "${WEB_DIR}" && npm run lint)
    echo -e "${GREEN}✓ Frontend linting passed${NC}"

    echo -e "\n${BOLD}>>> [5/7] Frontend: Type Check (npx tsc --noEmit)${NC}"
    (cd "${WEB_DIR}" && npx tsc --noEmit)
    echo -e "${GREEN}✓ Frontend type check passed${NC}"

    echo -e "\n${BOLD}>>> [6/7] Frontend: Production Bundle Build (npm run build)${NC}"
    (cd "${WEB_DIR}" && npm run build)
    echo -e "${GREEN}✓ Frontend production build passed${NC}"
}

check_docs() {
    echo -e "\n${BOLD}>>> [7/7] Documentation: Checker Tests, Markdownlint & Link Integrity${NC}"
    (cd "${REPO_ROOT}" && python3 -m unittest discover -s scripts/tests -v)
    python3 "${REPO_ROOT}/scripts/check_docs.py"
    echo -e "${GREEN}✓ Documentation checks passed${NC}"
}

TARGET="${1:-all}"

echo -e "${BOLD}${CYAN}====================================================${NC}"
echo -e "${BOLD}${CYAN}      HazardLens Pre-PR Verification Suite          ${NC}"
echo -e "${BOLD}${CYAN}====================================================${NC}"

case "${TARGET}" in
    backend)
        check_backend
        ;;
    frontend)
        check_frontend
        ;;
    docs)
        check_docs
        ;;
    all)
        check_backend
        check_frontend
        check_docs
        ;;
    *)
        echo -e "${RED}Unknown target: ${TARGET}. Usage: $0 [all|backend|frontend|docs]${NC}" >&2
        exit 1
        ;;
esac

echo -e "\n${BOLD}${GREEN}====================================================${NC}"
echo -e "${BOLD}${GREEN}  All requested verification checks passed!         ${NC}"
echo -e "${BOLD}${GREEN}====================================================${NC}"
