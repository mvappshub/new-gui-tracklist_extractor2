from __future__ import annotations

from pathlib import Path
from unittest import mock

import numpy as np
import pyqtgraph as pg
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

pytestmark = pytest.mark.gui

import waveform_viewer
from waveform_viewer import WaveformViewerDialog


@pytest.fixture(autouse=True)
def _ensure_test_config(isolated_config, monkeypatch):
    """Ensure waveform_viewer uses the isolated configuration."""
    monkeypatch.setattr(waveform_viewer, "cfg", isolated_config, raising=False)
    return isolated_config


@pytest.fixture(autouse=True)
def fake_multimedia(monkeypatch):
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
def viewer_dialog(qapp, mock_wav_zip, qtbot) -> WaveformViewerDialog:
    zip_path, wav_name = mock_wav_zip
    dialog = WaveformViewerDialog(zip_path, wav_name)
    qtbot.addWidget(dialog)
    try:
        yield dialog
    finally:
        dialog.close()


class TestWaveformViewerDialog:
    def test_dialog_creation(self, viewer_dialog, mock_wav_zip):
        zip_path, wav_name = mock_wav_zip
        assert wav_name in viewer_dialog.windowTitle()
        assert viewer_dialog._zip_path == Path(zip_path)
        assert viewer_dialog._wav_filename == wav_name
        assert viewer_dialog.width() == 900
        assert viewer_dialog.height() == 600

    def test_multimedia_unavailable(self, monkeypatch, mock_wav_zip):
        zip_path, wav_name = mock_wav_zip
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", False)
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_IMPORT_ERROR", ImportError("missing Qt multimedia"))
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(RuntimeError):
                WaveformViewerDialog(zip_path, wav_name)
        critical.assert_called_once()
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", True)

    def test_ui_components_exist(self, viewer_dialog):
        assert isinstance(viewer_dialog.plot_widget, pg.PlotWidget)
        assert viewer_dialog.play_button.text() == "Play"
        assert viewer_dialog.pause_button.text() == "Pause"
        assert viewer_dialog.stop_button.text() == "Stop"
        assert viewer_dialog.time_current.text() == "00:00"
        assert viewer_dialog.time_total.text() != ""
        assert viewer_dialog.position_slider.minimum() == 0
        assert viewer_dialog.volume_slider.maximum() == 100

    def test_plot_widget_configuration(self, viewer_dialog):
        plot_item = viewer_dialog.plot_widget.getPlotItem()
        assert plot_item.getAxis("left").labelText == "Amplitude"
        assert plot_item.getAxis("bottom").labelText == "Time"

    def test_waveform_extraction(self, mock_wav_zip, qtbot):
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name)
        qtbot.addWidget(dialog)
        assert dialog._temp_wav is not None
        assert dialog._temp_wav.exists()
        assert dialog._temp_wav.suffix == ".wav"

    def test_waveform_loading_success(self, monkeypatch, tmp_path, qtbot):
        fake_wav = tmp_path / "fake.wav"
        fake_wav.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake_wav

        mono = np.linspace(-1, 1, 1000, dtype=np.float32)
        with mock.patch.object(waveform_viewer, "sf") as mock_sf, mock.patch.object(
            waveform_viewer.pg.PlotDataItem, "setData", autospec=True
        ) as set_data:
            mock_sf.read.return_value = (mono, 100)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            dialog = WaveformViewerDialog(tmp_path / "dummy.zip", "test.wav")
            qtbot.addWidget(dialog)
            assert dialog._duration_ms > 0
            assert dialog.time_total.text().startswith("00:")
            assert set_data.called

    def test_waveform_loading_stereo_to_mono(self, monkeypatch, tmp_path, qtbot):
        fake = tmp_path / "fake.wav"
        fake.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake

        stereo = np.column_stack(
            [np.linspace(-1, 1, 1000, dtype=np.float32), np.linspace(1, -1, 1000, dtype=np.float32)]
        )
        with mock.patch.object(waveform_viewer, "sf") as mock_sf:
            mock_sf.read.return_value = (stereo, 100)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            dialog = WaveformViewerDialog(tmp_path / "dummy.zip", "test.wav")
            qtbot.addWidget(dialog)
            assert dialog._duration_ms > 0

    def test_waveform_downsampling(self, monkeypatch, tmp_path, qtbot, isolated_config):
        isolated_config.waveform_downsample_factor = 20
        monkeypatch.setattr(waveform_viewer, "cfg", isolated_config, raising=False)

        fake = tmp_path / "fake.wav"
        fake.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake

        mono = np.linspace(-1, 1, 4000, dtype=np.float32)
        with mock.patch.object(waveform_viewer, "sf") as mock_sf, mock.patch.object(
            waveform_viewer.pg.PlotDataItem, "setData", autospec=True
        ) as set_data:
            mock_sf.read.return_value = (mono, 400)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            WaveformViewerDialog(tmp_path / "dummy.zip", "test.wav")
            # We cannot easily inspect internals but ensure plotting called with compressed data
            args, _ = set_data.call_args
            x_values = args[1]
            assert len(x_values) < mono.size

    def test_play_button_triggers_playback(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "play") as play_mock:
            qtbot.mouseClick(viewer_dialog.play_button, Qt.MouseButton.LeftButton)
            play_mock.assert_called_once()

    def test_pause_button_triggers_pause(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "pause") as pause_mock:
            qtbot.mouseClick(viewer_dialog.pause_button, Qt.MouseButton.LeftButton)
            pause_mock.assert_called_once()

    def test_stop_button_resets_position(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "stop") as stop_mock:
            with mock.patch.object(viewer_dialog, "_on_position_changed") as on_position:
                qtbot.mouseClick(viewer_dialog.stop_button, Qt.MouseButton.LeftButton)
                stop_mock.assert_called_once()
                on_position.assert_called_with(0)

    def test_volume_slider_changes_volume(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._audio_output, "setVolume") as set_volume:
            viewer_dialog.volume_slider.setValue(75)
            qtbot.waitUntil(lambda: set_volume.called, timeout=1000)
            set_volume.assert_called_with(pytest.approx(0.75, rel=1e-2))
            assert viewer_dialog.volume_value.text() == "75%"

    def test_position_changed_updates_ui(self, viewer_dialog):
        viewer_dialog._on_position_changed(30000)
        assert viewer_dialog.position_slider.value() == 30000
        assert viewer_dialog.time_current.text() == "00:30"

    def test_slider_seeking(self, viewer_dialog):
        with mock.patch.object(viewer_dialog._player, "setPosition") as set_position:
            viewer_dialog._on_slider_pressed()
            viewer_dialog._on_slider_moved(60000)
            viewer_dialog._on_slider_released()
            set_position.assert_called_with(60000)

    @pytest.mark.parametrize(
        "millis, expected",
        [
            (0, "00:00"),
            (45_000, "00:45"),  # 45 seconds
            (125_000, "02:05"),  # 2 minutes 5 seconds
            (-1_000, "00:00"),  # Negative values should return 00:00
        ],
    )
    def test_format_time(self, millis, expected):
        """Test time formatting with milliseconds input (Qt QMediaPlayer API)."""
        assert WaveformViewerDialog._format_time(millis) == expected

    def test_default_volume_from_config(self, isolated_config, mock_wav_zip, qtbot, monkeypatch):
        isolated_config.waveform_default_volume = 0.7
        monkeypatch.setattr(waveform_viewer, "cfg", isolated_config, raising=False)
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name)
        qtbot.addWidget(dialog)
        assert dialog._audio_output.volume() == pytest.approx(0.7)

    def test_downsample_factor_from_config(self, isolated_config, mock_wav_zip, qtbot, monkeypatch):
        isolated_config.waveform_downsample_factor = 15
        monkeypatch.setattr(waveform_viewer, "cfg", isolated_config, raising=False)
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name)
        qtbot.addWidget(dialog)
        assert dialog._get_downsample_factor() == 15

    def test_waveform_colors_from_config(self, isolated_config, mock_wav_zip, qtbot, monkeypatch):
        isolated_config.waveform_waveform_color = "#ffffff"
        isolated_config.waveform_position_line_color = "#123456"
        monkeypatch.setattr(waveform_viewer, "cfg", isolated_config, raising=False)
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name)
        qtbot.addWidget(dialog)
        curve_color = dialog._plot_curve.opts["pen"].color().name()
        line_color = dialog._position_line.pen().color().name()
        assert curve_color.lower() == "#ffffff"
        assert line_color.lower() == "#123456"

    def test_missing_zip_file(self, tmp_path, qtbot):
        non_existent = tmp_path / "missing.zip"
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(non_existent, "track.wav")
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_missing_wav_in_zip(self, empty_zip, qtbot):
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(empty_zip, "missing.wav")
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_invalid_wav_data(self, invalid_wav_zip, qtbot):
        zip_path, wav_name = invalid_wav_zip
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(zip_path, wav_name)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_player_error_handling(self, viewer_dialog, monkeypatch):
        with mock.patch.object(QMessageBox, "warning") as warning:
            viewer_dialog._on_player_error(None, "Test error")
            warning.assert_called_once()

    def test_close_event_cleanup(self, viewer_dialog, qtbot):
        temp_wav = viewer_dialog._temp_wav
        assert temp_wav and temp_wav.exists()
        with mock.patch.object(viewer_dialog._player, "stop") as stop_mock:
            viewer_dialog.close()
            stop_mock.assert_called_once()
        if temp_wav:
            assert not temp_wav.exists()

    def test_position_line_stored_as_instance_variable(self, viewer_dialog):
        """Verify position line is created once and reused on updates."""
        initial_line = viewer_dialog._position_line
        viewer_dialog._on_position_changed(1000)
        viewer_dialog._on_position_changed(2000)
        assert viewer_dialog._position_line is initial_line
