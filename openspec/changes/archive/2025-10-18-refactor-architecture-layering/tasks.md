## P0 - ZahĹ™ĂˇtĂ­ motorĹŻ (Prerequisites)
- [x] 0.1 Confirm Track 1 (documentation update) is completed and archived
- [x] 0.2 Verify Traycer VS Code extension is installed and configured
- [x] 0.3 Confirm IDE agent (Cursor or Claude Code) for Hand-Off
- [x] 0.4 Run `openspec validate refactor-architecture-layering --strict`

## P1 - Retro-specifikace (Behavior Contract)
- [x] 1.1 Document current behavior scenarios in delta specs
- [x] 1.2 Create `specs/analysis/spec.md` delta for domain logic
- [x] 1.3 Create `specs/extraction/spec.md` delta for PDF/WAV extraction
- [x] 1.4 Define parity scenarios: file discovery, pairing, extraction, comparison
- [x] 1.5 Validate with `openspec validate --strict`
- [x] 1.6 Traycer: Generate Phases Workflow and visualize plan

## P2 - VrstvenĂ­ monolitu (Architecture Separation)
- [x] 2.1 Create directory structure: `core/domain/`, `core/models/`, `services/`, `adapters/filesystem/`
- [x] 2.2 Extract domain functions from `fluent_gui.py` (lines 183-225: `extract_numeric_id`, `discover_and_pair_files`)
- [x] 2.3 Move to `adapters/filesystem/file_discovery.py`
- [x] 2.4 Extract WAV/PDF extraction logic to `core/domain/extraction.py`
- [x] 2.5 Extract comparison logic (lines 340-402) to `core/domain/comparison.py`
- [x] 2.6 Create `services/analysis_service.py` to orchestrate domain operations
- [x] 2.7 Update `fluent_gui.py` to use service layer (AnalysisWorker class, lines 484-518)
- [x] 2.8 Traycer: Verify Changes in Workspace â†’ Fix forward â†’ Re-verify
- [x] 2.9 Quality gate: 0 Critical, 0 Major issues

## P3 - Qt6 API modernization
- [x] 3.1 Search for `.exec_()` calls and replace with `.exec()`
- [x] 3.2 Review High-DPI setup in `fluent_gui.py` (lines 1422-1451)
- [x] 3.3 Verify enum usage: Qt.AlignmentFlag, QAbstractItemView.SelectionMode, QHeaderView.ResizeMode
- [x] 3.4 Check QVariant usage in table models (TopTableModel, BottomTableModel)
- [x] 3.5 Traycer: Analyze Changes â†’ Propose fixes â†’ Apply â†’ Re-verify
- [x] 3.6 Quality gate: 0 Critical, 0 Major issues

## P4 - Ăšklid a verifikace
- [x] 4.1 Remove unused imports from refactored files
- [x] 4.2 Run `ruff` linter and fix issues
- [x] 4.3 Run `mypy` type checker and address warnings
- [x] 4.4 Verify all parity scenarios from P1 pass
- [x] 4.5 Traycer: Final Verify Changes in Workspace
- [x] 4.6 Quality gate: `openspec validate --strict` passes

## P5 - Archivace
- [x] 5.1 Run `openspec archive refactor-architecture-layering --yes`
- [x] 5.2 Verify deltas applied correctly to main specs
- [x] 5.3 Final validation: `openspec validate --strict`


