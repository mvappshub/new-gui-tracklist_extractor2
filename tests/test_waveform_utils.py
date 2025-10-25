from __future__ import annotations

import numpy as np
import pytest

from ui.waveform import utils


def test_format_mmss_basic():
    assert utils.format_mmss(0.0) == "00:00"
    assert utils.format_mmss(59.6) == "01:00"  # rounding up


def test_format_mmss_with_fraction_rollover():
    assert utils.format_mmss_with_fraction(59.999) == "01:00.0"
    assert utils.format_mmss_with_fraction(0.0) == "00:00.0"


def test_create_envelope_empty():
    out = utils.create_envelope(np.array([]), sample_rate=44100, max_points=2000)
    assert out.size == 0


def test_create_envelope_short_signal():
    data = np.zeros(10, dtype=np.float32)
    out = utils.create_envelope(data, 1000, max_points=100)
    assert out.shape[1] == 2
    assert out.shape[0] >= 2


def test_create_envelope_large_values():
    data = np.linspace(-1e3, 1e3, 10_000, dtype=np.float32)
    out = utils.create_envelope(data, 10_000, max_points=500)
    assert out.shape[1] == 2
    assert out.shape[0] > 0


def test_time_axis_item_tick_strings():
    axis = utils.TimeAxisItem(orientation="bottom")
    labels = axis.tickStrings([0.0, 30.0, 60.0], scale=1.0, spacing=1.0)
    assert labels == ["00:00", "00:30", "01:00"]
