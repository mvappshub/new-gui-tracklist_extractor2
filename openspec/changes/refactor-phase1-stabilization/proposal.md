## Why
Phase 1 of the stabilization effort establishes a reliable baseline before diving into deeper architectural refactoring. Current quality gaps make it risky to proceed: type workarounds in `core/domain/comparison.py` (lines 57-58) hide model compatibility problems, unreachable `logging.info()` code in `adapters/filesystem/file_discovery.py` (line 100) points to missing review discipline, characterization tests are absent so behavior changes can slip by unnoticed, and we do not have automated quality gates to prevent regressions.

## What Changes
- Fix type handling in `compare_data()` so it accepts Pydantic models directly instead of dumping to dictionaries
- Remove the unreachable `logging.info()` statement that sits after the return path in `discover_and_pair_files()`
- Add characterization tests with golden JSON outputs that lock today’s observable behavior
- Create `tools/check.sh` to run pytest, coverage (≥85%), ruff, `mypy --strict`, and `openspec validate`

This change is **non-breaking** and focuses solely on internal quality improvements.

## Impact
- Affected specs: `analysis` (type safety, dead code), `extraction` (characterization tests), `export` (golden outputs)
- Affected code: `core/domain/comparison.py`, `adapters/filesystem/file_discovery.py`, new `tests/test_characterization.py`, new `tools/check.sh`
- User experience: No visible changes; stabilization only
- Dependencies: No new packages required
- Testing: Establishes regression safety net for later refactor phases
