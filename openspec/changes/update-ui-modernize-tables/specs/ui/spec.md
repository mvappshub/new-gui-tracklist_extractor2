## ADDED Requirements

### Requirement: Robustní a Konzistentní Vizuální Styl Tabulek
Všechny tabulky v aplikaci MUST dodržovat jednotný, výkonný a ergonomický designový systém.

#### Scenario: Inteligentní správa prostoru
- **WHEN** se zobrazí tabulka
- **THEN** šířky sloupců se dynamicky přizpůsobí obsahu, přičemž prioritu má čitelnost dlouhých textů.
- **AND** uživatelsky změněné šířky a pořadí sloupců se MUSÍ zachovat mezi spuštěními aplikace.

#### Scenario: Prázdný stav (Empty State)
- **WHEN** tabulka neobsahuje žádná data
- **THEN** je zobrazena informativní zpráva ("No Data") místo prázdné plochy.
- **AND** toto zobrazení nenarušuje hlavní layout.

#### Scenario: Přístupnost a zpětná vazba
- **WHEN** je text v buňce nebo hlavičce příliš dlouhý pro zobrazení
- **THEN** se po najetí myší zobrazí tooltip s plným textem.
- **AND** aktivní prvek (řádek/buňka) je jasně vizuálně indikován pro navigaci myší (hover) i klávesnicí (focus).
