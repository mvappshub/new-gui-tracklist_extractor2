from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path

from audio_utils import get_wav_duration
from core.models.analysis import WavInfo


class ZipWavFileReader:
    """Adapter that encapsulates ZIP file handling and WAV duration probing for the extraction pipeline.

    Responsibilities:
    - Enumerate WAV members within a ZIP archive
    - Materialize entries into a temporary directory for duration inspection
    - Delegate duration probing to `audio_utils.get_wav_duration`
    - Surface results as `WavInfo` domain objects while containing all file I/O concerns
    """

    def read_wav_files(self, zip_path: Path) -> list[WavInfo]:
        """Extract WAV files from the provided ZIP archive and return their durations."""
        wav_infos: list[WavInfo] = []
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                names = [name for name in zf.namelist() if name.lower().endswith(".wav")]
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
