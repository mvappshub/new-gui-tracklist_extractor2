from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ToleranceSettings:
    """Duration comparison thresholds controlling WARN and FAIL classifications."""

    warn_tolerance: int
    fail_tolerance: int


@dataclass
class ExportSettings:
    """Settings defining automatic export behaviour."""

    auto_export: bool
    export_dir: Path


@dataclass
class IdExtractionSettings:
    """Settings controlling numeric ID extraction from filenames."""

    min_digits: int
    max_digits: int
    ignore_numbers: list[str]
