## Why

The export functionality is currently accessible through two paths: the canonical `services.export_service.export_results_to_json()` function and a backward-compatibility wrapper `fluent_gui._export_results_to_json()` (lines 142-146). This duplication creates confusion about the correct import path and violates the single source of truth principle. The wrapper was introduced during the transition from monolithic `fluent_gui.py` to modular architecture, but now that Phase 1-3 refactoring is complete and `fluent_gui.py` is marked deprecated (lines 3-6), the wrapper serves no purpose. The UI layer (`ui/main_window.py`) already imports from the service directly (line 27), demonstrating the correct pattern. Only `test_export_auto.py` still uses the wrapper (line 24), creating technical debt. Phase 4 completes the export consolidation by removing the wrapper and ensuring all code uses the centralized service.

## What Changes

- Remove `_export_results_to_json()` wrapper function from `fluent_gui.py` (lines 142-146)
- Remove `_export_results_to_json` from `fluent_gui.__all__` export list (line 79)
- Update `test_export_auto.py` to import `export_results_to_json` from `services.export_service` instead of `fluent_gui` (line 24)
- Update `test_export_auto.py` to import `SideResult`, `TrackInfo`, `WavInfo` from `core.models.analysis` instead of `fluent_gui` (line 24)
- Verify no other code depends on the wrapper by searching for `fluent_gui._export_results_to_json` references
- Document in `services/export_service.py` docstring that it is the single source of truth for export operations
- Add comment in `fluent_gui.py` noting that export functionality has been moved to the service layer

This change is **non-breaking** because the wrapper was an internal API only and no external code depends on it.

## Impact

- Affected specs: `export` (single source of truth documentation)
- Affected code: `fluent_gui.py` (remove wrapper), `test_export_auto.py` (update imports), `services/export_service.py` (add documentation)
- User Experience: No visible changes
- Dependencies: No new dependencies
- Testing: Tests continue to pass with updated imports; no behavior changes
- Architecture: Completes export consolidation; establishes service layer as canonical location for export logic
- Migration: No migration needed - wrapper was internal only
