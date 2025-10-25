# Spec Delta: UI

## ADDED Requirements

### Requirement: Waveform Editor Component Architecture
The waveform editor SHALL be decomposed into specialized, single-responsibility components following the Mediator pattern.

#### Scenario: Audio loading isolation
- WHEN waveform editor needs to load audio from ZIP
- THEN it uses `AudioLoader` component from `ui.waveform.audio_loader`
- AND AudioLoader handles ZIP extraction and soundfile loading
- AND AudioLoader manages temporary file lifecycle

#### Scenario: Plot rendering isolation
- WHEN waveform editor needs to render waveform
- THEN it uses `WaveformPlotController` component from `ui.waveform.plot_controller`
- AND WaveformPlotController manages pyqtgraph PlotWidget
- AND WaveformPlotController handles region selection and PDF markers

#### Scenario: Playback control isolation
- WHEN waveform editor needs playback functionality
- THEN it uses `PlaybackController` component from `ui.waveform.playback_controller`
- AND PlaybackController manages QMediaPlayer and transport controls
- AND PlaybackController synchronizes position slider and playhead line

#### Scenario: Mediator coordination
- WHEN components need to communicate
- THEN WaveformEditorDialog acts as Mediator
- AND components emit signals that Mediator routes to other components
- AND no direct coupling exists between AudioLoader, WaveformPlotController, and PlaybackController

#### Scenario: Component testability
- WHEN developer needs to test waveform functionality
- THEN they can test AudioLoader, WaveformPlotController, and PlaybackController independently
- AND each component has focused unit tests
- AND components can be mocked for integration testing

## MODIFIED Requirements

### Requirement: Modular UI Architecture
The UI layer SHALL be organized into separate packages for models, workers, dialogs, waveform components, and utilities, with each module having a single, well-defined responsibility.

#### Scenario: Waveform component isolation
- WHEN waveform editor needs modification
- THEN developers work with focused components in `ui/waveform/` package
- AND changes to audio loading do not affect playback or rendering
- AND each component can be tested and modified independently

#### Scenario: Utility function reuse
- WHEN multiple components need time formatting or envelope creation
- THEN they use shared utilities from `ui/waveform/utils.py`
- AND utility functions are pure and testable
- AND no duplicate implementation exists across components

## References
- openspec/specs/ui/spec.md
