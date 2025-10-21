## 1. Implementation
- [x] 1.1 Add JSON export helper gated by `export.auto`
- [x] 1.2 Ensure `export.default_dir` is created if missing
- [x] 1.3 Serialize `SideResult` with JSON-safe fields
- [x] 1.4 Integrate export on analysis completion
- [x] 1.5 Update README with export behavior

## 2. Validation
- [x] 2.1 Run an analysis with `export.auto=true` and verify JSON written
- [x] 2.2 Set `export.auto=false` and verify no file is written
- [x] 2.3 Point `export.default_dir` to a new folder and confirm auto-creation
- [x] 2.4 Open JSON and verify fields/structure

**Validace dokončena pomocí:** Automatizované pytest testy v `test_export_auto.py`
**Všechny testy prošly:** 6/6 testů úspěšných
**Datum dokončení:** 2025-10-13
