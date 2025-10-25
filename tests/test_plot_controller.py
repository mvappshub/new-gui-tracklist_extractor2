from __future__ import annotations

from typing import List, Tuple

import numpy as np
import pyqtgraph as pg
import pytest

from core.models.settings import ToleranceSettings
from ui.waveform.plot_controller import WaveformPlotController

pytestmark = pytest.mark.gui


def _make_plot(qtbot) -> pg.PlotWidget:
    w = pg.PlotWidget(axisItems={"bottom": pg.AxisItem(orientation="bottom")})
    qtbot.addWidget(w)
    return w


def test_construct_and_render_no_crash(qtbot):
    plot = _make_plot(qtbot)
    ctrl = WaveformPlotController(plot)
    # simple ramp
    audio = np.linspace(-1, 1, 1000, dtype=np.float32)
    ctrl.render_waveform(audio, sample_rate=1000, overview_points=200)
    # at least one data item present
    items = plot.listDataItems()
    assert len(items) >= 1


def test_set_pdf_markers_counts(qtbot):
    plot = _make_plot(qtbot)
    ctrl = WaveformPlotController(plot)
    pdf_tracks = [
        {"duration_sec": 0.5, "label": "Intro"},
        {"duration_sec": 1.0, "label": "Main"},
    ]
    wav_tracks = [
        {"duration_sec": 0.52},
        {"duration_sec": 1.05},
    ]
    ctrl.set_pdf_markers(pdf_tracks, wav_tracks, ToleranceSettings(warn_tolerance=2, fail_tolerance=5))
    assert len(ctrl.markers()) == 2
    assert len(ctrl.marker_times()) == 2


def test_region_change_emits(qtbot):
    plot = _make_plot(qtbot)
    ctrl = WaveformPlotController(plot)
    audio = np.sin(np.linspace(0, 2 * np.pi, 10_000, dtype=np.float32))
    events: List[Tuple[float, float]] = []
    ctrl.region_changed.connect(lambda a, b: events.append((a, b)))
    ctrl.setup_region_selection(
        duration_sec=5.0,
        initial_region=(0.0, 1.0),
        min_region_duration=0.3,
        snapping_enabled=True,
        audio=audio,
        sample_rate=1000,
        snap_tolerance=0.1,
    )
    # move region
    assert ctrl._region_item is not None  # type: ignore[attr-defined]
    ctrl._region_item.setRegion([0.5, 1.2])  # type: ignore[attr-defined]
    ctrl._on_region_changed(0.3, True, audio, 1000, 0.1)  # type: ignore[attr-defined]
    assert events, "region_changed should have been emitted"
    a, b = events[-1]
    assert b > a >= 0.0


def test_zoom_functions_adjust_view(qtbot):
    plot = _make_plot(qtbot)
    ctrl = WaveformPlotController(plot)
    ctrl.setup_region_selection( duration_sec=5.0, initial_region=(0.0, 1.0), min_region_duration=0.3, snapping_enabled=False )
    initial_range = plot.viewRange()[0]
    ctrl.zoom_in(min_region_duration=0.3)
    after_zoom_in = plot.viewRange()[0]
    # width decreased or clamped
    assert (after_zoom_in[1] - after_zoom_in[0]) <= (initial_range[1] - initial_range[0])
    ctrl.zoom_out()
    after_zoom_out = plot.viewRange()[0]
    assert (after_zoom_out[1] - after_zoom_out[0]) >= (after_zoom_in[1] - after_zoom_in[0])
    ctrl.fit_all()
    fit_all_range = plot.viewRange()[0]
    assert pytest.approx(fit_all_range[0], rel=1e-3) == 0.0


def test_clear_pdf_markers_idempotent(qtbot):
    plot = _make_plot(qtbot)
    ctrl = WaveformPlotController(plot)
    ctrl.clear_pdf_markers()
    ctrl.clear_pdf_markers()  # should not raise
    assert ctrl.markers() == []
    assert ctrl.marker_times() == []
