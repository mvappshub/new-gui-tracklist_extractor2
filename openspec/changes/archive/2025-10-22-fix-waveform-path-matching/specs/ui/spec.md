## MODIFIED Requirements

### Requirement: Table Interactions
The application SHALL provide interactive tables for browsing analysis results.

#### Scenario: Waveform viewer opens for files in ZIP subdirectories
- **WHEN** user clicks the "View" button for a WAV file located in a subdirectory of a ZIP archive
- **THEN** the `WaveformEditorDialog` opens successfully
- **AND** the correct WAV file is extracted and displayed without a `FileNotFoundError`