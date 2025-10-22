Vinyl Project Tracklist Extractor

A desktop tool to extract tracklists from PDF cue sheets using a Vision LLM, compare them with mastered WAV durations, and review results in a Fluent-style PyQt GUI.

Quick Start
- Prereqs: Python 3.11 (recommended), Git
- Clone and setup
  - Windows (PowerShell):
    - `py -3.11 -m venv .venv311; .\.venv311\Scripts\Activate.ps1`
  - macOS/Linux:
    - Ensure your default `python` is 3.11, then:
    - `python -m venv .venv && source .venv/bin/activate`
  - Install deps: `
  `

Environment (.env)
- Copy `.env.example` to `.env` and set your API key:
  - `OPENROUTER_API_KEY="YOUR_API_KEY"`
- Optional overrides:
  - `OPENROUTER_MODEL` (default configured in app settings)
  - `OPENAI_API_KEY` / `OPENAI_MODEL` (fallback if you use OpenAI directly)

Run
- GUI (Final Cue Sheet Checker):
  - Windows (PowerShell):
    - `$env:QT_QPA_PLATFORM = "windows"`
    - `.\.venv\Scripts\python.exe .\app.py`
    - Alternatively: `.\.venv\Scripts\python.exe .\app.py -platform windows`
  - macOS/Linux: `python app.py`
  - In the Settings page, set:
    - `PDF input directory`: folder with tracklist PDFs
    - `WAV input directory`: folder with ZIPs containing mastered WAVs
    - `Export directory`: where reports/exports are written
  - After each analysis run, results auto-export to JSON in `export.default_dir` when `export.auto` is true (filename `analysis_YYYYMMDD_HHMMSS.json`). Use the centralized `services.export_service.export_results_to_json()` helper for all exports.
- WAV batch utility (optional): `python wav_extractor_wave.py "C:\path\to\masters"`
- Headless/CI runs set `QT_QPA_PLATFORM=offscreen` automatically. To supply fonts in that mode, place `.ttf` files (e.g. DejaVuSans) into the repository `fonts/` directory and they will be loaded on startup.


Dev Commands
- Format: `black .`
- Lint: `ruff check .`
- Types: `mypy .`
- Tests: `pytest -q`

Pre-commit Hook (optional)
Enable repo-provided hook to run format/lint/types before committing:
```
git config core.hooksPath .githooks
```

Notes
- Use Python 3.11 for best compatibility with binary wheels (PyMuPDF, Qt, OpenAI deps). Newer runtimes may require building extra packages.
- The app can call external LLM APIs to parse PDF page images. Ensure you have rights to process the content before enabling extraction.
- `settings.json` and `.env` are ignored by Git; configure them locally.
## Architecture

This project follows a clean, layered architecture to separate concerns and improve testability.

- **`app.py`**: The main application entry point. Responsible for loading configuration, assembling dependencies, and launching the main window.
- **`ui/`**: A dedicated package for all presentation layer components, organized into sub-packages:
  - `ui/main_window.py`: The `MainWindow` class, which orchestrates the UI.
  - `ui/models/`: Contains `QAbstractTableModel` implementations (`ResultsTableModel`, `TracksTableModel`).
  - `ui/workers/`: Handles background processing with `AnalysisWorker` and `AnalysisWorkerManager`.
  - `ui/dialogs/`: Contains UI dialogs like `SettingsDialog`.
  - `ui/constants.py` & `ui/theme.py`: Centralized UI constants and styling helpers.
- **Dependency Injection (DI)**: The UI layer strictly uses constructor injection. Components receive their dependencies (like configuration models or services) upon creation, making them highly testable and decoupled from global state.
- **`services/`**: Contains application services, such as `AnalysisService` (orchestrates analysis) and `export_service.py` (handles JSON exports and is the single source of truth for exports). These services are pure Python and Qt-agnostic.
- **`core/`**: Contains the core domain logic and models of the application (`comparison.py`, `extraction.py`, `models/analysis.py`). This layer is completely independent of any UI or framework.
- **`fluent_gui.py`**: Now serves as a backward-compatibility wrapper to ensure old entry points and imports continue to work. New development should use `app.py` and the `ui/` package directly.
- **`adapters/`**: Contains infrastructure adapters that implement ports defined in `core/ports.py`. Adapters handle external dependencies like file I/O, AI services, and other infrastructure concerns.
- **`core/ports.py`**: Defines protocol interfaces (ports) that abstract external dependencies, enabling clean hexagonal architecture with dependency inversion.

## Refactoring Status

✅ **COMPLETED**: 5-phase strategic refactoring to hexagonal architecture

### Phase 1: Stabilization (✅ Complete)
- Type safety with strict mypy checking
- Comprehensive characterization tests
- Quality tooling (ruff, black, pytest)

### Phase 2: Dependency Injection (✅ Complete)
- Settings dataclasses instead of global config
- Constructor injection throughout the codebase
- No global `cfg` imports in domain or adapter layers

### Phase 3: I/O Modularization (✅ Complete)
- File system adapters for ZIP/WAV reading
- Infrastructure concerns isolated in adapter layer
- Domain layer completely free of I/O operations

### Phase 4: Export Service (✅ Complete)
- Centralized export in `services/export_service.py`
- Single `export_results_to_json()` function for all exports
- UI and automated tests use the same export mechanism

### Phase 5: AI Port (✅ Complete)
- `AudioModeDetector` protocol in `core/ports.py`
- `AiAudioModeDetector` wrapping wav_extractor_wave functions
- `FakeAudioModeDetector` for deterministic tests
- AI dependencies isolated in adapter layer only

## Quality Metrics

- **Test Coverage**: 97% (55 passing tests)
- **Type Safety**: mypy --strict passes
- **Code Quality**: ruff clean, zero dead code
- **Architecture**: Complete hexagonal architecture with zero infrastructure dependencies in domain layer

## Development Workflow

- **Local quality gates**: `tools/check.sh`
- **OpenSpec-driven development**: All changes validated through OpenSpec CLI
- **Git workflow**: Conventional commits with atomic checkpoints
- **Testing**: Fake adapters enable fast, deterministic test execution
