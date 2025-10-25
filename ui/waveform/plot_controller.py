from __future__ import annotations

from typing import List, Tuple, Dict, Optional

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QObject, pyqtSignal

from core.models.settings import ToleranceSettings
from ui.waveform.utils import (
    TimeAxisItem,
    create_envelope,
    format_mmss,
    format_mmss_with_fraction,
)


class WaveformPlotController(QObject):
    """Controller for waveform plotting, region selection, markers and navigation.

    UI-only logic. No business/domain logic here.
    """

    region_changed = pyqtSignal(float, float)
    marker_clicked = pyqtSignal(int, float)

    def __init__(self, plot_widget: pg.PlotWidget):
        super().__init__(plot_widget)
        self.plot_widget = plot_widget
        self._waveform_curve: Optional[pg.PlotDataItem] = None
        self._region_item: Optional[pg.LinearRegionItem] = None
        self._duration_sec: float = 0.0
        self._pdf_markers: List[pg.InfiniteLine] = []
        self._marker_times: List[float] = []

    # ------------ Rendering ------------
    def render_waveform(self, audio: np.ndarray, sample_rate: int, overview_points: int) -> None:
        if self.plot_widget is None or audio is None:
            return
        env = create_envelope(audio, sample_rate, max_points=max(1, int(overview_points)))
        if env.size == 0:
            return
        if self._waveform_curve is None:
            self._waveform_curve = self.plot_widget.plot(pen=pg.mkPen("#3B82F6", width=1))
        self._waveform_curve.setData(env[:, 0], env[:, 1])

    # ------------ Region Selection ------------
    def setup_region_selection(
        self,
        duration_sec: float,
        initial_region: Tuple[float, float] = (0.0, 1.0),
        min_region_duration: float = 0.3,
        snapping_enabled: bool = True,
        audio: Optional[np.ndarray] = None,
        sample_rate: int = 0,
        snap_tolerance: float = 0.1,
    ) -> None:
        self._duration_sec = max(0.0, float(duration_sec))
        if not self.plot_widget:
            return

        # region item
        self._region_item = pg.LinearRegionItem(values=list(initial_region), bounds=[0.0, self._duration_sec])
        self._region_item.setBrush(pg.mkBrush("#3B82F640"))
        self._region_item.setMovable(True)
        self._region_item.sigRegionChanged.connect(
            lambda: self._on_region_changed(min_region_duration, snapping_enabled, audio, sample_rate, snap_tolerance)
        )
        self.plot_widget.addItem(self._region_item)
        self._apply_view_limits(min_region_duration)

        # Initialize
        self._on_region_changed(min_region_duration, snapping_enabled, audio, sample_rate, snap_tolerance)

    def _apply_view_limits(self, min_region_duration: float) -> None:
        if not self.plot_widget:
            return
        max_range = float(self._duration_sec) if self._duration_sec > 0 else 1.0
        min_range = min(max_range, max(0.5, float(min_region_duration)))
        self.plot_widget.setLimits(xMin=0.0, xMax=max_range, minXRange=min_range, maxXRange=max_range)
        vb = self.plot_widget.getViewBox()
        if vb is not None:
            vb.setXRange(0.0, max_range, padding=0)

    def _on_region_changed(
        self,
        min_region: float,
        snapping_enabled: bool,
        audio: Optional[np.ndarray],
        sample_rate: int,
        snap_tolerance: float,
    ) -> None:
        if not self._region_item:
            return
        min_val, max_val = self._region_item.getRegion()
        if snapping_enabled:
            snapped_min, snapped_max = self._snap_region_to_audio(min_val, max_val, audio, sample_rate, snap_tolerance)
        else:
            snapped_min, snapped_max = min_val, max_val

        # Enforce minimum size
        if snapped_max - snapped_min < min_region:
            if min_val == snapped_min:
                snapped_max = snapped_min + min_region
            else:
                snapped_min = snapped_max - min_region

        snapped_min = max(0.0, snapped_min)
        snapped_max = min(self._duration_sec, snapped_max)

        if abs(min_val - snapped_min) > 0.01 or abs(max_val - snapped_max) > 0.01:
            self._region_item.setRegion([snapped_min, snapped_max])

        self.region_changed.emit(snapped_min, snapped_max)

    def _snap_region_to_audio(
        self,
        min_val: float,
        max_val: float,
        audio: Optional[np.ndarray],
        sample_rate: int,
        tolerance: float,
    ) -> Tuple[float, float]:
        if audio is None or audio.size == 0 or sample_rate <= 0:
            return (min_val, max_val)
        search_start = max(0.0, min_val - tolerance)
        search_end = min(self._duration_sec, max_val + tolerance)
        peaks = self._find_rms_peaks(audio, sample_rate, search_start, search_end)
        zeros = self._find_zero_crossings(audio, sample_rate, search_start, search_end)
        snap_points = sorted(set(peaks + zeros))
        snapped_min = min_val
        if snap_points:
            candidates = [p for p in snap_points if abs(p - min_val) <= tolerance]
            if candidates:
                snapped_min = min(candidates, key=lambda p: abs(p - min_val))
        snapped_max = max_val
        if snap_points:
            candidates = [p for p in snap_points if abs(p - max_val) <= tolerance]
            if candidates:
                snapped_max = min(candidates, key=lambda p: abs(p - max_val))
        return (snapped_min, snapped_max)

    def _find_rms_peaks(
        self, audio: np.ndarray, sample_rate: int, start_time: float, end_time: float
    ) -> List[float]:
        peaks: List[float] = []
        sr = sample_rate
        window_size = max(1, int(0.1 * sr))
        half_step = max(1, window_size // 2)
        start = max(0, int(start_time * sr))
        end = min(len(audio), int(end_time * sr))
        if end - start <= window_size:
            return peaks
        local_rms: List[Tuple[float, int]] = []
        for offset in range(start, end - window_size, half_step):
            window = audio[offset : offset + window_size]
            rms = float(np.sqrt(np.mean(window**2)))
            local_rms.append((rms, offset + window_size // 2))
        for i in range(1, len(local_rms) - 1):
            prev_r, _ = local_rms[i - 1]
            cur_r, idx = local_rms[i]
            next_r, _ = local_rms[i + 1]
            if cur_r > prev_r and cur_r > next_r:
                peaks.append(idx / sr)
        return peaks

    def _find_zero_crossings(
        self, audio: np.ndarray, sample_rate: int, start_time: float, end_time: float
    ) -> List[float]:
        crossings: List[float] = []
        sr = sample_rate
        start = max(1, int(start_time * sr))
        end = min(len(audio), int(end_time * sr))
        for i in range(start, end):
            if audio[i - 1] * audio[i] < 0:
                crossings.append(i / sr)
        return crossings

    # ------------ PDF Markers ------------
    def set_pdf_markers(
        self,
        pdf_tracks: List[Dict],
        wav_tracks: List[Dict],
        tolerance_settings: ToleranceSettings,
    ) -> None:
        self.clear_pdf_markers()
        if not pdf_tracks or not self.plot_widget:
            return
        import numpy as np

        tol_warn = float(tolerance_settings.warn_tolerance)
        tol_fail = float(tolerance_settings.fail_tolerance)

        pdf_durations: List[float] = []
        pdf_labels: List[str] = []
        for idx, pdf_track in enumerate(pdf_tracks, start=1):
            if hasattr(pdf_track, "duration_sec"):
                duration = float(getattr(pdf_track, "duration_sec", 0.0))
                label = getattr(pdf_track, "label", f"PDF {idx}")
            else:
                duration = float(pdf_track.get("duration_sec", 0.0))
                label = str(pdf_track.get("label", f"PDF {idx}"))
            pdf_durations.append(max(0.0, duration))
            pdf_labels.append(label)
        if not pdf_durations:
            return
        pdf_end_times = np.cumsum(pdf_durations)

        wav_durations: List[float] = []
        for wav_track in wav_tracks:
            if hasattr(wav_track, "duration_sec"):
                wav_durations.append(max(0.0, float(getattr(wav_track, "duration_sec", 0.0))))
            else:
                wav_durations.append(max(0.0, float(wav_track.get("duration_sec", 0.0))))
        wav_end_times = np.cumsum(wav_durations) if wav_durations else []

        for i, end_time in enumerate(pdf_end_times):
            delta_t = 0.0
            if i < len(wav_end_times):
                delta_t = wav_end_times[i] - end_time
            if abs(delta_t) <= tol_warn:
                color = "#10B981"
            elif abs(delta_t) <= tol_fail:
                color = "#F59E0B"
            else:
                color = "#EF4444"
            marker = pg.InfiniteLine(pos=end_time, angle=90, pen=pg.mkPen(color, width=2, style=pg.QtCore.Qt.PenStyle.DashLine), movable=False)
            marker.setToolTip(
                f"{pdf_labels[i]} - {format_mmss(end_time)} (delta {self._format_delta(delta_t)})"
            )
            marker.setZValue(2)
            self.plot_widget.addItem(marker)
            self._pdf_markers.append(marker)
            self._marker_times.append(end_time)

    def clear_pdf_markers(self) -> None:
        if self.plot_widget:
            for m in self._pdf_markers:
                try:
                    self.plot_widget.removeItem(m)
                except Exception:
                    pass
        self._pdf_markers.clear()
        self._marker_times.clear()

    def _format_delta(self, delta_seconds: float) -> str:
        return f"{float(delta_seconds):+0.1f} s"

    def click_marker(self, index: int) -> None:
        """Testing/helper method to simulate marker click and emit marker_clicked.

        In GUI, this would be wired via scene events; for tests we expose a direct trigger.
        """
        if 0 <= index < len(self._marker_times):
            self.marker_clicked.emit(index, float(self._marker_times[index]))

    # ------------ Navigation / Zoom ------------
    def zoom_in(self, min_region_duration: float) -> None:
        if not self.plot_widget or self._duration_sec <= 0:
            return
        view_min, view_max = self.plot_widget.viewRange()[0]
        current_width = max(0.0, view_max - view_min)
        if current_width <= 0:
            return
        min_range = min(float(self._duration_sec), max(0.5, float(min_region_duration)))
        new_width = max(current_width * 0.5, min_range)
        center = (view_min + view_max) / 2.0
        half_width = new_width / 2.0
        new_min = max(0.0, center - half_width)
        new_max = min(float(self._duration_sec), center + half_width)
        if new_max - new_min < min_range:
            new_max = min(float(self._duration_sec), new_min + new_width)
        self.plot_widget.setXRange(new_min, new_max, padding=0)

    def zoom_out(self) -> None:
        if not self.plot_widget or self._duration_sec <= 0:
            return
        view_min, view_max = self.plot_widget.viewRange()[0]
        current_width = max(0.0, view_max - view_min)
        if current_width <= 0:
            return
        max_range = float(self._duration_sec)
        new_width = min(current_width * 2.0, max_range)
        center = (view_min + view_max) / 2.0
        half_width = new_width / 2.0
        new_min = max(0.0, center - half_width)
        new_max = min(max_range, center + half_width)
        if new_max - new_min < new_width:
            new_max = min(max_range, new_min + new_width)
        self.plot_widget.setXRange(new_min, new_max, padding=0)

    def fit_all(self) -> None:
        if not self.plot_widget or self._duration_sec <= 0:
            return
        self.plot_widget.setXRange(0.0, float(self._duration_sec), padding=0)

    # ------------ Introspection ------------
    def marker_times(self) -> List[float]:
        return list(self._marker_times)

    def markers(self) -> List[pg.InfiniteLine]:
        return list(self._pdf_markers)
