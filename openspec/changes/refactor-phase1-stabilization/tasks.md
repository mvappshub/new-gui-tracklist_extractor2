## 1. Type System Fixes
- [x] 1.1 Analyze `SideResult` model in `core/models/analysis.py` - fields `pdf_tracks` and `wav_tracks` expect `List[TrackInfo]` and `List[WavInfo]` respectively
- [x] 1.2 Remove `model_dump()` calls on lines 57-58 in `core/domain/comparison.py`
- [x] 1.3 Pass `pdf_tracks` and `wav_tracks` directly as Pydantic model lists to `SideResult` constructor
- [x] 1.4 Remove unnecessary `cast(Any, ...)` type suppressions
- [x] 1.5 Run `mypy --strict core/domain/comparison.py` and verify no errors

## 2. Dead Code Removal
- [x] 2.1 Locate unreachable `logging.info()` on line 100 in `adapters/filesystem/file_discovery.py`
- [x] 2.2 Delete the unreachable statement (appears after `return` on line 99)
- [x] 2.3 Run `ruff check adapters/filesystem/file_discovery.py` to confirm no unreachable code warnings

## 3. Characterization Tests
- [x] 3.1 Create `tests/test_characterization.py` for behavior locking
- [x] 3.2 Add test for `discover_and_pair_files()` with known PDF/ZIP fixtures - capture pairs dictionary as golden output
- [x] 3.3 Add test for `compare_data()` with sample PDF tracks and WAV files - capture `SideResult` list as golden JSON
- [x] 3.4 Create `tests/data/golden/` directory for reference outputs
- [x] 3.5 Store golden JSON files: `golden_pairs.json`, `golden_comparison.json`
- [x] 3.6 Implement JSON comparison logic with tolerance for floating-point durations
- [x] 3.7 Run `pytest tests/test_characterization.py -v` and verify all pass

## 4. Quality Tooling
- [x] 4.1 Create `tools/` directory if it doesn't exist
- [x] 4.2 Create `tools/check.sh` bash script with shebang `#!/usr/bin/env bash` and `set -euo pipefail`
- [x] 4.3 Add pytest execution (N/A – covered by coverage run)
- [x] 4.4 Add coverage check: `coverage run -m pytest && coverage report --fail-under=85`
- [x] 4.5 Add ruff linting: `python -m ruff check .`
- [x] 4.6 Add mypy type checking: `mypy --strict core adapters services`
- [x] 4.7 Add OpenSpec validation: `openspec validate refactor-phase1-stabilization --strict`
- [x] 4.8 Add success message: `echo "All checks passed"`
- [x] 4.9 Make script executable: `chmod +x tools/check.sh`
- [x] 4.10 Run `tools/check.sh` locally and verify all gates pass

## 5. Validation and Documentation
- [x] 5.1 Run `openspec validate refactor-phase1-stabilization --strict` and fix any issues
- [x] 5.2 Verify all delta specs have at least one `#### Scenario:` per requirement
- [x] 5.3 Confirm `proposal.md` clearly explains non-breaking nature
- [x] 5.4 Update `tasks.md` checkboxes as work progresses
- [x] 5.5 Final quality gate: all checks in `tools/check.sh` pass
