from __future__ import annotations

import pytest

pytestmark = pytest.mark.gui

import config
import settings_page as settings_module
from settings_page import SettingsPage


@pytest.fixture(autouse=True)
def _isolate_config(isolated_config, monkeypatch):
    monkeypatch.setattr(config, "cfg", isolated_config, raising=False)
    monkeypatch.setattr(settings_module, "cfg", isolated_config, raising=False)
    return isolated_config


class TestWaveformConfig:
    def test_waveform_downsample_factor_default(self, isolated_config):
        assert isolated_config.waveform_downsample_factor.value == 10

    def test_waveform_downsample_factor_setter(self, isolated_config):
        isolated_config.waveform_downsample_factor = 25
        assert isolated_config.waveform_downsample_factor.value == 25
        assert isolated_config.get("waveform/downsample_factor") == 25

    @pytest.mark.parametrize("invalid_value", [0, 101])
    def test_waveform_downsample_factor_validation(self, isolated_config, invalid_value):
        with pytest.raises(ValueError):
            isolated_config.waveform_downsample_factor = invalid_value

    def test_waveform_default_volume_default(self, isolated_config):
        assert pytest.approx(isolated_config.waveform_default_volume.value, rel=1e-6) == 0.5

    def test_waveform_default_volume_setter(self, isolated_config):
        isolated_config.waveform_default_volume = 0.75
        assert pytest.approx(isolated_config.waveform_default_volume.value, rel=1e-6) == 0.75
        assert pytest.approx(isolated_config.get("waveform/default_volume"), rel=1e-6) == 0.75

    @pytest.mark.parametrize("invalid_value", [-0.1, 1.5])
    def test_waveform_default_volume_validation(self, isolated_config, invalid_value):
        with pytest.raises(ValueError):
            isolated_config.waveform_default_volume = invalid_value

    def test_waveform_color_defaults(self, isolated_config):
        assert isolated_config.get("waveform/waveform_color") == "#3B82F6"
        assert isolated_config.get("waveform/position_line_color") == "#EF4444"


class TestWaveformSettingsPage:
    @pytest.fixture
    def page(self, qapp, qtbot, isolated_config, monkeypatch):
        monkeypatch.setattr(settings_module, "cfg", isolated_config, raising=False)
        page = SettingsPage()
        qtbot.addWidget(page)
        return page

    def test_settings_page_waveform_group_exists(self, page):
        titles = []
        for i in range(page.container_layout.count()):
            item = page.container_layout.itemAt(i)
            widget = item.widget() if item is not None else None
            if widget and hasattr(widget, "title"):
                titles.append(widget.title())
        assert "Waveform Viewer" in titles
        assert page.downsample_slider is not None
        assert page.volume_slider is not None

    def test_downsample_slider_initialization(self, page, isolated_config):
        assert page.downsample_slider.value() == isolated_config.get("waveform/downsample_factor")
        assert page.downsample_value_label.text() == f"{page.downsample_slider.value()}x"

    def test_downsample_slider_change(self, page, isolated_config, qtbot):
        page.downsample_slider.setValue(30)
        qtbot.waitUntil(lambda: isolated_config.get("waveform/downsample_factor") == 30)
        assert page.downsample_value_label.text() == "30x"

    def test_volume_slider_initialization(self, page, isolated_config):
        expected = int(isolated_config.get("waveform/default_volume") * 100)
        assert page.volume_slider.value() == expected
        assert page.volume_value_label.text() == f"{expected}%"

    def test_volume_slider_change(self, page, isolated_config, qtbot):
        page.volume_slider.setValue(60)
        qtbot.waitUntil(lambda: isolated_config.get("waveform/default_volume") == pytest.approx(0.6, rel=1e-3))
        assert page.volume_value_label.text() == "60%"

    def test_settings_sync_from_config(self, page, isolated_config):
        isolated_config.set("waveform/downsample_factor", 40)
        isolated_config.set("waveform/default_volume", 0.9)
        page._sync_from_config()
        assert page.downsample_slider.value() == 40
        assert page.downsample_value_label.text() == "40x"
        assert page.volume_slider.value() == 90
        assert page.volume_value_label.text() == "90%"
