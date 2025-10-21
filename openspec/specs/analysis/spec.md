# analysis Specification

## Purpose
Defines expected behavior, interfaces, and stability rules for the respective module.
## Requirements
### Requirement: File Discovery and Pairing
The system SHALL discover PDF and ZIP files in configured directories and pair them by numeric ID.

#### Scenario: Successful pairing
- **WHEN** PDF directory contains `12345_tracklist.pdf` and ZIP directory contains `12345_masters.zip`
- **THEN** the system creates a pair with ID "12345" linking both files

#### Scenario: Ambiguous pairing
- **WHEN** multiple PDFs or ZIPs share the same numeric ID
- **THEN** the system logs a warning and skips the ambiguous pair

#### Scenario: No matches
- **WHEN** no PDF-ZIP pairs share numeric IDs
- **THEN** the system returns an empty pairs dictionary

### Requirement: Numeric ID Extraction
The system SHALL extract numeric IDs from filenames based on configurable digit length and ignore list.

#### Scenario: ID filtering by length
- **WHEN** filename is "test_12345_master.zip" and min_digits=3, max_digits=6
- **THEN** the system extracts ID 12345

#### Scenario: Ignored numbers
- **WHEN** filename contains "2024" and ignore_numbers includes "2024"
- **THEN** the system excludes 2024 from extracted IDs

### Requirement: Track Comparison
The system SHALL compare PDF tracklist durations with WAV file durations and classify mismatches.

#### Scenario: Perfect match
- **WHEN** PDF track duration is 240s and WAV duration is 240.1s
- **THEN** the system classifies as "OK" (within tolerance)

#### Scenario: Warning threshold
- **WHEN** difference exceeds tolerance_warn (2s) but below tolerance_fail (5s)
- **THEN** the system classifies as "WARN"

#### Scenario: Failure threshold
- **WHEN** difference exceeds tolerance_fail (5s)
- **THEN** the system classifies as "FAIL"
