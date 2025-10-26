from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyStateOverlay(QWidget):
    """Overlay widget displayed when a table has no rows."""

    def __init__(self, parent: Optional[QWidget] = None, *, icon: Optional[QIcon] = None, text: str = "No Data"):
        super().__init__(parent)
        self.setObjectName("EmptyStateOverlay")
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        self.setAutoFillBackground(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._icon_label = QLabel(self)
        self._icon_label.setObjectName("EmptyStateOverlayIcon")
        self._icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._text_label = QLabel(text, self)
        self._text_label.setObjectName("EmptyStateOverlayText")
        self._text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._text_label.setWordWrap(True)

        layout.addWidget(self._icon_label)
        layout.addWidget(self._text_label)

        if icon:
            self.set_icon(icon)
        else:
            self._icon_label.hide()

    def set_icon(self, icon: QIcon, size: int = 48) -> None:
        """Set overlay icon."""
        if icon.isNull():
            self._icon_label.hide()
            return
        pixmap = icon.pixmap(size, size)
        if pixmap.isNull():
            self._icon_label.hide()
            return
        self._icon_label.setPixmap(pixmap)
        self._icon_label.show()

    def set_text(self, text: str) -> None:
        """Set overlay text."""
        self._text_label.setText(text)
