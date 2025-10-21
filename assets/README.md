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