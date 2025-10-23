# Implementační Checklist - Refaktor Unified Audit Plan

## Krok 1: Vytvoření Základních Stavebních Bloků (Vysoká priorita)

- [ ] **1.1: Refaktorovat Parsování Názvů Souborů**
  - [ ] 1.1.1 Vytvořit třídu `StrictFilenameParser` (doménová služba) pro centralizaci logiky parsování `side` a `position`
  - [ ] 1.1.2 Nahradit logiku v `FakeAudioModeDetector` (method `_parse_filename`) a `wav_extractor_wave.py` (function `strict_from_path`) voláním této nové třídy
  - [ ] 1.1.3 Odstranit magická čísla (např. 999 v `fake_mode_detector.py` lines 58, 118) a nahradit je pojmenovanými konstantami

- [ ] **1.2: Zavést Doménové Objekty pro Párování Souborů**
  - [ ] 1.2.1 Vytvořit `@dataclass class FilePair: pdf: Path; zip: Path` v `core/domain/` nebo `core/models/`
  - [ ] 1.2.2 Upravit funkci `discover_and_pair_files` v `adapters/filesystem/file_discovery.py`, aby vracela `dict[int, FilePair]` místo `dict[str, dict[str, Path]]`
  - [ ] 1.2.3 Zajistit konzistentní použití `int` pro ID v celém procesu párování (aktuálně používá string klíče na line 75)

## Krok 2: Implementace Architektonických Vzorů (Vysoká priorita)

- [ ] **2.1: Implementovat Chain of Responsibility pro Detekci Režimu Audia**
  - [ ] 2.1.1 Vytvořit orchestrátor `ChainedAudioModeDetector`, který přijímá seznam detekčních kroků
  - [ ] 2.1.2 Definovat společný protokol/rozhraní pro každý krok řetězu (např. `DetectionStep` Protocol)
  - [ ] 2.1.3 Implementovat jednotlivé kroky:
    - `StrictParserStep`: Používá `StrictFilenameParser` z kroku 1.1
    - `AiParserStep`: Obaluje logiku z `wav_extractor_wave.py` functions `ai_parse_batch` a `merge_ai_results`
    - `DeterministicFallbackStep`: Obaluje logiku z `wav_extractor_wave.py` function `_fallback_assign_when_all_unknown`
  - [ ] 2.1.4 Integrovat `ChainedAudioModeDetector` do `AnalysisService` jako výchozí implementaci `AudioModeDetector` portu z `core/ports.py`

## Krok 3: Dekompozice Monolitických Modulů (Střední priorita)

- [ ] **3.1: Rozdělit `wav_extractor_wave.py`**
  - [ ] 3.1.1 Přesunout logiku parsování do `StrictFilenameParser` (viz 1.1)
  - [ ] 3.1.2 Přesunout logiku volání AI do `AiParserStep` (viz 2.1.3)
  - [ ] 3.1.3 Přesunout normalizační logiku (function `normalize_positions`) do orchestrátoru nebo samostatné utility
  - [ ] 3.1.4 Deprecate/odstranit `wav_extractor_wave.py` a nahradit všechny jeho použití novou architekturou

- [ ] **3.2: Rozdělit `pdf_extractor.py`**
  - [ ] 3.2.1 Vytvořit `PdfImageRenderer` (adapter pro PyMuPDF) - obaluje function `_render_pdf_to_images`
  - [ ] 3.2.2 Vytvořit `VlmClient` (adapter pro VLM API) - obaluje functions `_call_vlm_json` a `_to_data_url`
  - [ ] 3.2.3 Vytvořit `TracklistParser` (doménová služba pro parsování JSONu) - obaluje function `_consolidate_and_parse_tracks`
  - [ ] 3.2.4 Nahradit stávající funkce v `pdf_extractor.py` orchestrací těchto nových tříd v function `extract_pdf_tracklist`

## Krok 4: Finální Vyčištění a Zpevnění (Nízká priorita)

- [ ] **4.1: Zpřesnit Zpracování Výjimek**
  - [ ] 4.1.1 Projít `ZipWavFileReader` v `adapters/audio/wav_reader.py`
  - [ ] 4.1.2 Nahradit `except Exception:` (lines 71, 78) specifickými výjimkami (`zipfile.BadZipFile`, `IOError`, `OSError`)

- [ ] **4.2: Plánované Odstranění `fluent_gui.py`**
  - [ ] 4.2.1 Vytvořit ticket v projektovém managementu pro budoucí odstranění `fluent_gui.py` (pokud je stále relevantní)
  - [ ] 4.2.2 Ověřit, že deprecation notice v souboru je stále platná a srozumitelná