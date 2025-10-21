from __future__ import annotations

from pathlib import Path

import pytest
from PyQt6.QtCore import Qt

from core.models.analysis import SideResult, TrackInfo, WavInfo
from core.models.settings import ToleranceSettings
from ui.constants import SYMBOL_CHECK, SYMBOL_CROSS
from ui.models.tracks_table_model import TracksTableModel

pytestmark = pytest.mark.usefixtures("qtbot")


@pytest.fixture
def tolerance_settings():
    return ToleranceSettings(warn_tolerance=2, fail_tolerance=5)


@pytest.fixture
def mock_side_result_tracks():
    pdf_track = TrackInfo(title="Track 1", side="A", position=1, duration_sec=180)
    wav_track = WavInfo(filename="track1.wav", duration_sec=181.0, side="A", position=1)
    return SideResult(
        seq=1,
        pdf_path=Path("test.pdf"),
        zip_path=Path("test.zip"),
        side="A",
        mode="tracks",
        status="OK",
        pdf_tracks=[pdf_track],
        wav_tracks=[wav_track],
        total_pdf_sec=180,
        total_wav_sec=181.0,
        total_difference=1,
    )


def test_tracks_table_model_creation(tolerance_settings):
    model = TracksTableModel(tolerance_settings=tolerance_settings)
    assert model.rowCount() == 0
    assert model.columnCount() == len(model._headers)


def test_update_data_populates_model(tolerance_settings, mock_side_result_tracks):
    model = TracksTableModel(tolerance_settings=tolerance_settings)
    model.update_data(mock_side_result_tracks)
    # One track row + total row
    assert model.rowCount() == 2


def test_track_match_symbol_ok(tolerance_settings, mock_side_result_tracks):
    model = TracksTableModel(tolerance_settings=tolerance_settings)
    model.update_data(mock_side_result_tracks)

    index_match = model.index(0, 6)
    assert model.data(index_match, Qt.ItemDataRole.DisplayRole) == SYMBOL_CHECK


def test_track_match_symbol_fail(tolerance_settings, mock_side_result_tracks):
    failure_result = mock_side_result_tracks.model_copy()
    failure_result.wav_tracks[0] = failure_result.wav_tracks[0].model_copy(update={"duration_sec": 184.0})
    failure_result.total_difference = 4

    model = TracksTableModel(tolerance_settings=tolerance_settings)
    model.update_data(failure_result)

    index_match = model.index(0, 6)
    assert model.data(index_match, Qt.ItemDataRole.DisplayRole) == SYMBOL_CROSS
