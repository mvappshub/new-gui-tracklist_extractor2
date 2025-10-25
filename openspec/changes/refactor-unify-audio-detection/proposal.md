# Proposal: Unify Audio Detection

## Why
Soubor `wav_extractor_wave.py` je již označen jako DEPRECATED (řádky 1-10) a jeho funkčnost byla přesunuta do dedikovaných komponent (`core.domain.parsing.StrictFilenameParser`, `adapters.audio.chained_detector.ChainedAudioModeDetector`). Odstranění zastaralého kódu zvýší přehlednost a eliminuje duplicitní logiku.

## What Changes
- Odstranit soubor `wav_extractor_wave.py`
- Odstranit všechny importy a reference na tento modul
- Ověřit, že všechny části kódu používají `ChainedAudioModeDetector` a `core.models.analysis.WavInfo`
- Aktualizovat testy pro použití nových komponent

## Impact
- Affected specs: `analysis/spec.md` (Audio Mode Detection Port), `extraction/spec.md` (Audio Mode Detection)
- Affected code: `wav_extractor_wave.py` (odstranění), potenciální importy v testech nebo scripts
- Breaking changes: Žádné - deprecated modul by již neměl být používán v produkčním kódu

## References
- wav_extractor_wave.py
- adapters/audio/chained_detector.py
- core/models/analysis.py
