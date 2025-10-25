# extraction Specification

## Purpose
Defines expected behavior, interfaces, and stability rules for the respective module.
## Requirements
### Requirement: PDF Tracklist Extraction
The system SHALL extract track information from PDF cue sheets using Vision LLM and consolidate by side.

#### Scenario: Multi-page PDF extraction
- **WHEN** PDF contains multiple pages with track listings
- **THEN** the system renders each page, sends to LLM, and consolidates tracks by side

#### Scenario: Side detection
- **WHEN** PDF contains headers like "Side A" or "SIDE B"
- **THEN** the system correctly assigns tracks to their respective sides

### Requirement: WAV Duration Extraction
The system SHALL extract WAV file durations from ZIP archives using adapter layer that encapsulates wave module and soundfile fallback logic.

#### Scenario: Standard WAV extraction
- **WHEN** ZIP contains valid WAV files
- **THEN** the system reads frame count and sample rate to calculate duration

#### Scenario: Corrupted WAV fallback
- **WHEN** wave module fails to read WAV header
- **THEN** the system attempts soundfile extraction via temporary file

#### Scenario: Side inference from filename
- **WHEN** WAV filename is "A1_track.wav"
- **THEN** the system infers side="A" and position=1

#### Scenario: Adapter-based extraction
- **WHEN** `ZipWavFileReader.read_wav_files()` is called with ZIP path
- **THEN** the adapter opens ZIP, extracts WAV files to temporary directory
- **AND** probes each WAV using `get_wav_duration` from `audio_utils`
- **AND** returns `list[WavInfo]` with filename and duration_sec populated
- **AND** cleans up temporary files automatically

#### Scenario: Service layer integration
- **WHEN** `AnalysisService` processes a PDF-ZIP pair
- **THEN** it uses `ZipWavFileReader` instance to extract WAV metadata
- **AND** passes resulting `list[WavInfo]` to domain comparison logic
- **AND** domain layer performs no file I/O operations

### Requirement: Audio Mode Detection
The system SHALL detect audio mode (stereo/mono) from WAV files with AI fallback.

#### Scenario: Stereo detection
- **WHEN** WAV file has 2 channels
- **THEN** the system reports mode as "stereo"

#### Scenario: Mono detection
- **WHEN** WAV file has 1 channel
- **THEN** the system reports mode as "mono"

### Requirement: Behavior Characterization
The system SHALL maintain consistent extraction behavior verified by golden reference outputs.

#### Scenario: PDF extraction consistency
- **WHEN** the same PDF cue sheet is processed multiple times
- **THEN** extracted track data matches golden JSON reference
- **AND** side assignments, positions, and durations remain stable

#### Scenario: WAV extraction consistency
- **WHEN** the same ZIP archive is processed multiple times
- **THEN** extracted WAV metadata matches golden JSON reference
- **AND** duration calculations remain deterministic

#### Scenario: Pairing consistency
- **WHEN** PDF and ZIP files are discovered and paired
- **THEN** pairing results match golden reference
- **AND** numeric ID extraction follows configured rules consistently

### Requirement: Settings Propagation in Extraction Pipeline
The system SHALL propagate configuration settings through the extraction pipeline from entry points to domain functions.

#### Scenario: Worker receives settings
- **WHEN** `AnalysisWorker` is constructed
- **THEN** it receives `ToleranceSettings` and `IdExtractionSettings` as constructor parameters
- **AND** stores them for use during analysis

#### Scenario: Settings passed to file discovery
- **WHEN** worker calls `discover_and_pair_files()`
- **THEN** it passes `IdExtractionSettings` as parameter
- **AND** file discovery uses injected settings for ID extraction

#### Scenario: Settings passed to comparison
- **WHEN** worker calls `compare_data()`
- **THEN** it passes `ToleranceSettings` as parameter
- **AND** comparison uses injected settings for threshold classification

#### Scenario: No global config in extraction flow
- **WHEN** extraction pipeline executes from file discovery through comparison
- **THEN** no function accesses global `cfg` object
- **AND** all configuration flows through explicit parameters

### Requirement: WAV File I/O Adapter
The system SHALL use an adapter layer to isolate ZIP and WAV file I/O operations from domain logic, with specific and narrowed exception handling.

#### Scenario: ZIP reading via adapter
- **WHEN** the system needs to extract WAV files from a ZIP archive
- **THEN** it uses `ZipWavFileReader` adapter from `adapters.audio.wav_reader`
- **AND** domain layer receives `list[WavInfo]` objects without performing I/O

#### Scenario: Adapter error handling
- **WHEN** a ZIP file is corrupted
- **THEN** the adapter catches a specific `zipfile.BadZipFile` exception
- **AND** logs an appropriate error message
- **AND** returns an empty list without crashing

#### Scenario: Specific exception types
- **WHEN** adapter encounters I/O errors during WAV extraction
- **THEN** it catches specific exceptions (`zipfile.BadZipFile`, `IOError`, `OSError`) instead of broad `Exception`
- **AND** each exception type is handled with appropriate logging and recovery
- **AND** no generic `except Exception` clauses exist in production code paths

### Requirement: Domain Layer Purity
The system SHALL maintain domain layer free of file I/O operations and infrastructure dependencies.

#### Scenario: No I/O imports in domain
- **WHEN** domain modules in `core/domain/` are inspected
- **THEN** they contain no imports of `zipfile`, `tempfile`, `shutil`, `os.path`, or `open()`
- **AND** all file operations are delegated to adapter layer

#### Scenario: Domain receives data objects
- **WHEN** domain functions need WAV metadata
- **THEN** they receive `WavInfo` objects from adapters
- **AND** do not access file system directly
- **AND** remain testable without real files

#### Scenario: Adapter instantiation at service layer
- **WHEN** service layer orchestrates extraction workflow
- **THEN** it instantiates `ZipWavFileReader` adapter
- **AND** passes results to domain functions
- **AND** domain functions remain pure and side-effect free

### Requirement: PDF Extraction Module Decomposition
**ADDED:** The system SHALL decompose PDF extraction logic into single-responsibility components following adapter and domain service patterns.

#### Scenario: PDF rendering isolation
- **WHEN** the system needs to render PDF pages to images
- **THEN** it uses `PdfImageRenderer` adapter that encapsulates PyMuPDF operations
- **AND** rendering logic is isolated from VLM communication and parsing

#### Scenario: VLM client isolation
- **WHEN** the system needs to call Vision LLM API
- **THEN** it uses `VlmClient` adapter that encapsulates API communication
- **AND** API logic is isolated from rendering and parsing

#### Scenario: Tracklist parsing isolation
- **WHEN** the system needs to parse and consolidate track data from VLM response
- **THEN** it uses `TracklistParser` domain service
- **AND** parsing logic is isolated from I/O operations
- **AND** parser is testable with mock VLM responses

