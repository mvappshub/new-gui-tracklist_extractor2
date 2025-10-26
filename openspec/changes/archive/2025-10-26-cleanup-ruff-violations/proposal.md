# Proposal: cleanup-ruff-violations

### 1. Reasoning
Během finalizace změny `fix-waveform-port-integration` bylo zjištěno 91 existujících `ruff` chyb v codebase. Aby se odblokovala aktuální změna, byly tyto chyby dočasně potlačeny pomocí konfigurace v `.ruff.toml`.

Cílem této změny je systematicky opravit všechny tyto nahlášené problémy a následně odstranit dočasné výjimky z konfigurace linteru, čímž se obnoví plná platnost "Quality Gate".

### 2. Approach
1.  Analyzovat chyby nahlášené `ruff check .` (před aplikováním `exclude`).
2.  Postupně opravit všechny problémy v dotčených souborech.
3.  Odstranit `[lint.exclude]` sekci z `.ruff.toml`.
4.  Ověřit, že `ruff check .` projde bez chyb a bez výjimek.
