from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel


class TrackInfo(BaseModel):
    title: str
    side: str
    position: int
    duration_sec: int


class WavInfo(BaseModel):
    filename: str
    duration_sec: float
    side: str | None = None
    position: int | None = None


class SideResult(BaseModel):
    seq: int
    pdf_path: Path
    zip_path: Path
    side: str
    mode: str
    status: str
    pdf_tracks: list[TrackInfo]
    wav_tracks: list[WavInfo]
    total_pdf_sec: int
    total_wav_sec: float
    total_difference: int

from dataclasses import dataclass


@dataclass
class FilePair:
    """Represents a paired PDF and ZIP file based on a shared numeric ID."""
    pdf: Path
    zip: Path
