from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import cast

from config import cfg
from core.models.analysis import SideResult, TrackInfo, WavInfo
from wav_extractor_wave import detect_audio_mode_with_ai, normalize_positions

DetectFn = Callable[[list[WavInfo]], dict[str, list[WavInfo]]]
NormalizeFn = Callable[[dict[str, list[WavInfo]]], None]
_detect: DetectFn = cast(DetectFn, detect_audio_mode_with_ai)
_normalize: NormalizeFn = cast(NormalizeFn, normalize_positions)

def detect_audio_mode(wavs: list[WavInfo]) -> tuple[dict[str, str], dict[str, list[WavInfo]]]:
    """
    Vylepšená detekce stran/pořadí:
    strict z názvu → AI fallback (je-li k dispozici) → deterministické fallback,
    poté normalizace pořadí per strana.
    """
    # Pydantic WavInfo má stejné atributy jako dataclass v extraktoru,
    # takže to funguje přímo ("duck-typing").
    side_map = _detect(wavs)
    _normalize(side_map)
    # Phase 1 verification: compare_data consumes SideResult data as Pydantic models without dict conversions.

    modes: dict[str, str] = {
        side: ('side' if len(items) == 1 else 'tracks')
        for side, items in side_map.items()
    }
    return modes, side_map


def compare_data(
    pdf_data: dict[str, list[TrackInfo]],
    wav_data: list[WavInfo],
    pair_info: dict[str, Path],
) -> list[SideResult]:
    results: list[SideResult] = []
    modes, wavs_by_side = detect_audio_mode(wav_data)
    all_sides = set(pdf_data.keys()) | set(wavs_by_side.keys())

    tolerance_warn = cfg.analysis_tolerance_warn.value
    tolerance_fail = cfg.analysis_tolerance_fail.value

    for side in sorted(all_sides):
        pdf_tracks = pdf_data.get(side, [])
        wav_tracks = wavs_by_side.get(side, [])
        sorted_wav_tracks = sorted(
            wav_tracks,
            key=lambda track: track.position if track.position is not None else 99,
        )
        mode = modes.get(side, 'tracks')

        total_pdf_sec = sum(t.duration_sec for t in pdf_tracks)
        total_wav_sec = sum(w.duration_sec for w in wav_tracks)
        difference = round(total_wav_sec - total_pdf_sec)

        status = "OK"
        if abs(difference) > tolerance_fail:
            status = "FAIL"
        elif abs(difference) > tolerance_warn:
            status = "WARN"

        results.append(SideResult(
            seq=0,  # Will be assigned by TopTableModel.add_result()
            pdf_path=pair_info['pdf'],
            zip_path=pair_info['zip'],
            side=side,
            mode=mode,
            status=status,
            pdf_tracks=pdf_tracks,
            wav_tracks=sorted_wav_tracks,
            total_pdf_sec=total_pdf_sec,
            total_wav_sec=total_wav_sec,
            total_difference=difference
        ))
    return results
