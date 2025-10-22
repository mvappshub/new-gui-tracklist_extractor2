## ADDED Requirements

### Requirement: Custom Iconography
The application SHALL use custom SVG icons for key status indicators and actions to ensure visual consistency, brand alignment, and cross-platform compatibility.

#### Scenario: Consistent Match symbols
- **WHEN** the tracks table is displayed
- **THEN** the "Match" column (column 6) SHALL render a custom green SVG checkmark icon for successful matches
- **AND** SHALL render a custom red SVG cross icon for failed matches
- **AND** SHALL NOT display text symbols like '✓', '✗', or arrows
- **AND** the icons SHALL be loaded from `assets/icons/check.svg` and `assets/icons/cross.svg`

#### Scenario: Consistent Waveform action icon
- **WHEN** the tracks table is displayed
- **THEN** the "Waveform" column (column 7) SHALL render a custom blue SVG "play" icon for the view waveform action
- **AND** SHALL NOT display a generic system arrow or text symbol
- **AND** the icon SHALL be loaded from `assets/icons/play.svg`

#### Scenario: Icon caching for performance
- **WHEN** icons are loaded multiple times
- **THEN** the application SHALL cache loaded icons in memory
- **AND** SHALL NOT reload the same icon from disk repeatedly

#### Scenario: Graceful fallback
- **WHEN** a custom icon file is missing or cannot be loaded
- **THEN** the application SHALL log a warning
- **AND** SHALL fall back to system icons or empty icons
- **AND** SHALL NOT crash or display error dialogs