# Design Document: Unified Audit Refactoring

## Context

This refactoring is based on a unified audit identifying architectural code smells (Large Class/Module, Duplicate Code, Primitive Obsession, Overly Broad Exception Handling). While the previous 5-phase refactoring established clean layered architecture, this change applies specific design patterns and techniques to refine implementation within those layers.

## Goals / Non-Goals

### Goals
- Improve maintainability and readability
- Increase type safety
- Formalize orchestration logic using established patterns
- Enhance testability through smaller components
- Eliminate code duplication

### Non-Goals
- No new user-facing features
- No changes to external behavior
- No modifications to service layer public API

## Decisions

### Decision 1: Chain of Responsibility for Audio Mode Detection

**What**: Implement Chain of Responsibility pattern for AudioModeDetector. Create orchestrator ChainedAudioModeDetector that processes list of detection strategies (StrictParserStep, AiParserStep, DeterministicFallbackStep)

**Why**: Current logic in wav_extractor_wave.py (function detect_audio_mode_with_ai) is an implicit chain. This pattern makes orchestration explicit, configurable, and extensible. Each step is self-contained and testable. Complements existing Strategy pattern defined in core/ports.py

**Alternatives considered**: Complex if/elif/else structure within single class. Rejected as less flexible and harder to maintain

### Decision 2: Extract Class for Filename Parsing

**What**: Create domain service class StrictFilenameParser to centralize all regex-based parsing logic for side and position

**Why**: Logic duplicated in fake_mode_detector.py (method _parse_filename) and wav_extractor_wave.py (function strict_from_path). Dedicated class adheres to SRP and DRY principles, provides single source of truth

**Alternatives considered**: Simple utility function. Rejected in favor of class to allow future extension and state management

### Decision 3: Replace Primitive with Object for File Pairing

**What**: Introduce @dataclass class FilePair(pdf: Path, zip: Path) and refactor discover_and_pair_files in adapters/filesystem/file_discovery.py to return dict[int, FilePair]

**Why**: Current use of dict[str, dict[str, Path]] is classic Primitive Obsession. Dedicated FilePair object improves type safety, code clarity, and self-documentation. Allows consistent use of int for IDs

**Alternatives considered**: Using TypedDict. Rejected because dataclass provides more features (methods) for future use

### Decision 4: Decompose Monolithic Modules

**What**: Break down wav_extractor_wave.py and pdf_extractor.py into smaller, single-responsibility components

**Why**: These modules violate Single Responsibility Principle and are difficult to test and maintain (Large Class/Module code smell)

**Implementation**:
- wav_extractor_wave.py: Logic distributed among StrictFilenameParser and Chain of Responsibility steps
- pdf_extractor.py: Break into PdfImageRenderer (Adapter), VlmClient (Adapter), and TracklistParser (Domain Service)

## Migration Plan

Execution order to minimize risk:

1. **Foundation**: Implement StrictFilenameParser and FilePair. Update callers
2. **Architecture**: Implement Chain of Responsibility pattern for audio detection
3. **Decomposition**: Decompose monolithic modules, replacing internal logic with new components
4. **Hardening**: Refine exception handling by replacing broad except Exception with specific exceptions