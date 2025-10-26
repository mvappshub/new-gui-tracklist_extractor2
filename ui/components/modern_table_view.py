from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QEvent, QObject, QSettings, Qt, QByteArray
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QTableView

from ui.components.empty_state_overlay import EmptyStateOverlay


class ModernTableView(QTableView):
    """Enhanced table view with empty-state overlay and header persistence."""

    _MODEL_SIGNALS = ("modelReset", "rowsInserted", "rowsRemoved", "layoutChanged")

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        self.setObjectName("ModernTableView")

        self.setMouseTracking(True)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)

        horizontal = self.horizontalHeader()
        horizontal.setTextElideMode(Qt.TextElideMode.ElideRight)
        horizontal.setHighlightSections(False)

        vertical = self.verticalHeader()
        vertical.setDefaultSectionSize(36)
        vertical.setMinimumSectionSize(24)
        vertical.setFixedWidth(36)

        self._empty_overlay = EmptyStateOverlay(self.viewport())
        self._empty_overlay.hide()

        self._header_state_group = "tables"
        self.viewport().installEventFilter(self)

    def setModel(self, model):  # type: ignore[override]
        previous = self.model()
        if previous is not None:
            self._disconnect_model_signals(previous)

        super().setModel(model)

        if model is not None:
            self._connect_model_signals(model)
        self._update_overlay_visibility()

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:  # noqa: D401
        if watched is self.viewport() and event.type() in (
            QEvent.Type.Resize,
            QEvent.Type.Show,
            QEvent.Type.LayoutRequest,
        ):
            self._update_overlay_geometry()
        return super().eventFilter(watched, event)

    def resizeEvent(self, event):  # type: ignore[override]
        super().resizeEvent(event)
        self._update_overlay_geometry()

    def saveHeaderState(self, key: str, *, settings: Optional[QSettings] = None) -> bool:
        """Persist the current header configuration into QSettings."""
        if not key:
            return False
        header = self.horizontalHeader()
        if header is None:
            return False

        state = header.saveState()
        if not state:
            return False
        if not isinstance(state, QByteArray):
            try:
                state = QByteArray(state)
            except TypeError:
                return False

        target = settings or QSettings()
        target.beginGroup(self._header_state_group)
        target.setValue(key, state)
        target.endGroup()
        return True

    def restoreHeaderState(self, key: str, *, settings: Optional[QSettings] = None) -> bool:
        """Restore header configuration from QSettings."""
        if not key:
            return False
        target = settings or QSettings()
        target.beginGroup(self._header_state_group)
        value = target.value(key, None)
        target.endGroup()

        if value is None:
            return False

        if isinstance(value, QByteArray):
            byte_array = value
        elif isinstance(value, bytes):
            byte_array = QByteArray(value)
        elif isinstance(value, str):
            byte_array = QByteArray()
            tried_decoders = (
                QByteArray.fromBase64,
                QByteArray.fromHex,
            )
            for decoder in tried_decoders:
                try:
                    decoded = decoder(value.encode("ascii"))
                    if decoded and not decoded.isEmpty():
                        byte_array = decoded
                        break
                except Exception:
                    continue
            if byte_array.isEmpty() and value:
                byte_array = QByteArray(value.encode("utf-8"))
        else:
            try:
                byte_array = QByteArray(value)
            except TypeError:
                byte_array = QByteArray()

        if byte_array.isEmpty():
            return False

        header = self.horizontalHeader()
        success = header.restoreState(byte_array)
        return bool(success)

    def set_empty_state(self, *, text: Optional[str] = None, icon: Optional[QIcon] = None) -> None:
        """Customize empty-state overlay content."""
        if text is not None:
            self._empty_overlay.set_text(text)
        if icon is not None:
            self._empty_overlay.set_icon(icon)

    def set_theme(self, theme: str) -> None:
        """Assign theme property used by QSS styles."""
        self.setProperty("theme", theme)
        self._empty_overlay.setProperty("theme", theme)
        style = self.style()
        if style is not None:
            style.unpolish(self)
            style.polish(self)
        overlay_style = self._empty_overlay.style()
        if overlay_style is not None:
            overlay_style.unpolish(self._empty_overlay)
            overlay_style.polish(self._empty_overlay)

    def _connect_model_signals(self, model) -> None:
        for signal_name in self._MODEL_SIGNALS:
            signal = getattr(model, signal_name, None)
            if signal is not None:
                try:
                    signal.connect(self._update_overlay_visibility)
                except Exception:
                    pass

    def _disconnect_model_signals(self, model) -> None:
        for signal_name in self._MODEL_SIGNALS:
            signal = getattr(model, signal_name, None)
            if signal is not None:
                try:
                    signal.disconnect(self._update_overlay_visibility)
                except Exception:
                    pass

    def _update_overlay_visibility(self) -> None:
        model = self.model()
        if model is None or model.rowCount() == 0:
            self._empty_overlay.show()
            self._update_overlay_geometry()
        else:
            self._empty_overlay.hide()

    def _update_overlay_geometry(self) -> None:
        if self._empty_overlay.isHidden():
            return
        rect = self.viewport().rect()
        self._empty_overlay.setGeometry(rect)
