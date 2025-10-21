## 1. Create Settings Dataclasses
- [x] 1.1 Add `IdExtractionSettings` dataclass to `ui/config_models.py` with fields: `min_digits: int`, `max_digits: int`, `ignore_numbers: list[str]`
- [x] 1.2 Create `load_id_extraction_settings(cfg: AppConfig) -> IdExtractionSettings` helper in `ui/config_models.py` that reads `cfg.analysis_min_id_digits.value`, `cfg.analysis_max_id_digits.value`, `cfg.analysis_ignore_numbers.value`
- [x] 1.3 Verify existing `ToleranceSettings` and `ExportSettings` dataclasses are sufficient (no changes needed)
- [x] 1.4 Add type hints and docstrings to new dataclass and loader function
- [x] 1.5 Introduce `WaveformSettings` dataclass and loader in `ui/config_models.py` to replace direct waveform configuration access

## 2. Refactor Domain Layer (core/domain/)
- [x] 2.1 Update `compare_data()` signature in `core/domain/comparison.py` to accept `tolerance_settings: ToleranceSettings` parameter
- [x] 2.2 Replace `cfg.analysis_tolerance_warn.value` (line 44) with `tolerance_settings.warn_tolerance`
- [x] 2.3 Replace `cfg.analysis_tolerance_fail.value` (line 45) with `tolerance_settings.fail_tolerance`
- [x] 2.4 Remove `from config import cfg` import (line 7)
- [x] 2.5 Update function docstring to document new parameter
- [x] 2.6 Run `mypy --strict core/domain/comparison.py` to verify type safety

## 3. Refactor Adapter Layer (adapters/filesystem/)
- [x] 3.1 Update `extract_numeric_id()` signature in `adapters/filesystem/file_discovery.py` to accept `settings: IdExtractionSettings` parameter
- [x] 3.2 Replace `cfg.analysis_min_id_digits.value` (line 19) with `settings.min_digits`
- [x] 3.3 Replace `cfg.analysis_max_id_digits.value` (line 23) with `settings.max_digits`
- [x] 3.4 Replace `cfg.analysis_ignore_numbers.value` (line 30) with `settings.ignore_numbers`
- [x] 3.5 Update `discover_and_pair_files()` signature to accept `settings: IdExtractionSettings` parameter
- [x] 3.6 Pass `settings` to `extract_numeric_id()` calls (lines 60, 69)
- [x] 3.7 Remove `from config import cfg` import (line 7)
- [x] 3.8 Update function docstrings to document new parameters
- [x] 3.9 Run `mypy --strict adapters/filesystem/file_discovery.py` to verify type safety

## 4. Update Service Layer and Workers
- [x] 4.1 Locate `AnalysisWorker` class in `ui/workers/analysis_worker.py`
- [x] 4.2 Update worker constructor to accept `tolerance_settings: ToleranceSettings` and `id_extraction_settings: IdExtractionSettings`
- [x] 4.3 Pass settings to `discover_and_pair_files()` and `compare_data()` calls within worker
- [x] 4.4 Update `AnalysisWorkerManager` in `ui/workers/worker_manager.py` to construct workers with settings
- [x] 4.5 Verify `app.py` entry point (lines 73-76) already loads settings and can pass them to worker manager
- [x] 4.6 Update `fluent_gui.py` if it directly calls domain functions (search for `compare_data` and `discover_and_pair_files` calls)

## 5. Update Entry Points
- [x] 5.1 In `app.py`, add `id_extraction_settings = load_id_extraction_settings(cfg)` after line 73
- [x] 5.2 Pass `id_extraction_settings` to `AnalysisWorkerManager` constructor (line 78)
- [x] 5.3 Verify `fluent_gui.py` entry point constructs and injects settings appropriately
- [x] 5.4 Keep `from config import cfg` imports in entry points (`app.py`, `fluent_gui.py`, `settings_page.py`) - these are the only files that should access global config

## 6. Refactor Tests
- [x] 6.1 Update `tests/test_characterization.py` to create settings objects instead of mutating `cfg` (lines 51-54, 84-87)
- [x] 6.2 Create pytest fixtures in `tests/conftest.py`: `@pytest.fixture def tolerance_settings()`, `@pytest.fixture def id_extraction_settings()`
- [x] 6.3 Update test functions to accept settings fixtures as parameters
- [x] 6.4 Remove direct `cfg` usage from characterization and export tests while leaving configuration-focused suites (`test_config.py`, `test_settings_dialog.py`) unchanged
- [x] 6.5 Parametrize tests to verify different settings combinations (e.g., different tolerance thresholds, different ID digit ranges)
- [x] 6.6 Keep `cfg` import in `test_config.py` since it tests the config system itself

## 7. Remove Remaining Global Config Imports
- [x] 7.1 Update `waveform_viewer.py` (line 38) to receive waveform settings via constructor instead of importing `cfg`
- [x] 7.2 Verify no other non-entry-point files import `cfg` by running: `rg "from config import cfg" --type py | grep -v "app.py\|fluent_gui.py\|settings_page.py\|test_config.py"`
- [x] 7.3 Document in code comments which files are allowed to import `cfg` (entry points only)

## 8. Validation and Quality Gates
- [x] 8.1 Run `tools/check.sh` and verify all checks pass (pytest, coverage ≥85%, ruff, mypy --strict, openspec validate)
- [x] 8.2 Run characterization tests and verify golden outputs still match (no behavior changes)
- [x] 8.3 Verify `mypy --strict` passes for refactored modules: `mypy --strict core/ adapters/ ui/config_models.py waveform_viewer.py`
- [x] 8.4 Run `openspec validate refactor-phase2-dependency-injection --strict` and fix any issues
- [x] 8.5 Verify all delta specs have at least one `#### Scenario:` per requirement
- [x] 8.6 Confirm proposal.md clearly explains non-breaking nature
- [x] 8.7 Update tasks.md checkboxes as work progresses
- [x] 8.8 Final smoke test: run application and perform analysis to verify functionality unchanged
