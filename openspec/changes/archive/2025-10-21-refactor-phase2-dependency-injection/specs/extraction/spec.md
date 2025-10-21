## ADDED Requirements

### Requirement: Settings Propagation in Extraction Pipeline
The system SHALL propagate configuration settings through the extraction pipeline from entry points to domain functions.

#### Scenario: Worker receives settings
- **WHEN** `AnalysisWorker` is constructed
- **THEN** it receives `ToleranceSettings` and `IdExtractionSettings` as constructor parameters
- **AND** stores them for use during analysis

#### Scenario: Settings passed to file discovery
- **WHEN** worker calls `discover_and_pair_files()`
- **THEN** it passes `IdExtractionSettings` as parameter
- **AND** file discovery uses injected settings for ID extraction

#### Scenario: Settings passed to comparison
- **WHEN** worker calls `compare_data()`
- **THEN** it passes `ToleranceSettings` as parameter
- **AND** comparison uses injected settings for threshold classification

#### Scenario: No global config in extraction flow
- **WHEN** extraction pipeline executes from file discovery through comparison
- **THEN** no function accesses global `cfg` object
- **AND** all configuration flows through explicit parameters
