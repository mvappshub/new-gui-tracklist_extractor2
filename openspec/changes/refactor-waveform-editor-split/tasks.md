# Tasks: Waveform Editor Split

## 1. Preparation
- [ ] 1.1 Vytvořit package `ui/waveform/` s `__init__.py`
- [ ] 1.2 Přidat characterization testy pro WaveformEditorDialog před refaktoringem
- [ ] 1.3 Dokumentovat současné chování a edge cases

## 2. Create AudioLoader component
- [ ] 2.1 Vytvořit `ui/waveform/audio_loader.py`
- [ ] 2.2 Implementovat `AudioLoader` třídu s metodami `extract_wav()` a `load_audio_data()`
- [ ] 2.3 Přesunout logiku z `_extract_wav()` a části `_load_audio_data()` z WaveformEditorDialog
- [ ] 2.4 Přidat unit testy pro AudioLoader

## 3. Create utility functions
- [ ] 3.1 Vytvořit `ui/waveform/utils.py`
- [ ] 3.2 Přesunout `_create_envelope()` jako standalone funkci
- [ ] 3.3 Přesunout time formatting funkce (`_format_mmss`, `_format_mmss_with_fraction`)
- [ ] 3.4 Přesunout `TimeAxisItem` třídu
- [ ] 3.5 Přidat unit testy pro utility funkce

## 4. Create WaveformPlotController component
- [ ] 4.1 Vytvořit `ui/waveform/plot_controller.py`
- [ ] 4.2 Implementovat `WaveformPlotController` s metodami pro rendering, region selection, PDF markers
- [ ] 4.3 Přesunout logiku z `_render_waveform()`, `_setup_region_selection()`, `set_pdf_track_markers()`, zoom metod
- [ ] 4.4 Implementovat signály pro komunikaci s Mediatorem (např. `region_changed`, `marker_clicked`)
- [ ] 4.5 Přidat unit testy pro WaveformPlotController

## 5. Create PlaybackController component
- [ ] 5.1 Vytvořit `ui/waveform/playback_controller.py`
- [ ] 5.2 Implementovat `PlaybackController` s QMediaPlayer management
- [ ] 5.3 Přesunout logiku z `_handle_play()`, `_handle_pause()`, `_handle_stop()`, slider handlers
- [ ] 5.4 Implementovat signály pro komunikaci s Mediatorem (např. `position_changed`, `playback_error`)
- [ ] 5.5 Přidat unit testy pro PlaybackController

## 6. Refactor WaveformEditorDialog to Mediator
- [ ] 6.1 Aktualizovat `WaveformEditorDialog.__init__` pro vytvoření instancí komponent
- [ ] 6.2 Připojit signály mezi komponentami přes Mediator
- [ ] 6.3 Delegovat volání metod na příslušné komponenty
- [ ] 6.4 Odstranit duplicitní kód, který byl přesunut do komponent
- [ ] 6.5 Zachovat veřejné API (konstruktor, `set_pdf_track_markers()`, `closeEvent()`)

## 7. Integration and Testing
- [ ] 7.1 Spustit všechny existující testy: `pytest tests/test_waveform_editor.py`
- [ ] 7.2 Spustit integration testy: `pytest tests/test_waveform_integration.py`
- [ ] 7.3 Manuální testování: otevřít waveform editor a ověřit všechny funkce
- [ ] 7.4 Ověřit, že characterization testy stále procházejí

## 8. Cleanup
- [ ] 8.1 Odstranit zakomentovaný kód z WaveformEditorDialog
- [ ] 8.2 Aktualizovat docstringy a type hints
- [ ] 8.3 Spustit `mypy ui/waveform/` a opravit type errors
- [ ] 8.4 Spustit `ruff check ui/waveform/` a opravit lint warnings

## References
- waveform_viewer.py
- tests/test_waveform_editor.py
