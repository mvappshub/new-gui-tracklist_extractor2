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

# Tasks: Unify Audio Detection

## 1. Audit Usage
- [ ] 1.1 Spustit `rg "wav_extractor_wave" --type py` pro nalezení všech importů
- [ ] 1.2 Spustit `rg "from wav_extractor_wave import" --type py` pro specifické importy
- [ ] 1.3 Zkontrolovat `scripts/` adresář pro použití deprecated modulu
- [ ] 1.4 Zkontrolovat `tests/` adresář pro použití deprecated modulu
- [ ] 1.5 Vytvořit seznam všech souborů, které potřebují aktualizaci

## 2. Update Imports
- [ ] 2.1 Nahradit importy `WavInfo` z `wav_extractor_wave` za `from core.models.analysis import WavInfo`
- [ ] 2.2 Nahradit volání `detect_audio_mode_with_ai()` za použití `ChainedAudioModeDetector`
- [ ] 2.3 Nahradit volání `normalize_positions()` za použití `ChainedAudioModeDetector` (který již normalizuje)
- [ ] 2.4 Aktualizovat všechny dotčené soubory

## 3. Update Tests
- [ ] 3.1 Zkontrolovat `tests/test_characterization.py` pro použití deprecated modulu
- [ ] 3.2 Aktualizovat testy pro použití `ChainedAudioModeDetector` nebo `FakeAudioModeDetector`
- [ ] 3.3 Ověřit, že testy stále procházejí: `pytest tests/`

## 4. Remove Deprecated Module
- [ ] 4.1 Smazat soubor `wav_extractor_wave.py`
- [ ] 4.2 Ověřit, že žádné importy nezůstaly: `rg "wav_extractor_wave" --type py`
- [ ] 4.3 Spustit všechny testy: `pytest`
- [ ] 4.4 Spustit type checking: `mypy .`

## 5. Final Verification
- [ ] 5.1 Spustit smoke test: `python scripts/smoke_test.py`
- [ ] 5.2 Spustit smoke test bez AI: `python scripts/run_analysis_no_ai.py`
- [ ] 5.3 Manuální testování: spustit aplikaci a provést analýzu
- [ ] 5.4 Ověřit, že audio mode detection funguje správně

## References
- wav_extractor_wave.py
- scripts/smoke_test.py
