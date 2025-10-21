## MODIFIED Requirements

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

## ADDED Requirements

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
