from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from config import AppConfig
from core.models.settings import (
    ExportSettings,
    IdExtractionSettings,
    ToleranceSettings,
)

# NOTE: Only application entry points should import the global cfg object.
# Other layers construct settings via these dataclasses and receive them via DI.


@dataclass
class PathSettings:
    pdf_dir: Path
    wav_dir: Path


@dataclass
class ThemeSettings:
    font_family: str
    font_size: int
    stylesheet_path: Path
    status_colors: Dict[str, str]
    logo_path: Path
    claim_visible: bool
    claim_text: str
    action_bg_color: str
    total_row_bg_color: str
    theme_variant: str


@dataclass
class WorkerSettings:
    pdf_dir: Path
    wav_dir: Path


@dataclass
class WaveformSettings:
    """Settings controlling waveform viewer/editor behavior."""

    overview_points: int
    min_region_duration: float
    snap_tolerance: float
    enable_snapping: bool
    default_volume: float
    waveform_color: str
    position_line_color: str
    downsample_factor: int


def load_tolerance_settings(cfg: AppConfig) -> ToleranceSettings:
    return ToleranceSettings(
        warn_tolerance=cfg.analysis_tolerance_warn.value,
        fail_tolerance=cfg.analysis_tolerance_fail.value,
    )


def load_export_settings(cfg: AppConfig) -> ExportSettings:
    return ExportSettings(
        auto_export=cfg.export_auto.value,
        export_dir=Path(cfg.export_default_dir.value),
    )


def load_path_settings(cfg: AppConfig) -> PathSettings:
    return PathSettings(
        pdf_dir=Path(cfg.input_pdf_dir.value),
        wav_dir=Path(cfg.input_wav_dir.value),
    )


def load_id_extraction_settings(cfg: AppConfig) -> IdExtractionSettings:
    """Load numeric ID extraction settings from application configuration."""

    def _safe_int(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    min_digits = _safe_int(cfg.analysis_min_id_digits.value, default=1)
    max_digits = _safe_int(cfg.analysis_max_id_digits.value, default=min_digits)
    # Normalize so downstream code can assume min_digits <= max_digits.
    if min_digits > max_digits:
        min_digits, max_digits = max_digits, min_digits

    raw_ignore = cfg.analysis_ignore_numbers.value or []
    ignore_numbers: list[str] = []
    seen: set[str] = set()
    for item in raw_ignore:
        if item is None:
            continue
        candidate = str(item).strip()
        if not candidate:
            continue
        if candidate not in seen:
            ignore_numbers.append(candidate)
            seen.add(candidate)
        if candidate.isdigit():
            normalized = str(int(candidate))
            if normalized not in seen:
                ignore_numbers.append(normalized)
                seen.add(normalized)

    return IdExtractionSettings(
        min_digits=min_digits,
        max_digits=max_digits,
        ignore_numbers=ignore_numbers,
    )


def load_theme_settings(cfg: AppConfig) -> ThemeSettings:
    logo_attr = getattr(cfg, "gz_logo_path", None)
    logo_path = Path(getattr(logo_attr, "value", "assets/gz_logo_white.png"))

    def _detect_auto_theme() -> str:
        try:
            from PyQt6.QtGui import QPalette
            from PyQt6.QtWidgets import QApplication
        except Exception:
            return "light"

        app = QApplication.instance()
        if app is None:
            return "light"

        palette = app.palette()
        window_color = palette.color(QPalette.ColorRole.Window)
        text_color = palette.color(QPalette.ColorRole.WindowText)
        try:
            if window_color.lightnessF() < text_color.lightnessF():
                return "dark"
        except AttributeError:
            if window_color.value() < text_color.value():
                return "dark"
        return "light"

    claim_visible_attr = getattr(cfg, "gz_claim_visible", None)
    claim_visible = bool(getattr(claim_visible_attr, "value", True))

    claim_text_attr = getattr(cfg, "gz_claim_text", None)
    claim_text = getattr(claim_text_attr, "value", "Emotions. Materialized.")

    action_color_attr = getattr(cfg, "ui_table_action_bg_color", None)
    action_bg_color = getattr(action_color_attr, "value", "#E0E7FF")

    total_row_bg_color = cfg.get("ui/total_row_bg_color", "#F3F4F6")

    raw_theme = str(getattr(cfg.ui_theme, "value", "") or "").strip().lower()
    theme_map = {"dark": "dark", "light": "light"}
    if raw_theme in theme_map:
        theme_variant = theme_map[raw_theme]
    elif raw_theme == "auto":
        theme_variant = _detect_auto_theme()
    else:
        theme_variant = "light"

    return ThemeSettings(
        font_family=cfg.ui_base_font_family.value,
        font_size=cfg.ui_base_font_size.value,
        stylesheet_path=Path("gz_media.qss"),
        status_colors={
            "ok": cfg.gz_status_ok_color.value,
            "warn": cfg.gz_status_warn_color.value,
            "fail": cfg.gz_status_fail_color.value,
        },
        logo_path=logo_path,
        claim_visible=claim_visible,
        claim_text=claim_text,
        action_bg_color=action_bg_color,
        total_row_bg_color=total_row_bg_color,
        theme_variant=theme_variant,
    )


def load_worker_settings(cfg: AppConfig) -> WorkerSettings:
    return WorkerSettings(
        pdf_dir=Path(cfg.input_pdf_dir.value),
        wav_dir=Path(cfg.input_wav_dir.value),
    )


def load_waveform_settings(cfg: AppConfig) -> WaveformSettings:
    """Load waveform viewer/editor settings from application configuration."""

    def _get_with_default(key: str, default: Any) -> Any:
        try:
            return cfg.get(key, default)
        except Exception:
            return default

    def _to_int(value: Any, default: int) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _to_float(value: Any, default: float) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    overview_points = _to_int(
        _get_with_default("waveform_editor/overview_points", 2000),
        default=2000,
    )
    min_region_duration = _to_float(
        _get_with_default("waveform_editor/min_region_duration", 0.3),
        default=0.3,
    )
    snap_tolerance = _to_float(
        _get_with_default("waveform_editor/snap_tolerance", 0.1),
        default=0.1,
    )
    enable_snapping = bool(_get_with_default("waveform_editor/enable_snapping", True))
    default_volume = _to_float(getattr(cfg.waveform_default_volume, "value", 0.5), 0.5)
    waveform_color = str(_get_with_default("waveform/waveform_color", "#3B82F6") or "#3B82F6")
    position_line_color = str(_get_with_default("waveform/position_line_color", "#EF4444") or "#EF4444")
    downsample_factor = _to_int(
        getattr(cfg.waveform_downsample_factor, "value", 10),
        default=10,
    )

    return WaveformSettings(
        overview_points=max(1, overview_points),
        min_region_duration=max(0.0, min_region_duration),
        snap_tolerance=max(0.0, snap_tolerance),
        enable_snapping=enable_snapping,
        default_volume=max(0.0, min(1.0, default_volume)),
        waveform_color=waveform_color,
        position_line_color=position_line_color,
        downsample_factor=max(1, downsample_factor),
    )
