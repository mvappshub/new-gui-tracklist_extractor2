# analysis Specification

## Purpose
Defines expected behavior, interfaces, and stability rules for the respective module.
## Requirements
### Requirement: File Discovery and Pairing
The system SHALL discover PDF and ZIP files in configured directories and pair them by a numeric ID, returning a structured FilePair object for each match.

#### Scenario: Successful pairing
- **WHEN** PDF directory contains `12345_tracklist.pdf` and ZIP directory contains `12345_masters.zip`
- **THEN** the system creates a pair with ID `12345` (as `int`)
- **AND** the result for this ID is a `FilePair` object containing the `Path` objects for both files

#### Scenario: Ambiguous pairing
- **WHEN** multiple PDFs or ZIPs share the same numeric ID
- **THEN** the system logs a warning and skips the ambiguous pair

#### Scenario: Type-safe pairing structure
- **WHEN** `discover_and_pair_files()` returns paired files
- **THEN** the return type is `dict[int, FilePair]` instead of `dict[str, dict[str, Path]]`
- **AND** all ID keys are integers for consistent type handling
- **AND** each value is a `FilePair` dataclass with `pdf: Path` and `zip: Path` attributes

#### Scenario: No matches
- **WHEN** no PDF-ZIP pairs share numeric IDs
- **THEN** the system returns an empty pairs dictionary

### Requirement: Numeric ID Extraction
The system SHALL extract numeric IDs from filenames using injected ID extraction settings that specify digit length and ignore list constraints.

#### Scenario: ID filtering by length
- **WHEN** filename is "test_12345_master.zip" and min_digits=3, max_digits=6
- **THEN** the system extracts ID 12345

#### Scenario: Ignored numbers
- **WHEN** filename contains "2024" and ignore_numbers includes "2024"
- **THEN** the system excludes 2024 from extracted IDs

#### Scenario: Injected ID extraction settings
- **WHEN** different `IdExtractionSettings` objects are supplied to `extract_numeric_id()`
- **THEN** the function filters IDs according to those settings
- **AND** behavior remains deterministic without relying on global config

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

### Requirement: Code Quality Standards
The system SHALL maintain zero unreachable code and pass strict type checking.

#### Scenario: No dead code
- **WHEN** static analysis tools scan the codebase
- **THEN** no unreachable statements are detected
- **AND** all code paths are executable

#### Scenario: Strict type checking
- **WHEN** mypy runs with --strict flag
- **THEN** all type annotations are valid
- **AND** no type: ignore comments are needed for core domain logic

### Requirement: Configuration Dependency Injection
The system SHALL inject configuration settings as explicit parameters to domain and adapter functions instead of accessing global state.

#### Scenario: Domain layer purity
- **WHEN** domain functions in `core/domain/` are invoked
- **THEN** all configuration is received via function parameters
- **AND** no global `cfg` imports exist in domain layer

#### Scenario: Adapter layer purity
- **WHEN** adapter functions in `adapters/` are invoked
- **THEN** all configuration is received via function parameters
- **AND** no global `cfg` imports exist in adapter layer

#### Scenario: Entry point responsibility
- **WHEN** application entry points (`app.py`, `fluent_gui.py`) start
- **THEN** they load configuration from global `cfg`
- **AND** construct settings dataclasses
- **AND** inject settings into lower layers

### Requirement: Audio Mode Detection Port
The system SHALL use a port interface and a `Chain of Responsibility` pattern to isolate and orchestrate AI-based audio mode detection from domain logic.

#### Scenario: Chain of Responsibility orchestration
- **WHEN** the `AudioModeDetector` is invoked
- **THEN** it processes a sequence of detection strategies (e.g., strict parsing, AI fallback, deterministic fallback)
- **AND** each strategy attempts to resolve the side and position
- **AND** the process stops once a definitive result is found or all strategies are exhausted

#### Scenario: Centralized filename parsing
- **WHEN** strict parsing step needs to extract side and position from filename
- **THEN** it uses `StrictFilenameParser` domain service
- **AND** no duplicate parsing logic exists across adapters
- **AND** parsing behavior is consistent and testable in isolation

#### Scenario: Real AI adapter
- **WHEN** `AiAudioModeDetector` is instantiated
- **THEN** it acts as one step in the detection chain
- **AND** requires OpenAI/OpenRouter API credentials for its operation

#### Scenario: Fake test adapter
- **WHEN** `FakeAudioModeDetector` is instantiated
- **THEN** it uses a centralized, deterministic `StrictFilenameParser` for its logic
- **AND** guarantees consistent results for the same inputs
- **AND** contains no duplicate parsing implementation

#### Scenario: Port interface definition
- **WHEN** `AudioModeDetector` Protocol is defined
- **THEN** it specifies `detect(wavs: list[WavInfo]) -> dict[str, list[WavInfo]]` method
- **AND** output guarantees normalized positions (sequential 1, 2, 3... per side)
- **AND** output guarantees no gaps or duplicates in positions

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

#### Scenario: Detection via port
- **WHEN** the system needs to detect side and position from WAV filenames
- **THEN** it uses `AudioModeDetector` port from `core.ports`
- **AND** domain layer receives normalized results without knowing detection strategy

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

