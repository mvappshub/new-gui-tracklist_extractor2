# Design: Modernizace a Optimalizace UI Tabulek (Revize)

## 1. Architektura Komponent
- **`ModernTableView(QTableView)`**: Nová komponenta v `ui/components/modern_table_view.py`. Bude zodpovědná za:
    - **Perzistenci hlaviček:** Implementuje metody `saveHeaderState(key)` a `restoreHeaderState(key)`, které ukládají/načítají stav horizontální hlavičky do `QSettings` pomocí `QHeaderView.saveState()/restoreState()`.
    - **Správu "Empty State":** Bude obsahovat instanci `EmptyStateOverlay` a řídit její viditelnost na základě `model()->rowCount()`.
    - **Základní konfiguraci:** V `__init__` aplikuje klíčové vlastnosti: `setMouseTracking(True)`, `setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)`, `setTextElideMode(Qt.TextElideMode.ElideMiddle)`, `horizontalHeader().setTextElideMode(Qt.TextElideMode.ElideRight)`.
- **`EmptyStateOverlay(QWidget)`**: Komponenta v `ui/components/empty_state_overlay.py`. Bude přichycena k `viewport()` tabulky, bude mít nastaveno `setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)` a bude obsahovat ikonu a text "No Data".

## 2. Strategie Šířky Sloupců
- Bude explicitně nastaveno `horizontalHeader().setStretchLastSection(False)`.
- **Počáteční nastavení:** Po prvním naplnění daty se jednorázově zavolá `resizeColumnsToContents()`.
- **Finální režim (obnoven z QSettings nebo default):**
    - Sloupce s ikonami a krátkým obsahem: `QHeaderView.ResizeMode.Interactive`.
    - Sloupce `File`, `Title`, `WAV file`: `QHeaderView.ResizeMode.Stretch`.

## 3. Styling (QSS) a Tematizace
- Vytvoří se soubor `assets/stylesheets/tables.qss` s podporou pro světlý a tmavý režim.
- Bude použit selektor `QWidget[theme="dark"]` pro tematizaci.
- **Focus State:** Pro zvýraznění fokusu bude použit selektor na úrovni widgetu (`QTableView:focus`) a pro zvýraznění výběru kombinace `::item:selected:active` a `::item:selected:!active`.

## 4. Konfigurace Hlaviček a Řádků
- **Výška řádků:** `verticalHeader().setDefaultSectionSize(36)`.
- **Šířka vertikální hlavičky (`#`):** `verticalHeader().setFixedWidth(36)`.
- **API `setUniformRowHeights` se nepoužije**, jelikož není součástí `QTableView`.

## 5. Proxy Model
- Pro filtrování a řazení bude použit `QSortFilterProxyModel`.
