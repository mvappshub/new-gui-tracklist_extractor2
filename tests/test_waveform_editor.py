from __future__ import annotations

from pathlib import Path
from unittest import mock
import pyqtgraph as pg
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

pytestmark = pytest.mark.gui

import waveform_viewer
from waveform_viewer import WaveformEditorDialog


@pytest.fixture(autouse=True)
def fake_multimedia(monkeypatch):
    """Provide dummy multimedia classes so tests run without QtMultimedia."""

    class DummySignal:
        def __init__(self):
            self._callbacks = []

        def connect(self, callback):
            self._callbacks.append(callback)

        def emit(self, *args, **kwargs):
            for callback in list(self._callbacks):
                callback(*args, **kwargs)

    class DummyAudioOutput:
        def __init__(self, parent=None):
            self._volume = 1.0

        def setVolume(self, volume):
            self._volume = volume

        def volume(self):
            return self._volume

    class DummyMediaPlayer:
        def __init__(self, parent=None):
            self.positionChanged = DummySignal()
            self.durationChanged = DummySignal()
            self.errorOccurred = DummySignal()
            self._audio_output = None
            self._source = None

        def setAudioOutput(self, audio_output):
            self._audio_output = audio_output

        def setSource(self, source):
            self._source = source

        def play(self):
            pass

        def pause(self):
            pass

        def stop(self):
            pass

        def setPosition(self, position_ms):
            pass

    monkeypatch.setattr(waveform_viewer, "QAudioOutput", DummyAudioOutput, raising=False)
    monkeypatch.setattr(waveform_viewer, "QMediaPlayer", DummyMediaPlayer, raising=False)
    yield


@pytest.fixture
def editor_dialog(qapp, mock_wav_zip, qtbot, waveform_settings) -> WaveformEditorDialog:
    """Create a fully initialised WaveformEditorDialog for tests."""
    zip_path, wav_name = mock_wav_zip
    dialog = WaveformEditorDialog(zip_path, wav_name, waveform_settings)
    qtbot.addWidget(dialog)
    try:
        yield dialog
    finally:
        dialog.close()


class TestWaveformEditorDialog:
    def test_editor_creation(self, editor_dialog, mock_wav_zip):
        zip_path, wav_name = mock_wav_zip
        assert wav_name in editor_dialog.windowTitle()
        assert editor_dialog._zip_path == Path(zip_path)
        assert editor_dialog._wav_filename == wav_name
        assert editor_dialog.width() == 1200
        assert editor_dialog.height() == 800

    def test_multimedia_unavailable(self, monkeypatch, mock_wav_zip, waveform_settings):
        zip_path, wav_name = mock_wav_zip
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", False)
        monkeypatch.setattr(
            waveform_viewer, "_MULTIMEDIA_IMPORT_ERROR", ImportError("missing Qt multimedia")
        )
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(RuntimeError):
                WaveformEditorDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called_once()
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", True)

    def test_ui_components_exist(self, editor_dialog):
        assert isinstance(editor_dialog.plot_widget, pg.PlotWidget)
        assert editor_dialog.region_label.text().startswith("Region:")
        assert editor_dialog.position_slider.minimum() == 0
        assert editor_dialog.play_button.text() == "Play"
        assert editor_dialog.pause_button.text() == "Pause"
        assert editor_dialog.stop_button.text() == "Stop"

    def test_audio_data_loading(self, editor_dialog):
        assert editor_dialog._audio_data is not None
        assert editor_dialog._audio_data.size > 0
        assert editor_dialog._sample_rate > 0
        assert editor_dialog._duration_sec > 0

    def test_waveform_curve_has_data(self, editor_dialog):
        assert editor_dialog._waveform_curve is not None
        x_data, y_data = editor_dialog._waveform_curve.getData()
        assert len(x_data) > 0
        assert len(x_data) == len(y_data)

    def test_region_item_created(self, editor_dialog):
        assert isinstance(editor_dialog._region_item, pg.LinearRegionItem)
        region = editor_dialog._region_item.getRegion()
        assert pytest.approx(region[0]) == 0.0
        assert region[1] > region[0]

    def test_region_change_updates_bounds(self, editor_dialog):
        initial_range = editor_dialog.plot_widget.viewRange()[0]
        editor_dialog._region_item.setRegion([0.5, 1.0])
        editor_dialog._on_region_changed()
        assert editor_dialog._region_bounds[0] >= 0.0
        assert editor_dialog._region_bounds[1] > editor_dialog._region_bounds[0]
        updated_range = editor_dialog.plot_widget.viewRange()[0]
        assert pytest.approx(updated_range[0], rel=1e-3) == pytest.approx(initial_range[0], rel=1e-3)
        assert pytest.approx(updated_range[1], rel=1e-3) == pytest.approx(initial_range[1], rel=1e-3)

    def test_minimum_region_duration_enforced(self, editor_dialog):
        editor_dialog._region_item.setRegion([0.0, 0.01])
        editor_dialog._on_region_changed()
        updated_region = editor_dialog._region_item.getRegion()
        assert (updated_region[1] - updated_region[0]) >= editor_dialog._min_region_duration

    def test_find_rms_peaks_returns_values(self, editor_dialog):
        peaks = editor_dialog._find_rms_peaks(
            0.0, editor_dialog._duration_sec, editor_dialog._snap_tolerance
        )
        assert isinstance(peaks, list)
        assert all(isinstance(p, float) for p in peaks)

    def test_find_zero_crossings_returns_values(self, editor_dialog):
        crossings = editor_dialog._find_zero_crossings(
            0.0, editor_dialog._duration_sec, editor_dialog._snap_tolerance
        )
        assert isinstance(crossings, list)
        assert all(isinstance(c, float) for c in crossings)
        assert len(crossings) > 0

    def test_position_change_creates_playhead_line(self, editor_dialog):
        editor_dialog._on_position_changed(500)
        assert editor_dialog._playhead_line is not None
        assert pytest.approx(editor_dialog._playhead_line.value(), rel=1e-3) == 0.5

    def test_set_pdf_tracks_creates_markers(self, editor_dialog, tolerance_settings):
        pdf_tracks = [
            {"duration_sec": 0.5, "title": "Intro", "position": 1},
            {"duration_sec": 1.0, "title": "Main", "position": 2},
        ]
        wav_tracks = [
            {"duration_sec": 0.52, "title": "Intro", "position": 1},
            {"duration_sec": 1.05, "title": "Main", "position": 2},
        ]
        editor_dialog.set_pdf_tracks(pdf_tracks, wav_tracks, tolerance_settings)
        assert len(editor_dialog._pdf_markers) == len(pdf_tracks)
        assert len(editor_dialog._marker_times) == len(pdf_tracks)
        assert pytest.approx(editor_dialog._marker_times[0], rel=1e-3) == pytest.approx(0.5, rel=1e-3)
        assert pytest.approx(editor_dialog._marker_times[1], rel=1e-3) == pytest.approx(1.5, rel=1e-3)

    def test_clear_pdf_markers(self, editor_dialog, tolerance_settings):
        pdf_tracks = [{"duration_sec": 0.5, "title": "Intro", "position": 1}]
        editor_dialog.set_pdf_tracks(pdf_tracks, pdf_tracks, tolerance_settings)
        assert editor_dialog._pdf_markers
        editor_dialog._clear_pdf_markers()
        assert not editor_dialog._pdf_markers
        assert not editor_dialog._marker_times

    def test_zoom_controls_adjust_range(self, editor_dialog):
        initial_range = editor_dialog.plot_widget.viewRange()[0]
        editor_dialog._zoom_in()
        zoomed_range = editor_dialog.plot_widget.viewRange()[0]
        assert (zoomed_range[1] - zoomed_range[0]) < (initial_range[1] - initial_range[0])
        editor_dialog._zoom_out()
        widened_range = editor_dialog.plot_widget.viewRange()[0]
        assert (widened_range[1] - widened_range[0]) >= (zoomed_range[1] - zoomed_range[0])
        editor_dialog._fit_to_region()
        fitted_range = editor_dialog.plot_widget.viewRange()[0]
        region_duration = editor_dialog._region_bounds[1] - editor_dialog._region_bounds[0]
        assert pytest.approx(fitted_range[1] - fitted_range[0], rel=1e-2) == pytest.approx(
            region_duration, rel=1e-2
        )
        editor_dialog._fit_all()
        fit_all_range = editor_dialog.plot_widget.viewRange()[0]
        assert pytest.approx(fit_all_range[0], rel=1e-3) == pytest.approx(0.0, rel=1e-3)
        assert pytest.approx(fit_all_range[1], rel=1e-3) == pytest.approx(
            editor_dialog._duration_sec, rel=1e-3
        )

    def test_playback_controls_trigger_player(self, editor_dialog, qtbot):
        with mock.patch.object(editor_dialog._player, "play") as play_mock:
            qtbot.mouseClick(editor_dialog.play_button, Qt.MouseButton.LeftButton)
            play_mock.assert_called_once()
        with mock.patch.object(editor_dialog._player, "pause") as pause_mock:
            qtbot.mouseClick(editor_dialog.pause_button, Qt.MouseButton.LeftButton)
            pause_mock.assert_called_once()
        with mock.patch.object(editor_dialog._player, "stop") as stop_mock:
            qtbot.mouseClick(editor_dialog.stop_button, Qt.MouseButton.LeftButton)
            stop_mock.assert_called_once()

    def test_get_performance_stats(self, editor_dialog):
        stats = editor_dialog.get_performance_stats()
        assert set(stats.keys()) == {
            "duration_sec",
            "sample_rate",
            "audio_size_mb",
            "waveform_points",
        }

    def test_close_event_cleanup(self, editor_dialog, qtbot):
        temp_wav = editor_dialog._temp_wav
        assert temp_wav and temp_wav.exists()
        with mock.patch.object(editor_dialog._player, "stop") as stop_mock:
            editor_dialog.close()
            stop_mock.assert_called_once()
        if temp_wav:
            assert not temp_wav.exists()

    def test_missing_zip_file(self, tmp_path, qtbot, waveform_settings):
        non_existent = tmp_path / "missing.zip"
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(FileNotFoundError):
                WaveformEditorDialog(non_existent, "track.wav", waveform_settings)
        critical.assert_not_called()

    def test_missing_wav_in_zip(self, empty_zip, qtbot, waveform_settings):
        with pytest.raises(FileNotFoundError):
            WaveformEditorDialog(empty_zip, "missing.wav", waveform_settings)

    def test_invalid_audio_data(self, invalid_wav_zip, waveform_settings):
        zip_path, wav_name = invalid_wav_zip
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformEditorDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()
        dialog.close()
