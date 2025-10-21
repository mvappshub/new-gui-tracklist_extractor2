## ADDED Requirements

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

