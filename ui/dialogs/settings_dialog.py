from __future__ import annotations

from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QScrollArea,
    QFrame,
    QDialogButtonBox,
    QMessageBox,
)

from config import save_config
from settings_page import SettingsPage


class SettingsDialog(QDialog):
    """Modal settings dialog containing SettingsPage with Save/Cancel buttons."""

    def __init__(self, settings_filename: Path, parent=None):
        super().__init__(parent)
        self.settings_filename = Path(settings_filename)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.settings_page = SettingsPage()
        scroll_area.setWidget(self.settings_page)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _on_save(self) -> None:
        """Handle save button click - save config and accept dialog."""
        try:
            save_config(self.settings_filename)
            self.accept()
        except Exception as exc:
            QMessageBox.critical(self, "Save Error", f"Failed to save settings:\n{exc}")
