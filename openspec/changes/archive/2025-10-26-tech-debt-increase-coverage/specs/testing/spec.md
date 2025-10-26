## ADDED Requirements

### Requirement: Coverage Threshold Restored
Coverage report MUST dosahovat cílového prahu; tato změna neovlivňuje žádné funkční požadavky projektu, pouze vylepšuje kvalitu testů.

#### Scenario: Coverage Gate Passes
- **WHEN** spustíme `coverage report --fail-under=<threshold>`
- **THEN** kontrola prochází bez selhání.
