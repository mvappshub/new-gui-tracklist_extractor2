## ADDED Requirements

### Requirement: WAV File I/O Adapter
The system SHALL use an adapter layer to isolate ZIP and WAV file I/O operations from domain logic.

#### Scenario: ZIP reading via adapter
- **WHEN** the system needs to extract WAV files from a ZIP archive
- **THEN** it uses `ZipWavFileReader` adapter from `adapters.audio.wav_reader`
- **AND** domain layer receives `list[WavInfo]` objects without performing I/O

#### Scenario: Adapter error handling
- **WHEN** ZIP file cannot be opened or is corrupted
- **THEN** the adapter logs appropriate error messages
- **AND** returns empty list without crashing
- **AND** domain layer handles empty results gracefully

#### Scenario: Temporary file management
- **WHEN** adapter extracts WAV files for duration probing
- **THEN** it creates temporary directory for extraction
- **AND** cleans up temporary files after processing
- **AND** domain layer is unaware of temporary file operations

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

## MODIFIED Requirements

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
