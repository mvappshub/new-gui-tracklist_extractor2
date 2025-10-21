## Why
Soubor `fluent_gui.py` (~1161 řádků) je monolitický a obsahuje veškerou logiku prezentační vrstvy: konstanty, pomocné funkce, exportní logiku, threading workers, datové modely tabulek, hlavní okno, dialog nastavení a spouštěcí kód aplikace. Tato struktura ztěžuje údržbu, testování a budoucí rozšíření (např. `redesign-gz-media-ui`). Jednotlivé komponenty nelze snadno testovat izolovaně a změny v jedné části často vyžadují úpravy v nesouvisejících částech kódu.

Další problémy:
- **Porušení Dependency Inversion Principle (DIP)**: Komponenty přímo importují globální `config.cfg`, což snižuje testovatelnost
- **Porušení Single Responsibility Principle (SRP)**: `MainWindow` přímo řídí životní cyklus vláken a workerů
- **Nízká testovatelnost**: Těsné vazby na globální stav znemožňují izolované unit testy
- **Rigidní konfigurace**: Pevně zakódované cesty a závislosti

## What Changes
- **Vytvoření modulární struktury `ui/` balíčku** s podbalíčky pro modely, workers, dialogy a utility
- **Rozdělení `fluent_gui.py`** na samostatné moduly s jasně oddělenými zodpovědnostmi
- **Zavedení Dependency Injection (DI)**:
  - Vytvoření konfiguračních abstrakcí (`ui/config_models.py`) pomocí Pydantic/dataclass
  - Injektování konfigurace do konstruktorů komponent místo přímých importů
  - `MainWindow` a `app.py` načítají konfiguraci a předávají relevantní části komponentám
- **Vytvoření AnalysisWorkerManager** (`ui/workers/worker_manager.py`):
  - Zapouzdření správy životního cyklu QThread a AnalysisWorker
  - Odstranění detailů správy vláken z `MainWindow`
  - Delegace operací workerů přes manažera
- **Parametrizace vstupního bodu** (`app.py`):
  - Flexibilní cesty ke konfiguračním souborům
  - Podpora environmentálních proměnných
- **Characterization Tests**:
  - Testy pro ověření zpětné kompatibility před refaktoringem
  - Validace všech exportovaných symbolů z `fluent_gui.py`
- **Explicitní exporty** v `ui/__init__.py` s `__all__`

## Impact
- **Affected specs:** `specs/ui/spec.md` (přidání požadavků na DI, modulární architekturu, worker management)
- **Affected code:**
  - `fluent_gui.py` - transformace na compatibility wrapper
  - Nové soubory v `ui/` balíčku včetně `config_models.py` a `worker_manager.py`
  - `services/export_service.py` - přesun exportní logiky
  - Testy - nové characterization testy + aktualizace existujících
  - `README.md` - dokumentace nové struktury a DI vzorů
- **Benefits:**
  - **Výrazně lepší testovatelnost**: Komponenty lze testovat izolovaně s mock závislostmi
  - **SOLID principy**: DIP, SRP, OCP dodrženy v celé UI vrstvě
  - **Snadnější údržba**: Jasné oddělení zodpovědností
  - **Flexibilita**: Parametrizovatelná konfigurace
  - **Příprava pro redesign**: Čistá architektura pro `redesign-gz-media-ui`
  - **Žádná změna funkčnosti**: Pouze reorganizace a architektonické vylepšení
