# GZ Media Assets

Tento adresář obsahuje grafické assety pro GZ Media branding aplikace Final Cue Sheet Checker.

## Požadované logo soubory

### `gz_logo_white.png`
- **Formát:** PNG s průhledným pozadím
- **Barva:** Bílá varianta GZ Media loga
- **Rozměry:** Doporučeno 128x32 pixelů (4:1 poměr)
- **Umístění:** Levý horní roh hlavního okna
- **Pozadí:** Průhledné pro správné zobrazení na různých barvách

### `gz_logo_dark.png` (volitelné)
- **Formát:** PNG s průhledným pozadím
- **Barva:** Tmavá varianta pro světlé pozadí
- **Rozměry:** Stejné jako bílá varianta
- **Použití:** Automatické přepínání podle theme modu

## UI Icons

### `icons/check.svg`
- **Formát:** SVG
- **Rozměry:** 16x16 pixelů
- **Barva:** Zelená (#10B981)
- **Použití:** Indikace úspěšného match v tabulce (sloupec Match)
- **Design:** Checkmark symbol s kulatými konci

### `icons/cross.svg`
- **Formát:** SVG
- **Rozměry:** 16x16 pixelů
- **Barva:** Červená (#EF4444)
- **Použití:** Indikace neúspěšného match v tabulce (sloupec Match)
- **Design:** Cross symbol s kulatými konci

### `icons/play.svg`
- **Formát:** SVG
- **Rozměry:** 16x16 pixelů
- **Barva:** Modrá (#3B82F6)
- **Použití:** Tlačítko pro zobrazení waveform (sloupec Waveform)
- **Design:** Play triangle symbol

## Fallback chování

Pokud SVG ikony nejsou nalezeny nebo se nepodaří načíst, aplikace automaticky použije systémové ikony:
- **check.svg** → Systémová checkmark ikona
- **cross.svg** → Systémová cross ikona
- **play.svg** → Systémová play ikona (SP_MediaPlay)

Aplikace zobrazí warning v logu, ale nepřestane fungovat.

## Technické požadavky

- **Formát:** PNG s průhledností (RGBA)
- **Velikost:** Optimalizované pro rychlé načítání (< 50KB)
- **Rozměry:** Šířka max 200px, výška max 40px
- **Kvalita:** Ostré hrany, žádné kompresní artefakty

## Fallback chování

Pokud logo soubory nejsou nalezeny, aplikace zobrazí textový fallback:
- **Text:** "GZ Media"
- **Font:** Poppins Bold
- **Barva:** GZ Primary Blue (#1E3A8A)

## Claim

Claim "Emotions. Materialized." se zobrazuje v pravém dolním rohu okna:
- **Font:** Poppins Italic
- **Velikost:** 8pt
- **Barva:** GZ Gray (#6B7280)
- **Konfigurace:** Lze zapnout/vypnout v settings

## Přidání nových assetů

1. Uložte logo soubory do tohoto adresáře
2. Aktualizujte `config.py` - `gz_logo_path` konfiguraci
3. Restartujte aplikaci pro načtení nových assetů

## Brand Guidelines

Všechny assety musí být v souladu s GZ Media brand guidelines:
- ✅ Pouze oficiální GZ Media logo
- ✅ Správné proporce a barevnost
- ✅ Profesionální kvalita
- ❌ Žádné modifikace nebo úpravy loga