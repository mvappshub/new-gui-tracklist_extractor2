## MODIFIED Requirements

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