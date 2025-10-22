# Analysis Capability - Phase 5 Delta Spec

## ADDED Requirements

### Requirement: Audio Mode Detection Port
The system SHALL use a port interface to isolate AI-based audio mode detection from domain logic.

#### Scenario: Detection via port
- **WHEN** the system needs to detect side and position from WAV filenames
- **THEN** it uses `AudioModeDetector` port from `core.ports`
- **AND** domain layer receives normalized results without knowing detection strategy

#### Scenario: Port interface definition
- **WHEN** `AudioModeDetector` Protocol is defined
- **THEN** it specifies `detect(wavs: list[WavInfo]) -> dict[str, list[WavInfo]]` method
- **AND** output guarantees normalized positions (sequential 1, 2, 3... per side)
- **AND** output guarantees no gaps or duplicates in positions

#### Scenario: Real AI adapter
- **WHEN** `AiAudioModeDetector` is instantiated
- **THEN** it wraps existing `detect_audio_mode_with_ai` and `normalize_positions` functions
- **AND** provides strict parsing → AI fallback → deterministic fallback → normalization
- **AND** requires OpenAI/OpenRouter API credentials for AI fallback

#### Scenario: Fake test adapter
- **WHEN** `FakeAudioModeDetector` is instantiated
- **THEN** it uses deterministic filename parsing with no external API calls
- **AND** guarantees consistent results for same inputs
- **AND** enables fast test execution without mocking external services

#### Scenario: Service layer integration
- **WHEN** `AnalysisService` is constructed
- **THEN** it accepts `audio_mode_detector: AudioModeDetector | None` parameter
- **AND** defaults to `AiAudioModeDetector()` if not provided
- **AND** passes detector to `compare_data()` function

#### Scenario: Test integration
- **WHEN** tests verify comparison behavior
- **THEN** they use `FakeAudioModeDetector` via pytest fixture
- **AND** avoid external API calls for deterministic, fast execution
- **AND** can test different detection scenarios by configuring fake detector

### Requirement: Complete Domain Layer Purity
The system SHALL maintain domain layer completely free of infrastructure dependencies including AI services.

#### Scenario: No AI imports in domain
- **WHEN** domain modules in `core/domain/` are inspected
- **THEN** they contain no imports from `wav_extractor_wave` or AI libraries
- **AND** all AI detection is delegated to adapter layer via port interface

#### Scenario: Domain depends on abstractions
- **WHEN** `compare_data()` function needs audio mode detection
- **THEN** it receives `AudioModeDetector` port via parameter
- **AND** calls `detector.detect(wavs)` without knowing implementation
- **AND** remains testable with any detector implementation

#### Scenario: No module-level infrastructure
- **WHEN** domain modules are loaded
- **THEN** they contain no module-level variables referencing infrastructure
- **AND** no module-level function casts to external implementations
- **AND** all dependencies are explicit via function parameters

## MODIFIED Requirements

### Requirement: Track Comparison
The system SHALL compare PDF tracklist durations with WAV file durations using injected tolerance settings and audio mode detector together with strongly-typed Pydantic models and classify mismatches based on configurable tolerances.

#### Scenario: Perfect match
- **WHEN** PDF track duration is 240s and WAV duration is 240.1s
- **THEN** the system classifies as "OK" (within tolerance)

#### Scenario: Warning threshold
- **WHEN** difference exceeds tolerance_warn (2s) but below tolerance_fail (5s)
- **THEN** the system classifies as "WARN"

#### Scenario: Failure threshold
- **WHEN** difference exceeds tolerance_fail (5s)
- **THEN** the system classifies as "FAIL"

#### Scenario: Type-safe model handling
- **WHEN** `compare_data()` receives `TrackInfo` and `WavInfo` Pydantic models
- **THEN** the system constructs `SideResult` with model instances directly
- **AND** no dictionary conversion or type casting occurs

#### Scenario: Injected tolerance settings
- **WHEN** `compare_data()` is called with `ToleranceSettings(warn_tolerance=2, fail_tolerance=5)`
- **THEN** the provided thresholds drive warning and failure classification
- **AND** no global configuration is accessed inside the function

#### Scenario: Injected audio mode detector
- **WHEN** `compare_data()` is called with `audio_mode_detector` parameter
- **THEN** the system uses the provided detector for side/position detection
- **AND** no direct imports from `wav_extractor_wave` occur
- **AND** detection strategy can be swapped without changing domain code

#### Scenario: Detector returns normalized results
- **WHEN** detector processes WAV files
- **THEN** returned `dict[str, list[WavInfo]]` has normalized positions per side
- **AND** positions are sequential (1, 2, 3...) with no gaps
- **AND** domain layer does not need to perform additional normalization

## REMOVED Requirements

None. Phase 5 adds capabilities without removing existing functionality.

## Migration Notes

Phase 5 is **optional** but recommended for architectural completeness:
- **Before**: Domain layer imports AI functions directly from `wav_extractor_wave.py`
- **After**: Domain layer depends on `AudioModeDetector` port, adapters implement detection strategies
- **Benefits**: (1) Domain layer is pure with zero infrastructure dependencies, (2) Tests run faster without external API calls, (3) Detection strategy can be swapped (e.g., rule-based, ML model, external service), (4) Hexagonal architecture is complete
- **No breaking changes**: All existing functionality preserved, only internal architecture improved