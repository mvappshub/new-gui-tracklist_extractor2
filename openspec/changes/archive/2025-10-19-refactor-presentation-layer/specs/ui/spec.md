## MODIFIED Requirements

### Requirement: Main Window Interface
The application SHALL provide a main window using pure PyQt6 components (QMainWindow, QTableView, QPushButton) with GZ Media branding and intuitive controls for cue sheet analysis. The UI SHALL be organized into modular, reusable components within a `ui/` package structure with dependency injection for configuration and services.

#### Scenario: Application startup
- **WHEN** the application starts
- **THEN** it displays the main window with GZ Media logo, control buttons, and dual table layout using standard PyQt6 widgets
- **AND** the UI components are loaded from modular packages (`ui.models`, `ui.workers`, `ui.dialogs`, `ui.main_window`)
- **AND** all components receive their dependencies via constructor injection

#### Scenario: Component reusability
- **WHEN** a developer needs to modify or test a UI component
- **THEN** they can work with isolated modules (e.g., `ResultsTableModel`, `AnalysisWorker`) without touching unrelated code
- **AND** each component has clear dependencies and can be unit tested independently with mock dependencies

#### Scenario: File opening
- **WHEN** user clicks on PDF or ZIP file icons in the top table
- **THEN** the corresponding file opens in the default system application

### Requirement: File Analysis Controls
The application SHALL provide controls for running analysis via a service layer that orchestrates domain operations, with worker lifecycle managed by a dedicated manager.

#### Scenario: Analysis execution
- **WHEN** user clicks "Run analysis" button
- **THEN** the MainWindow delegates to `AnalysisWorkerManager` which creates and manages the worker thread
- **AND** the worker invokes `AnalysisService` which coordinates file discovery, extraction, and comparison

#### Scenario: Progress reporting
- **WHEN** analysis is running
- **THEN** the worker manager forwards progress signals from the service to the GUI
- **AND** the GUI updates the status bar and progress indicator

#### Scenario: Worker cleanup
- **WHEN** analysis completes or the window closes
- **THEN** the worker manager safely terminates the worker thread and cleans up resources
- **AND** no memory leaks or zombie threads remain

## ADDED Requirements

### Requirement: Dependency Injection Architecture
The UI layer SHALL use dependency injection for all configuration and service dependencies, eliminating direct imports of global configuration objects.

#### Scenario: Configuration injection
- **WHEN** a UI component needs configuration values
- **THEN** it receives a specific configuration object (e.g., `ToleranceSettings`, `ExportSettings`) via constructor parameter
- **AND** the component does not directly import or access global `config.cfg`

#### Scenario: Service injection
- **WHEN** MainWindow needs worker management
- **THEN** it receives an `AnalysisWorkerManager` instance via constructor
- **AND** the MainWindow does not directly create or manage QThread instances

#### Scenario: Testability with mocks
- **WHEN** a developer writes unit tests for a UI component
- **THEN** they can inject mock configuration and service objects
- **AND** the component can be tested in isolation without global state

### Requirement: Configuration Abstractions
The application SHALL provide typed configuration models that represent specific subsets of configuration needed by components.

#### Scenario: Tolerance settings
- **WHEN** TracksTableModel needs tolerance values for match calculation
- **THEN** it receives a `ToleranceSettings` object with `warn_tolerance` and `fail_tolerance` fields
- **AND** the model uses these values without accessing global configuration

#### Scenario: Export settings
- **WHEN** ExportService needs to determine export behavior
- **THEN** it receives an `ExportSettings` object with `auto_export` and `export_dir` fields
- **AND** uses the injected settings for export behavior
- **AND** returns the export path to the UI for status display

#### Scenario: Theme settings
- **WHEN** ResultsTableModel needs status colors
- **THEN** it receives a `ThemeSettings` object with `status_colors` dictionary
- **AND** the model uses these colors for cell background rendering

### Requirement: Worker Lifecycle Management
The application SHALL encapsulate all worker and thread lifecycle management in a dedicated manager class, separating this concern from the main window.

#### Scenario: Worker creation
- **WHEN** analysis needs to start
- **THEN** AnalysisWorkerManager creates a new QThread and AnalysisWorker
- **AND** connects all necessary signals
- **AND** starts the thread

#### Scenario: Worker monitoring
- **WHEN** the UI needs to check if analysis is running
- **THEN** it queries `worker_manager.is_running()`
- **AND** receives accurate state without accessing thread internals

#### Scenario: Worker termination
- **WHEN** analysis completes or user closes the window
- **THEN** AnalysisWorkerManager safely stops the worker
- **AND** waits for thread completion with timeout
- **AND** cleans up all resources

### Requirement: Modular UI Architecture
The UI layer SHALL be organized into separate packages for models, workers, dialogs, and utilities, with each module having a single, well-defined responsibility.

#### Scenario: Table model isolation
- **WHEN** the results table needs modification
- **THEN** developers work only with `ui/models/results_table_model.py`
- **AND** changes do not affect other UI components

#### Scenario: Worker thread isolation
- **WHEN** analysis threading logic needs updates
- **THEN** developers work only with `ui/workers/analysis_worker.py` or `ui/workers/worker_manager.py`
- **AND** the worker can be tested independently with mock services

#### Scenario: Theme management
- **WHEN** GZ Media branding needs updates
- **THEN** developers modify only `ui/theme.py`
- **AND** theme changes apply consistently across all UI components

#### Scenario: Constants centralization
- **WHEN** UI strings or constants need updates
- **THEN** developers modify only `ui/constants.py`
- **AND** changes propagate to all components that import them

### Requirement: Export Service Separation
Export functionality SHALL be moved from the presentation layer to the service layer with dependency injection for configuration.

#### Scenario: JSON export with injected settings
- **WHEN** analysis results need to be exported
- **THEN** the `export_results_to_json` function in `services/export_service.py` receives results and `ExportSettings`
- **AND** uses the injected settings for export behavior
- **AND** returns the export path to the UI for status display

#### Scenario: Export configuration
- **WHEN** auto-export is enabled in settings
- **THEN** the export service checks `export_settings.auto_export`
- **AND** creates timestamped JSON files in `export_settings.export_dir`

### Requirement: Parametrized Application Entry Point
The application SHALL support flexible configuration paths via parameters and environment variables.

#### Scenario: Default configuration
- **WHEN** the application starts without parameters
- **THEN** it loads configuration from default `settings.json` path
- **AND** initializes all components with loaded settings

#### Scenario: Custom configuration path
- **WHEN** the application is started with `main(config_path=Path('custom.json'))`
- **THEN** it loads configuration from the specified path
- **AND** initializes all components with custom settings

#### Scenario: Environment variable configuration
- **WHEN** `TRACKLIST_CONFIG` environment variable is set
- **THEN** the application uses that path for configuration
- **AND** overrides the default path

### Requirement: Backward Compatibility
The refactored codebase SHALL maintain backward compatibility with existing imports from `fluent_gui.py` through a compatibility wrapper.

#### Scenario: Legacy imports
- **WHEN** existing code imports classes from `fluent_gui`
- **THEN** the imports continue to work via the compatibility wrapper
- **AND** wrapper functions handle global config access for legacy callers

#### Scenario: Entry point compatibility
- **WHEN** the application is started via `python fluent_gui.py`
- **THEN** it launches correctly by delegating to `app.main()`
- **AND** the behavior is identical to running `python app.py`

#### Scenario: Characterization test validation
- **WHEN** characterization tests run against the refactored code
- **THEN** all tests pass with identical behavior to pre-refactoring baseline
- **AND** all previously exported symbols remain accessible

### Requirement: Explicit Package Exports
The `ui` package SHALL explicitly define its public API through `__init__.py` with clear exports and `__all__` definition.

#### Scenario: Public API definition
- **WHEN** a developer imports from `ui` package
- **THEN** they have access to all public classes and functions listed in `__all__`
- **AND** the imports are explicit and documented

#### Scenario: IDE autocomplete support
- **WHEN** a developer types `from ui import`
- **THEN** their IDE shows all available exports from `__all__`
- **AND** provides accurate type hints for imported symbols
