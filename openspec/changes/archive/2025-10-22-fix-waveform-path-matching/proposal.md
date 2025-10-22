## Why
The application crashes with a `FileNotFoundError` when a user tries to open the waveform viewer for a WAV file located in a subdirectory within the ZIP archive. The current implementation incorrectly compares the full internal path of the WAV file with just its basename, causing the file lookup to fail. This is a critical regression that blocks a core user workflow.

## What Changes
- Modify the file matching logic in `waveform_viewer.py` to compare the full internal path from the ZIP archive member list against the full path stored in the `WavInfo` model.
- Add a new scenario to the `ui` specification to formalize the correct behavior and prevent future regressions.

## Impact
- **Affected specs:** `specs/ui/spec.md` (one new scenario added).
- **Affected code:** `waveform_viewer.py` (one line of code changed).
- **User Experience:** Critical bug fix. Restores the ability to view waveforms for all valid ZIP archive structures.