# Tasks: Modernizace a Optimalizace UI Tabulek (Revize)

## Fáze 1: Vytvoření Základních Komponent
- [ ] 1. Vytvořit soubor `ui/components/empty_state_overlay.py` a implementovat `EmptyStateOverlay` (QWidget s QIcon a QLabel). V `__init__` nastavit `setAttribute(Qt.WA_TransparentForMouseEvents, True)`.
- [ ] 2. Vytvořit soubor `ui/components/modern_table_view.py` a implementovat `ModernTableView`.
- [ ] 3. V `ModernTableView` implementovat metody `saveHeaderState(key: str)` a `restoreHeaderState(key: str)` využívající `QSettings` a `QHeaderView.saveState()/restoreState()`.
- [ ] 4. V `ModernTableView` integrovat `EmptyStateOverlay` a napojit jeho viditelnost na signály modelu (`rowsInserted`, `rowsRemoved`, `modelReset`).
- [ ] 5. V `ModernTableView.__init__` nastavit:
    - `self.setMouseTracking(True)`
    - `self.setTextElideMode(Qt.TextElideMode.ElideMiddle)`
    - `self.horizontalHeader().setTextElideMode(Qt.TextElideMode.ElideRight)`
    - `self.verticalHeader().setFixedWidth(36)`
    - `self.verticalHeader().setDefaultSectionSize(36)`

## Fáze 2: Styling a Integrace
- [ ] 6. Vytvořit adresář `assets/stylesheets/`.
- [ ] 7. Vytvořit soubor `assets/stylesheets/tables.qss` se správnými selektory (`:focus` na widgetu, `:selected:active` na item).
- [ ] 8. V `ui/main_window.py` implementovat logiku pro načtení `tables.qss` a nastavení `theme` property na hlavní okno.
- [ ] 9. V `ui/main_window.py` nahradit `QTableView` za `ModernTableView`.
- [ ] 10. V `ui/main_window.py` upravit `setup_tables`:
    - [ ] 10.1 Explicitně nastavit `horizontalHeader().setStretchLastSection(False)`.
    - [ ] 10.2 Implementovat strategii šířky sloupců. Po prvním naplnění daty zavolat `resizeColumnsToContents()`, poté nastavit režimy `Interactive` a `Stretch`.
- [ ] 11. V `closeEvent` `MainWindow` zavolat `saveHeaderState()` pro obě tabulky.
- [ ] 12. V `__init__` `MainWindow` zavolat `restoreHeaderState()` pro obě tabulky.
- [ ] 13. V modelech `ResultsTableModel` a `TracksTableModel` implementovat `data()` pro `Qt.ToolTipRole`.

## Fáze 3: Ověření
- [ ] 14. Vizuálně ověřit všechny aspekty a funkčnost na světlém i tmavém motivu.
- [ ] 15. Spustit `pytest` a zajistit, že všechny testy procházejí.
