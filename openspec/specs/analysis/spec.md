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
The system SHALL extract numeric IDs from filenames using injected ID extraction settings that specify digit length and ignore list constraints.

#### Scenario: ID filtering by length
- **WHEN** filename is "test_12345_master.zip" and min_digits=3, max_digits=6
- **THEN** the system extracts ID 12345

#### Scenario: Ignored numbers
- **WHEN** filename contains "2024" and ignore_numbers includes "2024"
- **THEN** the system excludes 2024 from extracted IDs

#### Scenario: Injected ID extraction settings
- **WHEN** different `IdExtractionSettings` objects are supplied to `extract_numeric_id()`
- **THEN** the function filters IDs according to those settings
- **AND** behavior remains deterministic without relying on global config

### Requirement: Track Comparison
The system SHALL compare PDF tracklist durations with WAV file durations using injected tolerance settings together with strongly-typed Pydantic models and classify mismatches based on configurable tolerances.

#### Scenario: Perfect match
- **WHEN** PDF track duration is 240s and WAV duration is 240.1s
- **THEN** the system classifies as "OK" (within tolerance)

#### Scenario: Warning threshold
- **WHEN** difference exceeds tolerance_warn (2s) but below tolerance_fail (5s)
- **THEN** the system classifies as "WARN"

#### Scenario: Failure threshold
- **WHEN** difference exceeds tolerance_fail (5s)
- **THEN** the system classifies as "FAIL"

#### Scenario: Type-safe model handling
- **WHEN** `compare_data()` receives `TrackInfo` and `WavInfo` Pydantic models
- **THEN** the system constructs `SideResult` with model instances directly
- **AND** no dictionary conversion or type casting occurs

#### Scenario: Injected tolerance settings
- **WHEN** `compare_data()` is called with `ToleranceSettings(warn_tolerance=2, fail_tolerance=5)`
- **THEN** the provided thresholds drive warning and failure classification
- **AND** no global configuration is accessed inside the function

### Requirement: Code Quality Standards
The system SHALL maintain zero unreachable code and pass strict type checking.

#### Scenario: No dead code
- **WHEN** static analysis tools scan the codebase
- **THEN** no unreachable statements are detected
- **AND** all code paths are executable

#### Scenario: Strict type checking
- **WHEN** mypy runs with --strict flag
- **THEN** all type annotations are valid
- **AND** no type: ignore comments are needed for core domain logic

### Requirement: Configuration Dependency Injection
The system SHALL inject configuration settings as explicit parameters to domain and adapter functions instead of accessing global state.

#### Scenario: Domain layer purity
- **WHEN** domain functions in `core/domain/` are invoked
- **THEN** all configuration is received via function parameters
- **AND** no global `cfg` imports exist in domain layer

#### Scenario: Adapter layer purity
- **WHEN** adapter functions in `adapters/` are invoked
- **THEN** all configuration is received via function parameters
- **AND** no global `cfg` imports exist in adapter layer

#### Scenario: Entry point responsibility
- **WHEN** application entry points (`app.py`, `fluent_gui.py`) start
- **THEN** they load configuration from global `cfg`
- **AND** construct settings dataclasses
- **AND** inject settings into lower layers

