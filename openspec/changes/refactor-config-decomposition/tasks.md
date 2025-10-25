# Tasks: Config Decomposition Completion

## 1. Refactor settings_page.py
- [ ] 1.1 Upravit `SettingsPage.__init__` pro příjem `AppConfig` instance jako parametr
- [ ] 1.2 Odstranit `from config import cfg` import
- [ ] 1.3 Použít předanou instanci místo globálního `cfg`
- [ ] 1.4 Aktualizovat volání v `fluent_gui.py` nebo `ui/main_window.py` pro předání instance

## 2. Refactor fluent_gui.py
- [ ] 2.1 Zkontrolovat, zda je `fluent_gui.py` stále používán jako entry point
- [ ] 2.2 Pokud ano, upravit pro použití DI pattern jako v `app.py`
- [ ] 2.3 Pokud ne, přidat deprecation warning a delegovat na `app.main()`

## 3. Fix tracks_table_model.py fallback
- [ ] 3.1 Odstranit fallback import `from config import cfg` z `TracksTableModel.__init__`
- [ ] 3.2 Zajistit, že `theme_settings` je vždy předán přes konstruktor
- [ ] 3.3 Aktualizovat všechna volání `TracksTableModel()` pro explicitní předání `theme_settings`

## 4. Update tests
- [ ] 4.1 Vytvořit pytest fixture pro `AppConfig` instanci v `tests/conftest.py`
- [ ] 4.2 Aktualizovat testy v `tests/test_config.py` pro použití fixture
- [ ] 4.3 Aktualizovat GUI testy pro předání config přes DI
- [ ] 4.4 Aktualizovat `scripts/smoke_test.py` pro použití DI pattern

## 5. Validation
- [ ] 5.1 Spustit `rg "from config import cfg" --type py` a ověřit, že zůstávají pouze entry pointy
- [ ] 5.2 Spustit všechny testy: `pytest`
- [ ] 5.3 Spustit type checking: `mypy .`
- [ ] 5.4 Spustit smoke test: `python scripts/smoke_test.py`

## References
- settings_page.py
- fluent_gui.py
- ui/models/tracks_table_model.py
- tests/conftest.py
