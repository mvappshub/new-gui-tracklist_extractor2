# Proposal: Waveform Editor Split

## Why
Třída `WaveformEditorDialog` v `waveform_viewer.py` má více než 740 řádků kódu (řádky 67-810) a porušuje Single Responsibility Principle. Třída současně spravuje audio loading, waveform rendering, region selection, playback control a PDF markers. Tato komplexita ztěžuje údržbu, testování a budoucí rozšíření.

## What Changes
- Vytvořit novou třídu `AudioLoader` pro extrakci a načítání audio dat z ZIP archivů
- Vytvořit novou třídu `WaveformPlotController` pro správu pyqtgraph PlotWidget a vykreslování
- Vytvořit novou třídu `PlaybackController` pro zapouzdření QMediaPlayer a ovládacích prvků
- Refaktorovat `WaveformEditorDialog` do role Mediator, který koordinuje komunikaci mezi komponentami
- Přesunout pomocné metody (time formatting, envelope creation) do utility modulů

## Impact
- Affected specs: `ui/spec.md` (Modular UI Architecture)
- Affected code: `waveform_viewer.py` (hlavní změna), nové soubory v `ui/waveform/`
- Breaking changes: Žádné - veřejné API `WaveformEditorDialog.__init__` zůstává stejné

## References
- waveform_viewer.py
