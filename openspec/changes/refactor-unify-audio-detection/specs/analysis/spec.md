# Spec Delta: Analysis

## REMOVED Requirements

### Requirement: Legacy Audio Mode Detection
Reason: Deprecated module `wav_extractor_wave.py` has been fully replaced by `ChainedAudioModeDetector` and related components.

Migration: All code should use `ChainedAudioModeDetector` from `adapters.audio.chained_detector` and `WavInfo` from `core.models.analysis`.

## MODIFIED Requirements

### Requirement: Audio Mode Detection Port
The system SHALL use ONLY the port interface and Chain of Responsibility pattern for audio mode detection, with no legacy fallback code.

#### Scenario: Unified detection interface
- WHEN the system needs to detect side and position from WAV filenames
- THEN it uses `ChainedAudioModeDetector` from `adapters.audio.chained_detector`
- AND no code imports from deprecated `wav_extractor_wave` module
- AND all detection flows through the Chain of Responsibility pattern

#### Scenario: Canonical data model
- WHEN the system works with WAV metadata
- THEN it uses `WavInfo` from `core.models.analysis`
- AND no duplicate `WavInfo` definitions exist in the codebase
- AND all components use the same canonical model

#### Scenario: No legacy imports
- WHEN codebase is scanned for imports
- THEN no imports from `wav_extractor_wave` exist
- AND all audio detection uses modern adapter pattern
- AND deprecated code has been completely removed

## References
- openspec/specs/analysis/spec.md
