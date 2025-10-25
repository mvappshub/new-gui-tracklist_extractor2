from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QObject, pyqtSignal

try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
except Exception:  # pragma: no cover - tests will monkeypatch
    QAudioOutput = None  # type: ignore[assignment]
    QMediaPlayer = None  # type: ignore[assignment]


class PlaybackController(QObject):
    """Controller managing QMediaPlayer/QAudioOutput for playback.

    UI-only responsibility: manages media state and emits position/error signals.
    """

    position_changed = pyqtSignal(int)
    playback_error = pyqtSignal(str)

    def __init__(self, parent: Optional[QObject] = None):
        super().__init__(parent)
        if QMediaPlayer is None or QAudioOutput is None:  # pragma: no cover
            # In tests, these are monkeypatched
            self._player = None
            self._audio_output = None
            self._duration_ms = 0
            return

        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)

        self._duration_ms: int = 0

        self._player.positionChanged.connect(self._on_position_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.errorOccurred.connect(self._on_error)

    # ----- Public API -----
    def play(self) -> None:
        if self._player is None:
            return
        self._player.play()

    def pause(self) -> None:
        if self._player is None:
            return
        self._player.pause()

    def stop(self) -> None:
        if self._player is None:
            return
        self._player.stop()
        # Reset playhead to start for idempotence in UI
        self._on_position_changed(0)

    def set_position(self, position_ms: int) -> None:
        if self._player is None:
            return
        self._player.setPosition(int(position_ms))

    def duration(self) -> int:
        return int(self._duration_ms)

    def position(self) -> int:
        if self._player is None:
            return 0
        try:
            return int(self._player.position())  # type: ignore[no-any-return]
        except Exception:
            return 0

    def set_source_local_file(self, path: str) -> None:
        """Set local media source (delegated by UI owner)."""
        if self._player is None:  # pragma: no cover
            return
        from PyQt6.QtCore import QUrl  # local import to avoid hard dep in tests

        self._player.setSource(QUrl.fromLocalFile(path))

    # ----- Slots -----
    def _on_position_changed(self, position_ms: int) -> None:
        self.position_changed.emit(int(position_ms))

    def _on_duration_changed(self, duration_ms: int) -> None:
        if duration_ms <= 0:
            return
        self._duration_ms = int(duration_ms)

    def _on_error(self, _error, error_string: str) -> None:
        self.playback_error.emit(str(error_string or "Unknown playback error"))
