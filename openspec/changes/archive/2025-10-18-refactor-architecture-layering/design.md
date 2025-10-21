## Context
The current monolithic `fluent_gui.py` (1468 lines) mixes GUI, domain logic, and I/O. This refactoring separates concerns following Clean Architecture principles while maintaining behavior parity.

## Goals / Non-Goals
**Goals:**
- Separate domain logic (comparison, extraction) from GUI
- Improve testability through dependency injection
- Maintain 100% behavior parity (no user-visible changes)
- Enable future feature development without touching GUI

**Non-Goals:**
- Changing UI appearance or user workflows
- Adding new features (pure refactoring)
- Modifying external APIs (PDF/WAV extraction interfaces)

## Decisions

### Decision 1: Three-layer architecture
**What:** Organize code into `core/` (domain logic), `services/` (orchestration), `adapters/` (I/O), with GUI as presentation layer.

**Why:** 
- Domain logic becomes testable without Qt dependencies
- Services provide clear API for GUI to consume
- Adapters isolate filesystem/ZIP operations

**Alternatives considered:**
- Keep monolith: Rejected - testing and maintenance too difficult
- Full DDD with repositories: Rejected - over-engineering for this app size

### Decision 2: Extract functions, not classes initially
**What:** Move pure functions from `fluent_gui.py` to modules, keep existing function signatures.

**Why:**
- Minimal risk - functions are already well-defined
- Easy to verify behavior parity
- Can introduce classes later if needed

**Alternatives considered:**
- Create service classes immediately: Rejected - adds complexity without clear benefit yet

### Decision 3: Keep Pydantic models in core/models/
**What:** Move `TrackInfo`, `WavInfo`, `SideResult` from `fluent_gui.py` to `core/models/`.

**Why:**
- These are domain models, not GUI concerns
- Already well-defined with Pydantic validation
- Shared between domain and GUI layers

### Decision 4: AnalysisService as orchestrator
**What:** Create `services/analysis_service.py` that coordinates file discovery, extraction, comparison.

**Why:**
- GUI's `AnalysisWorker` (QThread) becomes thin wrapper around service
- Service can be tested without Qt event loop
- Clear separation: service = what to do, worker = how to do it in background

## Risks / Trade-offs

**Risk:** Breaking behavior during extraction
- **Mitigation:** P1 retro-spec defines parity scenarios; verify after each phase

**Risk:** Import cycles between layers
- **Mitigation:** Strict dependency direction: GUI → services → core → adapters (no reverse)

**Trade-off:** More files to navigate
- **Benefit:** Each file has single responsibility, easier to understand

## Migration Plan

**Phase P2 - Vrstvení:**
1. Create directory structure
2. Move pure functions (no Qt dependencies) first: `extract_numeric_id`, `discover_and_pair_files`
3. Move models to `core/models/`
4. Create `AnalysisService` wrapping moved functions
5. Update `AnalysisWorker` to delegate to service
6. Verify: run analysis, compare results with pre-refactor baseline

**Rollback:** Git revert if any parity scenario fails

## Open Questions
- Should `pdf_extractor.py` and `wav_extractor_wave.py` move to `adapters/` or stay at root? **Decision:** Move in future PR to keep this refactoring focused.

