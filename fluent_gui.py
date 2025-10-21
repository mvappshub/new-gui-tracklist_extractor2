#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DEPRECATION WARNING:
# This file is a backward-compatibility wrapper.
# New development should use the modular components from the `ui/` package
# and the new entry point `app.py`.
# Export helpers moved to services/export_service.py.

from PyQt6.QtWidgets import QApplication, QDialogButtonBox

from config import cfg, load_config
from core.models.analysis import SideResult, TrackInfo, WavInfo
from ui import (
    AnalysisWorker,
    AnalysisWorkerManager,
    BUTTON_RUN_ANALYSIS,
    COLOR_WHITE,
    COMMENT_APP_STARTUP,
    COMMENT_BUTTON_COLOR,
    COMMENT_BUTTON_COLOR_DESC,
    COMMENT_CONFIG_ERROR,
    COMMENT_CONFIG_LOAD,
    COMMENT_MAX_WIDTH_WAV,
    COMMENT_SETUP_BOTTOM_TABLE,
    COMMENT_SETUP_TOP_TABLE,
    FILTER_ALL,
    FILTER_FAIL,
    FILTER_OK,
    FILTER_WARN,
    INTERFACE_MAIN,
    LABEL_FILTER,
    LABEL_TOTAL_TRACKS,
    MSG_DONE,
    MSG_ERROR,
    MSG_ERROR_PATHS,
    MSG_NO_PAIRS,
    MSG_PROCESSING_PAIR,
    MSG_SCANNING,
    MainWindow as UIMainWindow,
    PLACEHOLDER_DASH,
    ResultsTableModel,
    SETTINGS_FILENAME,
    STATUS_ANALYZING,
    STATUS_FAIL,
    STATUS_OK,
    STATUS_READY,
    STATUS_WARN,
    SYMBOL_CHECK,
    SYMBOL_CROSS,
    SYMBOL_OPEN,
    TABLE_HEADERS_BOTTOM,
    TABLE_HEADERS_TOP,
    TracksTableModel,
    WINDOW_TITLE,
    get_gz_color as _ui_get_gz_color,
    load_export_settings,
    load_gz_media_fonts as _ui_load_fonts,
    load_gz_media_stylesheet as _ui_load_stylesheet,
    load_theme_settings,
    load_id_extraction_settings,
    load_waveform_settings,
    load_tolerance_settings,
    load_worker_settings,
    SettingsDialog as UISettingsDialog,
)
from ui.theme import get_system_file_icon

__all__ = [
    "MainWindow",
    "TopTableModel",
    "BottomTableModel",
    "ResultsTableModel",
    "TracksTableModel",
    "AnalysisWorker",
    "AnalysisWorkerManager",
    "SettingsDialog",
    "get_gz_color",
    "load_gz_media_fonts",
    "load_gz_media_stylesheet",
    "SideResult",
    "TrackInfo",
    "WavInfo",
    "ICON_OPEN_QICON",
    "BUTTON_RUN_ANALYSIS",
    "COLOR_WHITE",
    "COMMENT_APP_STARTUP",
    "COMMENT_BUTTON_COLOR",
    "COMMENT_BUTTON_COLOR_DESC",
    "COMMENT_CONFIG_ERROR",
    "COMMENT_CONFIG_LOAD",
    "COMMENT_MAX_WIDTH_WAV",
    "COMMENT_SETUP_BOTTOM_TABLE",
    "COMMENT_SETUP_TOP_TABLE",
    "FILTER_ALL",
    "FILTER_FAIL",
    "FILTER_OK",
    "FILTER_WARN",
    "INTERFACE_MAIN",
    "LABEL_FILTER",
    "LABEL_TOTAL_TRACKS",
    "MSG_DONE",
    "MSG_ERROR",
    "MSG_ERROR_PATHS",
    "MSG_NO_PAIRS",
    "MSG_PROCESSING_PAIR",
    "MSG_SCANNING",
    "PLACEHOLDER_DASH",
    "SETTINGS_FILENAME",
    "STATUS_ANALYZING",
    "STATUS_FAIL",
    "STATUS_OK",
    "STATUS_READY",
    "STATUS_WARN",
    "SYMBOL_CHECK",
    "SYMBOL_CROSS",
    "SYMBOL_OPEN",
    "TABLE_HEADERS_BOTTOM",
    "TABLE_HEADERS_TOP",
    "WINDOW_TITLE",
]

TopTableModel = ResultsTableModel
BottomTableModel = TracksTableModel
ICON_OPEN_QICON = get_system_file_icon("file")


def get_gz_color(color_key: str):
    theme_settings = load_theme_settings(cfg)
    return _ui_get_gz_color(color_key, theme_settings.status_colors)


def load_gz_media_fonts(app):
    theme_settings = load_theme_settings(cfg)
    _ui_load_fonts(app, font_family=theme_settings.font_family, font_size=theme_settings.font_size)


def load_gz_media_stylesheet(app):
    theme_settings = load_theme_settings(cfg)
    _ui_load_stylesheet(app, stylesheet_path=theme_settings.stylesheet_path)


# Export functionality moved to services/export_service.py (Phase 4 refactoring)


class SettingsDialog(UISettingsDialog):
    def __init__(self, parent=None):
        super().__init__(settings_filename=SETTINGS_FILENAME, parent=parent)
        button_box = self.findChild(QDialogButtonBox)
        self.save_button = None
        if button_box is not None:
            self.save_button = button_box.button(QDialogButtonBox.StandardButton.Save)


class MainWindow(UIMainWindow):
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
            return

        load_config(SETTINGS_FILENAME)
        tolerance_settings = load_tolerance_settings(cfg)
        export_settings = load_export_settings(cfg)
        theme_settings = load_theme_settings(cfg)
        worker_settings = load_worker_settings(cfg)
        id_extraction_settings = load_id_extraction_settings(cfg)
        waveform_settings = load_waveform_settings(cfg)

        app = QApplication.instance()
        if app is not None:
            _ui_load_fonts(app, theme_settings.font_family, theme_settings.font_size)
            _ui_load_stylesheet(app, theme_settings.stylesheet_path)

        worker_manager = AnalysisWorkerManager(
            worker_settings=worker_settings,
            tolerance_settings=tolerance_settings,
            id_extraction_settings=id_extraction_settings,
        )

        super().__init__(
            tolerance_settings=tolerance_settings,
            export_settings=export_settings,
            theme_settings=theme_settings,
            waveform_settings=waveform_settings,
            worker_manager=worker_manager,
            settings_filename=SETTINGS_FILENAME,
        )


if __name__ == "__main__":
    from app import main

    main()
