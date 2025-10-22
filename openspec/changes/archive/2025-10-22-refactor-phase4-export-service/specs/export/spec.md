## MODIFIED Requirements

### Requirement: Auto Export Analysis Results
The system SHALL automatically export analysis results to JSON after each analysis run when `export.auto` is true, using the centralized export service.

#### Scenario: Success
- WHEN an analysis run completes with one or more `SideResult` items
- AND `export.auto` is true
- THEN the app calls `export_results_to_json()` from `services.export_service`
- AND writes a JSON file to `export.default_dir`
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

#### Scenario: Injected export settings
- **WHEN** `ExportSettings(auto_export=True, export_dir=Path("exports"))` is provided
- **THEN** export decisions rely solely on the injected settings object
- **AND** no global configuration is accessed during export

#### Scenario: Service layer usage
- **WHEN** UI layer needs to export results
- **THEN** it imports `export_results_to_json` from `services.export_service`
- **AND** passes `results` and `export_settings` parameters
- **AND** receives `Optional[Path]` return value (exported file path or None)

