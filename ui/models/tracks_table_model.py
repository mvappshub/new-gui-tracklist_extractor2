from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QFont, QPalette
from PyQt6.QtWidgets import QApplication

from core.models.analysis import SideResult
from core.models.settings import ToleranceSettings
from ui.constants import (
    LABEL_TOTAL_TRACKS,
    PLACEHOLDER_DASH,
    STATUS_OK,
    SYMBOL_CHECK,
    SYMBOL_CROSS,
    TABLE_HEADERS_BOTTOM,
)
from ui.theme import get_system_file_icon


class TracksTableModel(QAbstractTableModel):
    """Model for the bottom table showing track details."""

    def __init__(self, tolerance_settings: ToleranceSettings):
        super().__init__()
        self.tolerance_settings = tolerance_settings
        self._headers = TABLE_HEADERS_BOTTOM
        self._data: Optional[SideResult] = None

    def flags(self, index: QModelIndex):
        base = super().flags(index)
        if not index.isValid():
            return base
        if index.row() == self.rowCount() - 1:
            return base & ~Qt.ItemFlag.ItemIsSelectable
        return base

    def rowCount(self, parent: QModelIndex = QModelIndex()):  # type: ignore[override]
        if not self._data or not self._data.pdf_tracks:
            return 0
        return len(self._data.pdf_tracks) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()):  # type: ignore[override]
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if not index.isValid() or not self._data:
            return None

        row = index.row()
        column = index.column()
        is_total_row = row == self.rowCount() - 1

        if role == Qt.ItemDataRole.DecorationRole and column == 7 and not is_total_row:
            wav_track_exists = False
            if self._data.mode == "tracks":
                wav_track_exists = row < len(self._data.wav_tracks)
            else:
                wav_track_exists = bool(self._data.wav_tracks)
            if wav_track_exists:
                return get_system_file_icon("play")

        if role == Qt.ItemDataRole.ToolTipRole and column == 7 and not is_total_row:
            return "View waveform"

        if role == Qt.ItemDataRole.DisplayRole:
            if is_total_row:
                return self.get_total_row_data(column)
            return self.get_track_row_data(row, column)

        if role == Qt.ItemDataRole.BackgroundRole and is_total_row:
            palette = QApplication.instance().palette()
            try:
                base = palette.color(QPalette.ColorRole.Window)
                alternate = palette.color(QPalette.ColorRole.AlternateBase)
            except AttributeError:
                base = palette.color(QPalette.Base)
                alternate = palette.color(QPalette.AlternateBase)

            if alternate != base:
                return alternate
            try:
                is_dark = base.lightness() < 128
            except AttributeError:
                is_dark = False
            return base.darker(105) if is_dark else base.lighter(105)

        if role == Qt.ItemDataRole.FontRole and is_total_row:
            font = QFont()
            font.setBold(True)
            return font

        if role == Qt.ItemDataRole.TextAlignmentRole and column == 7:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def get_track_row_data(self, row: int, column: int):
        if not self._data or row >= len(self._data.pdf_tracks):
            return ""

        pdf_track = self._data.pdf_tracks[row]

        if self._data.mode == "tracks":
            wav_track = self._data.wav_tracks[row] if row < len(self._data.wav_tracks) else None
            difference = (wav_track.duration_sec - pdf_track.duration_sec) if wav_track else None

            try:
                track_tolerance = float(self.tolerance_settings.warn_tolerance)
            except (TypeError, ValueError):
                track_tolerance = 2.0

            match_symbol = SYMBOL_CHECK if wav_track and difference is not None and abs(difference) <= track_tolerance else SYMBOL_CROSS

            if column == 0:
                return pdf_track.position
            if column == 1:
                return wav_track.filename if wav_track else PLACEHOLDER_DASH
            if column == 2:
                return pdf_track.title
            if column == 3:
                return f"{pdf_track.duration_sec // 60:02d}:{pdf_track.duration_sec % 60:02d}"
            if column == 4:
                if wav_track:
                    return f"{int(wav_track.duration_sec) // 60:02d}:{int(wav_track.duration_sec) % 60:02d}"
                return PLACEHOLDER_DASH
            if column == 5:
                return f"{difference:+.0f}" if difference is not None else PLACEHOLDER_DASH
            if column == 6:
                return match_symbol
            if column == 7:
                return ""
        else:
            if column == 0:
                return pdf_track.position
            if column == 1:
                return PLACEHOLDER_DASH
            if column == 2:
                return pdf_track.title
            if column == 3:
                return f"{pdf_track.duration_sec // 60:02d}:{pdf_track.duration_sec % 60:02d}"
            if column == 4:
                return PLACEHOLDER_DASH
            if column == 5:
                return PLACEHOLDER_DASH
            if column == 6:
                return PLACEHOLDER_DASH
            if column == 7:
                return ""
            return PLACEHOLDER_DASH
        return ""

    def get_total_row_data(self, column: int):
        if not self._data:
            return ""

        if column == 1:
            if self._data.mode == "side" and self._data.wav_tracks:
                return self._data.wav_tracks[0].filename
            return LABEL_TOTAL_TRACKS
        if column == 2:
            return f"{len(self._data.pdf_tracks)} tracks"
        if column == 3:
            return f"{self._data.total_pdf_sec // 60:02d}:{self._data.total_pdf_sec % 60:02d}"
        if column == 4:
            return f"{int(self._data.total_wav_sec) // 60:02d}:{int(self._data.total_wav_sec) % 60:02d}"
        if column == 5:
            return f"{self._data.total_difference:+.0f}"
        if column == 6:
            return SYMBOL_CHECK if self._data.status == STATUS_OK else SYMBOL_CROSS
        if column == 7:
            return ""
        return ""

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
            if role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setBold(True)
                return font
        return None

    def update_data(self, result: Optional[SideResult]) -> None:
        self.beginResetModel()
        self._data = result
        self.endResetModel()
