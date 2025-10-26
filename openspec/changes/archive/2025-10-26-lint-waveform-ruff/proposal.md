# OpenSpec Proposal: lint-waveform-ruff

- Change ID: lint-waveform-ruff
- Summary: Introduce Ruff linting for ui/waveform package and fix lint issues.
- Scope: Developer tooling + non-functional style fixes (no behavior changes).
- Risk: Low (style-only). Gate with full test + mypy + openspec checks.

## Motivation
- Keep the newly extracted waveform components consistent and maintainable.
- Catch style and simple correctness issues early via Ruff.

## Plan
1) Add Ruff as a dev dependency (requirements.txt).
2) Run `ruff check ui/waveform` and fix reported issues in-place.
3) Keep changes behavioral-neutral; if Ruff suggests refactors, prefer the minimal style change.
4) Validate via OpenSpec, Pytest, Mypy.

## Gates
- openspec validate lint-waveform-ruff --strict
- pytest -q
- mypy --strict

## Out of scope
- Applying Ruff to the whole repository (future change).
- Enforcing Ruff in CI (future change).
