#!/usr/bin/env python3
# wav_extractor_wave.py
# Jediný režim: python wav_extractor_wave.py "C:\cesta\k\masters"
# - projde ZIPy rekurzivně
# - spočítá délky WAV
# - side/position: strict -> AI (pokud je k dispozici) -> deterministický fallback
# - normalizace pozic (žádné 0/None, žádné duplicity)
# - uloží JSONy po stranách do ./output/

import json
import os
import re
import sys
import wave
import zipfile
from dataclasses import dataclass
from io import BufferedReader
from pathlib import Path
from typing import Optional, List, Dict, Tuple

# --------------------------- Datový model ---------------------------


@dataclass
class WavInfo:
    filename: str
    duration_sec: float
    side: Optional[str] = None
    position: Optional[int] = None


# ---------------------- WAV načtení a délky ------------------------


def _read_wav_duration(fileobj) -> float:
    with BufferedReader(fileobj) as buf:
        with wave.open(buf, "rb") as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return 0.0 if rate <= 0 else frames / float(rate)


def extract_wav_durations(zip_path: Path) -> List[WavInfo]:
    wavs: List[WavInfo] = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if not name.lower().endswith(".wav"):
                    continue
                base = Path(name).name
                try:
                    with zf.open(name, "r") as f:
                        dur = _read_wav_duration(f)
                    wavs.append(WavInfo(filename=base, duration_sec=dur))
                except Exception as e:
                    print(f"[WARN] WAV chyba '{name}' v '{zip_path}': {e}", file=sys.stderr)
    except Exception as e:
        print(f"[ERROR] ZIP chyba '{zip_path}': {e}", file=sys.stderr)
    return wavs


# -------------- Strict detekce side/position z názvu ---------------


def strict_from_path(s: str) -> Tuple[Optional[str], Optional[int]]:
    name = Path(s).stem

    # side: "Side_A", "Side-AA"
    m_side = re.search(r"(?i)side[^A-Za-z0-9]*([A-Za-z]+)", name)
    side = m_side.group(1).upper() if m_side else None

    # pos: prefix číslo "01_Track"
    m_pos = re.match(r"^0*([1-9][0-9]?)\b", name)
    pos = int(m_pos.group(1)) if m_pos else None

    # "A1", "AA02"
    if side is None:
        m_pref = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)\b", name)
        if m_pref:
            side = m_pref.group(1).upper()
            if pos is None:
                pos = int(m_pref.group(2))

    # "Side_A_01", "SideA_02", "Side_A01"
    if pos is None and side:
        m_pos2 = re.search(rf"(?i)side[^A-Za-z0-9]*{re.escape(side)}[^0-9]*0*([1-9][0-9]?)", name)
        if m_pos2:
            pos = int(m_pos2.group(1))

    return side, pos


# ------------------------- AI fallback (pokud je) -------------------


def _load_ai_client():
    try:
        from openai import OpenAI
    except Exception:
        return None, None
    # OpenRouter má přednost; když není, zkus OpenAI
    if os.getenv("OPENROUTER_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
            model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
            return client, model
        except Exception:
            pass
    if os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            return client, model
        except Exception:
            pass
    return None, None


def ai_parse_batch(filenames: List[str]) -> Dict[str, Tuple[Optional[str], Optional[int]]]:
    client, model = _load_ai_client()
    if not client or not model or not filenames:
        return {}
    system = (
        "You extract metadata from WAV filenames. "
        "For each filename, infer 'side' (letters only, like A,B,AA) and 'position' (1..99). "
        'Return STRICT JSON object mapping filename -> {"side": str|null, "position": int|null}. No extra text.'
    )
    user = {"filenames": filenames}
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            cleaned = content.strip().strip("`").replace("json\n", "").strip()
            data = json.loads(cleaned)
        out: Dict[str, Tuple[Optional[str], Optional[int]]] = {}
        for fn in filenames:
            rec = data.get(fn, {})
            s_raw = rec.get("side")
            p_raw = rec.get("position")
            side = s_raw.strip().upper() if isinstance(s_raw, str) and s_raw.strip() else None
            pos = int(p_raw) if isinstance(p_raw, int) else None
            out[fn] = (side, pos)
        return out
    except Exception as e:
        print(f"[WARN] AI fallback selhal: {e}", file=sys.stderr)
        return {}


def merge_ai_results(wavs: List[WavInfo], ai_map: Dict[str, Tuple[Optional[str], Optional[int]]]) -> None:
    if not ai_map:
        return
    for w in wavs:
        if w.filename in ai_map:
            s_ai, p_ai = ai_map[w.filename]
            if (w.side is None or w.side == "UNKNOWN") and s_ai:
                w.side = s_ai
            if w.position is None and p_ai is not None:
                w.position = p_ai


# ----------------------- Fallback a mapování stran ------------------


def _fallback_assign_when_all_unknown(wavs: List[WavInfo]) -> None:
    if not wavs:
        return
    if any(w.side and w.side != "UNKNOWN" for w in wavs):
        return
    wavs.sort(key=lambda x: x.filename.lower())
    n = len(wavs)
    if n == 1:
        wavs[0].side = "A"
        wavs[0].position = wavs[0].position or 1
        return
    if n == 2:
        wavs[0].side = "A"
        wavs[0].position = wavs[0].position or 1
        wavs[1].side = "B"
        wavs[1].position = wavs[1].position or 1
        return
    for i, w in enumerate(wavs, start=1):
        w.side = "A"
        if w.position is None:
            w.position = i


def detect_audio_mode_with_ai(wavs: List[WavInfo]) -> Dict[str, List[WavInfo]]:
    if not wavs:
        return {}
    # strict
    for w in wavs:
        s, p = strict_from_path(w.filename)
        w.side = s or "UNKNOWN"
        w.position = p
    # AI fallback (jen když něco chybí)
    if any((w.side == "UNKNOWN" or w.position is None) for w in wavs):
        names = [w.filename for w in wavs]
        ai_map = ai_parse_batch(names)
        merge_ai_results(wavs, ai_map)
    # finální fallback
    _fallback_assign_when_all_unknown(wavs)
    # side map + předběžné seřazení
    side_map: Dict[str, List[WavInfo]] = {}
    for w in wavs:
        side_map.setdefault(w.side, []).append(w)
    for items in side_map.values():
        items.sort(key=lambda x: (999 if x.position is None else x.position, x.filename.lower()))
    return side_map


# -------------------- Normalizace pozic (KONEČNĚ) -------------------


def _renumber_sequential(items: List[WavInfo]) -> None:
    items.sort(key=lambda x: (x.position is None, x.filename.lower()))
    for i, w in enumerate(items, start=1):
        w.position = i


def normalize_positions(side_map: Dict[str, List[WavInfo]]) -> None:
    for items in side_map.values():
        if not items:
            continue
        missing = any((w.position is None) or (not isinstance(w.position, int)) or (w.position <= 0) for w in items)
        seen = set()
        dup = False
        for w in items:
            if isinstance(w.position, int) and w.position > 0:
                if w.position in seen:
                    dup = True
                    break
                seen.add(w.position)
        if missing or dup:
            _renumber_sequential(items)
        else:
            items.sort(key=lambda x: (x.position, x.filename.lower()))


# -------------------------- Export / JSON ---------------------------


def _format_mmss(seconds: float) -> str:
    t = int(seconds)
    return f"{t // 60:02d}:{t % 60:02d}"


def build_payload(zip_path: Path, side_map: Dict[str, List[WavInfo]]) -> List[dict]:
    album = zip_path.stem
    out: List[dict] = []
    for side, wavs in side_map.items():
        if not wavs:
            continue
        block = {"source_type": "wav", "path_id": f"{album}_Side_{side}", "album": album, "side": side, "tracks": []}
        for w in wavs:
            block["tracks"].append(
                {
                    "filename": w.filename,
                    "side": w.side,
                    "position": int(w.position) if isinstance(w.position, int) and w.position > 0 else 1,
                    "duration_seconds": round(w.duration_sec, 3),
                    "duration_formatted": _format_mmss(w.duration_sec),
                }
            )
        out.append(block)
    return out


def save_json_outputs(blocks: List[dict], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    for b in blocks:
        out_path = out_dir / f"{b['album']}_Side_{b['side']}.json"
        try:
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(b, f, ensure_ascii=False, indent=2)
            print(f"[OK] {out_path}")
        except Exception as e:
            print(f"[ERROR] Nelze uložit {out_path}: {e}", file=sys.stderr)


# ------------------------------- Main -------------------------------


def main():
    if len(sys.argv) != 2:
        print('Použití: python wav_extractor_wave.py "C:\\cesta\\k\\masters"', file=sys.stderr)
        sys.exit(2)

    root_dir = Path(sys.argv[1])
    if not root_dir.exists():
        print(f"[ERROR] Složka neexistuje: {root_dir}", file=sys.stderr)
        sys.exit(2)

    all_blocks: List[dict] = []
    for zp in root_dir.rglob("*.zip"):
        wavs = extract_wav_durations(zp)
        side_map = detect_audio_mode_with_ai(wavs)
        normalize_positions(side_map)
        blocks = build_payload(zp, side_map)
        all_blocks.extend(blocks)

    save_json_outputs(all_blocks, Path("output"))


if __name__ == "__main__":
    main()
