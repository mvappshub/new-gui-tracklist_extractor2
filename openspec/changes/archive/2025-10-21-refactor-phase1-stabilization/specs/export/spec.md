## ADDED Requirements

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
