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
  - After each analysis run, results auto-export to JSON in `export.default_dir` when `export.auto` is true (filename `analysis_YYYYMMDD_HHMMSS.json`).
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
- **`services/`**: Contains application services, such as `AnalysisService` (orchestrates analysis) and `export_service.py` (handles JSON exports). These services are pure Python and Qt-agnostic.
- **`core/`**: Contains the core domain logic and models of the application (`comparison.py`, `extraction.py`, `models/analysis.py`). This layer is completely independent of any UI or framework.
- **`fluent_gui.py`**: Now serves as a backward-compatibility wrapper to ensure old entry points and imports continue to work. New development should use `app.py` and the `ui/` package directly.
