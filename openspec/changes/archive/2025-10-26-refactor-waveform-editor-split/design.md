# Design: Waveform Editor Split

## Context
WaveformEditorDialog je masivní třída s více než 740 řádky, která porušuje SRP. Refaktoring vyžaduje pečlivé rozdělení odpovědností při zachování funkčnosti.

## Goals / Non-Goals
**Goals:**
- Rozdělit WaveformEditorDialog na menší, testovatelné komponenty
- Zachovat všechny existující funkce (playback, region selection, PDF markers)
- Zlepšit testovatelnost jednotlivých komponent
- Zachovat zpětnou kompatibilitu veřejného API

**Non-Goals:**
- Přidávat nové funkce do waveform editoru
- Měnit UI layout nebo uživatelské rozhraní
- Refaktorovat WaveformViewerDialog (jiná třída, menší rozsah)

## Decisions

### Decision 1: Mediator Pattern
**What:** WaveformEditorDialog se stane Mediatorem, který koordinuje komunikaci mezi AudioLoader, WaveformPlotController a PlaybackController.

**Why:** Mediator pattern snižuje přímou provázanost mezi komponentami a centralizuje koordinační logiku.

**Alternatives considered:**
- Observer pattern: Příliš složité pro tento use case
- Direct coupling: Porušuje SRP a ztěžuje testování

### Decision 2: Component Responsibilities
**AudioLoader:**
- Extrakce WAV z ZIP (`_extract_wav`)
- Načítání audio dat pomocí soundfile
- Správa temporary files

**WaveformPlotController:**
- Správa pyqtgraph PlotWidget
- Vykreslování waveform envelope (`_render_waveform`, `_create_envelope`)
- Správa region selection (`_setup_region_selection`, `_snap_to_features`)
- Správa PDF markers (`set_pdf_track_markers`, `clear_pdf_markers`)
- Zoom a view navigation (`_zoom_in`, `_zoom_out`, `_fit_all`)

**PlaybackController:**
- Správa QMediaPlayer a QAudioOutput
- Transport controls (play, pause, stop)
- Position slider synchronizace
- Playhead line aktualizace

**WaveformEditorDialog (Mediator):**
- UI layout a dialog management
- Koordinace mezi komponentami
- Event routing (např. region změna → playback update)

### Decision 3: Package Structure
Vytvořit nový package `ui/waveform/` s:
- `audio_loader.py` - AudioLoader třída
- `plot_controller.py` - WaveformPlotController třída
- `playback_controller.py` - PlaybackController třída
- `utils.py` - Pomocné funkce (time formatting, envelope creation)

**Why:** Jasná separace concerns, snadnější navigace a testování.

## Risks / Trade-offs

**Risk:** Regrese v chování během refaktoringu
**Mitigation:** Zachovat existující testy, přidat characterization testy před refaktoringem

**Trade-off:** Více souborů vs. lepší organizace
**Decision:** Přijmout více souborů pro lepší maintainability

## Migration Plan

1. Vytvořit nové komponenty s testy
2. Postupně přesouvat logiku z WaveformEditorDialog
3. Aktualizovat WaveformEditorDialog pro použití nových komponent
4. Spustit všechny testy a smoke testy
5. Odstranit duplicitní kód z původní třídy

**Rollback:** Pokud testy selžou, vrátit změny a analyzovat problém před dalším pokusem.

## Open Questions
- Měla by být `TimeAxisItem` třída také přesunuta do `ui/waveform/`? (Doporučení: Ano, pro konzistenci)
