# Spec Delta: UI

## MODIFIED Requirements

### Requirement: Dependency Injection Architecture
The UI layer SHALL use dependency injection for all configuration and service dependencies, with NO fallback to global configuration objects.

#### Scenario: Configuration injection
- WHEN a UI component needs configuration values
- THEN it receives a specific configuration object (e.g., `ToleranceSettings`, `ExportSettings`, `ThemeSettings`) via constructor parameter
- AND the component does not directly import or access global `config.cfg`
- AND NO fallback imports exist in component code

#### Scenario: Settings page configuration
- WHEN SettingsPage is instantiated
- THEN it receives an `AppConfig` instance via constructor parameter
- AND uses the injected instance for all configuration access
- AND does not import global `cfg` object

#### Scenario: Table model configuration
- WHEN TracksTableModel is instantiated
- THEN it receives `ThemeSettings` via constructor parameter
- AND does not have fallback logic to import global `cfg`
- AND caller is responsible for providing theme settings

#### Scenario: Testability with mocks
- WHEN a developer writes unit tests for a UI component
- THEN they can inject mock configuration and service objects
- AND the component can be tested in isolation without global state
- AND tests use pytest fixtures for configuration instances

## References
- openspec/specs/ui/spec.md
