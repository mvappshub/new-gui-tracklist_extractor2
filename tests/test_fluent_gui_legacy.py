"""Characterization tests for the legacy fluent_gui module."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

import pytest


pytest.importorskip("PyQt6")


@pytest.fixture(scope="session", autouse=True)
def _force_offscreen_platform() -> None:
    """Ensure Qt uses the offscreen platform during tests."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def fluent_gui_module():
    return importlib.import_module("fluent_gui")


@pytest.fixture(scope="module")
def qapp():
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(scope="module", autouse=True)
def _load_legacy_config():
    from config import load_config

    return load_config("settings.json")


def _assert_attributes_exist(module, names: Iterable[str]) -> None:
    missing = [name for name in names if not hasattr(module, name)]
    assert not missing, f"Missing expected attributes: {missing}"


def test_expected_classes_are_available(fluent_gui_module):
    required_classes = [
        "MainWindow",
        "TopTableModel",
        "BottomTableModel",
        "AnalysisWorker",
        "SettingsDialog",
    ]
    _assert_attributes_exist(fluent_gui_module, required_classes)


def test_expected_functions_are_available(fluent_gui_module):
    required_functions = [
        "get_system_file_icon",
        "get_gz_color",
        "load_gz_media_fonts",
        "load_gz_media_stylesheet",
    ]
    _assert_attributes_exist(fluent_gui_module, required_functions)


def test_expected_constants_are_available(fluent_gui_module):
    required_constants = [
        "SETTINGS_FILENAME",
        "STATUS_READY",
        "STATUS_ANALYZING",
        "MSG_ERROR_PATHS",
        "MSG_NO_PAIRS",
        "MSG_DONE",
        "MSG_ERROR",
        "MSG_SCANNING",
        "MSG_PROCESSING_PAIR",
        "WINDOW_TITLE",
        "BUTTON_RUN_ANALYSIS",
        "LABEL_FILTER",
        "FILTER_ALL",
        "FILTER_OK",
        "FILTER_FAIL",
        "FILTER_WARN",
        "TABLE_HEADERS_TOP",
        "TABLE_HEADERS_BOTTOM",
        "SYMBOL_OPEN",
        "ICON_OPEN_QICON",
        "COLOR_WHITE",
        "STATUS_OK",
        "STATUS_WARN",
        "STATUS_FAIL",
        "SYMBOL_CHECK",
        "SYMBOL_CROSS",
        "PLACEHOLDER_DASH",
        "LABEL_TOTAL_TRACKS",
        "INTERFACE_MAIN",
        "COMMENT_SETUP_TOP_TABLE",
        "COMMENT_SETUP_BOTTOM_TABLE",
        "COMMENT_MAX_WIDTH_WAV",
        "COMMENT_APP_STARTUP",
        "COMMENT_CONFIG_LOAD",
        "COMMENT_CONFIG_ERROR",
        "COMMENT_BUTTON_COLOR",
        "COMMENT_BUTTON_COLOR_DESC",
    ]
    _assert_attributes_exist(fluent_gui_module, required_constants)


def test_main_window_can_instantiate(fluent_gui_module, qapp):
    window = fluent_gui_module.MainWindow()
    try:
        assert window.windowTitle() == fluent_gui_module.WINDOW_TITLE
    finally:
        window.close()
        window.deleteLater()


def test_fluent_gui_entrypoint_launches(project_root):
    env = os.environ.copy()
    env.setdefault("QT_QPA_PLATFORM", "offscreen")

    process = subprocess.Popen(
        [sys.executable, "fluent_gui.py"],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)
        assert process.poll() is None, "fluent_gui.py terminated prematurely"
    finally:
        process.terminate()
        try:
            process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)
