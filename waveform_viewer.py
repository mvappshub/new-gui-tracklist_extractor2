#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Waveform viewer dialog with audio playback controls."""

from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple, Dict

import numpy as np
import pyqtgraph as pg
import soundfile as sf
from PyQt6.QtCore import Qt, QUrl

try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

    _MULTIMEDIA_AVAILABLE = True
    _MULTIMEDIA_IMPORT_ERROR = None
except ImportError as exc:
    QAudioOutput = None  # type: ignore[assignment]
    QMediaPlayer = None  # type: ignore[assignment]
    _MULTIMEDIA_AVAILABLE = False
    _MULTIMEDIA_IMPORT_ERROR = exc
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from core.models.settings import ToleranceSettings
from ui.config_models import WaveformSettings
from ui.waveform.audio_loader import AudioLoader
from ui.waveform.utils import TimeAxisItem as UtilsTimeAxisItem, create_envelope, format_mmss, format_mmss_with_fraction
from ui.waveform.plot_controller import WaveformPlotController
from ui.waveform.playback_controller import PlaybackController

# Waveform display configuration defaults
DEFAULT_OVERVIEW_POINTS = 2000  # Maximum points for waveform envelope
MIN_REGION_DURATION = 0.3  # Minimum region duration in seconds
DEFAULT_SNAP_TOLERANCE = 0.1  # Default snap tolerance in seconds
RMS_WINDOW_SIZE = 0.1  # RMS calculation window in seconds
INITIAL_DETAIL_DURATION = 10.0  # Initial detail view duration in seconds


class TimeAxisItem(UtilsTimeAxisItem):
    pass


class WaveformEditorDialog(QDialog):
    """Advanced waveform editor with a single interactive waveform view for precise audio analysis."""

    def __init__(
        self,
        zip_path: Path,
        wav_filename: str,
        waveform_settings: WaveformSettings,
        parent=None,
    ):
        super().__init__(parent)
        self._zip_path = Path(zip_path)
        self._wav_filename = wav_filename
        self._temp_wav: Optional[Path] = None
        self._duration_sec: float = 0.0
        self._sample_rate: int = 0
        self._audio_data: Optional[np.ndarray] = None

        # Waveform plot and overlays
        self.plot_widget: Optional[pg.PlotWidget] = None

        # Mediator components
        self._audio_loader: Optional[AudioLoader] = None
        self._plot_controller: Optional[WaveformPlotController] = None
        self._playback_controller: Optional[PlaybackController] = None
        self._pdf_markers: List[pg.InfiniteLine] = []
        self._marker_times: List[float] = []
        self._pdf_tracks: List[Dict] = []  # Store PDF track data
        self._playhead_line: Optional[pg.InfiniteLine] = None

        # Compatibility shims for tests (populated after controller setup)
        self._region_item: Optional[pg.LinearRegionItem] = None
        self._waveform_curve: Optional[pg.PlotDataItem] = None
        self._region_bounds: Tuple[float, float] = (0.0, 1.0)

        # Inherit extraction method from parent class
        self._slider_updating = False

        # Waveform editor configuration
        self._waveform_settings = waveform_settings
        self._overview_points = max(1, waveform_settings.overview_points)
        self._min_region_duration = max(0.0, waveform_settings.min_region_duration)
        self._snap_tolerance = max(0.0, waveform_settings.snap_tolerance)
        self._snapping_enabled = waveform_settings.enable_snapping

        self.setWindowTitle(f"Waveform Editor - {wav_filename}")
        self.resize(1200, 800)

        if not _MULTIMEDIA_AVAILABLE:
            QMessageBox.critical(
                self,
                "Qt Multimedia Required",
                "Waveform playback requires the PyQt6 QtMultimedia module. "
                "Install PyQt6>=6.4 with Qt Multimedia support to enable this feature.",
            )
            raise RuntimeError("Qt Multimedia module not available") from _MULTIMEDIA_IMPORT_ERROR

        # Instantiate mediator components
        self._playback_controller = PlaybackController(self)

        self._init_ui()
        self._init_mediator()
        self._load_audio_data()

    def _init_ui(self) -> None:
        """Initialize editor layout with a single waveform plot and controls."""
        main_layout = QVBoxLayout(self)

        # Title
        name_label = QLabel(f"{self._wav_filename}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setObjectName("waveformEditorTitle")
        main_layout.addWidget(name_label)

        # Single waveform plot with custom time axis
        self.plot_widget = pg.PlotWidget(self, axisItems={"bottom": TimeAxisItem(orientation="bottom")})
        self.plot_widget.setBackground("k")
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.setLabel("left", "Amplitude")
        self.plot_widget.setMouseEnabled(x=True, y=False)
        view_box = self.plot_widget.getViewBox()
        if view_box is not None:
            view_box.setMouseEnabled(x=True, y=False)
        if self.plot_widget.scene() is not None:
            self.plot_widget.scene().sigMouseMoved.connect(self._on_plot_mouse_moved)
        self.plot_widget.setToolTip(self._format_mmss_with_fraction(0.0))
        main_layout.addWidget(self.plot_widget, stretch=1)

        # Controls
        controls_layout = QHBoxLayout()

        # Region info
        self.region_label = QLabel("Region: 00:00.0 - 00:01.0", self)
        controls_layout.addWidget(self.region_label)

        controls_layout.addStretch()

        # Zoom controls
        zoom_in_btn = QPushButton("Zoom In", self)
        zoom_out_btn = QPushButton("Zoom Out", self)
        fit_all_btn = QPushButton("Fit", self)
        fit_region_btn = QPushButton("Fit to Region", self)

        zoom_in_btn.clicked.connect(self._zoom_in)
        zoom_out_btn.clicked.connect(self._zoom_out)
        fit_all_btn.clicked.connect(self._fit_all)
        fit_region_btn.clicked.connect(self._fit_to_region)

        controls_layout.addWidget(zoom_in_btn)
        controls_layout.addWidget(zoom_out_btn)
        controls_layout.addWidget(fit_all_btn)
        controls_layout.addWidget(fit_region_btn)

        main_layout.addLayout(controls_layout)

        # Transport controls
        transport_layout = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        transport_layout.addWidget(self.play_button)
        transport_layout.addWidget(self.pause_button)
        transport_layout.addWidget(self.stop_button)
        transport_layout.addStretch()

        self.play_button.clicked.connect(lambda: self._playback_controller and self._playback_controller.play())
        self.pause_button.clicked.connect(lambda: self._playback_controller and self._playback_controller.pause())
        self.stop_button.clicked.connect(lambda: self._playback_controller and self._playback_controller.stop())

        main_layout.addLayout(transport_layout)

        # Position slider
        slider_layout = QHBoxLayout()
        self.time_current = QLabel("00:00.0", self)
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 0)
        self.time_total = QLabel("00:00.0", self)
        slider_layout.addWidget(self.time_current)
        slider_layout.addWidget(self.position_slider, stretch=1)
        slider_layout.addWidget(self.time_total)
        main_layout.addLayout(slider_layout)

        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        self.position_slider.sliderMoved.connect(self._on_slider_moved)

    def _load_audio_data(self) -> None:
        """Load and process audio data for the waveform view."""
        import time

        start_time = time.time()

        try:
            loader = AudioLoader(self._zip_path, self._wav_filename)
            # Extract WAV
            self._temp_wav = loader.extract_wav()
            if not self._temp_wav:
                raise FileNotFoundError("Temporary WAV file missing after extraction")

            # Load audio via AudioLoader
            load_start = time.time()
            data, sr, duration = loader.load_audio_data(self._temp_wav)
            load_duration = time.time() - load_start

            self._audio_data = data
            self._sample_rate = sr
            self._duration_sec = duration

            # Render waveform via controller
            if self._plot_controller and self.plot_widget is not None:
                self._plot_controller.render_waveform(self._audio_data, self._sample_rate, self._overview_points)
                # Populate compatibility shim for _waveform_curve
                self._waveform_curve = self._plot_controller.waveform_curve()

                self._plot_controller.setup_region_selection(
                    duration_sec=self._duration_sec,
                    initial_region=(0.0, min(1.0, self._duration_sec)),
                    min_region_duration=self._min_region_duration,
                    snapping_enabled=self._snapping_enabled,
                    audio=self._audio_data,
                    sample_rate=self._sample_rate,
                    snap_tolerance=self._snap_tolerance,
                )
                # Populate compatibility shim for _region_item
                self._region_item = self._plot_controller.region_item()

            # Setup player source
            if self._playback_controller is not None and self._temp_wav is not None:
                self._playback_controller.set_source_local_file(str(self._temp_wav))

            # Initialize slider range and labels based on known duration
            total_ms = int(self._duration_sec * 1000)
            self.position_slider.setRange(0, total_ms)
            self.time_total.setText(self._format_time(self._duration_sec))
            self.time_current.setText(self._format_time(0.0))
            if self._plot_controller:
                self._plot_controller.update_playhead(0.0)

            total_duration = time.time() - start_time
            logging.info(
                "Waveform editor loaded in %.2fs (audio load: %.2fs, duration: %.0fs)",
                total_duration,
                load_duration,
                self._duration_sec,
            )

        except FileNotFoundError:
            raise
        except Exception as exc:
            logging.error("Failed to load waveform data: %s", exc, exc_info=True)
            QMessageBox.critical(
                self,
                "Waveform Error",
                f"Unable to load WAV file '{self._wav_filename}'.\n\nError: {exc}",
            )
            for widget in (
                self.play_button,
                self.pause_button,
                self.stop_button,
                self.position_slider,
            ):
                widget.setEnabled(False)

    def _extract_wav(self) -> None:
        """Backward-compat wrapper: delegate to AudioLoader."""
        loader = AudioLoader(self._zip_path, self._wav_filename)
        self._temp_wav = loader.extract_wav()

    def _render_waveform(self) -> None:
        """Render the waveform envelope on the primary plot."""
        if not self.plot_widget or self._audio_data is None:
            return

        overview_points = max(1, int(self._overview_points))
        envelope = self._create_envelope(self._audio_data, self._sample_rate, max_points=overview_points)

        if envelope.size == 0:
            return

        if self._waveform_curve is None:
            self._waveform_curve = self.plot_widget.plot(pen=pg.mkPen("#3B82F6", width=1))

        self._waveform_curve.setData(envelope[:, 0], envelope[:, 1])
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setXRange(0, self._duration_sec, padding=0)

    def _apply_view_limits(self) -> None:
        """Clamp navigation to the valid time range."""
        if not self.plot_widget:
            return

        max_range = float(self._duration_sec) if self._duration_sec > 0 else 1.0
        min_range = min(max_range, max(0.5, float(self._min_region_duration)))
        self.plot_widget.setLimits(
            xMin=0.0,
            xMax=max_range,
            minXRange=min_range,
            maxXRange=max_range,
        )
        view_box = self.plot_widget.getViewBox()
        if view_box is not None:
            view_box.setXRange(0.0, max_range, padding=0)

    def _create_envelope(
        self,
        data,
        sample_rate: int,
        max_points: int = DEFAULT_OVERVIEW_POINTS,
    ):
        """Create envelope from audio data for efficient display (delegates to utils)."""
        return create_envelope(data, sample_rate, max_points=max_points)

    def _setup_region_selection(self) -> None:
        """Deprecated: region selection is handled by WaveformPlotController."""
        pass

    def _on_region_changed(self) -> None:
        """Compatibility shim: delegates to mediator with current region values."""
        if self._plot_controller:
            start, end = self._plot_controller.get_region()
            self._on_region_changed_mediator(start, end)

    def _snap_region_to_audio(self, min_val: float, max_val: float) -> Tuple[float, float]:
        """Snap region boundaries to audio features (RMS peaks and zero crossings)."""
        if self._audio_data is None:
            return (min_val, max_val)

        # Get tolerance from configuration (seconds)
        snap_tolerance = max(0.0, float(self._snap_tolerance))
        search_start = max(0.0, min_val - snap_tolerance)
        search_end = min(self._duration_sec, max_val + snap_tolerance)

        # Find nearby RMS peaks
        rms_peaks = self._find_rms_peaks(search_start, search_end, snap_tolerance)

        # Find nearby zero crossings
        zero_crossings = self._find_zero_crossings(search_start, search_end, snap_tolerance)

        # Combine all snap points
        snap_points = sorted(set(rms_peaks + zero_crossings))

        # Snap min_val to nearest point
        snapped_min = min_val
        if snap_points:
            # Find closest snap point for start
            start_candidates = [p for p in snap_points if abs(p - min_val) <= snap_tolerance]
            if start_candidates:
                snapped_min = min(start_candidates, key=lambda p: abs(p - min_val))

        # Snap max_val to nearest point
        snapped_max = max_val
        if snap_points:
            # Find closest snap point for end
            end_candidates = [p for p in snap_points if abs(p - max_val) <= snap_tolerance]
            if end_candidates:
                snapped_max = min(end_candidates, key=lambda p: abs(p - max_val))

        return (snapped_min, snapped_max)

    def _find_rms_peaks(self, start_time: float, end_time: float, tolerance: float) -> List[float]:
        """Find RMS peaks within a bounded window around the region."""
        if self._audio_data is None:
            return []

        peaks = []
        sr = self._sample_rate
        window_size = max(1, int(RMS_WINDOW_SIZE * sr))  # 100ms windows
        half_step = max(1, window_size // 2)

        search_start_sample = max(0, int((start_time - tolerance) * sr))
        search_end_sample = min(len(self._audio_data), int((end_time + tolerance) * sr))

        if search_end_sample - search_start_sample <= window_size:
            return peaks

        local_rms = []
        for offset in range(search_start_sample, search_end_sample - window_size, half_step):
            window = self._audio_data[offset : offset + window_size]
            rms = float(np.sqrt(np.mean(window**2)))
            center_sample = offset + window_size // 2
            local_rms.append((rms, center_sample))

        for idx in range(1, len(local_rms) - 1):
            prev_rms, _ = local_rms[idx - 1]
            current_rms, sample_idx = local_rms[idx]
            next_rms, _ = local_rms[idx + 1]
            if current_rms > prev_rms and current_rms > next_rms:
                peaks.append(sample_idx / sr)

        return peaks

    def _find_zero_crossings(self, start_time: float, end_time: float, tolerance: float) -> List[float]:
        """Find zero crossings within a bounded window around the region."""
        if self._audio_data is None:
            return []

        crossings = []
        sr = self._sample_rate
        search_start_sample = max(1, int((start_time - tolerance) * sr))
        search_end_sample = min(len(self._audio_data), int((end_time + tolerance) * sr))

        for i in range(search_start_sample, search_end_sample):
            # Detect sign changes
            if self._audio_data[i - 1] * self._audio_data[i] < 0:
                time_pos = i / self._sample_rate
                crossings.append(time_pos)

        return crossings

    def _update_region_label(self) -> None:
        """Update region time display."""
        if hasattr(self, "region_label"):
            start_label = self._format_mmss_with_fraction(self._region_bounds[0])
            end_label = self._format_mmss_with_fraction(self._region_bounds[1])
            self.region_label.setText(f"Region: {start_label} - {end_label}")

    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics for validation."""
        waveform_points = 0
        if self.plot_widget:
            try:
                items = self.plot_widget.listDataItems()
                if items:
                    x, _y = items[0].getData()
                    waveform_points = len(x) if x is not None else 0
            except Exception:
                waveform_points = 0
        return {
            "duration_sec": self._duration_sec,
            "sample_rate": self._sample_rate,
            "audio_size_mb": len(self._audio_data) * 4 / (1024 * 1024) if self._audio_data is not None else 0,
            "waveform_points": waveform_points,
        }

    @staticmethod
    def _format_mmss(seconds: float) -> str:
        """Format seconds as MM:SS without decimals (delegates to utils)."""
        return format_mmss(seconds)

    @staticmethod
    def _format_mmss_with_fraction(seconds: float) -> str:
        """Format seconds as MM:SS.s with one decimal place (delegates to utils)."""
        return format_mmss_with_fraction(seconds)

    @staticmethod
    def _format_delta(delta_seconds: float) -> str:
        """Format time delta in seconds with sign."""
        return f"{float(delta_seconds):+0.1f} s"

    def set_pdf_tracks(
        self,
        pdf_tracks: List[Dict],
        wav_tracks: List[Dict],
        tolerance_settings: ToleranceSettings,
    ) -> None:
        """Set PDF track markers (delegates to PlotController, mirrors internal state for tests)."""
        self._pdf_tracks = pdf_tracks
        if self._plot_controller:
            self._plot_controller.set_pdf_markers(pdf_tracks, wav_tracks, tolerance_settings)
            # Mirror controller state for backward-compatible tests
            self._pdf_markers = self._plot_controller.markers()
            self._marker_times = self._plot_controller.marker_times()

    def _clear_pdf_markers(self) -> None:
        """Remove all PDF markers from the plot."""
        if self._plot_controller:
            self._plot_controller.clear_pdf_markers()
        self._pdf_markers.clear()
        self._marker_times.clear()

    def _on_plot_mouse_moved(self, scene_position) -> None:
        """Update plot tooltip with the cursor time."""
        if not self.plot_widget:
            return
        if self.plot_widget.scene() is None:
            return
        view_box = self.plot_widget.getViewBox()
        if view_box is None:
            return
        if not self.plot_widget.sceneBoundingRect().contains(scene_position):
            return

        mouse_point = view_box.mapSceneToView(scene_position)
        time_value = max(0.0, min(float(self._duration_sec), mouse_point.x()))
        self.plot_widget.setToolTip(self._format_mmss_with_fraction(time_value))

    def _zoom_in(self) -> None:
        """Zoom in on the waveform around the current view center."""
        if not self.plot_widget or self._duration_sec <= 0:
            return

        view_min, view_max = self.plot_widget.viewRange()[0]
        current_width = max(0.0, view_max - view_min)
        if current_width <= 0:
            return

        min_range = min(float(self._duration_sec), max(0.5, float(self._min_region_duration)))
        new_width = max(current_width * 0.5, min_range)
        center = (view_min + view_max) / 2.0
        half_width = new_width / 2.0

        new_min = max(0.0, center - half_width)
        new_max = min(float(self._duration_sec), center + half_width)

        if new_max - new_min < min_range:
            new_min = max(0.0, new_max - min_range)
        self.plot_widget.setXRange(new_min, new_max, padding=0)

    def _zoom_out(self) -> None:
        """Zoom out from the current view while staying within bounds."""
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

    def _fit_all(self) -> None:
        """Fit the entire waveform into view."""
        if not self.plot_widget or self._duration_sec <= 0:
            return
        self.plot_widget.setXRange(0.0, float(self._duration_sec), padding=0)

    def _fit_to_region(self) -> None:
        """Fit the current selection region."""
        if not self.plot_widget:
            return
        start, end = self._region_bounds
        if end <= start:
            return
        self.plot_widget.setXRange(start, end, padding=0)

    def _on_position_changed(self, position_ms: int) -> None:
        """Mediator response to playback position changes: update labels and playhead."""
        position_sec = position_ms / 1000.0
        self.time_current.setText(self._format_time(position_sec))
        if self._plot_controller:
            self._plot_controller.update_playhead(position_sec)

    def _on_duration_changed(self, duration_ms: int) -> None:
        """Deprecated: duration is initialized after load by mediator."""
        if duration_ms > 0:
            self.position_slider.setRange(0, int(duration_ms))
            self.time_total.setText(self._format_time(duration_ms / 1000.0))

    def _on_slider_pressed(self) -> None:
        """Pause position updates while scrubbing."""
        self._slider_updating = True

    def _on_slider_released(self) -> None:
        """Apply slider position when released."""
        new_position = self.position_slider.value()
        if self._playback_controller:
            self._playback_controller.set_position(new_position)
        self._slider_updating = False

    def _on_slider_moved(self, position_ms: int) -> None:
        """Preview position while slider is moved."""
        position_sec = position_ms / 1000.0
        self.time_current.setText(self._format_time(position_sec))

    def _handle_play(self) -> None:
        """Deprecated: wired directly to PlaybackController."""
        if self._playback_controller:
            self._playback_controller.play()

    def _handle_pause(self) -> None:
        """Deprecated: wired directly to PlaybackController."""
        if self._playback_controller:
            self._playback_controller.pause()

    def _handle_stop(self) -> None:
        """Deprecated: wired directly to PlaybackController."""
        if self._playback_controller:
            self._playback_controller.stop()
            self._on_position_changed(0)

    def _on_player_error(self, _error, error_string: str) -> None:
        """Log playback errors."""
        if not error_string:
            error_string = "Unknown playback error"
        logging.error("Waveform playback error: %s", error_string)
        QMessageBox.warning(self, "Playback Error", error_string)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds as MM:SS.s string."""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02.1f}"

    def closeEvent(self, event) -> None:
        """Clean up resources via mediator."""
        try:
            if self._playback_controller:
                self._playback_controller.stop()
        finally:
            if self._temp_wav and self._temp_wav.exists():
                try:
                    self._temp_wav.unlink()
                except Exception as exc:
                    logging.warning("Failed to remove temporary WAV file: %s", exc)
            self._temp_wav = None
        super().closeEvent(event)

    def _init_mediator(self) -> None:
        """Create plot controller and wire signals between components."""
        if self.plot_widget is None:
            return
        self._plot_controller = WaveformPlotController(self.plot_widget)
        # Region change -> set player position to region start
        self._plot_controller.region_changed.connect(
            lambda start, end: self._on_region_changed_mediator(start, end)
        )
        # Playback position -> update labels/playhead
        if self._playback_controller is not None:
            self._playback_controller.position_changed.connect(self._on_position_changed)

    def _on_region_changed_mediator(self, start: float, end: float) -> None:
        self._region_bounds = (start, end)
        self._update_region_label()
        if self._playback_controller is not None:
            self._playback_controller.set_position(int(max(0.0, start) * 1000))


class WaveformViewerDialog(QDialog):
    """Modal dialog showing waveform visualization with playback controls."""

    def __init__(
        self,
        zip_path: Path,
        wav_filename: str,
        waveform_settings: WaveformSettings,
        parent=None,
    ):
        super().__init__(parent)
        self._zip_path = Path(zip_path)
        self._wav_filename = wav_filename
        self._temp_wav: Optional[Path] = None
        self._duration_ms: int = 0
        self._slider_updating = False
        self._waveform_settings = waveform_settings

        self.setWindowTitle(f"Waveform Viewer - {wav_filename}")
        self.resize(900, 600)

        if not _MULTIMEDIA_AVAILABLE:
            QMessageBox.critical(
                self,
                "Qt Multimedia Required",
                "Waveform playback requires the PyQt6 QtMultimedia module. "
                "Install PyQt6>=6.4 with Qt Multimedia support to enable this feature.",
            )
            raise RuntimeError("Qt Multimedia module not available") from _MULTIMEDIA_IMPORT_ERROR

        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)

        volume_value = max(0.0, min(1.0, float(waveform_settings.default_volume)))
        self._audio_output.setVolume(max(0.0, min(1.0, volume_value)))

        self._init_ui()
        self._load_waveform()

    def _init_ui(self) -> None:
        """Initialize dialog layout."""
        main_layout = QVBoxLayout(self)

        name_label = QLabel(f"{self._wav_filename}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setObjectName("waveformFilenameLabel")
        main_layout.addWidget(name_label)

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground("k")
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Amplitude")
        main_layout.addWidget(self.plot_widget, stretch=1)

        waveform_pen_color = waveform_settings.waveform_color or "#3B82F6"
        position_pen_color = waveform_settings.position_line_color or "#EF4444"

        self._plot_curve = self.plot_widget.plot(pen=pg.mkPen(waveform_pen_color, width=1))
        self._position_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen(position_pen_color, width=1))
        self.plot_widget.addItem(self._position_line)

        controls_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)

        # Transport controls
        transport_layout = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        transport_layout.addWidget(self.play_button)
        transport_layout.addWidget(self.pause_button)
        transport_layout.addWidget(self.stop_button)
        transport_layout.addStretch()

        self.play_button.clicked.connect(self._player.play)
        self.pause_button.clicked.connect(self._player.pause)
        self.stop_button.clicked.connect(self._handle_stop)

        controls_layout.addLayout(transport_layout)

        # Position slider
        slider_layout = QHBoxLayout()
        self.time_current = QLabel("00:00", self)
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 0)
        self.time_total = QLabel("00:00", self)
        slider_layout.addWidget(self.time_current)
        slider_layout.addWidget(self.position_slider, stretch=1)
        slider_layout.addWidget(self.time_total)
        controls_layout.addLayout(slider_layout)

        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        self.position_slider.sliderMoved.connect(self._on_slider_moved)

        # Volume controls
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:", self)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self._audio_output.volume() * 100))
        self.volume_value = QLabel(f"{self.volume_slider.value()}%", self)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value)
        controls_layout.addLayout(volume_layout)

        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        # Wire up player signals
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.errorOccurred.connect(self._on_player_error)

    def _load_waveform(self) -> None:
        """Extract WAV file and render waveform."""
        try:
            self._extract_wav()
            if not self._temp_wav:
                raise FileNotFoundError("Temporary WAV file missing after extraction")

            audio_data, sample_rate = sf.read(str(self._temp_wav), dtype="float32")

            if audio_data.ndim > 1:
                mono_data = audio_data.mean(axis=1)
            else:
                mono_data = audio_data

            if sample_rate <= 0 or mono_data.size == 0:
                raise ValueError("Invalid audio data encountered")

            duration_seconds = mono_data.shape[0] / float(sample_rate)

            target_pixels = max(200, int(self.plot_widget.width()))
            if target_pixels <= 0:
                target_pixels = 800
            downsample_factor = max(1, self._get_downsample_factor())
            segments = max(1, target_pixels // downsample_factor)
            window_size = max(1, int(np.ceil(mono_data.shape[0] / segments)))

            pad = (-mono_data.shape[0]) % window_size
            if pad:
                mono_padded = np.pad(mono_data, (0, pad), mode="edge")
            else:
                mono_padded = mono_data

            reshaped = mono_padded.reshape(-1, window_size)
            mins = reshaped.min(axis=1)
            maxs = reshaped.max(axis=1)

            if mins.size == 0 or maxs.size == 0:
                raise ValueError("Unable to compute waveform envelope")

            centers = ((np.arange(mins.size, dtype=float) * window_size) + (window_size / 2.0)) / float(sample_rate)
            time_pairs = np.repeat(centers, 2)
            amplitude_pairs = np.empty(time_pairs.size, dtype=mono_data.dtype)
            amplitude_pairs[0::2] = mins
            amplitude_pairs[1::2] = maxs

            self._plot_curve.setData(time_pairs, amplitude_pairs)
            self._position_line.setPos(0)
            self.plot_widget.setXRange(0, max(duration_seconds, 1.0))

            self._duration_ms = int(duration_seconds * 1000)
            self.time_total.setText(self._format_time(self._duration_ms))
            self.position_slider.setRange(0, self._duration_ms)

            self._player.setSource(QUrl.fromLocalFile(str(self._temp_wav)))
        except Exception as exc:
            logging.error("Failed to load waveform: %s", exc, exc_info=True)
            QMessageBox.critical(
                self,
                "Waveform Error",
                f"Unable to load WAV file '{self._wav_filename}'.\n\nError: {exc}",
            )
            self._set_controls_enabled(False)

    def _extract_wav(self) -> None:
        """Extract WAV file from ZIP archive to a temporary file."""
        if not self._zip_path.exists():
            raise FileNotFoundError(f"ZIP archive not found: {self._zip_path}")

        with zipfile.ZipFile(self._zip_path, "r") as zf:
            matching_entry: Optional[str] = None
            for member in zf.namelist():
                if member == self._wav_filename:
                    matching_entry = member
                    break

            if not matching_entry:
                raise FileNotFoundError(f"WAV file '{self._wav_filename}' not found in archive")

            with zf.open(matching_entry) as wav_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    shutil.copyfileobj(wav_file, temp_file)
                    self._temp_wav = Path(temp_file.name)

    def _get_downsample_factor(self) -> int:
        """Retrieve downsample factor from injected settings."""
        value = int(self._waveform_settings.downsample_factor)
        return max(1, min(100, value))

    def _set_controls_enabled(self, enabled: bool) -> None:
        """Enable or disable playback controls."""
        for widget in (
            self.play_button,
            self.pause_button,
            self.stop_button,
            self.position_slider,
            self.volume_slider,
        ):
            widget.setEnabled(enabled)

    def _on_position_changed(self, position_ms: int) -> None:
        """Update slider and position indicator when player position changes."""
        if self._slider_updating:
            return

        self._slider_updating = True
        self.position_slider.setValue(position_ms)
        self.time_current.setText(self._format_time(position_ms))
        self._update_position_line(position_ms)
        self._slider_updating = False

    def _on_duration_changed(self, duration_ms: int) -> None:
        """Handle player duration updates."""
        if duration_ms <= 0:
            return
        self._duration_ms = duration_ms
        self.position_slider.setRange(0, duration_ms)
        self.time_total.setText(self._format_time(duration_ms))

    def _on_slider_pressed(self) -> None:
        """Pause automatic updates while the user scrubs."""
        self._slider_updating = True

    def _on_slider_released(self) -> None:
        """Apply slider position when the user releases the handle."""
        new_position = self.position_slider.value()
        self._player.setPosition(new_position)
        self._update_position_line(new_position)
        self._slider_updating = False

    def _on_slider_moved(self, position_ms: int) -> None:
        """Preview position while the slider is moved."""
        self.time_current.setText(self._format_time(position_ms))
        self._update_position_line(position_ms)

    def _on_volume_changed(self, value: int) -> None:
        """Handle volume slider changes."""
        volume = max(0.0, min(1.0, value / 100.0))
        self._audio_output.setVolume(volume)
        self.volume_value.setText(f"{value}%")

    def _handle_stop(self) -> None:
        """Stop playback and reset position."""
        self._player.stop()
        self._on_position_changed(0)

    def _update_position_line(self, position_ms: int) -> None:
        """Update graphical position indicator."""
        if self._duration_ms <= 0:
            return
        position_sec = position_ms / 1000.0
        self._position_line.setPos(position_sec)

    def _on_player_error(self, _error, error_string: str) -> None:
        """Log playback errors and notify the user."""
        if not error_string:
            error_string = "Unknown playback error"
        logging.error("Waveform playback error: %s", error_string)
        QMessageBox.warning(self, "Playback Error", error_string)

    @staticmethod
    def _format_time(milliseconds: int) -> str:
        """Format milliseconds as MM:SS string."""
        try:
            millis_int = int(milliseconds)
        except (TypeError, ValueError):
            millis_int = 0
        if millis_int <= 0:
            return "00:00"
        seconds = millis_int / 1000.0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def closeEvent(self, event) -> None:  # noqa: D401
        """Ensure playback stops and temporary files are removed."""
        try:
            self._player.stop()
        finally:
            if self._temp_wav and self._temp_wav.exists():
                try:
                    self._temp_wav.unlink()
                except Exception as exc:
                    logging.warning("Failed to remove temporary WAV file: %s", exc)
            self._temp_wav = None
        super().closeEvent(event)
