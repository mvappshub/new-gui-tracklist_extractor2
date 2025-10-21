from __future__ import annotations

import logging
from PyQt6.QtCore import QObject, pyqtSignal

from services.analysis_service import AnalysisService
from ui.config_models import WorkerSettings


class AnalysisWorker(QObject):
    """Runs the analysis service in a background thread."""

    progress = pyqtSignal(str)
    result_ready = pyqtSignal(object)
    finished = pyqtSignal(str)

    def __init__(self, worker_settings: WorkerSettings):
        super().__init__()
        self.worker_settings = worker_settings

    def run(self) -> None:
        try:
            service = AnalysisService()
            service.start_analysis(
                pdf_dir=self.worker_settings.pdf_dir,
                wav_dir=self.worker_settings.wav_dir,
                progress_callback=self.progress.emit,
                result_callback=self.result_ready.emit,
                finished_callback=self.finished.emit,
            )
        except Exception as exc:
            logging.error("Critical error in AnalysisWorker", exc_info=True)
            self.finished.emit(f"Critical Worker Error: {exc}")
