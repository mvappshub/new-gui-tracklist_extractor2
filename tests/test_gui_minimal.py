#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from config import load_config

def test_gui_minimal():
    """Test minimal GUI initialization."""
    print("Testing minimal GUI initialization...")

    try:
        # Test QApplication creation
        app = QApplication(sys.argv)
        print("QApplication created successfully")

        # Test config loading
        load_config("settings.json")
        print("Configuration loaded successfully")

        # Try to import MainWindow class
        from fluent_gui import MainWindow
        print("MainWindow imported successfully")

        # Try to create MainWindow instance (this is where it might crash)
        print("Creating MainWindow instance...")
        window = MainWindow()
        print("MainWindow created successfully")

        # Don't show the window to avoid display issues
        # window.show()

        print("Minimal GUI test completed successfully!")
        return True

    except Exception as e:
        print(f"GUI initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gui_minimal()
    sys.exit(0 if success else 1)