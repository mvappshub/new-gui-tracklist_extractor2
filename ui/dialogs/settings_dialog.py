from __future__ import annotations

import logging
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
)

from config import save_config, AppConfig
from settings_page import SettingsPage


class SettingsDialog(QDialog):
    """Modal settings dialog containing SettingsPage with Save/Cancel buttons."""

    def __init__(self, settings_filename: Path, app_config: AppConfig, parent=None):
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

        self.settings_page = SettingsPage(app_config, self.settings_filename, show_action_buttons=False)
        scroll_area.setWidget(self.settings_page)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _show_safe_message_box(
        self,
        title: str,
        text: str,
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
    ):
        if os.getenv("QT_QPA_PLATFORM") == "offscreen":
            logging.error(f"MODAL_DIALOG_BLOCKED: Title: {title}, Text: {text}")
            return

        parent = self.parent()
        if parent and hasattr(parent, "_show_safe_message_box"):
            parent._show_safe_message_box(title, text, icon)
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.exec()

    def _on_save(self) -> None:
        """Handle save button click - save config and accept dialog."""
        try:
            save_config(self.settings_filename)
            self.accept()
        except Exception as exc:
            self._show_safe_message_box(
                "Save Error",
                f"Failed to save settings:\n{exc}",
                QMessageBox.Icon.Critical,
            )
