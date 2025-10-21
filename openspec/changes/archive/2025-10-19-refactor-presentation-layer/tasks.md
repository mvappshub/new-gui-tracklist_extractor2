## Fáze 0: Příprava a Characterization Tests
- [x] 0.1 Vytvořit `tests/test_fluent_gui_legacy.py` pro characterization testing
  - Importovat všechny třídy a funkce z `fluent_gui.py`
  - Ověřit dostupnost: `MainWindow`, `TopTableModel`, `BottomTableModel`, `AnalysisWorker`, `SettingsDialog`, všech konstant
  - Test minimální instance `MainWindow` (bez exec)
  - Test spuštění `python fluent_gui.py` (subprocess)
- [x] 0.2 Spustit characterization testy a zdokumentovat baseline chování
- [x] 0.3 Vytvořit seznam všech symbolů exportovaných z `fluent_gui.py` pro wrapper

## Fáze 1: Příprava struktury, konstanty a konfigurační abstrakce
- [x] 1.1 Vytvořit `ui/` balíček s `__init__.py`
- [x] 1.2 Vytvořit `ui/constants.py` se všemi UI konstantami z `fluent_gui.py` (řádky 36-142)
  - Konstanty aplikace: `SETTINGS_FILENAME`, `WINDOW_TITLE`
  - Stavové zprávy: `STATUS_READY`, `STATUS_ANALYZING`, `MSG_*`
  - Texty tlačítek a popisků: `BUTTON_RUN_ANALYSIS`, `LABEL_FILTER`
  - Filtry: `FILTER_ALL`, `FILTER_OK`, `FILTER_FAIL`, `FILTER_WARN`
  - Hlavičky tabulek: `TABLE_HEADERS_TOP`, `TABLE_HEADERS_BOTTOM`
  - Symboly: `SYMBOL_CHECK`, `SYMBOL_CROSS`, `PLACEHOLDER_DASH`
  - Statusy: `STATUS_OK`, `STATUS_WARN`, `STATUS_FAIL`
- [x] 1.3 Vytvořit `ui/theme.py` s pomocnými funkcemi pro témata (řádky 57-122)
  - `get_system_file_icon()` - ikona souboru z QStyle
  - `get_gz_color(color_key)` - GZ Media barvy z konfigurace (přijímá config jako parametr)
  - `load_gz_media_fonts(app, font_config)` - načtení Poppins fontu s injektovanou konfigurací
  - `load_gz_media_stylesheet(app, stylesheet_path)` - načtení QSS s parametrizovanou cestou
- [x] 1.4 Vytvořit `ui/config_models.py` s konfiguračními abstrakcemi
  - `ToleranceSettings` (dataclass/Pydantic): `warn_tolerance: int`, `fail_tolerance: int`
  - `ExportSettings` (dataclass/Pydantic): `auto_export: bool`, `export_dir: Path`
  - `PathSettings` (dataclass/Pydantic): `pdf_dir: Path`, `wav_dir: Path`
  - `ThemeSettings` (dataclass/Pydantic): `font_family: str`, `font_size: int`, `stylesheet_path: Path`, `status_colors: dict`
  - `WorkerSettings` (dataclass/Pydantic): `pdf_dir: Path`, `wav_dir: Path`
  - Funkce `load_tolerance_settings(cfg) -> ToleranceSettings` pro konverzi z globální konfigurace
  - Funkce `load_export_settings(cfg) -> ExportSettings`
  - Funkce `load_path_settings(cfg) -> PathSettings`
  - Funkce `load_theme_settings(cfg) -> ThemeSettings`
  - Funkce `load_worker_settings(cfg) -> WorkerSettings`

## Fáze 2: Datové modely s Dependency Injection
- [x] 2.1 Vytvořit `ui/models/` balíček s `__init__.py`
- [x] 2.2 Přesunout `TopTableModel` do `ui/models/results_table_model.py` (řádky 259-404)
  - Přejmenovat na `ResultsTableModel`
  - **DI**: Konstruktor přijímá `theme_settings: ThemeSettings` místo přímého importu `config`
  - Použít `theme_settings.status_colors` pro mapování barev
  - Importovat závislosti z `ui.constants`
  - Zachovat všechny metody: `add_result`, `get_result`, `clear`, `all_results`, `set_filter`
- [x] 2.3 Přesunout `BottomTableModel` do `ui/models/tracks_table_model.py` (řádky 406-576)
  - Přejmenovat na `TracksTableModel`
  - **DI**: Konstruktor přijímá `tolerance_settings: ToleranceSettings` místo přímého importu `config.cfg`
  - Použít `tolerance_settings.warn_tolerance` pro výpočet match symbolů
  - Importovat závislosti z `ui.constants`
  - Zachovat metody: `update_data`, `get_track_row_data`, `get_total_row_data`

## Fáze 3: Workers a Worker Manager
- [x] 3.1 Vytvořit `ui/workers/` balíček s `__init__.py`
- [x] 3.2 Přesunout `AnalysisWorker` do `ui/workers/analysis_worker.py` (řádky 233-258)
  - **DI**: Konstruktor přijímá `worker_settings: WorkerSettings` místo přímých Path parametrů
  - Zachovat signály: `progress`, `result_ready`, `finished`
  - Importovat `AnalysisService` ze `services/`
- [x] 3.3 Vytvořit `ui/workers/worker_manager.py` s třídou `AnalysisWorkerManager`
  - **Zodpovědnost**: Správa životního cyklu QThread a AnalysisWorker
  - Konstruktor přijímá `worker_settings: WorkerSettings`
  - Metody:
    - `start_analysis()` - vytvoří worker a thread, propojí signály, spustí
    - `is_running() -> bool` - vrací stav běhu
    - `stop_analysis()` - bezpečně ukončí worker a thread
    - `cleanup()` - vyčistí resources
  - Signály (přeposílané z workera): `progress`, `result_ready`, `finished`
  - Interní správa QThread a AnalysisWorker instancí
  - Automatické cleanup při dokončení

## Fáze 4: Dialogy s Dependency Injection
- [x] 4.1 Vytvořit `ui/dialogs/` balíček s `__init__.py`
- [x] 4.2 Přesunout `SettingsDialog` do `ui/dialogs/settings_dialog.py` (řádky 1077-1113)
  - **DI**: Konstruktor přijímá `settings_filename: Path` místo přímého importu `SETTINGS_FILENAME`
  - Importovat `SettingsPage` z `settings_page`
  - Importovat `save_config` z `config`
  - Zachovat metodu `_on_save()` s parametrizovanou cestou

## Fáze 5: Hlavní okno s Dependency Injection
- [x] 5.1 Vytvořit `ui/main_window.py` s třídou `MainWindow` (řádky 578-1075)
  - **DI**: Konstruktor přijímá:
    - `tolerance_settings: ToleranceSettings`
    - `export_settings: ExportSettings`
    - `theme_settings: ThemeSettings`
    - `worker_manager: AnalysisWorkerManager`
    - `settings_filename: Path`
  - Vytvořit modely s injektovanými nastaveními:
    - `ResultsTableModel(theme_settings)`
    - `TracksTableModel(tolerance_settings)`
  - Použít `worker_manager` pro správu analýzy místo přímé správy QThread
  - Zachovat všechny metody:
    - `__init__()` - inicializace s DI, toolbar, tabulky, signály
    - `setup_menu_bar()`, `setup_tables()`, `connect_signals()`
    - `run_analysis()` - delegace na `worker_manager.start_analysis()`
    - `on_analysis_finished()` - volání `export_service.export_results_to_json(results, export_settings)`
    - `on_filter_changed()`, `on_top_row_selected()`, `on_top_cell_clicked()`, `on_bottom_cell_clicked()`
    - `open_settings()` - vytvoření `SettingsDialog(settings_filename, self)`
    - `_set_status()`, `_set_analysis_state()`
    - `_update_gz_logo()`, `_update_gz_claim_visibility()`
    - Event handlery: `showEvent()`, `eventFilter()`, `closeEvent()` - volání `worker_manager.cleanup()`
  - Zahrnout vnořené funkce pro auto-resize hlaviček

## Fáze 6: Servisní vrstva s Dependency Injection
- [x] 6.1 Vytvořit `services/export_service.py`
  - Přesunout `_export_results_to_json` (řádky 156-228)
  - Přejmenovat na `export_results_to_json` (veřejná funkce)
  - **DI**: Signatura `export_results_to_json(results: List[SideResult], export_settings: ExportSettings) -> Optional[Path]`
  - Použít `export_settings.auto_export` a `export_settings.export_dir` místo přímého čtení z `config.cfg`
  - Importovat závislosti z `core.models.analysis`

## Fáze 7: Vstupní bod s parametrizací
- [x] 7.1 Vytvořit `app.py` jako nový vstupní bod (řádky 1115-1160)
  - Pre-QApplication DPI setup s parametrizovatelnou cestou
  - Funkce `main(config_path: Optional[Path] = None)`:
    - Parametr `config_path` s defaultem `Path('settings.json')` nebo z env proměnné `TRACKLIST_CONFIG`
    - Načtení konfigurace z `config_path`
    - Vytvoření konfiguračních objektů pomocí `ui.config_models.load_*_settings(cfg)`
    - Vytvoření `AnalysisWorkerManager` s `WorkerSettings`
    - Načtení fontů a stylů s injektovanými `ThemeSettings`
    - Vytvoření `MainWindow` s všemi injektovanými závislostmi
    - Zobrazení okna a spuštění event loop
  - `if __name__ == '__main__': main()`

## Fáze 8: Kompatibilita a explicitní exporty
- [x] 8.1 Aktualizovat `ui/__init__.py` pro explicitní exporty
  - Importovat a exportovat:
    - Z `ui.constants`: všechny konstanty (nebo `*`)
    - Z `ui.theme`: všechny funkce
    - Z `ui.models`: `ResultsTableModel`, `TracksTableModel`
    - Z `ui.workers`: `AnalysisWorker`, `AnalysisWorkerManager`
    - Z `ui.dialogs`: `SettingsDialog`
    - Z `ui.main_window`: `MainWindow`
    - Z `ui.config_models`: všechny settings třídy a load funkce
  - Definovat `__all__` seznam pro explicitní veřejné API
- [x] 8.2 Transformovat `fluent_gui.py` na compatibility wrapper
  - Zachovat hlavičku souboru
  - Importovat všechny třídy a funkce z nové struktury
  - Aliasy pro zpětnou kompatibilitu:
    - `TopTableModel = ResultsTableModel`
    - `BottomTableModel = TracksTableModel`
  - Pro funkce vyžadující config vytvořit wrapper funkce, které načtou globální config:
    ```python
    from config import cfg
    from ui.theme import get_gz_color as _get_gz_color
    def get_gz_color(color_key):
        from ui.config_models import load_theme_settings
        theme_settings = load_theme_settings(cfg)
        return _get_gz_color(color_key, theme_settings)
    ```
  - Zachovat `if __name__ == '__main__': main()`
  - Přidat deprecation komentář s doporučením použít `app.py` a `ui/` package

## Fáze 9: Testy a dokumentace
- [x] 9.1 Spustit characterization testy z Fáze 0 pro ověření wrapperu
- [x] 9.2 Vytvořit unit testy pro nové komponenty s DI:
  - `tests/test_results_table_model.py` - test s mock `ThemeSettings`
  - `tests/test_tracks_table_model.py` - test s mock `ToleranceSettings`
  - `tests/test_analysis_worker.py` - test s mock `WorkerSettings` a `AnalysisService`
  - `tests/test_worker_manager.py` - test správy životního cyklu
  - `tests/test_export_service.py` - test s mock `ExportSettings`
- [x] 9.3 Aktualizovat existující testy:
  - `tests/test_gui_minimal.py` - import z `ui.main_window`, vytvoření s mock závislostmi
  - `tests/test_gui_simple.py` - importy z `ui.models`, `ui.main_window`
  - `tests/test_gui_show.py` - import z `ui.main_window`
  - `tests/test_settings_dialog.py` - import z `ui.dialogs`, test s parametrizovanou cestou
- [x] 9.4 Spustit všechny testy pro ověření funkčnosti
- [x] 9.5 Aktualizovat `README.md` s dokumentací:
  - Nová modulární struktura `ui/` package
  - Dependency Injection vzory
  - Použití `AnalysisWorkerManager`
  - Parametrizace `app.py`
  - Příklady testování s mock závislostmi

## Fáze 10: Validace a dokončení
- [x] 10.1 Spustit `openspec validate refactor-presentation-layer --strict`
- [x] 10.2 Ověřit, že aplikace funguje identicky jako před refaktoringem
- [x] 10.3 Zkontrolovat, že všechny importy fungují správně (včetně legacy z `fluent_gui.py`)
- [x] 10.4 Ověřit, že `python fluent_gui.py` i `python app.py` fungují
- [x] 10.5 Připravit archivaci `refine-main-ui-layout` změny
- [x] 10.6 Zdokumentovat migrační cestu pro vývojáře (z legacy importů na nové)
