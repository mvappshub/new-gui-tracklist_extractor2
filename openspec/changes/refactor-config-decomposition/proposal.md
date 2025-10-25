# Proposal: Config Decomposition Completion

## Why
Globální konfigurační objekt `cfg` je stále používán v několika částech aplikace (`settings_page.py`, `fluent_gui.py`, `ui/models/tracks_table_model.py`), což porušuje již započatý refaktoring směrem k dependency injection. Dokončení tohoto refaktoringu sníží provázanost a zlepší testovatelnost.

## What Changes
- Odstranit přímé importy `from config import cfg` ze všech UI komponent
- Upravit `settings_page.py` pro příjem `AppConfig` instance přes konstruktor
- Upravit `fluent_gui.py` pro použití DI místo globálního `cfg`
- Opravit fallback v `ui/models/tracks_table_model.py` pro příjem `ThemeSettings` vždy přes DI
- Aktualizovat testy pro použití fixture místo globálního `cfg`

## Impact
- Affected specs: `ui/spec.md` (Dependency Injection Architecture), `analysis/spec.md` (Configuration Dependency Injection)
- Affected code: `settings_page.py`, `fluent_gui.py`, `ui/models/tracks_table_model.py`, test soubory
- Breaking changes: Žádné - změny jsou interní, veřejné API zůstává stejné

## References
- config.py
- ui/config_models.py
- settings_page.py
- fluent_gui.py
- ui/models/tracks_table_model.py
