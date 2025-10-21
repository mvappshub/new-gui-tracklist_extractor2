## Context
The `fluent_gui.py` file has grown to 1161 lines and violates multiple SOLID principles. The refactoring aims to create a clean, testable, maintainable architecture while preserving all existing functionality. Key stakeholders are developers working on UI features (especially the upcoming `redesign-gz-media-ui` change) and QA engineers writing tests.

## Goals / Non-Goals

### Goals
- Achieve 100% backward compatibility with existing `fluent_gui.py` imports
- Enable isolated unit testing of all UI components with mock dependencies
- Implement Dependency Inversion Principle (DIP) throughout UI layer
- Separate worker/thread lifecycle management from MainWindow (SRP)
- Create clear, documented module boundaries
- Prepare architecture for upcoming UI redesign

### Non-Goals
- Changing any user-facing functionality or behavior
- Modifying the service layer (`AnalysisService`) or domain logic
- Introducing new UI frameworks or libraries
- Performance optimization (unless it emerges as a side benefit)
- Changing the configuration file format or storage mechanism

<h2>Decisions</h2>

<h3>Decision 1: Dependency Injection via Constructor Parameters</h3>
<p><strong>What</strong>: All components receive their dependencies (configuration, services) through constructor parameters rather than importing global objects.</p>
<p><strong>Why</strong>:</p>
<ul>
<li>Enables testing with mock objects</li>
<li>Makes dependencies explicit and visible</li>
<li>Follows Dependency Inversion Principle</li>
<li>Reduces coupling to global state</li>
</ul>
<p><strong>Alternatives considered</strong>:</p>
<ul>
<li><strong>Service Locator pattern</strong>: Rejected because it hides dependencies and makes testing harder</li>
<li><strong>Property injection</strong>: Rejected because it allows components to be in invalid state after construction</li>
<li><strong>Keep global config imports</strong>: Rejected because it prevents isolated testing</li>
</ul>
<p><strong>Implementation</strong>:</p>
<ul>
<li>Create typed configuration models in <code>ui/config_models.py</code> (Pydantic or dataclasses)</li>
<li>Each component declares its config needs in constructor</li>
<li><code>app.py</code> loads global config and creates specific config objects</li>
<li><code>MainWindow</code> receives all dependencies and passes them to child components</li>
</ul>

<h3>Decision 2: AnalysisWorkerManager for Thread Lifecycle</h3>
<p><strong>What</strong>: Create a dedicated manager class that encapsulates all QThread and AnalysisWorker lifecycle management.</p>
<p><strong>Why</strong>:</p>
<ul>
<li>MainWindow has too many responsibilities (SRP violation)</li>
<li>Thread management is error-prone and should be centralized</li>
<li>Easier to test worker behavior in isolation</li>
<li>Cleaner MainWindow code focused on UI concerns</li>
</ul>
<p><strong>Alternatives considered</strong>:</p>
<ul>
<li><strong>Keep thread management in MainWindow</strong>: Rejected due to SRP violation and testing difficulty</li>
<li><strong>Use Qt's QThreadPool</strong>: Rejected because we need more control over worker lifecycle and signals</li>
<li><strong>Create abstract WorkerManager interface</strong>: Deferred to future if multiple worker types emerge</li>
</ul>
<p><strong>Implementation</strong>:</p>
<ul>
<li><code>AnalysisWorkerManager</code> owns QThread and AnalysisWorker instances</li>
<li>Provides high-level API: <code>start_analysis()</code>, <code>is_running()</code>, <code>stop_analysis()</code>, <code>cleanup()</code></li>
<li>Forwards worker signals to MainWindow</li>
<li>Handles all thread safety concerns internally</li>
</ul>

<h3>Decision 3: Configuration Abstractions with Typed Models</h3>
<p><strong>What</strong>: Create small, focused configuration classes (e.g., <code>ToleranceSettings</code>, <code>ExportSettings</code>) instead of passing entire config object.</p>
<p><strong>Why</strong>:</p>
<ul>
<li>Interface Segregation Principle - components only see what they need</li>
<li>Type safety and IDE autocomplete</li>
<li>Clear documentation of component dependencies</li>
<li>Easier to mock in tests</li>
</ul>
<p><strong>Alternatives considered</strong>:</p>
<ul>
<li><strong>Pass entire config object</strong>: Rejected because it hides actual dependencies</li>
<li><strong>Use dictionaries</strong>: Rejected because it loses type safety</li>
<li><strong>Environment variables</strong>: Rejected because it's less flexible and harder to test</li>
</ul>
<p><strong>Implementation</strong>:</p>
<ul>
<li>Define dataclasses/Pydantic models in <code>ui/config_models.py</code></li>
<li>Create <code>load_*_settings(cfg)</code> factory functions to convert from global config</li>
<li>Components declare specific settings type in constructor</li>
</ul>

<h3>Decision 4: Compatibility Wrapper for fluent_gui.py</h3>
<p><strong>What</strong>: Transform <code>fluent_gui.py</code> into a thin wrapper that imports from new modules and provides backward-compatible API.</p>
<p><strong>Why</strong>:</p>
<ul>
<li>Zero breaking changes for existing code</li>
<li>Gradual migration path for developers</li>
<li>Maintains existing entry point (<code>python fluent_gui.py</code>)</li>
</ul>
<p><strong>Alternatives considered</strong>:</p>
<ul>
<li><strong>Delete fluent_gui.py entirely</strong>: Rejected because it breaks existing imports</li>
<li><strong>Keep both implementations</strong>: Rejected because it creates maintenance burden</li>
<li><strong>Deprecate immediately</strong>: Rejected because it forces rushed migration</li>
</ul>
<p><strong>Implementation</strong>:</p>
<ul>
<li>Import all classes from new modules</li>
<li>Create type aliases (e.g., <code>TopTableModel = ResultsTableModel</code>)</li>
<li>Wrapper functions for functions that need config (load global config internally)</li>
<li>Deprecation comment directing to new structure</li>
<li>Characterization tests ensure compatibility</li>
</ul>

<h3>Decision 5: Characterization Tests Before Refactoring</h3>
<p><strong>What</strong>: Write comprehensive tests that capture current behavior before making any changes.</p>
<p><strong>Why</strong>:</p>
<ul>
<li>Safety net to detect regressions</li>
<li>Documents expected behavior</li>
<li>Validates compatibility wrapper</li>
<li>Enables confident refactoring</li>
</ul>
<p><strong>Alternatives considered</strong>:</p>
<ul>
<li><strong>Rely on existing tests</strong>: Rejected because coverage is incomplete</li>
<li><strong>Manual testing only</strong>: Rejected because it's not repeatable</li>
<li><strong>Skip characterization tests</strong>: Rejected because risk is too high</li>
</ul>
<p><strong>Implementation</strong>:</p>
<ul>
<li>Create <code>tests/test_fluent_gui_legacy.py</code></li>
<li>Test all exported symbols are importable</li>
<li>Test MainWindow can be instantiated</li>
<li>Test entry point execution</li>
<li>Run before and after refactoring to ensure identical behavior</li>
</ul>

<h2>Risks / Trade-offs</h2>

<h3>Risk: Increased Initial Complexity</h3>
<p><strong>Description</strong>: DI and manager classes add more files and indirection.</p>
<p><strong>Mitigation</strong>:</p>
<ul>
<li>Clear documentation and examples</li>
<li>Gradual rollout with compatibility wrapper</li>
<li>Training/code review for team</li>
</ul>
<p><strong>Trade-off</strong>: Short-term complexity for long-term maintainability</p>

<h3>Risk: Performance Overhead from DI</h3>
<p><strong>Description</strong>: Creating and passing config objects might add overhead.</p>
<p><strong>Mitigation</strong>:</p>
<ul>
<li>Config objects are created once at startup</li>
<li>Negligible impact compared to UI rendering and analysis</li>
<li>Profile if concerns arise</li>
</ul>
<p><strong>Trade-off</strong>: Minimal performance cost for massive testability gain</p>

<h3>Risk: Breaking Changes Despite Wrapper</h3>
<p><strong>Description</strong>: Subtle behavior differences might break existing code.</p>
<p><strong>Mitigation</strong>:</p>
<ul>
<li>Comprehensive characterization tests</li>
<li>Thorough manual testing</li>
<li>Gradual rollout with monitoring</li>
</ul>
<p><strong>Trade-off</strong>: Accept small risk for architectural improvement</p>

<h3>Risk: Maintenance of Two Code Paths</h3>
<p><strong>Description</strong>: Compatibility wrapper needs maintenance alongside new code.</p>
<p><strong>Mitigation</strong>:</p>
<ul>
<li>Wrapper is thin and mechanical</li>
<li>Plan deprecation timeline (e.g., 2 releases)</li>
<li>Document migration path</li>
</ul>
<p><strong>Trade-off</strong>: Temporary maintenance burden for smooth transition</p>

<h2>Migration Plan</h2>

<h3>Phase 1: Refactoring (This Change)</h3>
<ol>
<li>Implement new modular structure with DI</li>
<li>Create compatibility wrapper</li>
<li>Update tests</li>
<li>Validate with characterization tests</li>
<li>Deploy with both paths working</li>
</ol>

<h3>Phase 2: Migration (Future Change)</h3>
<ol>
<li>Update internal code to use new imports</li>
<li>Add deprecation warnings to wrapper</li>
<li>Update documentation</li>
<li>Communicate migration timeline</li>
</ol>

<h3>Phase 3: Cleanup (Future Change)</h3>
<ol>
<li>Remove compatibility wrapper</li>
<li>Remove legacy tests</li>
<li>Finalize documentation</li>
</ol>

<h2>Rollback Plan</h2>
<p>If critical issues are discovered:</p>
<ol>
<li>Revert to pre-refactoring commit</li>
<li>Compatibility wrapper ensures no code changes needed</li>
<li>Investigate issues in development environment</li>
<li>Fix and redeploy</li>
</ol>

<h2>Open Questions</h2>

<ol>
<li><strong>Q</strong>: Should we use Pydantic or dataclasses for config models?
   <strong>A</strong>: Start with dataclasses for simplicity. Migrate to Pydantic if validation becomes important.</li>
<li><strong>Q</strong>: How long should we maintain the compatibility wrapper?
   <strong>A</strong>: At least 2 releases (or 6 months), then deprecate with warnings.</li>
<li><strong>Q</strong>: Should AnalysisWorkerManager be a singleton?
   <strong>A</strong>: No, MainWindow owns its instance. Allows multiple windows in future if needed.</li>
<li><strong>Q</strong>: Should we refactor settings_page.py similarly?
   <strong>A</strong>: Defer to separate change. It's already modular and doesn't violate SOLID as severely.</li>
<li><strong>Q</strong>: How to handle theme.py functions that need config?
   <strong>A</strong>: Accept config as parameter. Wrapper functions in fluent_gui.py load global config for legacy callers.
</li></ol>
