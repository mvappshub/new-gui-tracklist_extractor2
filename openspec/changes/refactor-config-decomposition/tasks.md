Execution Policy (MANDATORY)
This policy overrides any other instruction. Non-compliance = stop work.
1) Stop-the-line
Jakmile selže cokoliv z níže uvedeného, okamžitě zastav práce, vrať poslední změny do zelené a teprve pak pokračuj:
openspec validate <change> --strict
pytest -q (doporučeno --maxfail=1)
mypy --strict
Žádné další úkoly se neprovádí, dokud nejsou všechny tři kontroly zelené.
2) Zelená po blocích (gated workflow)
Každá sekce v tasks.md (1., 2., 3., …) končí minimální sadou kontrol:
openspec validate <change> --strict
pytest -q
mypy --strict

Pokud je cokoliv červené, sekce je nehotová.
3) Výjimky (omezené a dohledatelné)
Flaky test: dočasně označ @pytest.mark.flaky(reruns=2) + popis důvodu a TODO v tasks.md.
Změna chování: nejdřív uprav spec (ADDED/MODIFIED/REMOVED), pak testy, až poté kód.
Karanténa: @pytest.mark.xfail(strict=True, reason="…", run=False) s datem odstranění.
4) Commity (granulární a auditovatelné)
1 podúkol = 1 commit. Formát Conventional Commits + OpenSpec tag:
type(scope): stručný popis  [refs: #openspec-task:<ID>]

Příklady:
refactor(ui): SettingsPage přijímá AppConfig v ctor [refs: #openspec-task:1.1]
test(tests): přidána AppConfig fixture [refs: #openspec-task:4.1]
chore(openspec): validate refactor-config-decomposition --strict (pass) [refs: #openspec-task:5.1]
5) Pre-push/CI brány (fail = žádný push/merge)
Před každým pushem spusť lokálně:
openspec validate <change> --strict && pytest -q && mypy --strict

V CI nastav povinné kontroly:
OpenSpec validate (strict)
Pytest
Mypy strict
6) Definition of Done (celá změna)
rg "from config import cfg" --type py (pro config změnu: výskyt pouze v entry pointech)
openspec validate <change> --strict = green
pytest = green
mypy --strict = green
Smoke skripty prošly (pokud jsou součástí projektu)

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
