from __future__ import annotations


from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QSlider,
    QPushButton,
    QLineEdit,
    QMessageBox,
    QFileDialog,
    QScrollArea,
    QFrame,
)

from config import cfg, save_config


# NOTE: Directory config items are plain strings; using a single-folder card keeps
# the current typing without switching to list-based FolderListSettingCard.
class FolderSettingCard(QWidget):
    """Single-folder selector implemented with standard PyQt6 components."""

    def __init__(
        self,
        config_item,
        title: str,
        content: str | None = None,
        directory: str = "./",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.config_item = config_item
        self._dialog_directory = directory

        # Create main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        # Title label
        if title:
            title_label = QLabel(title)
            title_font = title_label.font()
            title_font.setBold(True)
            title_label.setFont(title_font)
            layout.addWidget(title_label)

        # Content label
        if content:
            content_label = QLabel(content)
            content_label.setStyleSheet("color: gray;")
            layout.addWidget(content_label)

        # Input controls layout
        controls_layout = QHBoxLayout()

        self.path_input = QLineEdit(self)
        self.path_input.setMinimumWidth(520)
        self.path_input.setClearButtonEnabled(True)
        self.path_input.editingFinished.connect(self._on_edit_finished)
        controls_layout.addWidget(self.path_input, 1)

        controls_layout.addSpacing(12)

        self.browse_button = QPushButton(self)
        self.browse_button.setText(self.tr("Browse"))
        self.browse_button.setFixedWidth(120)
        self.browse_button.clicked.connect(self._on_browse)
        controls_layout.addWidget(self.browse_button)

        layout.addLayout(controls_layout)

        # Set initial path
        self.set_path(
            cfg.get("input/pdf_dir")
            if config_item == cfg.input_pdf_dir
            else cfg.get("input/wav_dir")
            if config_item == cfg.input_wav_dir
            else cfg.get("export/default_dir")
            if config_item == cfg.export_default_dir
            else "",
            update_config=False,
        )

    def set_path(self, path: str, update_config: bool = True) -> None:
        normalized = path or ""
        if self.path_input.text() != normalized:
            self.path_input.blockSignals(True)
            self.path_input.setText(normalized)
            self.path_input.blockSignals(False)

    def _on_edit_finished(self) -> None:
        # Update config when editing is finished
        path = self.path_input.text().strip()
        if self.config_item == cfg.input_pdf_dir:
            cfg.set("input/pdf_dir", path)
        elif self.config_item == cfg.input_wav_dir:
            cfg.set("input/wav_dir", path)
        elif self.config_item == cfg.export_default_dir:
            cfg.set("export/default_dir", path)

    def _on_browse(self) -> None:
        current = self.path_input.text().strip() or self._dialog_directory
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"), current)
        if folder:
            self.set_path(folder)
            if self.config_item == cfg.input_pdf_dir:
                cfg.set("input/pdf_dir", folder)
            elif self.config_item == cfg.input_wav_dir:
                cfg.set("input/wav_dir", folder)
            elif self.config_item == cfg.export_default_dir:
                cfg.set("export/default_dir", folder)


class SettingsPage(QWidget):
    """Application settings interface."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("settingsPage")

        self._init_ui()
        self._sync_from_config()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.scroll = QScrollArea(self)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)  # No frame
        self.scroll.setWidgetResizable(True)
        layout.addWidget(self.scroll)

        self.container = QWidget()
        self.scroll.setWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(24, 24, 24, 24)
        self.container_layout.setSpacing(16)

        self._build_ui_group()
        self._build_model_group()
        self._build_paths_group()
        self._build_analysis_group()
        self._build_waveform_group()
        self._build_actions_group()

        self.container_layout.addStretch(1)

    def _build_ui_group(self) -> None:
        group = QGroupBox("User Interface", self.container)
        group_layout = QVBoxLayout(group)

        # Interface scaling
        scale_layout = QHBoxLayout()
        scale_label = QLabel("Interface scaling:")
        scale_label.setFixedWidth(150)
        scale_layout.addWidget(scale_label)

        self.scale_combo = QComboBox()
        self.scale_combo.addItems(["100%", "125%", "150%", "175%", "200%", "Follow system"])
        # Set current value
        current_scale = cfg.ui_dpi_scale.value if hasattr(cfg.ui_dpi_scale, "value") else cfg.ui_dpi_scale or "AUTO"
        scale_index = self.scale_combo.findText(current_scale)
        if scale_index >= 0:
            self.scale_combo.setCurrentIndex(scale_index)
        self.scale_combo.currentTextChanged.connect(self._on_scale_changed)
        scale_layout.addWidget(self.scale_combo)

        scale_layout.addStretch()
        group_layout.addLayout(scale_layout)

        self.container_layout.addWidget(group)

    def _build_waveform_group(self) -> None:
        group = QGroupBox("Waveform Viewer", self.container)
        group_layout = QVBoxLayout(group)

        # Downsample factor slider
        downsample_layout = QHBoxLayout()
        downsample_label = QLabel("Display quality:")
        downsample_label.setFixedWidth(150)
        downsample_layout.addWidget(downsample_label)

        self.downsample_slider = QSlider(Qt.Orientation.Horizontal)
        self.downsample_slider.setMinimum(1)
        self.downsample_slider.setMaximum(100)
        downsample_value = (
            cfg.waveform_downsample_factor.value
            if hasattr(cfg.waveform_downsample_factor, "value")
            else cfg.get("waveform/downsample_factor")
        )
        downsample_value = int(downsample_value or 10)
        self.downsample_slider.setValue(downsample_value)
        self.downsample_slider.setFixedWidth(200)
        downsample_layout.addWidget(self.downsample_slider)

        self.downsample_value_label = QLabel(f"{downsample_value}x")
        self.downsample_value_label.setFixedWidth(40)
        self.downsample_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        downsample_layout.addWidget(self.downsample_value_label)
        downsample_layout.addStretch()

        self.downsample_slider.valueChanged.connect(self._on_downsample_changed)
        group_layout.addLayout(downsample_layout)

        # Default volume slider
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Default volume:")
        volume_label.setFixedWidth(150)
        volume_layout.addWidget(volume_label)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        volume_value = (
            cfg.waveform_default_volume.value
            if hasattr(cfg.waveform_default_volume, "value")
            else cfg.get("waveform/default_volume")
        )
        volume_percentage = int(float(volume_value or 0.5) * 100)
        self.volume_slider.setValue(volume_percentage)
        self.volume_slider.setFixedWidth(200)
        volume_layout.addWidget(self.volume_slider)

        self.volume_value_label = QLabel(f"{volume_percentage}%")
        self.volume_value_label.setFixedWidth(40)
        self.volume_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        volume_layout.addWidget(self.volume_value_label)
        volume_layout.addStretch()

        self.volume_slider.valueChanged.connect(self._on_volume_changed)
        group_layout.addLayout(volume_layout)

        self.container_layout.addWidget(group)

    def _build_model_group(self) -> None:
        group = QGroupBox("Model Configuration", self.container)
        group_layout = QVBoxLayout(group)

        # Primary model selection
        model_layout = QHBoxLayout()
        model_label = QLabel("Primary model:")
        model_label.setFixedWidth(150)
        model_layout.addWidget(model_label)

        self.model_combo = QComboBox()
        # Use hardcoded model list from config validators
        model_options = [
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
        self.model_combo.addItems(model_options)

        # Set current value
        current_model = (
            cfg.llm_model.value if hasattr(cfg.llm_model, "value") else cfg.llm_model or "google/gemini-2.5-flash"
        )
        model_index = self.model_combo.findText(current_model)
        if model_index >= 0:
            self.model_combo.setCurrentIndex(model_index)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        model_layout.addWidget(self.model_combo)

        model_layout.addStretch()
        group_layout.addLayout(model_layout)

        self.container_layout.addWidget(group)

    def _build_paths_group(self) -> None:
        group = QGroupBox("Directory Paths", self.container)
        group_layout = QVBoxLayout(group)

        self.pdf_dir_card = FolderSettingCard(
            cfg.input_pdf_dir,
            "PDF input directory",
            "Folder scanned for tracklist PDF files.",
            parent=group,
        )
        group_layout.addWidget(self.pdf_dir_card)

        self.wav_dir_card = FolderSettingCard(
            cfg.input_wav_dir,
            "WAV input directory",
            "Folder containing mastered WAV files.",
            parent=group,
        )
        group_layout.addWidget(self.wav_dir_card)

        self.export_dir_card = FolderSettingCard(
            cfg.export_default_dir,
            "Export directory",
            "Destination directory for generated reports.",
            parent=group,
        )
        group_layout.addWidget(self.export_dir_card)

        self.container_layout.addWidget(group)

    def _build_analysis_group(self) -> None:
        group = QGroupBox("Analysis Configuration", self.container)
        group_layout = QVBoxLayout(group)

        # Warning tolerance
        warn_layout = QHBoxLayout()
        warn_label = QLabel("Warning tolerance:")
        warn_label.setFixedWidth(150)
        warn_layout.addWidget(warn_label)

        self.warn_slider = QSlider(Qt.Orientation.Horizontal)
        self.warn_slider.setMinimum(1)
        self.warn_slider.setMaximum(10)
        warn_value = (
            cfg.analysis_tolerance_warn.value
            if hasattr(cfg.analysis_tolerance_warn, "value")
            else cfg.analysis_tolerance_warn or 2
        )
        self.warn_slider.setValue(warn_value)
        self.warn_slider.setFixedWidth(200)
        warn_layout.addWidget(self.warn_slider)

        self.warn_value_label = QLabel(f"{self.warn_slider.value()}s")
        self.warn_value_label.setFixedWidth(30)
        self.warn_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        warn_layout.addWidget(self.warn_value_label)

        warn_layout.addStretch()
        self.warn_slider.valueChanged.connect(self._on_warn_value_changed)
        group_layout.addLayout(warn_layout)

        # Failure tolerance
        fail_layout = QHBoxLayout()
        fail_label = QLabel("Failure tolerance:")
        fail_label.setFixedWidth(150)
        fail_layout.addWidget(fail_label)

        self.fail_slider = QSlider(Qt.Orientation.Horizontal)
        self.fail_slider.setMinimum(1)
        self.fail_slider.setMaximum(20)
        fail_value = (
            cfg.analysis_tolerance_fail.value
            if hasattr(cfg.analysis_tolerance_fail, "value")
            else cfg.analysis_tolerance_fail or 5
        )
        self.fail_slider.setValue(fail_value)
        self.fail_slider.setFixedWidth(200)
        fail_layout.addWidget(self.fail_slider)

        self.fail_value_label = QLabel(f"{self.fail_slider.value()}s")
        self.fail_value_label.setFixedWidth(30)
        self.fail_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        fail_layout.addWidget(self.fail_value_label)

        fail_layout.addStretch()
        self.fail_slider.valueChanged.connect(self._on_fail_value_changed)
        group_layout.addLayout(fail_layout)

        self.container_layout.addWidget(group)

    def _build_actions_group(self) -> None:
        group = QGroupBox("Actions", self.container)
        group_layout = QVBoxLayout(group)

        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self._save_settings)
        group_layout.addWidget(self.save_button)

        # Reload button
        self.reload_button = QPushButton("Reload Settings")
        self.reload_button.setFixedHeight(40)
        self.reload_button.clicked.connect(self._reload_settings)
        group_layout.addWidget(self.reload_button)

        # Reset button
        self.reset_button = QPushButton("Reset to defaults")
        self.reset_button.setFixedHeight(40)
        self.reset_button.clicked.connect(self._reset_settings)
        group_layout.addWidget(self.reset_button)

        self.container_layout.addWidget(group)

    def _on_scale_changed(self, value: str) -> None:
        """Handle UI scale changes."""
        cfg.set("ui/dpi_scale", value)

    def _on_model_changed(self, value: str) -> None:
        """Handle model selection changes."""
        cfg.set("llm/model", value)

    def _on_warn_value_changed(self, value: int) -> None:
        """Handle warning tolerance changes."""
        self.warn_value_label.setText(f"{value}s")
        cfg.set("analysis/tolerance_warn", value)

    def _on_fail_value_changed(self, value: int) -> None:
        """Handle failure tolerance changes."""
        self.fail_value_label.setText(f"{value}s")
        cfg.set("analysis/tolerance_fail", value)

    def _on_downsample_changed(self, value: int) -> None:
        """Handle waveform downsample changes."""
        if hasattr(self, "downsample_value_label"):
            self.downsample_value_label.setText(f"{value}x")
        cfg.set("waveform/downsample_factor", int(value))

    def _on_volume_changed(self, value: int) -> None:
        """Handle waveform default volume changes."""
        if hasattr(self, "volume_value_label"):
            self.volume_value_label.setText(f"{value}%")
        cfg.set("waveform/default_volume", value / 100.0)

    def _save_settings(self) -> None:
        try:
            from fluent_gui import SETTINGS_FILENAME

            save_config(SETTINGS_FILENAME)
            self._show_message("Settings saved", "Configuration saved successfully.", "info")
        except Exception as error:  # pragma: no cover - UI feedback path
            self._show_message("Save failed", str(error), "error")

    def _reload_settings(self) -> None:
        try:
            # QSettings automatically persists; sync to reload from disk
            cfg.settings.sync()
            self._sync_from_config()
            self._show_message("Settings reloaded", "Configuration reloaded from disk.", "info")
        except Exception as error:  # pragma: no cover - UI feedback path
            self._show_message("Reload failed", str(error), "error")

    def _reset_settings(self) -> None:
        reply = QMessageBox.question(
            self,
            "Reset settings",
            "This will restore all settings to their default values.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        cfg.reset_to_defaults()
        from fluent_gui import SETTINGS_FILENAME

        save_config(SETTINGS_FILENAME)

        try:
            cfg.save()
        except Exception as error:
            self._show_message("Reset failed", str(error), "error")
            return

        self._sync_from_config()
        self._show_message("Defaults restored", "All settings were reset to defaults.", "info")
        self._reenable_widgets()

    def _reenable_widgets(self) -> None:
        scroll = getattr(self, "scroll", None)
        if scroll is not None:
            scroll.setEnabled(True)
            viewport = scroll.viewport()
            if viewport is not None:
                viewport.setEnabled(True)
        container = getattr(self, "container", None)
        if container is not None:
            container.setEnabled(True)

    def _sync_from_config(self) -> None:
        # Update folder cards
        if hasattr(self, "pdf_dir_card"):
            pdf_value = (
                cfg.input_pdf_dir.value if hasattr(cfg.input_pdf_dir, "value") else cfg.input_pdf_dir or "./data/pdf"
            )
            self.pdf_dir_card.set_path(self._coerce_folder(pdf_value), update_config=False)

        if hasattr(self, "wav_dir_card"):
            wav_value = (
                cfg.input_wav_dir.value if hasattr(cfg.input_wav_dir, "value") else cfg.input_wav_dir or "./data/wav"
            )
            self.wav_dir_card.set_path(self._coerce_folder(wav_value), update_config=False)

        if hasattr(self, "export_dir_card"):
            export_value = (
                cfg.export_default_dir.value
                if hasattr(cfg.export_default_dir, "value")
                else cfg.export_default_dir or "exports"
            )
            self.export_dir_card.set_path(self._coerce_folder(export_value), update_config=False)

        # Update combo boxes
        if hasattr(self, "scale_combo"):
            scale_value = cfg.ui_dpi_scale.value if hasattr(cfg.ui_dpi_scale, "value") else cfg.ui_dpi_scale or "AUTO"
            scale_index = self.scale_combo.findText(scale_value)
            if scale_index >= 0:
                self.scale_combo.setCurrentIndex(scale_index)

        if hasattr(self, "model_combo"):
            model_value = (
                cfg.llm_model.value if hasattr(cfg.llm_model, "value") else cfg.llm_model or "google/gemini-2.5-flash"
            )
            model_index = self.model_combo.findText(model_value)
            if model_index >= 0:
                self.model_combo.setCurrentIndex(model_index)

        # Update sliders
        if hasattr(self, "warn_slider"):
            warn_value = (
                cfg.analysis_tolerance_warn.value
                if hasattr(cfg.analysis_tolerance_warn, "value")
                else cfg.analysis_tolerance_warn or 2
            )
            self.warn_slider.setValue(warn_value)
            self.warn_value_label.setText(f"{warn_value}s")

        if hasattr(self, "fail_slider"):
            fail_value = (
                cfg.analysis_tolerance_fail.value
                if hasattr(cfg.analysis_tolerance_fail, "value")
                else cfg.analysis_tolerance_fail or 5
            )
            self.fail_slider.setValue(fail_value)
            self.fail_value_label.setText(f"{fail_value}s")

        if hasattr(self, "downsample_slider"):
            downsample_value = (
                cfg.waveform_downsample_factor.value
                if hasattr(cfg.waveform_downsample_factor, "value")
                else cfg.get("waveform/downsample_factor")
            ) or 10
            downsample_value = int(downsample_value)
            self.downsample_slider.setValue(downsample_value)
            if hasattr(self, "downsample_value_label"):
                self.downsample_value_label.setText(f"{downsample_value}x")

        if hasattr(self, "volume_slider"):
            volume_value = (
                cfg.waveform_default_volume.value
                if hasattr(cfg.waveform_default_volume, "value")
                else cfg.get("waveform/default_volume")
            )
            volume_percentage = int(float(volume_value or 0.5) * 100)
            self.volume_slider.setValue(volume_percentage)
            if hasattr(self, "volume_value_label"):
                self.volume_value_label.setText(f"{volume_percentage}%")

    @staticmethod
    def _coerce_folder(value) -> str:
        if isinstance(value, list):
            return value[0] if value else ""
        return value or ""

    @staticmethod
    def _normalize_value(value):
        if isinstance(value, list):
            return value.copy()
        return value

    def _show_message(self, title: str, content: str, message_type: str = "info") -> None:
        if message_type == "error":
            QMessageBox.critical(self, title, content)
        elif message_type == "warning":
            QMessageBox.warning(self, title, content)
        else:
            QMessageBox.information(self, title, content)
