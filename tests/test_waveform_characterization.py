from __future__ import annotations

from pathlib import Path
import numpy as np
import pytest

import waveform_viewer
from waveform_viewer import WaveformEditorDialog

pytestmark = pytest.mark.gui


def test_time_formatting_characterization():
    # Stable formatting contracts to guard refactor
    assert WaveformEditorDialog._format_mmss(0.0) == "00:00"
    assert WaveformEditorDialog._format_mmss(59.6) == "01:00"  # rounding up edge
    assert WaveformEditorDialog._format_mmss_with_fraction(0.0) == "00:00.0"
    assert WaveformEditorDialog._format_time(0.0) == "00:00.0"


def test_envelope_characterization(qapp, mock_wav_zip, qtbot, waveform_settings):
    zip_path, wav_name = mock_wav_zip
    dlg = WaveformEditorDialog(zip_path, wav_name, waveform_settings)
    qtbot.addWidget(dlg)
    try:
        # Envelope data length correlates with overview points
        x, y = dlg._waveform_curve.getData()
        assert len(x) == len(y) and len(x) > 0
        assert dlg._overview_points >= 1
    finally:
        dlg.close()
