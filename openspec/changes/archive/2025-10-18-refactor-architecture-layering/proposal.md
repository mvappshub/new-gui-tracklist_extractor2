## Why
The current `fluent_gui.py` (1468 lines) is a monolith mixing domain logic (PDF/WAV extraction, comparison), I/O operations, and GUI presentation. This makes testing difficult, reduces code reusability, and violates separation of concerns. The user's P0-P5 strategy provides a proven methodology for safe, auditable refactoring.

## What Changes
- **P2 - Vrstvení monolitu:** Extract domain logic from GUI
  - Move PDF/WAV/compare functions from `fluent_gui.py` (lines 183-402) to `core/domain/` modules
  - Move I/O operations (ZIP reading, file discovery) to `adapters/filesystem/`
  - Create `services/analysis_service.py` for orchestration
  - GUI keeps only presentation logic (models, views, signals)
- **P3 - Qt6 API modernization:** Update deprecated patterns
  - Replace `.exec_()` with `.exec()` throughout
  - Verify High-DPI attributes (lines 1422-1451 in `fluent_gui.py`)
  - Modernize enum usage (Qt.AlignmentFlag, QAbstractItemView.SelectionMode)
- **P4 - Quality gates:** Establish verification at each phase
  - Zero Critical/Major issues in Traycer Verify
  - OpenSpec validate --strict passes
  - Behavior parity scenarios pass

**BREAKING:** None - internal refactoring only, no API changes

## Impact
- Affected specs: `specs/ui/spec.md`, new `specs/analysis/spec.md`, new `specs/extraction/spec.md`
- Affected code: `fluent_gui.py`, `pdf_extractor.py`, `wav_extractor_wave.py`, new modules in `core/`, `services/`, `adapters/`
- User Experience: No visible changes
- Dependencies: No new dependencies
- Testing: Improved testability through dependency injection

