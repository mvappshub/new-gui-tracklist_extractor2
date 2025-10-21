# export Specification

## Purpose
Defines expected behavior, interfaces, and stability rules for the respective module.
## Requirements
### Requirement: Auto Export Analysis Results
The system SHALL automatically export analysis results to JSON after each analysis run when `export.auto` is true.

#### Scenario: Success
- WHEN an analysis run completes with one or more `SideResult` items
- AND `export.auto` is true
- THEN the app writes a JSON file to `export.default_dir`
- AND the filename matches `analysis_YYYYMMDD_HHMMSS.json`
- AND each `SideResult` entry contains string paths and numeric durations

#### Scenario: Disabled
- GIVEN `export.auto` is false
- WHEN an analysis run completes
- THEN no JSON export is written

#### Scenario: Directory Creation
- GIVEN `export.default_dir` does not exist
- WHEN an analysis run completes and export is enabled
- THEN the directory is created automatically
- AND the JSON export is written

#### Scenario: Write Failure
- GIVEN the app cannot write to `export.default_dir`
- WHEN an analysis run completes and export is enabled
- THEN the app logs an error and continues without crashing

### Requirement: Golden Output Generation
The system SHALL support generating reference JSON outputs for regression testing.

#### Scenario: Comparison result serialization
- **WHEN** `SideResult` objects are serialized to JSON
- **THEN** all fields are properly converted to JSON-compatible types
- **AND** Path objects are converted to strings
- **AND** Pydantic models are serialized with their schema

#### Scenario: Golden file storage
- **WHEN** characterization tests run in record mode
- **THEN** current outputs are saved to `tests/data/golden/` directory
- **AND** subsequent test runs compare against these references

#### Scenario: Floating-point tolerance
- **WHEN** comparing golden outputs with current results
- **THEN** duration fields allow small floating-point differences (≤0.01s)
- **AND** integer fields require exact matches

