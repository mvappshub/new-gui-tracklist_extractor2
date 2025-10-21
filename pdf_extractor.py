import io
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

# --- Potřebné závislosti (ujistěte se, že jsou nainstalované) ---
# pip install openai pydantic PyMuPDF Pillow
try:
    import fitz  # PyMuPDF
    from openai import OpenAI
    from PIL import Image
except ImportError as e:
    print(f"Chyba: Chybí potřebná knihovna - {e}. Nainstalujte ji prosím pomocí 'pip install openai pydantic PyMuPDF Pillow'")
    sys.exit(1)

# --- Datové modely (stejné jako v hlavní aplikaci) ---
from core.models.analysis import TrackInfo

if TYPE_CHECKING:
    from PIL import Image

# --- Jádro extrakce (převzato a upraveno z funkční verze) ---

def _to_data_url(pil_image: Image.Image) -> str:
    """Převede obrázek na base64 data URL pro Vision API."""
    import base64
    buf = io.BytesIO()
    pil_image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    return f"data:image/png;base64,{b64}"

def _render_pdf_to_images(pdf_path: Path) -> list["Image.Image"]:
    """Převede stránky PDF na obrázky."""
    images = []
    doc = fitz.open(str(pdf_path))
    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
        images.append(img)
    return images

def _call_vlm_json(prompt: str, images: list["Image.Image"]) -> dict[str, Any]:
    """Zavolá Vision LLM a vrátí odpověď jako JSON."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ConnectionError("Chybí API klíč. Nastavte proměnnou prostředí OPENROUTER_API_KEY.")

    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *({"type": "image_url", "image_url": {"url": _to_data_url(img)}} for img in images)
            ]
        }
    ]

    response = client.chat.completions.create(
        model="google/gemini-2.5-flash", # Můžete si zde nastavit jiný model
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.0
    )
    
    content = response.choices[0].message.content
    if not content:
        raise ValueError("AI vrátila prázdnou odpověď.")
        
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Zkusíme jednoduchou opravu, pokud JSON není perfektní
        cleaned_content = content.strip().strip("`").strip("json\n")
        return json.loads(cleaned_content)

def _consolidate_and_parse_tracks(raw_tracks: list[dict[str, Any]]) -> list[TrackInfo]:
    """Vyčistí, deduplikuje a převede data z AI na striktní TrackInfo objekty."""
    final_tracks = []
    seen = set()
    
    # Jednoduchý regex pro parsování času
    time_pattern = re.compile(r'(\d{1,2}):([0-5]\d)')

    for track_data in raw_tracks:
        try:
            title = str(track_data.get("title", "")).strip()
            side = str(track_data.get("side", "?")).strip().upper()
            position = int(track_data.get("position", 99))
            duration_str = str(track_data.get("duration_formatted", "")).strip()

            if not title or not duration_str:
                continue

            match = time_pattern.match(duration_str)
            if not match:
                continue
            
            minutes, seconds = int(match.group(1)), int(match.group(2))
            duration_sec = minutes * 60 + seconds
            
            # Pojistka proti nesmyslným délkám
            if minutes > 25:
                logging.warning(f"Ignoruji nesmyslně dlouhý track: {title} ({duration_str})")
                continue

            # Deduplikace
            key = (title.lower(), side, duration_sec)
            if key in seen:
                continue
            seen.add(key)

            final_tracks.append(TrackInfo(
                title=title,
                side=side,
                position=position,
                duration_sec=duration_sec
            ))
        except (ValueError, TypeError, KeyError) as e:
            logging.warning(f"Chyba při zpracování tracku: {track_data}. Chyba: {e}")

    # Seřazení a přečíslování v rámci každé strany
    final_tracks.sort(key=lambda t: (t.side, t.position, t.title))
    
    # Zde by mohla být ještě logika pro přečíslování pozic, pokud je potřeba
    
    return final_tracks

def extract_pdf_tracklist(pdf_path: Path) -> dict[str, list[TrackInfo]]:
    """
    Hlavní a jediná funkce tohoto modulu.
    Vezme cestu k PDF, provede kompletní extrakci a vrátí strukturovaná data.
    """
    logging.info(f"Spouštím reálnou extrakci z PDF: {pdf_path.name}")
    
    try:
        images = _render_pdf_to_images(pdf_path)
        if not images:
            logging.warning(f"PDF soubor '{pdf_path.name}' neobsahuje žádné stránky.")
            return {}

        prompt = (
            "You are a tracklist extractor. Return STRICT JSON only.\n"
            "Schema: { \"tracks\": [ {\"title\": string, \"side\": string, \"position\": integer, \"duration_formatted\": \"MM:SS\" } ] }.\n"
            "- Extract all visible tracks.\n"
            "- Normalize time to MM:SS format.\n"
            "- Infer side and position if possible.\n"
            "- Do not invent data. Ignore non-track information."
        )

        all_raw_tracks = []
        for img in images:
            try:
                ai_response = _call_vlm_json(prompt, [img])
                if "tracks" in ai_response and isinstance(ai_response["tracks"], list):
                    all_raw_tracks.extend(ai_response["tracks"])
            except Exception as e:
                logging.error(f"Chyba při volání AI pro stránku z '{pdf_path.name}': {e}")
        
        if not all_raw_tracks:
            logging.warning(f"AI nevrátila žádné tracky pro soubor: {pdf_path.name}")
            return {}

        parsed_tracks = _consolidate_and_parse_tracks(all_raw_tracks)
        
        # Seskupení finálních tracků podle strany
        result_by_side: dict[str, list[TrackInfo]] = {}
        for track in parsed_tracks:
            if track.side not in result_by_side:
                result_by_side[track.side] = []
            result_by_side[track.side].append(track)
        
        logging.info(f"Extrakce z PDF '{pdf_path.name}' dokončena, nalezeno {len(parsed_tracks)} skladeb.")
        return result_by_side

    except Exception as e:
        logging.error(f"Kompletní selhání extrakce pro PDF '{pdf_path.name}': {e}", exc_info=True)
        return {}
