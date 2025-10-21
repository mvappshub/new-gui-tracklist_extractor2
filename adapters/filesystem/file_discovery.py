from __future__ import annotations

import logging
import re
from pathlib import Path

from config import cfg

ID_PATTERN = re.compile(r"\d+")


def extract_numeric_id(filename: str) -> list[int]:
    """Extract filtered numeric IDs from filename based on configuration."""
    matches = ID_PATTERN.findall(filename)
    if not matches:
        return []

    try:
        min_digits = int(cfg.analysis_min_id_digits.value)
    except (TypeError, ValueError):
        min_digits = 1
    try:
        max_digits = int(cfg.analysis_max_id_digits.value)
    except (TypeError, ValueError):
        max_digits = min_digits

    if min_digits > max_digits:
        min_digits, max_digits = max_digits, min_digits

    ignore_raw = cfg.analysis_ignore_numbers.value or []
    ignore_values = set()
    for item in ignore_raw:
        if item is None:
            continue
        value = str(item).strip()
        if not value:
            continue
        ignore_values.add(value)
        if value.isdigit():
            ignore_values.add(str(int(value)))

    filtered_ids: set[int] = set()
    for match in matches:
        if not match.isdigit():
            continue
        if not (min_digits <= len(match) <= max_digits):
            continue
        normalized = str(int(match))
        if match in ignore_values or normalized in ignore_values:
            continue
        filtered_ids.add(int(match))

    return sorted(filtered_ids)


def discover_and_pair_files(pdf_dir: Path, wav_dir: Path) -> tuple[dict[str, dict[str, Path]], int]:
    logging.info(f"Skenuji PDF v: {pdf_dir}")
    pdf_map: dict[int, list[Path]] = {}
    for p in pdf_dir.rglob("*.pdf"):
        ids = extract_numeric_id(p.name)
        if not ids:
            continue
        for id_val in ids:
            pdf_map.setdefault(id_val, []).append(p)

    logging.info(f"Skenuji ZIP v: {wav_dir}")
    zip_map: dict[int, list[Path]] = {}
    for p in wav_dir.rglob("*.zip"):
        ids = extract_numeric_id(p.name)
        if not ids:
            continue
        for id_val in ids:
            zip_map.setdefault(id_val, []).append(p)

    pairs: dict[str, dict[str, Path]] = {}
    skipped_count = 0
    seen_pairs: set[tuple[Path, Path]] = set()

    for id_val in sorted(set(pdf_map.keys()) & set(zip_map.keys())):
        pdf_files = pdf_map[id_val]
        zip_files = zip_map[id_val]

        if len(pdf_files) == 1 and len(zip_files) == 1:
            pair_key = (pdf_files[0], zip_files[0])
            if pair_key in seen_pairs:
                logging.debug(
                    f"Skipping duplicate pair for ID {id_val}: {pdf_files[0].name} & {zip_files[0].name}"
                )
                continue
            pairs[str(id_val)] = {"pdf": pdf_files[0], "zip": zip_files[0]}
            seen_pairs.add(pair_key)
        else:
            logging.warning(
                f"Ambiguous pairing for ID {id_val}: {len(pdf_files)} PDF(s), {len(zip_files)} ZIP(s)"
            )
            skipped_count += 1
    return pairs, skipped_count
