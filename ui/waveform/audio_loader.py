from __future__ import annotations

import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Tuple

import numpy as np
import soundfile as sf


class AudioLoader:
    """Component responsible for extracting WAV from ZIP and loading audio data."""

    def __init__(self, zip_path: Path, wav_filename: str):
        self._zip_path = Path(zip_path)
        self._wav_filename = wav_filename

    def extract_wav(self) -> Path:
        """Extract WAV file from ZIP archive to a temporary file.

        Returns:
            Path to a temporary WAV file.

        Raises:
            FileNotFoundError: If ZIP archive or WAV entry is missing.
            RuntimeError: If extraction fails due to ZIP corruption or IO errors.
        """
        if not self._zip_path.exists():
            raise FileNotFoundError(f"ZIP archive not found: {self._zip_path}")

        try:
            with zipfile.ZipFile(self._zip_path, "r") as zf:
                matching_entry: str | None = None
                for member in zf.namelist():
                    if member == self._wav_filename or member.endswith(f"/{self._wav_filename}"):
                        matching_entry = member
                        break

                if not matching_entry:
                    raise FileNotFoundError(f"WAV file '{self._wav_filename}' not found in archive")

                with zf.open(matching_entry) as wav_file:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                        shutil.copyfileobj(wav_file, temp_file)
                        return Path(temp_file.name)
        except zipfile.BadZipFile as exc:
            raise RuntimeError(f"Invalid ZIP archive: {self._zip_path}") from exc
        except OSError as exc:
            raise RuntimeError(f"Failed to extract WAV: {exc}") from exc

    def load_audio_data(self, wav_path: Path) -> Tuple[np.ndarray, int, float]:
        """Load audio data from a WAV file and return mono waveform, sample rate and duration.

        Args:
            wav_path: Path to a WAV file to read.

        Returns:
            Tuple of (mono_float32_audio, sample_rate, duration_seconds)

        Raises:
            ValueError: If audio data is invalid.
            RuntimeError: If reading fails.
        """
        try:
            data, sample_rate = sf.read(str(wav_path), dtype="float32")
        except Exception as exc:  # soundfile may raise RuntimeError or others
            raise RuntimeError(f"Failed to read WAV file: {wav_path}") from exc

        if data.ndim > 1:
            data = data.mean(axis=1)

        if sample_rate <= 0 or data.size == 0:
            raise ValueError("Invalid audio data encountered")

        duration_sec = float(data.shape[0]) / float(sample_rate)
        return data, int(sample_rate), duration_sec
