## ADDED Requirements

### Requirement: Ruff Cleanup
Lint konfigurace MUST remain without exceptions; tato změna neovlivňuje žádné funkční požadavky projektu, pouze vylepšuje kvalitu kódu.

#### Scenario: Quality Gate Restored
- **WHEN** vývojáři spustí `ruff check .`
- **THEN** lint prochází bez chyb i bez výjimek v konfiguraci.
