# Spec Delta: Extraction

## REMOVED Requirements

### Requirement: Legacy Audio Mode Detection Functions
Reason: Functions `detect_audio_mode_with_ai()` and `normalize_positions()` from deprecated `wav_extractor_wave.py` have been replaced by `ChainedAudioModeDetector`.

Migration: Use `ChainedAudioModeDetector.detect()` which handles both detection and normalization in a single call.

## MODIFIED Requirements

### Requirement: Audio Mode Detection
The system SHALL detect audio mode (side and position) from WAV files using ONLY the Chain of Responsibility pattern through `ChainedAudioModeDetector`.

#### Scenario: Unified detection flow
- WHEN the system needs to detect side and position from WAV filenames
- THEN it uses `ChainedAudioModeDetector.detect()` method
- AND detection automatically includes normalization (sequential positions per side)
- AND no separate normalization step is needed

#### Scenario: No legacy code
- WHEN extraction pipeline processes WAV files
- THEN it uses only modern adapter components
- AND no imports from `wav_extractor_wave` exist
- AND all detection logic is centralized in `adapters.audio` package

## References
- openspec/specs/extraction/spec.md
