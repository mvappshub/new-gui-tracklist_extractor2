## Why

The UI currently displays incorrect symbols (black arrows ►) in the "Match" and "Waveform" columns of the tracks table. This is caused by:
1. Font fallback issue: Poppins font is referenced in QSS but not physically present (only DejaVu fonts available)
2. Unicode symbols ✓/✗ render as arrows in the fallback font
3. System icon `QStyle.StandardPixmap.SP_MediaPlay` renders as an arrow on Windows

This creates visual inconsistency and reduces usability, as the meaning of the symbols is not immediately clear. Users cannot distinguish between match/mismatch states or understand the waveform action.

## What Changes

- **Introduce custom icon infrastructure**: Create `ui/theme.py::get_custom_icon()` function to load and cache SVG icons from `assets/icons/`
- **Create SVG icons**: Add three custom icons aligned with GZ Media branding:
  - `check.svg` (16x16, green #10B981) for successful matches
  - `cross.svg` (16x16, red #EF4444) for failed matches
  - `play.svg` (16x16, blue #3B82F6) for waveform view action
- **Replace text symbols with icons**: Modify `TracksTableModel` to return icons via `DecorationRole` instead of text via `DisplayRole`
- **Update tests**: Modify tests to check for `QIcon` in `DecorationRole` instead of text in `DisplayRole`
- **Deprecate old constants**: Mark `SYMBOL_CHECK` and `SYMBOL_CROSS` as deprecated

## Impact

- **Affected specs**: `specs/ui/spec.md` (new requirement: Custom Iconography)
- **Affected code**:
  - `ui/theme.py` - New function `get_custom_icon()`
  - `ui/models/tracks_table_model.py` - Icon rendering in columns 6 and 7
  - `ui/constants.py` - Deprecation comments
  - `tests/test_tracks_table_model.py` - Test updates
- **New files**:
  - `assets/icons/check.svg`
  - `assets/icons/cross.svg`
  - `assets/icons/play.svg`
- **User Experience**: **Critical improvement**. Replaces ambiguous arrows with clear, universally understood icons. Improves clarity, aesthetics, and cross-platform consistency.
- **Breaking changes**: None (backward compatible via deprecated constants)