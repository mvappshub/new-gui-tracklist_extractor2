## MODIFIED Requirements

### Requirement: File Analysis Controls
The application SHALL provide controls for running analysis via a service layer that orchestrates domain operations.

#### Scenario: Analysis execution
- **WHEN** user clicks "Run analysis" button
- **THEN** the application invokes `AnalysisService` which coordinates file discovery, extraction, and comparison through domain modules

#### Scenario: Progress reporting
- **WHEN** analysis is running
- **THEN** the service emits progress signals that update the GUI status bar and progress indicator

#### Scenario: Result display
- **WHEN** analysis completes
- **THEN** the service returns structured results that populate the table models without GUI knowing domain logic details

