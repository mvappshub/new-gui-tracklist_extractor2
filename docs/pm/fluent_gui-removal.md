# PM Ticket: Plan for fluent_gui.py Removal

- Context: fluent_gui.py is a backward-compatibility wrapper. New development uses app.py and ui/ package.
- Decision: Keep deprecation in place, plan removal in a future minor/major release.
- Steps:
  1) Monitor external/internal imports of fluent_gui.py for one release cycle.
  2) Announce removal in CHANGELOG one version ahead.
  3) Provide migration note: use app.py entry point and ui/ components.
- Owner: maintainers
- Status: planned
- Related change: openspec/changes/archive/2025-10-24-refactor-unified-audit-plan
