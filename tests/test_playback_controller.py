from __future__ import annotations

from typing import List

import pytest

import ui.waveform.playback_controller as pc_module
from ui.waveform.playback_controller import PlaybackController

pytestmark = pytest.mark.gui


class DummySignal:
    def __init__(self):
        self._callbacks: List = []

    def connect(self, cb):
        self._callbacks.append(cb)

    def emit(self, *args, **kwargs):
        for cb in list(self._callbacks):
            cb(*args, **kwargs)


class DummyAudioOutput:
    def __init__(self, parent=None):
        self._vol = 1.0

    def setVolume(self, v: float):
        self._vol = v


class DummyMediaPlayer:
    def __init__(self, parent=None):
        self.positionChanged = DummySignal()
        self.durationChanged = DummySignal()
        self.errorOccurred = DummySignal()
        self._audio_output = None
        self._position = 0
        self._duration = 0
        self._state = "stopped"

    def setAudioOutput(self, out):
        self._audio_output = out

    def setSource(self, source):
        pass

    def play(self):
        self._state = "playing"

    def pause(self):
        self._state = "paused"

    def stop(self):
        self._state = "stopped"

    def setPosition(self, pos_ms: int):
        self._position = int(pos_ms)
        self.positionChanged.emit(self._position)

    def position(self) -> int:
        return self._position

    # Helpers for tests
    def _set_duration(self, dur_ms: int):
        self._duration = int(dur_ms)
        self.durationChanged.emit(self._duration)


@pytest.fixture(autouse=True)
def fake_multimedia(monkeypatch):
    monkeypatch.setattr(pc_module, "QAudioOutput", DummyAudioOutput, raising=False)
    monkeypatch.setattr(pc_module, "QMediaPlayer", DummyMediaPlayer, raising=False)
    yield


def test_play_pause_stop_transitions(qtbot):
    ctrl = PlaybackController()
    # Access underlying dummy for state assertions
    player: DummyMediaPlayer = ctrl._player  # type: ignore[attr-defined]

    ctrl.play()
    assert player._state == "playing"

    ctrl.pause()
    assert player._state == "paused"

    ctrl.stop()
    assert player._state == "stopped"

    # idempotence
    ctrl.stop()
    assert player._state == "stopped"


def test_set_position_emits_signal(qtbot):
    ctrl = PlaybackController()
    positions: List[int] = []
    ctrl.position_changed.connect(lambda p: positions.append(p))

    ctrl.set_position(1234)
    assert positions and positions[-1] == 1234
    assert ctrl.position() == 1234


def test_duration_and_error_emission(qtbot):
    ctrl = PlaybackController()
    # duration default
    assert ctrl.duration() == 0

    # drive duration change via dummy
    player: DummyMediaPlayer = ctrl._player  # type: ignore[attr-defined]
    player._set_duration(2500)
    assert ctrl.duration() == 2500

    # error emission
    errors: List[str] = []
    ctrl.playback_error.connect(lambda m: errors.append(m))
    player.errorOccurred.emit(object(), "failure")
    assert errors and errors[-1] == "failure"


def test_ui_only_no_render_attributes(qtbot):
    ctrl = PlaybackController()
    # Ensure controller does not have plotting attributes
    assert not hasattr(ctrl, "plot_widget")
