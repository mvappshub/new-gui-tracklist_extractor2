from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.gui
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QMessageBox

import fluent_gui
from fluent_gui import (
    TABLE_HEADERS_BOTTOM,
    BottomTableModel,
    MainWindow,
    SideResult,
    TrackInfo,
    WavInfo,
)


@pytest.fixture
def main_window(qapp, qtbot, isolated_config, monkeypatch):
    monkeypatch.setattr(fluent_gui, "cfg", isolated_config, raising=False)
    monkeypatch.setattr(fluent_gui, "load_config", lambda path: isolated_config, raising=False)
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def _make_side_result(zip_path: Path, wav_filename: str, tmp_path: Path) -> SideResult:
    pdf_path = tmp_path / "track.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 dummy")
    return SideResult(
        seq=1,
        pdf_path=pdf_path,
        zip_path=zip_path,
        side="A",
        mode="tracks",
        status=fluent_gui.STATUS_OK,
        pdf_tracks=[TrackInfo(title="Test Track", side="A", position=1, duration_sec=120)],
        wav_tracks=[WavInfo(filename=wav_filename, duration_sec=120.0)],
        total_pdf_sec=120,
        total_wav_sec=120.0,
        total_difference=0,
    )


class TestWaveformIntegration:
    def test_bottom_table_waveform_column_exists(self):
        assert TABLE_HEADERS_BOTTOM[7] == "Waveform"
        model = BottomTableModel()
        assert model.columnCount() == 8

    def test_waveform_column_click_opens_dialog(self, main_window, mock_wav_zip, qtbot, tmp_path, monkeypatch):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)
        with mock.patch("waveform_viewer.WaveformEditorDialog", autospec=True) as dialog_cls:
            dialog_instance = dialog_cls.return_value
            main_window.on_bottom_cell_clicked(index)
            dialog_cls.assert_called_once()
            args, kwargs = dialog_cls.call_args
            assert args[:2] == (zip_path, wav_name)
            assert kwargs["waveform_settings"] == main_window.waveform_settings
            assert kwargs["parent"] is main_window
            dialog_instance.exec.assert_called_once()

    def test_waveform_click_no_selection(self, main_window, mock_wav_zip, qtbot):
        zip_path, wav_name = mock_wav_zip
        index = main_window.bottom_model.index(0, 7)
        with mock.patch("waveform_viewer.WaveformEditorDialog") as dialog_cls:
            main_window.on_bottom_cell_clicked(index)
            dialog_cls.assert_not_called()

    def test_waveform_click_missing_zip(self, main_window, mock_wav_zip, qtbot, tmp_path):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        result.zip_path = Path(tmp_path / "missing.zip")
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)
        index = main_window.bottom_model.index(0, 7)
        with mock.patch.object(QMessageBox, "warning") as warning:
            main_window.on_bottom_cell_clicked(index)
            warning.assert_called_once()

    def test_waveform_click_missing_dependencies(self, main_window, mock_wav_zip, qtbot, tmp_path, monkeypatch):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)

        def import_hook(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "waveform_viewer":
                raise ImportError("waveform viewer missing")
            return original_import(name, globals, locals, fromlist, level)

        original_import = __import__
        with mock.patch("builtins.__import__", side_effect=import_hook):
            with mock.patch.object(QMessageBox, "warning") as warning:
                main_window.on_bottom_cell_clicked(index)
                warning.assert_called_once()

    def test_bottom_table_clicked_signal_connected(self, main_window, qtbot, mock_wav_zip, tmp_path):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)
        if not main_window.isVisible():
            main_window.show()
            qtbot.waitForWindowShown(main_window)
        main_window.bottom_table.scrollTo(index)
        rect = main_window.bottom_table.visualRect(index)
        if not rect.isValid():
            qtbot.waitUntil(lambda: main_window.bottom_table.visualRect(index).isValid())
            rect = main_window.bottom_table.visualRect(index)
        spy = QSignalSpy(main_window.bottom_table.clicked)

        qtbot.mouseClick(
            main_window.bottom_table.viewport(),
            Qt.MouseButton.LeftButton,
            pos=rect.center(),
        )

        qtbot.waitUntil(lambda: len(spy) > 0)
        assert spy[0][0] == index

    def test_bottom_model_waveform_column_data(self, tmp_path):
        zip_path = tmp_path / "archive.zip"
        zip_path.write_bytes(b"")
        result = _make_side_result(zip_path, "track.wav", tmp_path)
        model = BottomTableModel()
        model.update_data(result)
        index = model.index(0, 7)
        assert model.data(index, Qt.ItemDataRole.DisplayRole) == "View"
        assert model.data(index, Qt.ItemDataRole.TextAlignmentRole) == Qt.AlignmentFlag.AlignCenter
