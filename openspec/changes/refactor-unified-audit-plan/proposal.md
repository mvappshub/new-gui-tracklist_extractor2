# Refactor Unified Audit Plan

## Why

The unified audit has identified several architectural weaknesses in the current implementation that violate established design principles and best practices:

### Architectural Weaknesses Identified

**Monolithic modules**: The `wav_extractor_wave.py` (297 lines) and `pdf_extractor.py` (184 lines) violate the Single Responsibility Principle by combining multiple concerns within single files. These modules handle file parsing, data extraction, format validation, and business logic all in one place.

**Duplicate code**: Filename parsing logic is duplicated between `wav_extractor_wave.py` (function `strict_from_path`) and `adapters/audio/fake_mode_detector.py` (method `_parse_filename`). This creates maintenance issues and potential inconsistencies when changes are needed.

**Primitive obsession**: `adapters/filesystem/file_discovery.py` returns `dict[str, dict[str, Path]]` instead of proper domain objects. This makes the code harder to understand, test, and maintain, as the data structure lacks semantic meaning.

**Magic numbers**: The value 999 is used for sorting in multiple locations without named constants, making the code less readable and maintainable. These magic numbers should be replaced with well-named constants that explain their purpose.

**Overly broad exception handling**: `adapters/audio/wav_reader.py` uses `except Exception` instead of specific exceptions like `zipfile.BadZipFile`. This makes debugging difficult and can hide real issues in the codebase.

While the previous 5-phase refactoring established a clean layered architecture with proper separation of concerns, this refactoring focuses on applying specific design patterns and refactoring techniques to improve implementation quality within those established layers.

## What Changes

This refactoring implements four main steps to address the identified architectural weaknesses:

### 1. Create Foundational Building Blocks
Introduce `StrictFilenameParser` domain service and `FilePair` dataclass to eliminate code duplication and primitive types. This will centralize filename parsing logic and provide type-safe data structures for file relationships.

### 2. Implement Architectural Patterns
Formalize audio mode detection using the Chain of Responsibility pattern with `ChainedAudioModeDetector` orchestrator. This will create a more flexible and extensible system for handling different audio detection strategies.

### 3. Decompose Monolithic Modules
Break down `wav_extractor_wave.py` and `pdf_extractor.py` into smaller, single-responsibility components. Each component will have a clear, focused purpose following the Single Responsibility Principle.

### 4. Final Cleanup and Hardening
Refine exception handling throughout the codebase and plan deprecation of legacy components. This includes replacing broad exception catches with specific exception types and establishing a clear migration path for deprecated functionality.

**Note**: This is marked as a non-breaking change focused purely on internal architecture improvements.

## Impact

### Affected Specs
- **analysis**: Requirements will be modified to reflect new architectural patterns and domain services
- **extraction**: Requirements will be updated to incorporate the new modular extraction components

### Affected Code
- `wav_extractor_wave.py` - Will be decomposed into smaller components
- `pdf_extractor.py` - Will be refactored following single responsibility principle
- `adapters/audio/fake_mode_detector.py` - Will use centralized filename parsing
- `adapters/filesystem/file_discovery.py` - Will return domain objects instead of primitive types
- `adapters/audio/wav_reader.py` - Will implement specific exception handling
- New domain services and orchestrators will be created

### User Experience
No visible changes to end users. All improvements are internal architectural enhancements.

### Dependencies
No new dependencies will be introduced. This refactoring works within the existing technology stack.

### Testing
The refactoring enables more isolated and robust unit testing by:
- Creating smaller, focused components that are easier to test in isolation
- Eliminating code duplication that previously required testing the same logic in multiple places
- Providing type-safe domain objects that make test setup and assertions clearer
- Implementing specific exception handling that allows for more precise testing of error conditions