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
The system SHALL extract WAV file durations from ZIP archives using wave module or soundfile fallback.

#### Scenario: Standard WAV extraction
- **WHEN** ZIP contains valid WAV files
- **THEN** the system reads frame count and sample rate to calculate duration

#### Scenario: Corrupted WAV fallback
- **WHEN** wave module fails to read WAV header
- **THEN** the system attempts soundfile extraction via temporary file

#### Scenario: Side inference from filename
- **WHEN** WAV filename is "A1_track.wav"
- **THEN** the system infers side="A" and position=1

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

