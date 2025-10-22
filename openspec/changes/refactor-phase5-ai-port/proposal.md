# Phase 5: AI Port (Optional)

## Why

The current domain layer in `core/domain/comparison.py` violates hexagonal architecture principles by directly importing AI detection logic from `wav_extractor_wave.py` (lines 9-14). This standalone script contains infrastructure code (OpenAI/OpenRouter API clients, external HTTP calls) that creates tight coupling between domain logic and external services. The module-level variables `_detect` and `_normalize` (lines 13-14) are cast from functions in the standalone script, making the domain layer dependent on AI availability and API credentials. This makes testing difficult (requires mocking external APIs), prevents swapping detection strategies, and violates the dependency inversion principle established in Phase 2-3. Domain functions should depend on abstractions (ports), not concrete implementations (adapters). Phase 5 completes the hexagonal architecture by isolating all AI logic behind a port interface, making the domain pure and the system testable without external dependencies.

## What Changes

- Create `core/ports.py` with `AudioModeDetector` Protocol defining the detection interface
- Create `adapters/audio/ai_mode_detector.py` with `AiAudioModeDetector` class that wraps existing `detect_audio_mode_with_ai` and `normalize_positions` functions from `wav_extractor_wave.py`
- Create `adapters/audio/fake_mode_detector.py` with `FakeAudioModeDetector` class for tests (deterministic, no external API calls)
- Update `core/domain/comparison.py` to remove direct imports from `wav_extractor_wave.py` (lines 9, 13-14)
- Update `detect_audio_mode()` function signature to accept `detector: AudioModeDetector` parameter
- Update `compare_data()` function signature to accept `detector: AudioModeDetector` parameter
- Update `services/analysis_service.py` to instantiate `AiAudioModeDetector` in constructor (like `wav_reader` from Phase 3)
- Update `services/analysis_service.py` to pass detector to `compare_data()` calls
- Update `scripts/smoke_test.py` to instantiate and use detector
- Update `tests/conftest.py` to add `audio_mode_detector` fixture using `FakeAudioModeDetector`
- Update `tests/test_characterization.py` to accept detector fixture and pass to `compare_data()`
- Ensure `core/domain/` has no imports from `wav_extractor_wave.py` after refactoring
- Mark Phase 5 as **OPTIONAL** in proposal - system works without it, but architecture is cleaner with it

This is a **non-breaking** change - internal refactoring only, behavior remains identical.

## Impact

- **Affected specs**: `analysis` (AI port introduction, domain layer purity)
- **Affected code**: `core/ports.py` (new), `adapters/audio/ai_mode_detector.py` (new), `adapters/audio/fake_mode_detector.py` (new), `core/domain/comparison.py`, `services/analysis_service.py`, `scripts/smoke_test.py`, test files
- **User Experience**: No visible changes
- **Dependencies**: No new dependencies (uses existing `wav_extractor_wave` functions)
- **Testing**: Dramatically improved testability - tests use fake detector with no external API calls, deterministic results, faster execution
- **Architecture**: Completes hexagonal architecture pattern with all infrastructure dependencies isolated behind ports
- **Optional**: System functions correctly without this change, but architecture is significantly cleaner with it
- **Classification**: Non-breaking; internal refactor only