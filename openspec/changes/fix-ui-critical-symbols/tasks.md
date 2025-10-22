## P0: Critical Icon and Symbol Fixes

### 1. Asset Creation
- [ ] 1.1 Create `assets/icons/` directory
- [ ] 1.2 Create `assets/icons/check.svg` (16x16, green #10B981)
- [ ] 1.3 Create `assets/icons/cross.svg` (16x16, red #EF4444)
- [ ] 1.4 Create `assets/icons/play.svg` (16x16, blue #3B82F6)

### 2. Theme and Configuration Update
- [ ] 2.1 Modify `ui/theme.py`: Create function `get_custom_icon(icon_name: str) -> QIcon`
  - Load SVG icons from `assets/icons/`
  - Implement icon caching for performance
  - Add error handling with fallback to system icons
  - Support icons: 'check', 'cross', 'play'

### 3. Model Implementation
- [ ] 3.1 Modify `ui/models/tracks_table_model.py`:
  - Import `get_custom_icon` from `ui.theme`
  - Column 6 (Match): Return icon via `DecorationRole`, empty string via `DisplayRole`
  - Column 7 (Waveform): Replace `get_system_file_icon('play')` with `get_custom_icon('play')`
  - Preserve match calculation logic (tolerance check)

### 4. Test Updates
- [ ] 4.1 Modify `tests/test_tracks_table_model.py`:
  - Update `test_track_match_symbol_ok`: Check `DecorationRole` for valid `QIcon`
  - Update `test_track_match_symbol_fail`: Check `DecorationRole` for valid `QIcon`
  - Add `test_track_match_display_empty`: Verify `DisplayRole` returns empty string for column 6

### 5. Cleanup
- [ ] 5.1 Modify `ui/constants.py`: Add deprecation comment above `SYMBOL_CHECK` and `SYMBOL_CROSS`