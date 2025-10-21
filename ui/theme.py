import logging
from pathlib import Path
from typing import Dict

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QStyle


def get_system_file_icon(icon_type: str = "file") -> QIcon:
    """Return a standard system icon for files, directories, or actions."""
    try:
        app = QApplication.instance()
        if not app:
            return QIcon()

        style = app.style()
        mapping = {
            "file": QStyle.StandardPixmap.SP_FileIcon,
            "dir": QStyle.StandardPixmap.SP_DirIcon,
            "play": QStyle.StandardPixmap.SP_MediaPlay,
        }
        return style.standardIcon(mapping.get(icon_type, QStyle.StandardPixmap.SP_FileIcon))
    except Exception:
        return QIcon()


def get_gz_color(color_key: str, status_colors: Dict[str, str]) -> str:
    """Resolve a brand color using provided status colors with safe fallbacks."""
    fallback_colors = {
        "white": "white",
        "ok": "#10B981",
        "warn": "#F59E0B",
        "fail": "#EF4444",
    }

    if color_key == "white":
        return "white"

    try:
        if status_colors and color_key in status_colors:
            return status_colors[color_key]
    except Exception:
        logging.debug("Failed to read status color '%s' from config", color_key, exc_info=True)

    return fallback_colors.get(color_key, color_key)


def load_gz_media_fonts(app: QApplication, font_family: str, font_size: int) -> None:
    """Apply the configured font family and size to the application."""
    try:
        resolved_family = font_family or "Poppins, Segoe UI, Arial, sans-serif"
        font = QFont(resolved_family)

        try:
            if font_size:
                font.setPointSize(int(font_size))
            else:
                font.setPointSize(10)
        except (TypeError, ValueError):
            font.setPointSize(10)

        app.setFont(font)
        logging.info("GZ Media font applied successfully")
    except Exception as exc:
        logging.warning("Failed to apply GZ Media font, using system default: %s", exc)


def load_gz_media_stylesheet(app: QApplication, stylesheet_path: Path) -> None:
    """Load the configured stylesheet if available."""
    try:
        if stylesheet_path and stylesheet_path.exists():
            with stylesheet_path.open("r", encoding="utf-8") as handle:
                qss_content = handle.read()
            app.setStyleSheet(qss_content)
            logging.info("GZ Media stylesheet loaded successfully")
        else:
            logging.warning("GZ Media stylesheet file not found at %s", stylesheet_path)
    except Exception as exc:
        logging.error("Failed to load GZ Media stylesheet from %s: %s", stylesheet_path, exc)
