## Why

The current codebase uses a global `cfg` singleton from `config.py` (line 661: `cfg = AppConfig()`) that is imported in 11 files across domain, adapter, UI, and test layers. This creates hidden dependencies that make functions harder to test, reduces reusability, and violates dependency inversion principle. Domain logic in `core/domain/comparison.py` (lines 44-45) and adapter logic in `adapters/filesystem/file_discovery.py` (lines 19-30) directly access global state instead of receiving configuration as parameters. While entry points like `app.py` already use dependency injection pattern with settings dataclasses (`ToleranceSettings`, `ExportSettings` from `ui/config_models.py`), this pattern hasn't been extended to lower layers. Phase 2 completes the DI transformation by eliminating global config access from domain/adapter layers, making functions pure and testable.

## What Changes

- Create `IdExtractionSettings` dataclass in `ui/config_models.py` with fields: `min_digits: int`, `max_digits: int`, `ignore_numbers: list[str]`
- Add `load_id_extraction_settings(cfg: AppConfig) -> IdExtractionSettings` loader function in `ui/config_models.py`
- Introduce `WaveformSettings` dataclass and loader in `ui/config_models.py` to encapsulate viewer/editor configuration
- Update `compare_data()` in `core/domain/comparison.py` to accept `ToleranceSettings` parameter instead of accessing `cfg.analysis_tolerance_warn/fail`
- Update `extract_numeric_id()` and `discover_and_pair_files()` in `adapters/filesystem/file_discovery.py` to accept `IdExtractionSettings` parameter
- Remove `from config import cfg` from 9 non-entry-point files: `core/domain/comparison.py`, `adapters/filesystem/file_discovery.py`, `waveform_viewer.py`, and test files
- Keep `cfg` imports only in entry points: `app.py`, `fluent_gui.py`, `settings_page.py`
- Update `AnalysisWorker` in `ui/workers/analysis_worker.py` to receive and pass settings to domain functions
- Update tests to use parametrized settings fixtures instead of mutating global `cfg`

Mark as **non-breaking** - internal refactoring only, no public API changes.

## Impact

- Affected specs: `analysis` (settings injection), `extraction` (ID extraction settings), `export` (settings propagation)
- Affected code: `core/domain/comparison.py`, `adapters/filesystem/file_discovery.py`, `ui/config_models.py`, `ui/workers/analysis_worker.py`, `ui/workers/worker_manager.py`, `services/analysis_service.py`, `waveform_viewer.py`, entry points, and tests
- User Experience: No visible changes
- Dependencies: No new dependencies
- Testing: Improved testability through explicit dependencies; tests can inject different settings without global state mutation
- Migration: Existing code continues to work; refactoring is internal only
