## Why
The project successfully migrated from qfluentwidgets to pure PyQt6, but `openspec/project.md` still references "PyQt-Fluent-Widgets (QFluentWidgets)" and "QFluentWidgets QConfig". This creates confusion for developers and AI assistants working on the codebase.

## What Changes
- Update `openspec/project.md` Tech Stack section to reflect pure PyQt6 usage
- Remove references to QFluentWidgets and QConfig
- Document custom `FolderSettingCard` implementation in `settings_page.py`
- Update configuration description to mention QSettings

## Impact
- Affected specs: `specs/ui/spec.md` (minor clarification)
- Affected code: None (documentation only)
- User Experience: No change
- Dependencies: No change

