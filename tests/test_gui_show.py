#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from config import load_config

def test_gui_show():
    """Test GUI show functionality."""
    print("Testing GUI show functionality...")

    try:
        # Test QApplication creation
        app = QApplication(sys.argv)
        print("QApplication created successfully")

        # Test config loading
        load_config("settings.json")
        print("Configuration loaded successfully")

        # Import and create MainWindow
        from fluent_gui import MainWindow
        print("MainWindow imported successfully")

        print("Creating MainWindow instance...")
        window = MainWindow()
        print("MainWindow created successfully")

        # Try to show the window (this might cause the crash)
        print("Showing MainWindow...")
        window.show()
        print("MainWindow shown successfully")

        print("GUI show test completed successfully!")
        print("Close the window to exit...")
        return app.exec()

    except Exception as e:
        print(f"GUI show error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(test_gui_show())