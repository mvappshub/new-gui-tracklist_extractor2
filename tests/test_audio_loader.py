from __future__ import annotations

from pathlib import Path
from typing import Tuple

import numpy as np
import pytest
import soundfile as sf

from ui.waveform.audio_loader import AudioLoader


def test_extract_wav_success(mock_wav_zip: Tuple[Path, str]) -> None:
    zip_path, wav_name = mock_wav_zip
    loader = AudioLoader(zip_path, wav_name)
    out = loader.extract_wav()
    assert out.exists()
    # basic sanity: loaded file is a wav
    data, sr = sf.read(str(out), dtype="float32")
    assert data.size > 0 and sr > 0


def test_extract_wav_missing_zip(tmp_path: Path) -> None:
    zip_path = tmp_path / "missing.zip"
    loader = AudioLoader(zip_path, "track.wav")
    with pytest.raises(FileNotFoundError):
        loader.extract_wav()


def test_extract_wav_missing_entry(empty_zip: Path) -> None:
    loader = AudioLoader(empty_zip, "missing.wav")
    with pytest.raises(FileNotFoundError):
        loader.extract_wav()


def test_extract_wav_bad_zip(tmp_path: Path) -> None:
    bad_zip = tmp_path / "bad.zip"
    bad_zip.write_bytes(b"not-a-zip")
    loader = AudioLoader(bad_zip, "track.wav")
    with pytest.raises(RuntimeError):
        loader.extract_wav()


def test_load_audio_data_success(mock_wav_zip: Tuple[Path, str]) -> None:
    zip_path, wav_name = mock_wav_zip
    loader = AudioLoader(zip_path, wav_name)
    wav_path = loader.extract_wav()
    data, sr, duration = loader.load_audio_data(wav_path)
    assert isinstance(data, np.ndarray)
    assert sr > 0
    assert duration > 0


def test_load_audio_data_read_failure(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    wav_path = tmp_path / "dummy.wav"
    wav_path.write_bytes(b"fake")

    def fake_read(_: str, dtype: str = "float32"):
        raise RuntimeError("read error")

    monkeypatch.setattr(sf, "read", fake_read)
    loader = AudioLoader(tmp_path / "archive.zip", "dummy.wav")
    with pytest.raises(RuntimeError):
        loader.load_audio_data(wav_path)


def test_load_audio_data_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    wav_path = tmp_path / "dummy.wav"
    wav_path.write_bytes(b"fake")

    def fake_read(_: str, dtype: str = "float32"):
        return np.array([]), 44100

    monkeypatch.setattr(sf, "read", fake_read)
    loader = AudioLoader(tmp_path / "archive.zip", "dummy.wav")
    with pytest.raises(ValueError):
        loader.load_audio_data(wav_path)
