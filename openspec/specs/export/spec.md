# export Specification

## Purpose
Defines expected behavior, interfaces, and stability rules for the respective module.
## Requirements
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

### Requirement: Export Settings Dataclass
The system SHALL use `ExportSettings` dataclass to encapsulate export configuration.

#### Scenario: Settings construction
- **WHEN** entry point loads configuration
- **THEN** it constructs `ExportSettings(auto_export=bool, export_dir=Path)` from global config
- **AND** passes settings to export service

#### Scenario: Settings validation
- **WHEN** `ExportSettings` is constructed with invalid values
- **THEN** validation occurs at construction time
- **AND** errors are caught early in entry point

### Requirement: Centralized Export Service
The system SHALL provide export functionality exclusively through `services.export_service` module as the single source of truth.

#### Scenario: Canonical import path
- **WHEN** code needs to export analysis results
- **THEN** it imports `export_results_to_json` from `services.export_service`
- **AND** no other modules provide export functionality

#### Scenario: UI layer integration
- **WHEN** UI components need to export results
- **THEN** they import from `services.export_service` directly
- **AND** do not use wrapper functions or indirect imports

#### Scenario: Test integration
- **WHEN** tests verify export functionality
- **THEN** they import from `services.export_service` directly
- **AND** test the canonical implementation, not wrappers

#### Scenario: No duplicate implementations
- **WHEN** searching codebase for export implementations
- **THEN** only `services/export_service.py` contains export logic
- **AND** no wrapper functions or duplicates exist in other modules

### Requirement: Export Service Documentation
The system SHALL document `services.export_service` as the authoritative export implementation.

#### Scenario: Module docstring clarity
- **WHEN** developers read `services/export_service.py` module docstring
- **THEN** it clearly states this is the single source of truth for exports
- **AND** provides guidance on correct import path

#### Scenario: Function docstring with usage example
- **WHEN** developers read `export_results_to_json()` docstring
- **THEN** it includes usage example showing correct import
- **AND** explains this is the canonical implementation

