# Phase 5: AI Port - Implementation Tasks

## 1. Create Port Interface
- [ ] 1.1 Create `core/ports.py` file (new file in core package)
- [ ] 1.2 Add module docstring: "Port interfaces for hexagonal architecture - domain depends on these abstractions, adapters implement them."
- [ ] 1.3 Define `AudioModeDetector` Protocol with `from typing import Protocol`
- [ ] 1.4 Add method signature: `def detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]: ...`
- [ ] 1.5 Add comprehensive docstring explaining: (a) Protocol purpose - detect side/position from WAV filenames, (b) Input: list of WavInfo with filename and duration_sec populated, (c) Output: dict mapping side (e.g., "A", "B") to list of WavInfo with side and position populated and normalized, (d) Normalization: positions must be sequential (1, 2, 3...) with no gaps or duplicates
- [ ] 1.6 Import `WavInfo` from `core.models.analysis`
- [ ] 1.7 Add type hints for all parameters and return values
- [ ] 1.8 Run `mypy --strict core/ports.py` to verify type safety
- [ ] 1.9 **Git commit**: `git commit -m "refactor(phase5): create AudioModeDetector port interface"`

## 2. Implement Real AI Adapter
- [ ] 2.1 Create `adapters/audio/ai_mode_detector.py` file
- [ ] 2.2 Import `AudioModeDetector` from `core.ports`
- [ ] 2.3 Import `detect_audio_mode_with_ai` and `normalize_positions` from `wav_extractor_wave`
- [ ] 2.4 Import `WavInfo` from `core.models.analysis`
- [ ] 2.5 Define `AiAudioModeDetector` class implementing `AudioModeDetector` Protocol
- [ ] 2.6 Implement `detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]` method
- [ ] 2.7 Method implementation: (a) Call `side_map = detect_audio_mode_with_ai(wavs)` to get initial detection, (b) Call `normalize_positions(side_map)` to ensure sequential positions, (c) Return normalized `side_map`
- [ ] 2.8 Add comprehensive docstring explaining: "Real AI-backed audio mode detector using OpenAI/OpenRouter APIs. Wraps existing wav_extractor_wave functions for strict parsing → AI fallback → deterministic fallback → normalization."
- [ ] 2.9 Add type hints for all parameters and return values
- [ ] 2.10 Handle edge cases: empty input list, all detection failures
- [ ] 2.11 Run `mypy --strict adapters/audio/ai_mode_detector.py` to verify type safety
- [ ] 2.12 **Git commit**: `git commit -m "refactor(phase5): implement AiAudioModeDetector adapter"`

## 3. Implement Fake Test Adapter
- [ ] 3.1 Create `adapters/audio/fake_mode_detector.py` file
- [ ] 3.2 Import `AudioModeDetector` from `core.ports`
- [ ] 3.3 Import `WavInfo` from `core.models.analysis`
- [ ] 3.4 Import `re` for filename parsing
- [ ] 3.5 Define `FakeAudioModeDetector` class implementing `AudioModeDetector` Protocol
- [ ] 3.6 Implement `detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]` method with deterministic logic
- [ ] 3.7 Deterministic detection logic: (a) Parse side from filename using regex `r"Side[_-]?([A-Za-z]+)"` (case-insensitive), (b) Parse position from filename using regex `r"^0*([1-9][0-9]?)\b"` or `r"([A-Za-z]+)0*([1-9][0-9]?)"`, (c) Default to side="A" if not found, (d) Group by side, (e) Sort by position (or filename if position missing), (f) Renumber positions sequentially (1, 2, 3...) per side
- [ ] 3.8 Add comprehensive docstring: "Fake audio mode detector for tests. Uses deterministic filename parsing with no external API calls. Guarantees consistent results for same inputs."
- [ ] 3.9 Add type hints for all parameters and return values
- [ ] 3.10 Ensure no external dependencies (no OpenAI, no HTTP calls)
- [ ] 3.11 Run `mypy --strict adapters/audio/fake_mode_detector.py` to verify type safety
- [ ] 3.12 **Git commit**: `git commit -m "refactor(phase5): implement FakeAudioModeDetector for tests"`

## 4. Refactor Domain Layer
- [ ] 4.1 Update `core/domain/comparison.py` to import `AudioModeDetector` from `core.ports` (add after line 8)
- [ ] 4.2 Remove import from `wav_extractor_wave` (delete line 9: `from wav_extractor_wave import detect_audio_mode_with_ai, normalize_positions`)
- [ ] 4.3 Remove module-level type aliases and casts (delete lines 11-14: `DetectFn`, `NormalizeFn`, `_detect`, `_normalize`)
- [ ] 4.4 Update `detect_audio_mode()` function signature (line 16) to accept `detector: AudioModeDetector` parameter: `def detect_audio_mode(wavs: list[WavInfo], detector: AudioModeDetector) -> tuple[dict[str, str], dict[str, list[WavInfo]]]:`
- [ ] 4.5 Update function body (line 24) to call detector: `side_map = detector.detect(wavs)` (replaces `_detect(wavs)` and `_normalize(side_map)` calls)
- [ ] 4.6 Remove line 25 `_normalize(side_map)` since detector returns normalized results
- [ ] 4.7 Update `compare_data()` function signature (line 35) to accept `detector: AudioModeDetector` parameter after `tolerance_settings`
- [ ] 4.8 Update `detect_audio_mode()` call (line 43) to pass detector: `modes, wavs_by_side = detect_audio_mode(wav_data, detector)`
- [ ] 4.9 Update function docstrings to document new `detector` parameter
- [ ] 4.10 Run `rg "wav_extractor_wave" core/domain/` to confirm no remaining imports
- [ ] 4.11 Run `mypy --strict core/domain/comparison.py` to verify type safety
- [ ] 4.12 **Git commit**: `git commit -m "refactor(phase5): remove AI dependencies from domain layer"`

## 5. Update Service Layer
- [ ] 5.1 Update `services/analysis_service.py` to import `AudioModeDetector` from `core.ports` (add after line 10)
- [ ] 5.2 Import `AiAudioModeDetector` from `adapters.audio.ai_mode_detector` (add after line 7)
- [ ] 5.3 Update `__init__` method signature (line 23) to accept `audio_mode_detector: AudioModeDetector | None = None` parameter after `wav_reader`
- [ ] 5.4 Store detector as instance attribute (after line 31): `self._audio_mode_detector = audio_mode_detector or AiAudioModeDetector()`
- [ ] 5.5 Update `compare_data()` call (line 65) to pass detector: `side_results = compare_data(pdf_data, wav_data, pair_info, self._tolerance_settings, self._audio_mode_detector)`
- [ ] 5.6 Update class docstring (lines 16-21) to mention detector injection
- [ ] 5.7 Run `mypy --strict services/analysis_service.py` to verify type safety
- [ ] 5.8 **Git commit**: `git commit -m "refactor(phase5): integrate AudioModeDetector in service layer"`

## 6. Update Entry Points and Scripts
- [ ] 6.1 Update `scripts/smoke_test.py` to import `AiAudioModeDetector` from `adapters.audio.ai_mode_detector` (add after line 8)
- [ ] 6.2 Instantiate detector after line 28: `audio_mode_detector = AiAudioModeDetector()`
- [ ] 6.3 Update `compare_data()` call (line 38) to pass detector: `side_results = compare_data(pdf_data, wav_data, pair_info, tolerance_settings, audio_mode_detector)`
- [ ] 6.4 Verify `app.py` doesn't need changes (it only instantiates `AnalysisWorkerManager`, which instantiates `AnalysisService` with default detector)
- [ ] 6.5 Run `rg "from wav_extractor_wave import" --type py` to confirm only `adapters/audio/ai_mode_detector.py` imports from it
- [ ] 6.6 **Git commit**: `git commit -m "refactor(phase5): update scripts to use AudioModeDetector"`

## 7. Update Test Infrastructure
- [ ] 7.1 Update `tests/conftest.py` to import `FakeAudioModeDetector` from `adapters.audio.fake_mode_detector` (add after line 16)
- [ ] 7.2 Add `audio_mode_detector` fixture after line 121: `@pytest.fixture\ndef audio_mode_detector() -> FakeAudioModeDetector:\n    """Provide fake audio mode detector for tests (no external API calls)."""\n    return FakeAudioModeDetector()`
- [ ] 7.3 Update `tests/test_characterization.py` to accept `audio_mode_detector` fixture in test functions
- [ ] 7.4 Update `test_compare_data_matches_golden` (line 81) to accept fixture: `def test_compare_data_matches_golden(tmp_path, tolerance_settings, audio_mode_detector) -> None:`
- [ ] 7.5 Update `compare_data()` call (line 100) to pass detector: `results = compare_data(pdf_data, wav_data, pair_info, tolerance_settings, audio_mode_detector)`
- [ ] 7.6 Update `test_compare_data_respects_injected_tolerances` (line 121) to accept fixture: `def test_compare_data_respects_injected_tolerances(tmp_path: Path, warn_tolerance: int, fail_tolerance: int, expected_status: str, audio_mode_detector) -> None:`
- [ ] 7.7 Update `compare_data()` call (line 147) to pass detector: `results = compare_data(pdf_data, wav_data, pair_info, tolerance, audio_mode_detector)`
- [ ] 7.8 Run `pytest tests/test_characterization.py -v` to verify tests pass with fake detector
- [ ] 7.9 Verify tests run faster (no external API calls)
- [ ] 7.10 **Git commit**: `git commit -m "test(phase5): update tests to use FakeAudioModeDetector"`

## 8. Create Unit Tests for Adapters
- [ ] 8.1 Create `tests/test_ai_mode_detector.py` for adapter tests
- [ ] 8.2 Add test for `AiAudioModeDetector` with valid WAV filenames: `test_ai_detector_with_valid_filenames`
- [ ] 8.3 Add test for `AiAudioModeDetector` with ambiguous filenames (triggers AI fallback): `test_ai_detector_with_ambiguous_filenames`
- [ ] 8.4 Add test for `AiAudioModeDetector` with empty input: `test_ai_detector_with_empty_input`
- [ ] 8.5 Add test for `FakeAudioModeDetector` with Side_A/Side_B filenames: `test_fake_detector_with_side_prefixes`
- [ ] 8.6 Add test for `FakeAudioModeDetector` with A1/B1 prefixes: `test_fake_detector_with_letter_number_prefixes`
- [ ] 8.7 Add test for `FakeAudioModeDetector` with ambiguous filenames (defaults to side A): `test_fake_detector_with_ambiguous_filenames`
- [ ] 8.8 Add test for `FakeAudioModeDetector` position normalization: `test_fake_detector_normalizes_positions`
- [ ] 8.9 Add test verifying `FakeAudioModeDetector` is deterministic (same input → same output): `test_fake_detector_is_deterministic`
- [ ] 8.10 Mock external API calls in `AiAudioModeDetector` tests to avoid real API usage
- [ ] 8.11 Run `pytest tests/test_ai_mode_detector.py -v` to verify all tests pass
- [ ] 8.12 **Git commit**: `git commit -m "test(phase5): add unit tests for audio mode detectors"`

## 9. Validation and Quality Gates
- [ ] 9.1 Run `tools/check.sh` and verify all checks pass (pytest, coverage ≥85%, ruff, mypy --strict, openspec validate)
- [ ] 9.2 Run `mypy --strict core/ports.py adapters/audio/ai_mode_detector.py adapters/audio/fake_mode_detector.py` to verify type safety
- [ ] 9.3 Run `rg "from wav_extractor_wave import" --type py` to confirm only `adapters/audio/ai_mode_detector.py` imports from it
- [ ] 9.4 Run `rg "import wav_extractor_wave" core/domain/` to confirm no domain imports
- [ ] 9.5 Verify `core/domain/comparison.py` has no infrastructure dependencies
- [ ] 9.6 Run `openspec validate refactor-phase5-ai-port --strict` and fix any issues
- [ ] 9.7 Verify all delta specs have at least one `#### Scenario:` per requirement
- [ ] 9.8 Confirm proposal.md clearly explains optional nature and non-breaking changes
- [ ] 9.9 Update tasks.md checkboxes as work progresses
- [ ] 9.10 Final smoke test: run `scripts/smoke_test.py` and verify functionality unchanged
- [ ] 9.11 Verify test suite runs faster (no external API calls in tests)
- [ ] 9.12 Verify coverage for new adapter code meets 85% threshold
- [ ] 9.13 **Git commit**: `git commit -m "refactor(phase5): complete AI port - all quality gates passed"`

**Note**: Each git commit command creates an atomic checkpoint. If issues arise, you can revert to the last successful commit. Use `git log --oneline` to view commit history and `git revert <commit-hash>` if rollback is needed.

**Optional Nature**: Phase 5 is marked as optional in the strategic plan. The system functions correctly without this change, but completing it provides significant architectural benefits: (1) domain layer becomes pure with zero infrastructure dependencies, (2) tests run faster without external API calls, (3) detection strategy can be swapped without changing domain code, (4) hexagonal architecture is complete.