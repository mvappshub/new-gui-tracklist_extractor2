## MODIFIED Requirements

### Requirement: Main Window Interface
The application SHALL provide a main window using pure PyQt6 components (QMainWindow, QTableView, QPushButton) with GZ Media branding and intuitive controls for cue sheet analysis.

#### Scenario: Application startup
- **WHEN** the application starts
- **THEN** it displays the main window with GZ Media logo, control buttons, and dual table layout using standard PyQt6 widgets

#### Scenario: File opening
- **WHEN** user clicks on PDF or ZIP file icons in the top table
- **THEN** the corresponding file opens in the default system application

## ADDED Requirements

### Requirement: Settings Management
The application SHALL provide a settings interface using custom PyQt6 components and QSettings for persistence.

#### Scenario: Settings dialog display
- **WHEN** user opens settings
- **THEN** the application displays a settings page with custom `FolderSettingCard` widgets implemented in pure PyQt6

#### Scenario: Settings persistence
- **WHEN** user saves settings
- **THEN** configuration is persisted via QSettings to the platform-specific location
