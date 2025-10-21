# Project Context

## Purpose
- Desktop tool to extract vinyl release tracklists from PDF cue sheets using a Vision LLM, compare them with mastered WAV durations, and surface mismatches in a "Final Cue Sheet Checker" GUI.
- Produces per-side summaries and optional JSON exports to aid mastering/QA before release.

## Tech Stack
- Language: Python 3.11 (CPython)
- GUI: PyQt6 (pure Qt6 widgets)
- Imaging/PDF: PyMuPDF (`fitz`), Pillow (`PIL`)
- LLM client: OpenRouter (preferred) and OpenAI via `openai` package
- Configuration: QSettings (platform-native persistence via settings.json) with optional .env
- Tooling: `black` (format), `ruff` (lint), `mypy` (types), `pytest` (tests)

## Project Conventions

### Code Style
- Follow PEP 8; prefer explicit, descriptive names.
- Format with `black` (default settings). Lint with `ruff` before commit.
- Type hints required in new/modified code; run `mypy` locally.
- Avoid I/O in pure logic functions; keep extractors deterministic and testable.
- Logging over prints for operational messages; user-facing feedback via GUI components.

### Architecture Patterns
- Single-process desktop app with clear separation of concerns:
  - `fluent_gui.py`: Main window and presentation logic (tables, theme, actions).
  Note: The UI relies on standard PyQt6 widgets. Custom components like `FolderSettingCard` in `settings_page.py` are built on this foundation without additional GUI frameworks.
  - `settings_page.py`: Settings UI backed by `QSettings` groups/keys defined in `config.py`.
  - `config.py`: Centralized configuration schema and defaults (LLM, image render, UI, analysis tolerances, paths).
  - `pdf_extractor.py`: PDF rendering (PyMuPDF) and Vision LLM JSON extraction; consolidates tracks by side.
  - `wav_extractor_wave.py`: Reads WAV durations from ZIPs; infers `side`/`position` strictly from filenames, then AI fallback, then deterministic fallback; normalizes positions and emits JSON-ready payloads.
- Environment and secrets via `.env` (loaded early) and `settings.json` (persisted app config).
- Keep AI calls isolated and mockable; prefer pure transformation helpers around them.

### Testing Strategy
- Framework: `pytest` (see `requirements.txt`).
- Unit tests focus on pure logic:
  - PDF track consolidation and time parsing in `pdf_extractor.py` (mock LLM responses).
  - WAV filename parsing, strict inference, normalization in `wav_extractor_wave.py`.
- Do not hit external LLMs in tests; mock `OpenAI` client or guard with env flags.
- Optional smoke tests for GUI construction (no rendering assertions) to catch import regressions.

### Git Workflow
- Feature branches off `main`; small, focused PRs.
- Require passing lint/format/type checks (`ruff`, `black`, `mypy`) before merge.
- Commit messages: concise, imperative (optionally Conventional Commits for clarity).

## Domain Context
- Track identification is anchored by a parsable duration (e.g., `MM:SS`). Titles are the meaningful text visually associated with that duration; multi-line titles should be combined.
- Side context comes from headers like `Side A`, `SIDE B` or filename patterns such as `A1`, `AA02`. Positions reset per side.
- Non-tracks (notes, totals, ISRCs, credits) must be ignored.
- WAV masters are provided in ZIPs; durations are computed from audio data and used to validate the PDF cue sheet.
- Analysis tolerances are configurable: soft warning (`analysis.tolerance_warn`) and hard failure (`analysis.tolerance_fail`).

## Important Constraints
- Privacy: PDF page images and filenames may be sent to external LLMs. Obtain consent and avoid sending sensitive content.
- Determinism: Parsing/normalization logic should remain deterministic; AI is a best-effort helper with strict JSON outputs and must be optional.
- Platform: Primary development environment is Windows (Fluent look-and-feel); keep code portable where feasible.
- Performance: Prefer single-pass parsing and avoid heavy image operations; render PDF pages at configured DPI only once per page.

## External Dependencies
- OpenRouter API (preferred) and/or OpenAI API via `openai` client.
  - Environment: `OPENROUTER_API_KEY` (preferred), `OPENAI_API_KEY` (optional); optional `OPENROUTER_MODEL`, `OPENAI_MODEL`.
  - Base URL defaults to `https://openrouter.ai/api/v1`.
- PyMuPDF (`fitz`) for PDF rendering; Pillow for image conversion.
- PyQt6 for UI and configuration storage.
- Configuration files and paths:
  - App config file: `settings.json` (persisted by `QSettings`).
  - Input folders: `input.pdf_dir`, `input.wav_dir` (set in `settings.json`).
  - Exports folder: `export.default_dir` for generated reports.
