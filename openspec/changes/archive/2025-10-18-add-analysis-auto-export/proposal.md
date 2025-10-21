## Why
Users need consistent, machine-readable records of each analysis run for downstream QA and archiving. Today exports are manual/implicit; adding automatic JSON export improves reliability and traceability.

## What Changes
- Add automatic JSON export of analysis results after each run.
- Respect `export.auto` flag; write into `export.default_dir`.
- Create timestamped filenames: `analysis_YYYYMMDD_HHMMSS.json`.
- Serialize `SideResult` items with JSON-safe fields (string paths, seconds totals, track diffs).
- Minimal UX: status label confirms export file name on completion.

## Impact
- Affected specs: `export` capability (new requirement: auto-export on completion).
- Affected code: `fluent_gui.py` (export helper + integration), `README.md` (usage docs).
