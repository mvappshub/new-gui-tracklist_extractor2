# Proposal: Modernizace a Optimalizace UI Tabulek

## Proč (Why)
Současné tabulky v uživatelském rozhraní jsou vizuálně zastaralé, nekonzistentní se zbytkem designu a trpí ergonomickými nedostatky. Neefektivní správa šířky sloupců vede k ořezávání důležitých informací a plýtvání místem. Chybí také klíčové prvky moderního UI, jako je správná vizuální hierarchie, interaktivní zpětná vazba a perzistence uživatelských nastavení.

## Co se Změní (What Changes)
Provedeme komplexní redesign a refaktoring tabulek s důrazem na výkon, udržovatelnost a vizuální konzistenci. Klíčové změny zahrnují:
- Vytvoření specializované komponenty `ModernTableView` a `EmptyStateOverlay`.
- Implementaci robustní strategie pro dynamickou šířku sloupců.
- Centralizaci stylingu do QSS souboru s podporou pro světlý/tmavý režim.
- Zavedení perzistence stavu hlaviček (šířka, pořadí) do `QSettings`.
- Vylepšení přístupnosti a interaktivity (tooltippy, focus state, hover efekty).

## Dopad (Impact)
- **Dotčené specifikace:** `ui/spec.md` (přidání nových požadavků na UI).
- **Dotčený kód:** `ui/main_window.py`, `config.py`, nové komponenty v `ui/components/`.
- **Breaking changes:** Žádné.
