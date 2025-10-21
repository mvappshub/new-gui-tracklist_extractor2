## 1. Create Adapter Infrastructure
- [x] 1.1 Create `adapters/audio/` directory
- [x] 1.2 Create `adapters/audio/__init__.py` with package initialization
- [x] 1.3 Verify directory structure matches existing `adapters/filesystem/` pattern
- [x] 1.4 **Git commit**: `git commit -m "refactor(phase3): create adapters/audio infrastructure"`

## 2. Implement ZipWavFileReader Adapter
- [ ] 2.1 Create `adapters/audio/wav_reader.py` file
- [ ] 2.2 Define `ZipWavFileReader` class with `__init__(self)` constructor
- [ ] 2.3 Implement `read_wav_files(self, zip_path: Path) -> list[WavInfo]` method
- [ ] 2.4 Move ZIP opening logic (currently inside `extract_wav_durations_sf` in `core/domain/extraction.py`) into the adapter
- [ ] 2.5 Move WAV member enumeration from `extract_wav_durations_sf` into the adapter
- [ ] 2.6 Move temporary directory handling from `extract_wav_durations_sf` into the adapter
- [ ] 2.7 Move WAV extraction loop from `extract_wav_durations_sf` into the adapter
- [ ] 2.8 Preserve the existing logging and error handling used in `extract_wav_durations_sf`
- [ ] 2.9 Import `get_wav_duration` from `audio_utils` (use `rg "get_wav_duration" core/domain/extraction.py` to locate the existing import)
- [ ] 2.10 Import `WavInfo` from `core.models.analysis` (see current usage in `core/domain/extraction.py`)
- [x] 2.11 Add comprehensive docstring explaining adapter's responsibility
- [ ] 2.12 Add type hints for all parameters and return values
- [ ] 2.13 **Git commit**: `git commit -m "refactor(phase3): implement ZipWavFileReader adapter with I/O logic"`

## 3. Refactor Domain Layer
- [ ] 3.1 Update `core/domain/extraction.py` to remove I/O operations
- [ ] 3.2 Option A: Keep `extract_wav_durations_sf` as thin wrapper that instantiates `ZipWavFileReader` and delegates (choose only if adapter indirection is required)
- [ ] 3.3 Option B: Deprecate `extract_wav_durations_sf` entirely and update all callers to use adapter directly
- [ ] 3.4 Remove `zipfile` import from `core/domain/extraction.py`
- [ ] 3.5 Remove `tempfile` import from `core/domain/extraction.py`
- [ ] 3.6 Remove `shutil` import from `core/domain/extraction.py`
- [ ] 3.7 Verify no `open()`, `os`, or other I/O operations remain in `core/domain/extraction.py`
- [ ] 3.8 Run `rg "import (zipfile|tempfile|shutil|os)" core/domain/` to confirm no I/O imports in domain layer
- [x] 3.9 Update module docstring to reflect new pure domain responsibility
- [ ] 3.10 **Git commit**: `git commit -m "refactor(phase3): remove I/O operations from domain layer"`

## 4. Update Service Layer
- [ ] 4.1 Update `services/analysis_service.py` to import `ZipWavFileReader` from `adapters.audio.wav_reader`
- [ ] 4.2 Add `ZipWavFileReader` instantiation in `AnalysisService.__init__` or as class attribute
- [ ] 4.3 Update `AnalysisService.start_analysis` to call `self.wav_reader.read_wav_files(pair_info["zip"])` instead of `extract_wav_durations_sf(pair_info["zip"])`
- [ ] 4.4 If keeping `extract_wav_durations_sf` as wrapper, update its import path accordingly
- [ ] 4.5 Verify service layer has no direct I/O operations
- [ ] 4.6 **Git commit**: `git commit -m "refactor(phase3): integrate ZipWavFileReader in service layer"`

## 5. Update Scripts and Entry Points
- [ ] 5.1 Update `scripts/smoke_test.py` import section to use `ZipWavFileReader` from `adapters.audio.wav_reader`
- [ ] 5.2 Instantiate `ZipWavFileReader` after constructing settings in `scripts/smoke_test.py`
- [ ] 5.3 Replace calls to `extract_wav_durations_sf` in `scripts/smoke_test.py` with `wav_reader.read_wav_files`
- [ ] 5.4 Search for any other direct calls to `extract_wav_durations_sf` using `rg "extract_wav_durations_sf" --type py`
- [ ] 5.5 Update all found references to use the new adapter pattern
- [ ] 5.6 **Git commit**: `git commit -m "refactor(phase3): update scripts to use ZipWavFileReader adapter"`

## 6. Create Unit Tests for Adapter
- [ ] 6.1 Create `tests/test_wav_reader.py` for adapter tests
- [ ] 6.2 Add test for valid ZIP with multiple WAV files: `test_read_wav_files_success`
- [ ] 6.3 Add test for corrupted ZIP file: `test_read_wav_files_corrupted_zip`
- [ ] 6.4 Add test for empty ZIP (no WAV files): `test_read_wav_files_empty_zip`
- [ ] 6.5 Add test for ZIP with corrupted WAV file: `test_read_wav_files_corrupted_wav`
- [ ] 6.6 Add test for ZIP with missing WAV extension: `test_read_wav_files_no_wav_extension`
- [ ] 6.7 Add test for soundfile fallback scenario: `test_read_wav_files_soundfile_fallback`
- [ ] 6.8 Add test for complete failure (both soundfile and wave fail): `test_read_wav_files_duration_extraction_failure`
- [ ] 6.9 Use pytest fixtures from `tests/conftest.py` for temporary ZIP creation
- [ ] 6.10 Mock `get_wav_duration` where appropriate to isolate adapter logic from `audio_utils`
- [ ] 6.11 Verify all tests pass: `pytest tests/test_wav_reader.py -v`
- [ ] 6.12 **Git commit**: `git commit -m "test(phase3): add comprehensive unit tests for ZipWavFileReader"`

## 7. Update Integration Tests
- [ ] 7.1 Review `tests/test_characterization.py` to ensure it still passes with adapter changes
- [ ] 7.2 If characterization tests call `extract_wav_durations_sf` directly, update to use the adapter
- [ ] 7.3 Verify golden outputs still match (no behavior changes)
- [ ] 7.4 Run full test suite: `pytest tests/ -v`
- [ ] 7.5 **Git commit**: `git commit -m "test(phase3): update integration tests for adapter pattern"`

## 8. Validation and Quality Gates
- [ ] 8.1 Run `tools/check.sh` and verify all checks pass (pytest, coverage ≥85%, ruff, mypy --strict, openspec validate)
- [ ] 8.2 Run `mypy --strict adapters/audio/` to verify new adapter has proper type hints
- [ ] 8.3 Run `rg "import (zipfile|tempfile|shutil|os\\.path|open\\()" core/domain/` to confirm no I/O in domain layer
- [ ] 8.4 Verify `core/domain/extraction.py` has no direct file operations
- [ ] 8.5 Run `openspec validate refactor-phase3-io-modularization --strict` and fix any issues
- [ ] 8.6 Verify all delta specs have at least one `#### Scenario:` per requirement
- [ ] 8.7 Confirm proposal.md clearly explains non-breaking nature
- [ ] 8.8 Update tasks.md checkboxes as work progresses
- [ ] 8.9 Final smoke test: run `scripts/smoke_test.py` and verify functionality unchanged
- [ ] 8.10 Verify coverage for new adapter code meets 85% threshold
- [ ] 8.11 **Git commit**: `git commit -m "refactor(phase3): complete I/O modularization - all quality gates passed"`

**Note**: Each git commit command creates an atomic checkpoint. If issues arise, you can revert to the last successful commit. Use `git log --oneline` to view commit history and `git revert <commit-hash>` if rollback is needed.
