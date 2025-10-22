# Changelog

## [Refactoring Complete] - 2025-10-22

### Architecture
- **COMPLETED**: 5-phase strategic refactoring to hexagonal architecture
- **Phase 1**: Stabilization - type safety, characterization tests, quality tooling
- **Phase 2**: Dependency Injection - settings dataclasses, no global config
- **Phase 3**: I/O Modularization - adapters for ZIP/WAV reading
- **Phase 4**: Export Service - centralized export
- **Phase 5**: AI Port - AudioModeDetector protocol

### Quality Improvements
- Test coverage: 97% (55 passing tests)
- Type safety: mypy --strict passes
- Code quality: ruff clean, zero dead code
- Domain layer: Zero infrastructure dependencies

### Testing
- Characterization tests with golden JSON outputs
- Fake adapters for deterministic tests
- No external API calls in test suite

### Developer Experience
- Added tools/check.sh for local quality gates
- OpenSpec-driven development
- Clear layer boundaries with explicit dependencies

### Non-Breaking Changes
- All phases maintained behavioral parity
- No user-facing changes
- Internal architecture improvements only

## [0.0.1] - 2025-10-21
### Fixed
- Refactor stabilization phase 1: internal type-safety, test coverage >=85%, dead code removal.
- Check script finalized with unified coverage run and clear success message.
- Documentation: replaced QConfig with QSettings, removed PyQt-Fluent-Widgets.
- Added Purpose sections to specs (analysis/export/extraction).

