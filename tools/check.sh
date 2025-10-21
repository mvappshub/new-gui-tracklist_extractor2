#!/usr/bin/env bash
set -euo pipefail

# Phase 1 quality gate script.

if [[ -n "${PYTHON_BIN:-}" ]]; then
  # Allow callers to override the interpreter path, e.g. PYTHON_BIN="py -3".
  # shellcheck disable=SC2206
  PYTHON_CMD=(${PYTHON_BIN})
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=("python")
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=("python3")
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=("py" "-3")
else
  echo "Python interpreter not found on PATH." >&2
  exit 1
fi

echo "Collecting coverage metrics..."
QT_QPA_PLATFORM=offscreen "${PYTHON_CMD[@]}" -m coverage run -m pytest -m "not gui"
"${PYTHON_CMD[@]}" -m coverage report --fail-under=85

echo "Running Ruff lint checks..."
"${PYTHON_CMD[@]}" -m ruff check .

echo "Running mypy in strict mode..."
"${PYTHON_CMD[@]}" -m mypy --strict core adapters services

if command -v openspec >/dev/null 2>&1; then
  echo "Validating OpenSpec specifications..."
  openspec validate refactor-phase1-stabilization --strict
else
  echo "Skipping OpenSpec validation (openspec CLI not found)..."
fi

echo "All checks passed"
