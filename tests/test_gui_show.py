#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from config import load_config
from ui import MainWindow, AnalysisWorkerManager, load_tolerance_settings, load_export_settings, load_theme_settings, load_waveform_settings, load_worker_settings, load_id_extraction_settings
from config import cfg

pytestmark = pytest.mark.gui

def test_gui_show(qapp, qtbot):
    """Test GUI show functionality."""
    print("Testing GUI show functionality...")

    # Mock dependencies for MainWindow constructor
    tolerance_settings = load_tolerance_settings(cfg)
    export_settings = load_export_settings(cfg)
    theme_settings = load_theme_settings(cfg)
    waveform_settings = load_waveform_settings(cfg)
    worker_settings = load_worker_settings(cfg)
    id_extraction_settings = load_id_extraction_settings(cfg)

    worker_manager = AnalysisWorkerManager(
        worker_settings=worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )

    try:
        print("Creating MainWindow instance...")
        window = MainWindow(
            tolerance_settings=tolerance_settings,
            export_settings=export_settings,
            theme_settings=theme_settings,
            waveform_settings=waveform_settings,
            worker_manager=worker_manager,
            settings_filename=cfg.file,
        )
        qtbot.addWidget(window)
        print("MainWindow created successfully")

        print("Showing MainWindow...")
        window.show()
        print("MainWindow shown successfully")

        # Allow the event loop to run briefly and then exit
        QTimer.singleShot(100, qapp.quit)
        qapp.exec()

    except Exception as e:
        print(f"GUI show error: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"GUI show error: {e}")
