from __future__ import annotations

from typing import List

import numpy as np
import pyqtgraph as pg

# Waveform display configuration defaults (duplicated constants kept local to utils)
DEFAULT_OVERVIEW_POINTS = 2000
RMS_WINDOW_SIZE = 0.1


class TimeAxisItem(pg.AxisItem):
    """Axis item that formats ticks as MM:SS."""

    def tickStrings(self, values, scale, spacing):  # type: ignore[override]
        labels: List[str] = []
        for value in values:
            total_seconds = max(0.0, float(value))
            minutes = int(total_seconds // 60)
            seconds = int(round(total_seconds - minutes * 60))
            if seconds == 60:
                minutes += 1
                seconds = 0
            labels.append(f"{minutes:02d}:{seconds:02d}")
        return labels


def format_mmss(seconds: float) -> str:
    total = max(0.0, float(seconds))
    minutes = int(total // 60)
    secs = int(round(total - minutes * 60))
    if secs == 60:
        minutes += 1
        secs = 0
    return f"{minutes:02d}:{secs:02d}"


def format_mmss_with_fraction(seconds: float) -> str:
    total = max(0.0, float(seconds))
    minutes = int(total // 60)
    secs = total - minutes * 60
    if secs >= 59.95:
        minutes += 1
        secs = 0.0
    return f"{minutes:02d}:{secs:04.1f}".replace(" ", "0")


def create_envelope(
    data: np.ndarray,
    sample_rate: int,
    max_points: int = DEFAULT_OVERVIEW_POINTS,
) -> np.ndarray:
    """Create envelope from audio data for efficient display.

    Mirrors the behavior in waveform_viewer.WaveformEditorDialog._create_envelope.
    """
    if data.size == 0:
        return np.array([])

    duration = len(data) / sample_rate
    points_per_second = max_points / duration if duration > 0 else max_points

    if points_per_second >= sample_rate / 2:
        time_points = np.arange(len(data)) / sample_rate
        return np.column_stack([time_points, data])

    window_size = max(1, int(sample_rate / points_per_second))

    pad_size = (window_size - len(data) % window_size) % window_size
    if pad_size > 0:
        padded_data = np.pad(data, (0, pad_size), mode="edge")
    else:
        padded_data = data

    reshaped = padded_data.reshape(-1, window_size)
    mins = reshaped.min(axis=1)
    maxs = reshaped.max(axis=1)

    time_points = (np.arange(len(mins)) * window_size + window_size // 2) / sample_rate

    envelope_data = np.empty((len(time_points) * 2, 2))
    envelope_data[0::2, 0] = time_points
    envelope_data[1::2, 0] = time_points
    envelope_data[0::2, 1] = mins
    envelope_data[1::2, 1] = maxs

    return envelope_data
