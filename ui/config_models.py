from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from config import AppConfig


@dataclass
class ToleranceSettings:
    warn_tolerance: int
    fail_tolerance: int


@dataclass
class ExportSettings:
    auto_export: bool
    export_dir: Path


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


@dataclass
class WorkerSettings:
    pdf_dir: Path
    wav_dir: Path


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


def load_theme_settings(cfg: AppConfig) -> ThemeSettings:
    logo_attr = getattr(cfg, "gz_logo_path", None)
    logo_path = Path(getattr(logo_attr, "value", "assets/gz_logo_white.png"))

    claim_visible_attr = getattr(cfg, "gz_claim_visible", None)
    claim_visible = bool(getattr(claim_visible_attr, "value", True))

    claim_text_attr = getattr(cfg, "gz_claim_text", None)
    claim_text = getattr(claim_text_attr, "value", "Emotions. Materialized.")

    action_color_attr = getattr(cfg, "ui_table_action_bg_color", None)
    action_bg_color = getattr(action_color_attr, "value", "#E0E7FF")

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
    )


def load_worker_settings(cfg: AppConfig) -> WorkerSettings:
    return WorkerSettings(
        pdf_dir=Path(cfg.input_pdf_dir.value),
        wav_dir=Path(cfg.input_wav_dir.value),
    )
