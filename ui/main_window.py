from __future__ import annotations

import logging
import os
from pathlib import Path

from PyQt6.QtCore import QEvent, QModelIndex, QSize, Qt, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from core.models.settings import ExportSettings, ToleranceSettings
from pdf_viewer import PdfViewerDialog
from services.export_service import export_results_to_json
from ui.config_models import ThemeSettings, WaveformSettings
from ui.constants import *
from ui.delegates.action_cell_delegate import ActionCellDelegate
from ui.dialogs.settings_dialog import SettingsDialog
from ui.components import ModernTableView
from ui.models.results_table_model import ResultsTableModel
from ui.models.tracks_table_model import TracksTableModel
from ui.workers.worker_manager import AnalysisWorkerManager
from config import AppConfig


class MainWindow(QMainWindow):
    def _show_safe_message_box(
        self,
        title: str,
        text: str,
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
    ):
        if os.getenv("QT_QPA_PLATFORM") == "offscreen":
            logging.error(f"MODAL_DIALOG_BLOCKED: Title: {title}, Text: {text}")
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.exec()

    def __init__(
        self,
        *,
        tolerance_settings: ToleranceSettings,
        export_settings: ExportSettings,
        theme_settings: ThemeSettings,
        waveform_settings: WaveformSettings,
        worker_manager: AnalysisWorkerManager,
        settings_filename: Path,
        app_config: AppConfig,
    ):
        super().__init__()
        self.tolerance_settings = tolerance_settings
        self.export_settings = export_settings
        self.theme_settings = theme_settings
        self.waveform_settings = waveform_settings
        self.worker_manager = worker_manager
        self.worker_manager.setParent(self)
        self.settings_filename = Path(settings_filename)
        self.app_config = app_config

        self.setWindowTitle(WINDOW_TITLE)
        self.resize(1200, 800)

        self.setup_menu_bar()

        central = QWidget(self)
        central.setObjectName("Main")
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(16)

        self.toolbar = QToolBar("Main Toolbar")
        self.toolbar.setObjectName("MainToolbar")
        self.toolbar.setMovable(False)
        self.toolbar.setFloatable(False)
        self.toolbar.setProperty("analysis-state", "false")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)

        self.run_button = QPushButton(BUTTON_RUN_ANALYSIS)
        self.run_button.setObjectName("RunButton")
        self.toolbar.addWidget(self.run_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.toolbar.addWidget(spacer)

        self.filter_section = QWidget()
        filter_layout = QHBoxLayout(self.filter_section)
        filter_layout.setContentsMargins(8, 0, 8, 0)
        filter_layout.addWidget(QLabel(LABEL_FILTER))

        self.filter_combo = QComboBox()
        self.filter_combo.setObjectName("FilterCombo")
        self.filter_combo.addItems([FILTER_ALL, FILTER_OK, FILTER_FAIL, FILTER_WARN])
        self.filter_combo.setMinimumWidth(100)
        filter_layout.addWidget(self.filter_combo)
        self.toolbar.addWidget(self.filter_section)

        spacer_between = QWidget()
        spacer_between.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        spacer_between.setFixedWidth(16)
        self.toolbar.addWidget(spacer_between)

        self.status_box = QWidget()
        status_layout = QHBoxLayout(self.status_box)
        status_layout.setContentsMargins(8, 0, 0, 0)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("ProgressBar")
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setTextVisible(False)
        status_layout.addWidget(self.progress_bar)

        self.status_label = QLabel(STATUS_READY)
        self.status_label.setObjectName("StatusLabel")
        self.status_label.setMinimumWidth(220)
        status_layout.addWidget(self.status_label)
        self.toolbar.addWidget(self.status_box)

        splitter = QSplitter(Qt.Orientation.Vertical)

        self.top_table = ModernTableView()
        self.top_model = ResultsTableModel(theme_settings=self.theme_settings)
        self.top_table.setModel(self.top_model)
        try:
            self.top_table.setIconSize(QSize(16, 16))
        except Exception:
            pass
        self.top_table.set_empty_state(text="No analysis results yet")

        self.bottom_table = ModernTableView()
        self.bottom_model = TracksTableModel(
            tolerance_settings=self.tolerance_settings, theme_settings=self.theme_settings
        )
        self.bottom_table.setModel(self.bottom_model)
        self.bottom_table.set_empty_state(text="Select a result to view track details")

        splitter.addWidget(self.top_table)
        splitter.addWidget(self.bottom_table)
        splitter.setSizes([300, 400])
        main_layout.addWidget(splitter)

        self.setCentralWidget(central)

        self._load_table_stylesheet()
        self._apply_theme_properties()
        self.setup_tables()
        self._restored_table_state = False
        self._restore_table_state()
        self.connect_signals()

        self._auto_resize_pending = False

        def _apply_header_resizes():
            self._apply_table_layouts()

        def _schedule_header_resizes():
            if self._auto_resize_pending:
                return
            self._auto_resize_pending = True

            def _runner():
                try:
                    _apply_header_resizes()
                finally:
                    self._auto_resize_pending = False

            QTimer.singleShot(0, _runner)

        self._schedule_header_resizes = _schedule_header_resizes  # type: ignore[assignment]
        self.top_model._schedule_header_resizes = _schedule_header_resizes  # type: ignore[attr-defined]
        self._schedule_header_resizes()

        if self.windowHandle() is not None:

            def _on_screen_changed(screen):
                try:
                    screen.logicalDotsPerInchChanged.connect(lambda _=None: _schedule_header_resizes())
                    screen.physicalDotsPerInchChanged.connect(lambda _=None: _schedule_header_resizes())
                except Exception:
                    pass
                _schedule_header_resizes()

            self.windowHandle().screenChanged.connect(_on_screen_changed)
            _on_screen_changed(self.windowHandle().screen())

        self.installEventFilter(self)

    def on_filter_changed(self, filter_text: str):
        self.top_model.set_filter(filter_text)
        if self.top_model.rowCount() > 0:
            self.top_table.selectRow(0)
        else:
            self.top_table.clearSelection()
            self.bottom_model.update_data(None)

    def setup_tables(self):
        self.top_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.top_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.bottom_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.bottom_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        header_top = self.top_table.horizontalHeader()
        top_font = header_top.font()
        top_font.setBold(True)
        header_top.setFont(top_font)

        header_bottom = self.bottom_table.horizontalHeader()
        bottom_font = header_bottom.font()
        bottom_font.setBold(True)
        header_bottom.setFont(bottom_font)

        self._apply_table_layouts()

        # Install hover affordance delegates for action cells
        self.top_delegate = ActionCellDelegate(self.theme_settings, {6, 7})
        self.top_table.setItemDelegateForColumn(6, self.top_delegate)
        self.top_table.setItemDelegateForColumn(7, self.top_delegate)

        self.bottom_delegate = ActionCellDelegate(self.theme_settings, {7})
        self.bottom_table.setItemDelegateForColumn(7, self.bottom_delegate)

    def _apply_table_layouts(self):
        try:
            top_header = self.top_table.horizontalHeader()
            top_header.setStretchLastSection(False)
            if not getattr(self, "_restored_table_state", False):
                self.top_table.resizeColumnsToContents()
            for col in (0, 2, 3, 4, 5):
                top_header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
            top_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            for col, width in ((6, 52), (7, 60)):
                top_header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
                self.top_table.setColumnWidth(col, width)

            bottom_header = self.bottom_table.horizontalHeader()
            bottom_header.setStretchLastSection(False)
            if not getattr(self, "_restored_table_state", False):
                self.bottom_table.resizeColumnsToContents()
            bottom_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
            bottom_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            bottom_header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
            for col in (3, 4, 5):
                bottom_header.setSectionResizeMode(col, QHeaderView.ResizeMode.Interactive)
            for col, width in ((6, 48), (7, 60)):
                bottom_header.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
                self.bottom_table.setColumnWidth(col, width)
        except Exception as exc:
            logging.exception("Failed to apply table layouts: %s", exc)

    def _load_table_stylesheet(self) -> None:
        try:
            tables_path = Path(__file__).resolve().parent.parent / "assets" / "stylesheets" / "tables.qss"
            if not tables_path.exists():
                logging.warning("Tables stylesheet not found at %s", tables_path)
                return

            qapp = QApplication.instance()
            if qapp is None:
                return

            stylesheet = tables_path.read_text(encoding="utf-8")
            current = qapp.styleSheet() or ""
            if stylesheet and stylesheet not in current:
                combined = f"{current}\n{stylesheet}" if current else stylesheet
                qapp.setStyleSheet(combined)
        except Exception as exc:
            logging.error("Failed to load tables stylesheet: %s", exc)

    def _derive_theme_variant(self) -> str:
        try:
            stylesheet_path = getattr(self.theme_settings, "stylesheet_path", None)
            if stylesheet_path:
                name = Path(stylesheet_path).stem.lower()
                if "dark" in name:
                    return "dark"
        except Exception:
            pass
        return "light"

    def _apply_theme_properties(self) -> None:
        configured_variant = getattr(self.theme_settings, "theme_variant", "")
        variant = configured_variant or self._derive_theme_variant()
        self._theme_variant = variant
        try:
            self.setProperty("theme", variant)
            style = self.style()
            if style is not None:
                style.unpolish(self)
                style.polish(self)
        except Exception as exc:
            logging.debug("Failed to polish main window theme: %s", exc)

        for table in (self.top_table, self.bottom_table):
            if hasattr(table, "set_theme"):
                try:
                    table.set_theme(variant)
                except Exception as exc:
                    logging.debug("Failed to set table theme: %s", exc)

    def _restore_table_state(self) -> None:
        try:
            settings = self.app_config.settings
        except Exception as exc:
            logging.debug("Table state could not access settings: %s", exc)
            return

        restored_results = self.top_table.restoreHeaderState("results-table", settings=settings)
        restored_tracks = self.bottom_table.restoreHeaderState("tracks-table", settings=settings)
        self._restored_table_state = restored_results or restored_tracks

    def connect_signals(self):
        self.run_button.clicked.connect(self.run_analysis)
        self.filter_combo.currentTextChanged.connect(self.on_filter_changed)
        selection_model = self.top_table.selectionModel()
        if selection_model:
            selection_model.currentRowChanged.connect(self.on_top_row_selected)
        self.top_table.clicked.connect(self.on_top_cell_clicked)
        self.bottom_table.clicked.connect(self.on_bottom_cell_clicked)

        # Connect hover tracking for action cell affordance
        self.top_table.entered.connect(lambda idx: self.top_delegate.set_hovered_index(idx))
        self.top_table.installEventFilter(self)

        self.bottom_table.entered.connect(lambda idx: self.bottom_delegate.set_hovered_index(idx))
        self.bottom_table.installEventFilter(self)

        self.worker_manager.progress.connect(lambda msg: self._set_status(msg, running=True))
        self.worker_manager.result_ready.connect(self.top_model.add_result)
        self.worker_manager.finished.connect(self.on_analysis_finished)

    def eventFilter(self, obj, event):
        event_type = event.type()
        if event_type in (
            QEvent.Type.PaletteChange,
            QEvent.Type.ApplicationPaletteChange,
            QEvent.Type.FontChange,
            QEvent.Type.ApplicationFontChange,
            QEvent.Type.Resize,
        ):
            if hasattr(self, "_schedule_header_resizes"):
                self._schedule_header_resizes()
        # Clear hover state when mouse leaves table
        elif event_type == QEvent.Type.Leave:
            if obj is self.top_table:
                self.top_delegate.set_hovered_index(None)
            elif obj is self.bottom_table:
                self.bottom_delegate.set_hovered_index(None)
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, "_schedule_header_resizes"):
            self._schedule_header_resizes()

    def closeEvent(self, event):
        self.worker_manager.cleanup()
        try:
            settings = self.app_config.settings
            self.top_table.saveHeaderState("results-table", settings=settings)
            self.bottom_table.saveHeaderState("tracks-table", settings=settings)
        except Exception as exc:
            logging.debug("Failed to persist table state: %s", exc)
        super().closeEvent(event)

    def run_analysis(self):
        if not self.worker_manager.is_running():
            self._set_analysis_state(True)
            self.run_button.setEnabled(False)
            self._set_status(STATUS_ANALYZING, running=True)
            self.top_model.clear()
            self.bottom_model.update_data(None)
            self.worker_manager.start_analysis()

    def _set_status(self, text: str, running: bool):
        self.progress_bar.setVisible(running)
        if len(text) > 50:
            for separator in [" - ", ": ", ", ", " "]:
                if separator in text[:45]:
                    parts = text.split(separator, 1)
                    text = parts[0] + separator.rstrip()
                    break
            else:
                text = text[:47] + "..."
        self.status_label.setText(text)

    def setup_menu_bar(self):
        menubar = self.menuBar()
        menubar.clear()
        settings_menu = menubar.addMenu("Settings")
        settings_action = settings_menu.addAction("Open settings...")
        settings_action.triggered.connect(self.open_settings)

    def _set_analysis_state(self, is_analyzing: bool):
        try:
            self.setProperty("analysis-state", "true" if is_analyzing else "false")
            if is_analyzing and hasattr(self, "status_label") and self.status_label is not None:
                self.status_label.setText(STATUS_ANALYZING)
        except Exception as exc:
            logging.exception("Failed to set analysis state: %s", exc)

    def on_analysis_finished(self, message: str):
        self._set_analysis_state(False)
        logging.info("Analysis finished: %s", message)

        try:
            all_results = getattr(self.top_model, "all_results", lambda: [])()
        except Exception:
            all_results = []

        export_path = export_results_to_json(
            results=all_results,
            export_settings=self.export_settings,
        )

        if export_path is not None:
            ready_msg = f"{STATUS_READY} - {message} - Exported: {export_path.name}"
        else:
            ready_msg = f"{STATUS_READY} - {message}"
        self._set_status(ready_msg, running=False)
        self.run_button.setEnabled(True)
        if self.top_model.rowCount() > 0:
            self.top_table.selectRow(0)

    def on_top_row_selected(self, current: QModelIndex, previous: QModelIndex):
        result = self.top_model.get_result(current.row())
        self.bottom_model.update_data(result)

    def on_top_cell_clicked(self, index: QModelIndex):
        result = self.top_model.get_result(index.row())
        if not result:
            return
        if index.column() == 6 and result.pdf_path:
            try:
                pdf_dialog = PdfViewerDialog(result.pdf_path, self)
                pdf_dialog.exec()
            except Exception as exc:
                logging.error("Failed to open PDF viewer: %s", exc)
                QDesktopServices.openUrl(QUrl.fromLocalFile(str(result.pdf_path)))
        elif index.column() == 7 and result.zip_path:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(result.zip_path)))

    def on_bottom_cell_clicked(self, index: QModelIndex):
        if not index.isValid() or index.column() != 7:
            return

        icon = self.bottom_model.data(index, Qt.ItemDataRole.DecorationRole)
        if icon is None or (hasattr(icon, "isNull") and icon.isNull()):
            return

        current_top_index = self.top_table.currentIndex()
        result = self.top_model.get_result(current_top_index.row()) if current_top_index.isValid() else None
        if not result:
            return

        if index.row() >= len(result.pdf_tracks):
            return

        wav_track = None
        if result.mode == "tracks":
            if index.row() < len(result.wav_tracks):
                wav_track = result.wav_tracks[index.row()]
        else:
            if result.wav_tracks:
                wav_track = result.wav_tracks[0]

        if not wav_track or not wav_track.filename:
            self._show_safe_message_box(
                "Waveform Unavailable",
                "No WAV track is available for waveform preview.",
                QMessageBox.Icon.Information,
            )
            return

        if not result.zip_path or not result.zip_path.exists():
            self._show_safe_message_box(
                "Missing ZIP",
                "The associated ZIP archive could not be found on disk.",
                QMessageBox.Icon.Warning,
            )
            return

        try:
            from waveform_viewer import WaveformEditorDialog
        except ImportError as exc:
            logging.error("Waveform editor dependencies missing: %s", exc, exc_info=True)
            self._show_safe_message_box(
                "Waveform Editor Unavailable",
                "Waveform editor requires optional dependencies (pyqtgraph, soundfile). "
                "Install them to enable waveform editing.",
                QMessageBox.Icon.Warning,
            )
            return

        try:
            pdf_tracks = []
            wav_tracks = []
            if result.mode == "tracks":
                pdf_tracks = result.pdf_tracks
                wav_tracks = result.wav_tracks
            else:
                if result.pdf_tracks:
                    pdf_tracks = result.pdf_tracks
                if result.wav_tracks:
                    wav_tracks = result.wav_tracks

            dialog = WaveformEditorDialog(
                result.zip_path,
                wav_track.filename,
                waveform_settings=self.waveform_settings,
                parent=self,
            )
            dialog.set_pdf_tracks(
                pdf_tracks,
                wav_tracks,
                self.tolerance_settings,
            )
            dialog.exec()
        except Exception as exc:
            logging.error("Failed to open waveform viewer: %s", exc, exc_info=True)
            self._show_safe_message_box(
                "Waveform Error",
                f"Could not open waveform viewer.\n\nError: {exc}",
                QMessageBox.Icon.Warning,
            )

    def open_settings(self):
        try:
            settings_dialog = SettingsDialog(settings_filename=self.settings_filename, app_config=self.app_config, parent=self)
            settings_dialog.exec()
        except Exception as exc:
            logging.error("Failed to open settings dialog: %s", exc)

    def _update_gz_logo(self):
        try:
            if not hasattr(self, "gz_logo_label"):
                self.gz_logo_label = QLabel(parent=self)
                self.gz_logo_label.setObjectName("gzLogo")

            logo_path = self.theme_settings.logo_path

            if logo_path.exists():
                from PyQt6.QtGui import QPixmap

                pixmap = QPixmap(str(logo_path))
                scaled_pixmap = pixmap.scaledToHeight(24, Qt.TransformationMode.SmoothTransformation)
                self.gz_logo_label.setPixmap(scaled_pixmap)
                self.gz_logo_label.show()
            else:
                self.gz_logo_label.setText("GZ Media")
                logging.warning("GZ Media logo file not found at %s, using text fallback", logo_path)
        except Exception as exc:
            logging.error("Failed to load GZ Media logo: %s", exc)
            if hasattr(self, "gz_logo_label"):
                self.gz_logo_label.hide()

    def _update_gz_claim_visibility(self):
        try:
            if not hasattr(self, "gz_claim_label"):
                self.gz_claim_label = QLabel(parent=self)

            if self.theme_settings.claim_visible:
                self.gz_claim_label.setText(self.theme_settings.claim_text)
                self.gz_claim_label.show()
            else:
                self.gz_claim_label.hide()
        except Exception as exc:
            logging.error("Failed to update GZ Media claim: %s", exc)
            if hasattr(self, "gz_claim_label"):
                self.gz_claim_label.hide()
