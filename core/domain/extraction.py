from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

from audio_utils import get_wav_duration
from core.models.analysis import WavInfo


def extract_wav_durations_sf(zip_path: Path) -> list[WavInfo]:
    """Robust WAV duration extraction using soundfile via temp files.

    Reads WAVs from a ZIP archive, writes each to a temporary file, probes
    duration via `soundfile`, and returns a list of WavInfo entries.
    """
    wav_infos: list[WavInfo] = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            names = [n for n in zf.namelist() if n.lower().endswith(".wav")]
            if not names:
                return wav_infos

            with tempfile.TemporaryDirectory(prefix="wavprobe_") as tmpdir:
                tmpdir_path = Path(tmpdir)
                for name in names:
                    try:
                        base = Path(name).name
                        dest = tmpdir_path / base
                        with zf.open(name) as src, dest.open("wb") as dst:
                            shutil.copyfileobj(src, dst)
                        duration = get_wav_duration(dest)
                        wav_infos.append(WavInfo(filename=base, duration_sec=duration))
                    except Exception as exc:  # noqa: BLE001
                        logging.warning(
                            "Nelze přečíst hlavičku WAV '%s' v archivu '%s': %s",
                            name,
                            zip_path.name,
                            exc,
                        )
    except Exception as exc:  # noqa: BLE001
        logging.error("Nelze otevřít ZIP archiv '%s': %s", zip_path.name, exc)
    return wav_infos


