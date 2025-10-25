# Extraction Capability Delta Specification

## Purpose
This delta specification defines MODIFIED and ADDED requirements for the extraction capability as part of the refactor-unified-audit-plan.

## MODIFIED Requirements

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

## ADDED Requirements

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