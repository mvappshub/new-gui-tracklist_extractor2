## Why
The current domain layer in `core/domain/extraction.py` violates hexagonal architecture principles by directly performing file I/O operations. The `extract_wav_durations_sf` function (lines 13-45) imports and uses `zipfile`, `tempfile`, and `shutil` to read ZIP archives, create temporary directories, and extract WAV files. This creates tight coupling between domain logic and infrastructure, making the code harder to test (requires real file system), harder to reuse (cannot swap I/O implementations), and violates the dependency inversion principle established in Phase 2. Domain functions should work with data objects, not perform I/O. Phase 3 completes the architectural layering by moving all file I/O operations to the adapter layer, keeping the domain pure and focused on business logic.

## What Changes
- Create `adapters/audio/` directory for audio-related adapters
- Create `adapters/audio/__init__.py` for package initialization
- Create `adapters/audio/wav_reader.py` with `ZipWavFileReader` class that encapsulates ZIP reading and WAV extraction logic
- Move ZIP opening, WAV file enumeration, temporary file creation, and duration extraction from `core/domain/extraction.py` to the new adapter
- Update `extract_wav_durations_sf` in `core/domain/extraction.py` to become a thin wrapper that delegates to `ZipWavFileReader`, or deprecate it entirely
- Remove imports of `zipfile`, `tempfile`, and `shutil` from `core/domain/extraction.py`
- Update `services/analysis_service.py` to instantiate `ZipWavFileReader` and use it directly instead of calling `extract_wav_durations_sf`
- Update `scripts/smoke_test.py` to use the new adapter
- Create unit tests for `ZipWavFileReader` covering: valid ZIP with WAVs, corrupted ZIP, empty ZIP, corrupted WAV files, missing WAV files, and soundfile/wave fallback scenarios
- Ensure `core/domain/` has no `open()`, `os`, `zipfile`, `tempfile`, or `shutil` imports after refactoring

## Impact
- Affected specs: `extraction` (I/O adapter layer introduction)
- Affected code: `core/domain/extraction.py`, new `adapters/audio/wav_reader.py`, `services/analysis_service.py`, `scripts/smoke_test.py`, new test files
- User Experience: No visible changes
- Dependencies: No new dependencies (uses existing `soundfile`, `wave`, `zipfile`)
- Testing: Improved testability through adapter pattern; can inject fake readers for unit tests without file system
- Architecture: Completes hexagonal architecture pattern with clear separation between domain and infrastructure layers
- Classification: Non-breaking; internal refactor only
