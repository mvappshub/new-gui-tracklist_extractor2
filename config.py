from __future__ import annotations

from pathlib import Path
from typing import Union, Any, List
import json

from PyQt6.QtCore import QSettings


def resolve_path(path: Union[str, Path]) -> Path:
    """Resolve a path relative to the project root directory.

    Args:
        path: Path to resolve, can be relative or absolute

    Returns:
        Absolute path resolved relative to the project root (where config.py is located)
    """
    if not path:
        return Path()

    path_obj = Path(path)

    # If path is already absolute, return it as-is
    if path_obj.is_absolute():
        return path_obj.resolve()

    # Otherwise, resolve relative to the project root (where config.py is located)
    project_root = Path(__file__).resolve().parent
    return (project_root / path_obj).resolve()


class ConfigValue:
    """Wrapper class for configuration values that provides .value attribute and backward compatibility."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __bool__(self):
        return bool(self.value)

    def __eq__(self, other):
        if isinstance(other, ConfigValue):
            return self.value == other.value
        return self.value == other

    def __repr__(self):
        return f"ConfigValue({self.value!r})"

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return self.value[key]

    def __iter__(self):
        return iter(self.value)

    def __contains__(self, item):
        return item in self.value


class AppConfig:
    """Application configuration using QSettings instead of qfluentwidgets QConfig."""

    def __init__(self):
        self.settings = QSettings("GZMedia", "TracklistExtractor")
        self._defaults = {}
        self._validators = {}
        self._init_defaults()

    def _init_defaults(self):
        """Initialize default values and validators for all configuration options."""

        # LLM Configuration
        self._defaults["llm/base_url"] = "https://openrouter.ai/api/v1"
        self._defaults["llm/model"] = "google/gemini-2.5-flash"
        self._validators["llm/model"] = [
            "google/gemini-2.5-flash",
            "qwen/qwen2.5-vl-72b-instruct",
            "anthropic/claude-3-haiku",
            "qwen/qwen2.5-vl-3b-instruct",
            "nousresearch/nous-hermes-2-vision-7b",
            "moonshotai/kimi-vl-a3b-thinking",
            "google/gemini-flash-1.5",
            "qwen/qwen2.5-vl-32b-instruct",
            "opengvlab/internvl3-14b",
            "openai/gpt-4o",
            "mistralai/pixtral-12b",
            "microsoft/phi-4-multimodal-instruct",
            "meta-llama/llama-3.2-90b-vision-instruct",
            "meta-llama/llama-3.2-11b-vision-instruct",
            "google/gemini-pro-1.5",
            "google/gemini-2.5-pro",
            "google/gemini-2.0-flash-001",
            "fireworks/firellava-13b",
            "bytedance/ui-tars-1.5-7b",
            "bytedance-research/ui-tars-72b",
            "baidu/ernie-4.5-vl-424b-a47b",
            "baidu/ernie-4.5-vl-28b-a3b",
            "01-ai/yi-vision",
            "z-ai/glm-4.5v",
            "x-ai/grok-2-vision-1212",
        ]
        self._defaults["llm/alt_models"] = [
            "qwen/qwen2.5-vl-72b-instruct",
            "anthropic/claude-3-haiku",
            "qwen/qwen2.5-vl-3b-instruct",
            "nousresearch/nous-hermes-2-vision-7b",
            "moonshotai/kimi-vl-a3b-thinking",
            "google/gemini-flash-1.5",
            "qwen/qwen2.5-vl-32b-instruct",
            "opengvlab/internvl3-14b",
            "openai/gpt-4o",
            "mistralai/pixtral-12b",
            "microsoft/phi-4-multimodal-instruct",
            "meta-llama/llama-3.2-90b-vision-instruct",
            "meta-llama/llama-3.2-11b-vision-instruct",
            "google/gemini-pro-1.5",
            "google/gemini-2.5-pro",
            "google/gemini-2.0-flash-001",
            "fireworks/firellava-13b",
            "bytedance/ui-tars-1.5-7b",
            "bytedance-research/ui-tars-72b",
            "baidu/ernie-4.5-vl-424b-a47b",
            "baidu/ernie-4.5-vl-28b-a3b",
            "01-ai/yi-vision",
            "z-ai/glm-4.5v",
            "x-ai/grok-2-vision-1212",
        ]
        self._defaults["llm/temperature"] = 0.0
        self._validators["llm/temperature"] = (0.0, 2.0)  # min, max

        # Extract Configuration
        self._defaults["extract/render_dpi"] = 380
        self._validators["extract/render_dpi"] = (72, 600)
        self._defaults["extract/max_side_px"] = 2000
        self._validators["extract/max_side_px"] = (500, 4000)
        self._defaults["extract/image_format"] = "jpeg"
        self._validators["extract/image_format"] = ["jpeg", "png"]
        self._defaults["extract/jpeg_quality"] = 85
        self._validators["extract/jpeg_quality"] = (1, 100)
        self._defaults["extract/use_unsharp"] = True
        self._defaults["extract/use_autocontrast"] = True

        # Prompts Configuration
        self._defaults["prompts/primary"] = (
            "You are a tracklist extractor. Your single purpose is to return STRICT JSON.\n"
            'Schema: { "tracks": [ {"title": string, "side": string, "position": integer, '
            '"duration_seconds": integer, "duration_formatted": "MM:SS" } ] }.\n'
            "Your entire logic is governed by this unbreakable rule:\n"
            "A track is anchored by its duration value (e.g., 4:40, 5m10s). The title is ALL meaningful text visually "
            "associated with that single time value. Combine multi-line text into one title.\n"
            "Follow these steps:\n"
            "Analyze Visual Layout: First, scan the entire image for structure. Identify columns, sections, and distinct visual blocks. "
            "Process multi-column layouts as separate lists.\n"
            "Find the Duration: For each potential track, locate the duration. This might be under a header like Time, Duration, or Length. "
            "If both Start/End times and a Length column exist, always prioritize the Length column.\n"
            "Establish Context: Use headers like SIDE A, Side B:, TAPE FLIP: A, or multi-track prefixes (A1, B-02) to determine the side "
            "and position. The prefix (B-02) is the most reliable source and overrides other context. Position numbering MUST reset for each new side.\n"
            "Strictly Filter: If a block of text has no clear, parsable duration anchored to it, it IS NOT a track. Aggressively ignore "
            "non-track lines: notes, pauses, headers, ISRC codes, credits, empty rows, and total runtimes."
        )
        self._defaults["prompts/user_instructions"] = ""

        # Input/Output Directories
        self._defaults["input/default_dir"] = "./data"
        self._defaults["input/pdf_dir"] = "./data/pdf"
        self._defaults["input/wav_dir"] = "./data/wav"
        self._defaults["export/default_dir"] = "exports"
        self._defaults["export/auto"] = True

        # Analysis Configuration
        self._defaults["analysis/tolerance_warn"] = 2
        self._validators["analysis/tolerance_warn"] = (0, 10)
        self._defaults["analysis/tolerance_fail"] = 5
        self._validators["analysis/tolerance_fail"] = (0, 20)
        self._defaults["analysis/min_id_digits"] = 3
        self._validators["analysis/min_id_digits"] = (1, 10)
        self._defaults["analysis/max_id_digits"] = 6
        self._validators["analysis/max_id_digits"] = (1, 10)
        self._defaults["analysis/ignore_numbers"] = []

        # Waveform Viewer Configuration
        self._defaults["waveform/downsample_factor"] = 10
        self._validators["waveform/downsample_factor"] = (1, 100)
        self._defaults["waveform/default_volume"] = 0.5
        self._validators["waveform/default_volume"] = (0.0, 1.0)
        self._defaults["waveform/waveform_color"] = "#3B82F6"
        self._defaults["waveform/position_line_color"] = "#EF4444"

        # Waveform Editor Configuration
        self._defaults["waveform_editor/overview_points"] = 2000
        self._validators["waveform_editor/overview_points"] = (500, 5000)
        self._defaults["waveform_editor/min_region_duration"] = 0.3
        self._validators["waveform_editor/min_region_duration"] = (0.1, 2.0)
        self._defaults["waveform_editor/snap_tolerance"] = 0.1
        self._validators["waveform_editor/snap_tolerance"] = (0.01, 1.0)
        self._defaults["waveform_editor/enable_snapping"] = True
        self._defaults["waveform_editor/show_pdf_markers"] = True
        self._defaults["waveform_editor/rms_stride_ratio"] = 2
        self._validators["waveform_editor/rms_stride_ratio"] = (1, 10)

        # UI Configuration
        self._defaults["ui/dpi_scale"] = "AUTO"
        self._validators["ui/dpi_scale"] = [1, 1.25, 1.5, 1.75, 2, "AUTO"]
        self._defaults["ui/theme"] = "AUTO"
        self._validators["ui/theme"] = ["AUTO", "DARK", "LIGHT"]
        self._defaults["ui/window_geometry"] = "1720x1440"
        self._defaults["ui/base_font_family"] = "Poppins, Segoe UI, Arial, sans-serif"
        self._defaults["ui/base_font_size"] = 13
        self._validators["ui/base_font_size"] = (8, 24)
        self._defaults["ui/heading_font_size"] = 12
        self._validators["ui/heading_font_size"] = (8, 24)
        self._defaults["ui/treeview_row_height"] = 28
        self._validators["ui/treeview_row_height"] = (20, 50)
        self._defaults["ui/update_interval_ms"] = 50
        self._validators["ui/update_interval_ms"] = (10, 1000)
        self._defaults["ui/total_row_bg_color"] = "#F3F4F6"

        # GZ Media Brand Configuration
        self._defaults["gz_brand/primary_blue"] = "#1E3A8A"
        self._defaults["gz_brand/light_blue"] = "#3B82F6"
        self._defaults["gz_brand/dark"] = "#1F2937"
        self._defaults["gz_brand/light_gray"] = "#757575"
        self._defaults["gz_brand/gray"] = "#6B7280"
        self._defaults["gz_brand/logo_path"] = "assets/gz_logo_white.png"

        self._defaults["gz_brand/claim_visible"] = True

        # Status Colors
        self._defaults["gz_status/ok_color"] = "#10B981"
        self._defaults["gz_status/warn_color"] = "#F59E0B"
        self._defaults["gz_status/fail_color"] = "#EF4444"

        # Dark Mode Colors
        self._defaults["dark_mode/background"] = "#1F2937"
        self._defaults["dark_mode/surface"] = "#374151"
        self._defaults["dark_mode/text"] = "#F9FAFB"
        self._defaults["dark_mode/text_secondary"] = "#D1D5DB"
        self._defaults["dark_mode/accent"] = "#3B82F6"

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if default is None and key in self._defaults:
            default = self._defaults[key]

        if self.settings.contains(key):
            try:
                value = self.settings.value(key)
            except TypeError:
                return default
            # Convert string representations back to appropriate types
            if isinstance(default, bool) and isinstance(value, str):
                return value.lower() in ("true", "1", "yes", "on")

            # Determine if value looks like a JSON list even when default is None
            is_json_like_string = (
                isinstance(value, str) and value.strip().startswith("[") and value.strip().endswith("]")
            )
            if (isinstance(default, list) or (default is None and is_json_like_string)) and isinstance(value, str):
                try:
                    return json.loads(value)
                except (json.JSONDecodeError, ValueError):
                    # Return default if provided, else original string value
                    return default if default is not None else value

            if isinstance(default, int) and isinstance(value, str):
                try:
                    return int(value)
                except ValueError:
                    return default
            if isinstance(default, float) and isinstance(value, str):
                try:
                    return float(value)
                except ValueError:
                    return default
            return value
        return default

    def get_value(self, key: str) -> ConfigValue:
        """Get a configuration value wrapped in ConfigValue for .value access pattern."""
        value = self.get(key)
        return ConfigValue(value)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value with validation."""
        self._validate_value(key, value)

        if isinstance(value, (list, dict)):
            self.settings.setValue(key, json.dumps(value))
        else:
            self.settings.setValue(key, value)

    def _validate_value(self, key: str, value: Any) -> None:
        """Validate a configuration value."""
        if key not in self._defaults:
            return  # Allow unknown keys

        if key in self._validators:
            validator = self._validators[key]

            # Options validation (list of allowed values)
            if isinstance(validator, list):
                if value not in validator:
                    raise ValueError(f"Invalid value '{value}' for {key}. Must be one of: {validator}")
            # Range validation (min, max tuple)
            elif isinstance(validator, tuple) and len(validator) == 2:
                min_val, max_val = validator
                if not (min_val <= value <= max_val):
                    raise ValueError(f"Value '{value}' for {key} must be between {min_val} and {max_val}")

    def reset_to_defaults(self) -> None:
        """Reset all settings to their default values."""
        for key, default_value in self._defaults.items():
            self.set(key, default_value)

    def save(self) -> None:
        """Save settings to disk."""
        self.settings.sync()

    def load(self, file_path: Union[str, Path]) -> None:
        """Load settings from a specific file path."""
        # For QSettings, we can't directly load from a specific file
        # but we can check if the file exists and import its contents
        file_path = Path(file_path)
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        self.set(key, value)
            except (json.JSONDecodeError, IOError):
                pass  # Ignore errors when loading

    def get_all_keys(self) -> List[str]:
        """Get all configuration keys."""
        return list(self._defaults.keys())

    def get_default(self, key: str) -> Any:
        """Get the default value for a key."""
        return self._defaults.get(key)

    def has_key(self, key: str) -> bool:
        """Check if a key exists in the configuration."""
        return key in self._defaults

    def remove(self, key: str) -> None:
        """Remove a configuration key."""
        if self.settings.contains(key):
            self.settings.remove(key)

    def clear(self) -> None:
        """Clear all settings."""
        for key in self._defaults.keys():
            if self.settings.contains(key):
                self.settings.remove(key)

    # Property accessors for backward compatibility
    @property
    def file(self) -> str:
        """Get the settings file path."""
        return self.settings.fileName()

    # Convenience properties for commonly used settings
    @property
    def llm_base_url(self) -> ConfigValue:
        return self.get_value("llm/base_url")

    @llm_base_url.setter
    def llm_base_url(self, value: str) -> None:
        self.set("llm/base_url", value)

    @property
    def llm_model(self) -> ConfigValue:
        return self.get_value("llm/model")

    @llm_model.setter
    def llm_model(self, value: str) -> None:
        self.set("llm/model", value)

    @property
    def llm_temperature(self) -> ConfigValue:
        return self.get_value("llm/temperature")

    @llm_temperature.setter
    def llm_temperature(self, value: float) -> None:
        self.set("llm/temperature", value)

    @property
    def input_pdf_dir(self) -> ConfigValue:
        """Get PDF input directory, resolved relative to project root."""
        path_value = self.get("input/pdf_dir")
        if path_value:
            resolved_path = resolve_path(path_value)
            return ConfigValue(str(resolved_path))
        return self.get_value("input/pdf_dir")

    @input_pdf_dir.setter
    def input_pdf_dir(self, value: str) -> None:
        """Set PDF input directory and validate it exists."""
        if value:
            resolved_path = resolve_path(value)
            if not resolved_path.exists():
                resolved_path.mkdir(parents=True, exist_ok=True)
            elif not resolved_path.is_dir():
                raise ValueError(f"PDF path is not a directory: {resolved_path}")
        self.set("input/pdf_dir", value)

    @property
    def input_wav_dir(self) -> ConfigValue:
        """Get WAV input directory, resolved relative to project root."""
        path_value = self.get("input/wav_dir")
        if path_value:
            resolved_path = resolve_path(path_value)
            return ConfigValue(str(resolved_path))
        return self.get_value("input/wav_dir")

    @input_wav_dir.setter
    def input_wav_dir(self, value: str) -> None:
        """Set WAV input directory and validate it exists."""
        if value:
            resolved_path = resolve_path(value)
            if not resolved_path.exists():
                resolved_path.mkdir(parents=True, exist_ok=True)
            elif not resolved_path.is_dir():
                raise ValueError(f"WAV path is not a directory: {resolved_path}")
        self.set("input/wav_dir", value)

    @property
    def export_default_dir(self) -> ConfigValue:
        """Get export directory, resolved relative to project root."""
        path_value = self.get("export/default_dir")
        if path_value:
            resolved_path = resolve_path(path_value)
            return ConfigValue(str(resolved_path))
        return self.get_value("export/default_dir")

    @export_default_dir.setter
    def export_default_dir(self, value: str) -> None:
        """Set export directory path."""
        if hasattr(value, "value"):
            value = getattr(value, "value")
        if value:
            value = str(resolve_path(value))
        self.set("export/default_dir", value)

    @export_default_dir.deleter
    def export_default_dir(self) -> None:
        default = self._defaults.get("export/default_dir", "")
        self.set("export/default_dir", default)

    @property
    def export_auto(self) -> ConfigValue:
        return self.get_value("export/auto")

    @export_auto.setter
    def export_auto(self, value: bool) -> None:
        if hasattr(value, "value"):
            value = getattr(value, "value")
        self.set("export/auto", bool(value))

    @export_auto.deleter
    def export_auto(self) -> None:
        default = self._defaults.get("export/auto", False)
        self.set("export/auto", default)

    @property
    def analysis_tolerance_warn(self) -> ConfigValue:
        return self.get_value("analysis/tolerance_warn")

    @analysis_tolerance_warn.setter
    def analysis_tolerance_warn(self, value: int) -> None:
        self.set("analysis/tolerance_warn", value)

    @property
    def analysis_tolerance_fail(self) -> ConfigValue:
        return self.get_value("analysis/tolerance_fail")

    @analysis_tolerance_fail.setter
    def analysis_tolerance_fail(self, value: int) -> None:
        self.set("analysis/tolerance_fail", value)

    @property
    def analysis_min_id_digits(self) -> ConfigValue:
        return self.get_value("analysis/min_id_digits")

    @analysis_min_id_digits.setter
    def analysis_min_id_digits(self, value: int) -> None:
        self.set("analysis/min_id_digits", value)

    @property
    def analysis_max_id_digits(self) -> ConfigValue:
        return self.get_value("analysis/max_id_digits")

    @analysis_max_id_digits.setter
    def analysis_max_id_digits(self, value: int) -> None:
        self.set("analysis/max_id_digits", value)

    @property
    def analysis_ignore_numbers(self) -> ConfigValue:
        return self.get_value("analysis/ignore_numbers")

    @analysis_ignore_numbers.setter
    def analysis_ignore_numbers(self, value: list) -> None:
        self.set("analysis/ignore_numbers", value)

    @property
    def waveform_downsample_factor(self) -> ConfigValue:
        return self.get_value("waveform/downsample_factor")

    @waveform_downsample_factor.setter
    def waveform_downsample_factor(self, value: int) -> None:
        self.set("waveform/downsample_factor", value)

    @property
    def waveform_default_volume(self) -> ConfigValue:
        return self.get_value("waveform/default_volume")

    @waveform_default_volume.setter
    def waveform_default_volume(self, value: float) -> None:
        self.set("waveform/default_volume", value)

    @property
    def waveform_waveform_color(self) -> ConfigValue:
        return self.get_value("waveform/waveform_color")

    @waveform_waveform_color.setter
    def waveform_waveform_color(self, value: str) -> None:
        self.set("waveform/waveform_color", value)

    @property
    def waveform_position_line_color(self) -> ConfigValue:
        return self.get_value("waveform/position_line_color")

    @waveform_position_line_color.setter
    def waveform_position_line_color(self, value: str) -> None:
        self.set("waveform/position_line_color", value)

    @property
    def ui_dpi_scale(self) -> ConfigValue:
        return self.get_value("ui/dpi_scale")

    @ui_dpi_scale.setter
    def ui_dpi_scale(self, value: str) -> None:
        self.set("ui/dpi_scale", value)

    @property
    def ui_theme(self) -> ConfigValue:
        return self.get_value("ui/theme")

    @ui_theme.setter
    def ui_theme(self, value: str) -> None:
        self.set("ui/theme", value)

    @property
    def ui_base_font_size(self) -> ConfigValue:
        return self.get_value("ui/base_font_size")

    @ui_base_font_size.setter
    def ui_base_font_size(self, value: int) -> None:
        self.set("ui/base_font_size", value)

    @property
    def ui_base_font_family(self) -> ConfigValue:
        return self.get_value("ui/base_font_family")

    @ui_base_font_family.setter
    def ui_base_font_family(self, value: str) -> None:
        self.set("ui/base_font_family", value)

    @property
    def ui_heading_font_size(self) -> ConfigValue:
        return self.get_value("ui/heading_font_size")

    @ui_heading_font_size.setter
    def ui_heading_font_size(self, value: int) -> None:
        self.set("ui/heading_font_size", value)

    @property
    def ui_treeview_row_height(self) -> ConfigValue:
        return self.get_value("ui/treeview_row_height")

    @ui_treeview_row_height.setter
    def ui_treeview_row_height(self, value: int) -> None:
        self.set("ui/treeview_row_height", value)

    @property
    def ui_update_interval_ms(self) -> ConfigValue:
        return self.get_value("ui/update_interval_ms")

    @ui_update_interval_ms.setter
    def ui_update_interval_ms(self, value: int) -> None:
        self.set("ui/update_interval_ms", value)

    @property
    def ui_total_row_bg_color(self) -> ConfigValue:
        return self.get_value("ui/total_row_bg_color")

    @ui_total_row_bg_color.setter
    def ui_total_row_bg_color(self, value: str) -> None:
        self.set("ui/total_row_bg_color", value)

    @property
    def ui_window_geometry(self) -> ConfigValue:
        return self.get_value("ui/window_geometry")

    @ui_window_geometry.setter
    def ui_window_geometry(self, value: str) -> None:
        self.set("ui/window_geometry", value)

    @property
    def gz_logo_path(self) -> ConfigValue:
        return self.get_value("gz_brand/logo_path")

    @gz_logo_path.setter
    def gz_logo_path(self, value: str) -> None:
        self.set("gz_brand/logo_path", value)

    @property
    def gz_claim_visible(self) -> ConfigValue:
        return self.get_value("gz_brand/claim_visible")

    @gz_claim_visible.setter
    def gz_claim_visible(self, value: bool) -> None:
        self.set("gz_brand/claim_visible", value)

    @property
    def gz_claim_text(self) -> ConfigValue:
        return self.get_value("gz_brand/claim_text")

    @gz_claim_text.setter
    def gz_claim_text(self, value: str) -> None:
        self.set("gz_brand/claim_text", value)

    @property
    def gz_status_ok_color(self) -> ConfigValue:
        return self.get_value("gz_status/ok_color")

    @gz_status_ok_color.setter
    def gz_status_ok_color(self, value: str) -> None:
        self.set("gz_status/ok_color", value)

    @property
    def gz_status_warn_color(self) -> ConfigValue:
        return self.get_value("gz_status/warn_color")

    @gz_status_warn_color.setter
    def gz_status_warn_color(self, value: str) -> None:
        self.set("gz_status/warn_color", value)

    @property
    def gz_status_fail_color(self) -> ConfigValue:
        return self.get_value("gz_status/fail_color")

    @gz_status_fail_color.setter
    def gz_status_fail_color(self, value: str) -> None:
        self.set("gz_status/fail_color", value)


cfg = AppConfig()


def load_config(file_path: Union[str, Path]) -> AppConfig:
    """Load configuration from a JSON file."""
    cfg.load(file_path)
    return cfg


def save_config(file_path: Union[str, Path]) -> None:
    """Save current configuration to a JSON file."""
    file_path = Path(file_path)
    config_data = {}

    for key in cfg.get_all_keys():
        config_data[key] = cfg.get(key)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
