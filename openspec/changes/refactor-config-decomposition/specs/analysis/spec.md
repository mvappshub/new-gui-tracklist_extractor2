# Spec Delta: Analysis

## MODIFIED Requirements

### Requirement: Configuration Dependency Injection
The system SHALL inject configuration settings as explicit parameters to domain and adapter functions with NO global state access outside entry points.

#### Scenario: Domain layer purity
- WHEN domain functions in `core/domain/` are invoked
- THEN all configuration is received via function parameters
- AND no global `cfg` imports exist in domain layer
- AND domain remains pure and testable

#### Scenario: Adapter layer purity
- WHEN adapter functions in `adapters/` are invoked
- THEN all configuration is received via function parameters
- AND no global `cfg` imports exist in adapter layer
- AND adapters remain testable with mock configuration

#### Scenario: Entry point responsibility
- WHEN application entry points (`app.py`, `fluent_gui.py`) start
- THEN they are the ONLY modules that import global `cfg`
- AND they load configuration and construct settings dataclasses
- AND they inject settings into lower layers via constructor parameters

#### Scenario: Test isolation
- WHEN tests need configuration
- THEN they use pytest fixtures to create configuration instances
- AND do not rely on global `cfg` object
- AND can test with different configurations independently

## References
- openspec/specs/analysis/spec.md
