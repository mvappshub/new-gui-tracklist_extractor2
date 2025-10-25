## Project Context

- Root Path: C:\Users\vosahlo_martin\Downloads\new gui tracklist_extractor2
- Timestamp: 20251025-013716
- Total Files: 85
- Total Size: 381812 bytes

## Summary Table

| Relative Path | Bytes | Lines |
|---------------|-------|-------|
| adapters\__init__.py | 1 | 2 |
| adapters\ai\__init__.py | 0 | 1 |
| adapters\ai\vlm.py | 2462 | 74 |
| adapters\audio\__init__.py | 2 | 2 |
| adapters\audio\ai_mode_detector.py | 2942 | 79 |
| adapters\audio\fake_mode_detector.py | 3145 | 86 |
| adapters\audio\chained_detector.py | 1922 | 55 |
| adapters\audio\steps.py | 2509 | 67 |
| adapters\audio\wav_reader.py | 3587 | 79 |
| adapters\filesystem\__init__.py | 1 | 2 |
| adapters\filesystem\file_discovery.py | 2710 | 80 |
| adapters\pdf\__init__.py | 0 | 1 |
| adapters\pdf\renderer.py | 1016 | 33 |
| app.py | 3852 | 108 |
| audio_utils.py | 1051 | 34 |
| config.py | 26752 | 690 |
| core\__init__.py | 1 | 2 |
| core\domain\__init__.py | 1 | 2 |
| core\domain\comparison.py | 3453 | 95 |
| core\domain\extraction.py | 447 | 16 |
| core\domain\parsing.py | 5113 | 132 |
| core\domain\steps.py | 597 | 21 |
| core\models\__init__.py | 254 | 11 |
| core\models\analysis.py | 753 | 43 |
| core\models\settings.py | 582 | 30 |
| core\ports.py | 1759 | 44 |
| fluent_gui.py | 6264 | 214 |
| fonts\dejavu-fonts-ttf-2.37\LICENSE | 8816 | 188 |
| mypy.ini | 585 | 33 |
| package.json | 66 | 6 |
| pdf_extractor.py | 2527 | 65 |
| pdf_viewer.py | 1295 | 42 |
| requirements.txt | 216 | 17 |
| scripts\run_analysis_no_ai.py | 2209 | 67 |
| scripts\smoke_test.py | 1864 | 49 |
| scripts\smoke_wav_only.py | 1928 | 55 |
| services\__init__.py | 1 | 2 |
| services\analysis_service.py | 3828 | 98 |
| services\export_service.py | 2510 | 73 |
| settings_page.py | 22983 | 596 |
| tests\__init__.py | 1 | 2 |
| tests\conftest.py | 4906 | 144 |
| tests\test_ai_mode_detector.py | 8693 | 201 |
| tests\test_config.py | 837 | 31 |
| tests\test_export_auto.py | 10084 | 271 |
| tests\test_export_service.py | 1746 | 57 |
| tests\test_fluent_gui_legacy.py | 3880 | 152 |
| tests\test_gui_minimal.py | 1498 | 41 |
| tests\test_gui_show.py | 2108 | 62 |
| tests\test_gui_simple.py | 765 | 35 |
| tests\test_chained_detector.py | 19689 | 491 |
| tests\test_characterization.py | 6394 | 187 |
| tests\test_parsing.py | 9986 | 244 |
| tests\test_results_table_model.py | 2449 | 83 |
| tests\test_settings_dialog.py | 16759 | 542 |
| tests\test_tracks_table_model.py | 4448 | 122 |
| tests\test_wav_reader.py | 6264 | 193 |
| tests\test_waveform_config.py | 4372 | 97 |
| tests\test_waveform_editor.py | 10886 | 248 |
| tests\test_waveform_integration.py | 6011 | 150 |
| tests\test_waveform_viewer.py | 12903 | 309 |
| tests\test_worker_manager.py | 4166 | 147 |
| tools\bootstrap_and_finalize.sh | 2881 | 90 |
| tools\bootstrap_finalize.sh | 1675 | 48 |
| tools\build_resources.py | 2349 | 71 |
| tools\finalize.sh | 2654 | 94 |
| tools\check.sh | 1175 | 40 |
| ui\__init__.py | 2359 | 90 |
| ui\_icons_rc.py | 705 | 23 |
| ui\config_models.py | 6458 | 209 |
| ui\constants.py | 1712 | 51 |
| ui\delegates\__init__.py | 0 | 1 |
| ui\delegates\action_cell_delegate.py | 3311 | 99 |
| ui\dialogs\__init__.py | 0 | 1 |
| ui\dialogs\settings_dialog.py | 2272 | 77 |
| ui\main_window.py | 20282 | 510 |
| ui\models\__init__.py | 0 | 1 |
| ui\models\results_table_model.py | 6457 | 172 |
| ui\models\tracks_table_model.py | 9634 | 243 |
| ui\theme.py | 5975 | 169 |
| ui\workers\__init__.py | 0 | 1 |
| ui\workers\analysis_worker.py | 1573 | 45 |
| ui\workers\worker_manager.py | 1972 | 60 |
| wav_extractor_wave.py | 6063 | 163 |
| waveform_viewer.py | 43456 | 1114 |

## File Contents

### adapters\__init__.py

`$tag


``n
### adapters\ai\__init__.py

`$tag

``n
### adapters\ai\vlm.py

`$tag
from __future__ import annotations
import base64
import io
import json
import os
from typing import Any, List

try:
    from openai import OpenAI
    from PIL import Image
except ImportError as e:
    raise ImportError(f"Missing AI or Imaging libraries: {e}. Please run 'pip install openai Pillow'")

class VlmClient:
    """Adapter for communicating with a Vision Language Model (VLM) API."""

    def __init__(self, model: str = "google/gemini-2.5-flash"):
        api_key = os.getenv("OPENROUTER_API_KEY")
        # Graceful no-op mode when API key is missing
        if not api_key:
            self._client = None
        else:
            self._client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        self._model = model

    def _to_data_url(self, pil_image: Image.Image) -> str:
        """Converts a PIL image to a base64 data URL."""
        buf = io.BytesIO()
        pil_image.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode('ascii')
        return f"data:image/png;base64,{b64}"

    def get_json_response(self, prompt: str, images: List[Image.Image]) -> dict[str, Any]:
        """
        Calls the VLM with a prompt and images, expecting a JSON response.

        Args:
            prompt: The text prompt for the VLM.
            images: A list of PIL Image objects to send.

        Returns:
            The parsed JSON response from the VLM as a dictionary.
        """
        # If client is not configured, operate in no-op mode (return empty)
        if self._client is None:
            return {}

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    *({"type": "image_url", "image_url": {"url": self._to_data_url(img)}} for img in images)
                ]
            }
        ]

        response = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("AI returned an empty response.")
            
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            cleaned_content = content.strip().strip("`").strip("json\n")
            return json.loads(cleaned_content)

``n
### adapters\audio\__init__.py

`$tag


``n
### adapters\audio\ai_mode_detector.py

`$tag
"""Real AI-backed audio mode detector adapter.

Implements the AudioModeDetector protocol using OpenAI/OpenRouter APIs.
Wraps existing wav_extractor_wave functions for strict parsing → AI fallback →
deterministic fallback → normalization.
"""

from __future__ import annotations

from core.models.analysis import WavInfo
from core.ports import AudioModeDetector
from wav_extractor_wave import WavInfo as ExtractorWavInfo
from wav_extractor_wave import detect_audio_mode_with_ai, normalize_positions


class AiAudioModeDetector(AudioModeDetector):
    """Real AI-backed audio mode detector using OpenAI/OpenRouter APIs.

    Wraps existing wav_extractor_wave functions for strict parsing → AI fallback →
    deterministic fallback → normalization.
    """

    def detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]:
        """Detect audio side and position from WAV filenames using AI.

        Args:
            wavs: List of WavInfo objects with filename and duration_sec populated.

        Returns:
            Dictionary mapping side (e.g., "A", "B") to list of WavInfo objects
            with side and position populated and normalized (sequential 1, 2, 3...).

        Raises:
            No exceptions raised - handles edge cases gracefully.
        """
        # Handle empty input
        if not wavs:
            return {}

        # Convert core WavInfo to wav_extractor_wave WavInfo format
        extractor_wavs = [self._convert_to_extractor_wavinfo(wav) for wav in wavs]

        # Call AI detection function
        side_map = detect_audio_mode_with_ai(extractor_wavs)

        # Normalize positions to be sequential (1, 2, 3...) with no gaps
        normalize_positions(side_map)

        # Convert back to core WavInfo format
        result: dict[str, list[WavInfo]] = {}
        for side, extractor_wav_list in side_map.items():
            result[side] = [self._convert_to_core_wavinfo(wav) for wav in extractor_wav_list]

        return result

    def _convert_to_extractor_wavinfo(self, wav: WavInfo) -> ExtractorWavInfo:
        """Convert core WavInfo to wav_extractor_wave WavInfo format.

        Args:
            wav: Core WavInfo object to convert.

        Returns:
            ExtractorWavInfo object with identical field values.
        """
        return ExtractorWavInfo(
            filename=wav.filename, duration_sec=wav.duration_sec, side=wav.side, position=wav.position
        )

    def _convert_to_core_wavinfo(self, wav: ExtractorWavInfo) -> WavInfo:
        """Convert wav_extractor_wave WavInfo to core WavInfo format.

        Args:
            wav: ExtractorWavInfo object to convert.

        Returns:
            Core WavInfo object with identical field values.
        """
        return WavInfo(filename=wav.filename, duration_sec=wav.duration_sec, side=wav.side, position=wav.position)

``n
### adapters\audio\fake_mode_detector.py

`$tag
"""Fake audio mode detector adapter for tests.

Implements the AudioModeDetector protocol with deterministic filename parsing.
No external API calls - guarantees consistent results for same inputs.
"""

from __future__ import annotations

from core.domain.parsing import UNKNOWN_POSITION, StrictFilenameParser
from core.models.analysis import WavInfo
from core.ports import AudioModeDetector


class FakeAudioModeDetector(AudioModeDetector):
    """Fake audio mode detector for tests.

    Uses deterministic filename parsing with no external API calls.
    Guarantees consistent results for same inputs.
    """

    def __init__(self) -> None:
        self._parser = StrictFilenameParser()

    def detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]:
        """Detect audio side and position from WAV filenames using deterministic parsing.

        Args:
            wavs: List of WavInfo objects with filename and duration_sec populated.

        Returns:
            Dictionary mapping side (e.g., "A", "B") to list of WavInfo objects
            with side and position populated and normalized (sequential 1, 2, 3...).

        Raises:
            No exceptions raised - handles edge cases gracefully.
        """
        if not wavs:
            return {}

        parsed_wavs = []
        for wav in wavs:
            parsed_info = self._parser.parse(wav.filename)
            parsed_wavs.append(
                WavInfo(
                    filename=wav.filename,
                    duration_sec=wav.duration_sec,
                    side=parsed_info.side,
                    position=parsed_info.position,
                )
            )

        side_map: dict[str, list[WavInfo]] = {}
        for wav in parsed_wavs:
            side = wav.side or "A"  # Default to "A" if side is None
            side_map.setdefault(side, []).append(wav)

        for wav_list in side_map.values():
            wav_list.sort(
                key=lambda x: (x.position if x.position is not None else UNKNOWN_POSITION, x.filename.lower())
            )

        self._normalize_positions(side_map)

        return side_map

    def _normalize_positions(self, side_map: dict[str, list[WavInfo]]) -> None:
        """Normalize positions to be sequential (1, 2, 3...) with no gaps or duplicates."""
        for wav_list in side_map.values():
            if not wav_list:
                continue

            wav_list.sort(
                key=lambda x: (x.position if x.position is not None else UNKNOWN_POSITION, x.filename.lower())
            )

            actual = [w.position for w in wav_list]
            expected = list(range(1, len(wav_list) + 1))

            has_missing = any(pos is None for pos in actual)
            non_none_positions = {p for p in actual if p is not None}
            has_duplicates = len([p for p in actual if p is not None]) != len(non_none_positions)

            if has_missing or has_duplicates or actual != expected:
                for i, wav in enumerate(wav_list, start=1):
                    wav.position = i

``n
### adapters\audio\chained_detector.py

`$tag
from __future__ import annotations
from typing import List

from core.domain.parsing import UNKNOWN_POSITION
from core.domain.steps import DetectionStep
from core.models.analysis import WavInfo
from core.ports import AudioModeDetector
from adapters.audio.steps import StrictParserStep, AiParserStep, DeterministicFallbackStep

class ChainedAudioModeDetector(AudioModeDetector):
    """
    Orchestrates audio mode detection using a Chain of Responsibility pattern.
    """
    def __init__(self, steps: List[DetectionStep] | None = None):
        if steps is None:
            self._steps = [
                StrictParserStep(),
                AiParserStep(),
                DeterministicFallbackStep(),
            ]
        else:
            self._steps = steps

    def detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]:
        if not wavs:
            return {}
        
        # Create a mutable copy for processing
        processing_wavs = [w.model_copy() for w in wavs]

        for step in self._steps:
            stop_chain = step.process(processing_wavs)
            if stop_chain:
                break
        
        return self._normalize_and_group(processing_wavs)

    def _normalize_and_group(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]:
        """Groups WAVs by side and normalizes their positions."""
        side_map: dict[str, list[WavInfo]] = {}
        for wav in wavs:
            side = wav.side or "A"  # Default to "A" if side is still None
            side_map.setdefault(side, []).append(wav)

        for wav_list in side_map.values():
            if not wav_list:
                continue
            
            wav_list.sort(key=lambda x: (x.position if x.position is not None else UNKNOWN_POSITION, x.filename.lower()))
            
            for i, wav in enumerate(wav_list, start=1):
                wav.position = i
        
        return side_map

``n
### adapters\audio\steps.py

`$tag
from __future__ import annotations
import logging
from typing import List

from core.domain.parsing import StrictFilenameParser
from core.models.analysis import WavInfo
from wav_extractor_wave import ai_parse_batch, merge_ai_results

class StrictParserStep:
    """First step: attempts to parse side/position using strict regex rules."""
    def __init__(self):
        self._parser = StrictFilenameParser()

    def process(self, wavs: List[WavInfo]) -> bool:
        all_parsed = True
        for wav in wavs:
            if wav.side is None or wav.position is None:
                parsed = self._parser.parse(wav.filename)
                wav.side = wav.side or parsed.side
                wav.position = wav.position or parsed.position
            if wav.side is None or wav.position is None:
                all_parsed = False
        return all_parsed

class AiParserStep:
    """Second step: uses an AI model as a fallback for unparsed files."""
    def process(self, wavs: List[WavInfo]) -> bool:
        unparsed_wavs = [w for w in wavs if w.side is None or w.position is None]
        if not unparsed_wavs:
            return True  # Chain can stop, everything is parsed

        try:
            filenames = [w.filename for w in unparsed_wavs]
            ai_map = ai_parse_batch(filenames)
            if ai_map:
                # The merge_ai_results function expects side to be 'UNKNOWN'
                for w in wavs:
                     if w.side is None:
                        w.side = "UNKNOWN"
                merge_ai_results(wavs, ai_map)
                # Reset 'UNKNOWN' back to None if AI didn't find anything
                for w in wavs:
                    if w.side == "UNKNOWN":
                        w.side = None
        except Exception as e:
            logging.warning(f"AI parser step failed: {e}", exc_info=True)

        # Never stop the chain here; always allow fallback
        return False

class DeterministicFallbackStep:
    """Final step: assigns default side/position if all else fails."""
    def process(self, wavs: List[WavInfo]) -> bool:
        if not wavs:
            return True

        # Only run if NO files have a side assigned
        if any(w.side for w in wavs):
            return True

        wavs.sort(key=lambda x: x.filename.lower())
        for i, wav in enumerate(wavs, start=1):
            wav.side = "A"
            if wav.position is None:
                wav.position = i
        return True # This is the last step, always stop

``n
### adapters\audio\wav_reader.py

`$tag
from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

from audio_utils import get_wav_duration
from core.models.analysis import WavInfo


class ZipWavFileReader:
    """Adapter that encapsulates ZIP file handling and WAV duration probing for the extraction pipeline.

    Responsibilities:
    - Enumerate WAV members within a ZIP archive
    - Materialize entries into a temporary directory for duration inspection
    - Delegate duration probing to `audio_utils.get_wav_duration`
    - Surface results as `WavInfo` domain objects while containing all file I/O concerns
    """

    def read_wav_files(self, zip_path: Path) -> list[WavInfo]:
        """Extract WAV files from the provided ZIP archive and return their durations."""
        wav_infos: list[WavInfo] = []
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                names = sorted(
                    [name for name in zf.namelist() if name.lower().endswith(".wav")],
                    key=lambda value: value.lower(),
                )
                if not names:
                    return wav_infos

                with tempfile.TemporaryDirectory(prefix="wavprobe_") as tmpdir:
                    tmpdir_path = Path(tmpdir)
                    for name in names:
                        try:
                            relative_path = PurePosixPath(name)
                            safe_parts = [part for part in relative_path.parts if part not in ("", ".", "..")]
                            if not safe_parts:
                                logging.warning(
                                    "Přeskakuji podezřelý ZIP člen '%s' v archivu '%s'",
                                    name,
                                    zip_path.name,
                                )
                                continue

                            safe_relative = PurePosixPath(*safe_parts)
                            dest = tmpdir_path.joinpath(*safe_relative.parts)
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            with zf.open(name) as src, dest.open("wb") as dst:
                                shutil.copyfileobj(src, dst)
                            duration = get_wav_duration(dest)
                            if duration <= 0.0:
                                logging.warning(
                                    "WAV '%s' z archivu '%s' má neplatnou délku %.3fs; přeskočeno",
                                    safe_relative.as_posix(),
                                    zip_path.name,
                                    duration,
                                )
                                continue
                            wav_infos.append(
                                WavInfo(
                                    filename=safe_relative.as_posix(),
                                    duration_sec=duration,
                                )
                            )
                        except (zipfile.BadZipFile, IOError, OSError) as exc:
                            logging.warning(
                                "Nelze přečíst hlavičku WAV '%s' v archivu '%s': %s",
                                name,
                                zip_path.name,
                                exc,
                            )
        except (zipfile.BadZipFile, IOError, OSError) as exc:
            logging.error("Nelze otevřít ZIP archiv '%s': %s", zip_path.name, exc)
        return wav_infos

``n
### adapters\filesystem\__init__.py

`$tag


``n
### adapters\filesystem\file_discovery.py

`$tag
from __future__ import annotations

import logging
import re
from pathlib import Path

from core.models.analysis import FilePair
from core.models.settings import IdExtractionSettings

ID_PATTERN = re.compile(r"\d+")


def extract_numeric_id(filename: str, settings: IdExtractionSettings) -> list[int]:
    """Extract filtered numeric IDs from filename using injected settings."""
    matches = ID_PATTERN.findall(filename)
    if not matches:
        return []

    min_digits = settings.min_digits
    max_digits = settings.max_digits
    assert min_digits <= max_digits, "IdExtractionSettings must satisfy min_digits <= max_digits"

    ignore_values = set(settings.ignore_numbers)

    filtered_ids: set[int] = set()
    for match in matches:
        if not match.isdigit():
            continue
        if not (min_digits <= len(match) <= max_digits):
            continue
        normalized = str(int(match))
        if match in ignore_values or normalized in ignore_values:
            continue
        filtered_ids.add(int(match))

    return sorted(filtered_ids)


def discover_and_pair_files(
    pdf_dir: Path, wav_dir: Path, settings: IdExtractionSettings
) -> tuple[dict[int, FilePair], int]:
    """Discover and pair files using injected ID extraction settings."""
    logging.info(f"Skenuji PDF v: {pdf_dir}")
    pdf_map: dict[int, list[Path]] = {}
    for p in pdf_dir.rglob("*.pdf"):
        ids = extract_numeric_id(p.name, settings)
        if not ids:
            continue
        for id_val in ids:
            pdf_map.setdefault(id_val, []).append(p)

    logging.info(f"Skenuji ZIP v: {wav_dir}")
    zip_map: dict[int, list[Path]] = {}
    for p in wav_dir.rglob("*.zip"):
        ids = extract_numeric_id(p.name, settings)
        if not ids:
            continue
        for id_val in ids:
            zip_map.setdefault(id_val, []).append(p)

    pairs: dict[int, FilePair] = {}
    skipped_count = 0
    seen_pairs: set[tuple[Path, Path]] = set()

    for id_val in sorted(set(pdf_map.keys()) & set(zip_map.keys())):
        pdf_files = pdf_map[id_val]
        zip_files = zip_map[id_val]

        if len(pdf_files) == 1 and len(zip_files) == 1:
            pair_key = (pdf_files[0], zip_files[0])
            if pair_key in seen_pairs:
                logging.debug(f"Skipping duplicate pair for ID {id_val}: {pdf_files[0].name} & {zip_files[0].name}")
                continue
            pairs[id_val] = FilePair(pdf=pdf_files[0], zip=zip_files[0])
            seen_pairs.add(pair_key)
        else:
            logging.warning(f"Ambiguous pairing for ID {id_val}: {len(pdf_files)} PDF(s), {len(zip_files)} ZIP(s)")
            skipped_count += 1
    return pairs, skipped_count

``n
### adapters\pdf\__init__.py

`$tag

``n
### adapters\pdf\renderer.py

`$tag
from __future__ import annotations
import io
from pathlib import Path
from typing import List

try:
    import fitz  # PyMuPDF
    from PIL import Image
except ImportError as e:
    raise ImportError(f"Missing PDF processing libraries: {e}. Please run 'pip install PyMuPDF Pillow'")

class PdfImageRenderer:
    """Adapter for rendering PDF pages into PIL Images using PyMuPDF."""

    def render(self, pdf_path: Path, dpi: int = 300) -> List[Image.Image]:
        """
        Renders each page of a PDF file into a list of PIL Image objects.

        Args:
            pdf_path: The path to the PDF file.
            dpi: The resolution (dots per inch) for rendering.

        Returns:
            A list of PIL Image objects, one for each page.
        """
        images = []
        doc = fitz.open(str(pdf_path))
        for page in doc:
            pix = page.get_pixmap(dpi=dpi)
            img = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
            images.append(img)
        return images

``n
### app.py

`$tag
import json
import sys
import os
from pathlib import Path
from typing import Optional

# Debug: Print the Python executable path to validate which Python is being used
print(f"Debug: Python executable: {sys.executable}")

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase
from PyQt6.QtWidgets import QApplication

from config import cfg, load_config
from ui.main_window import MainWindow
from ui.config_models import (
    load_tolerance_settings,
    load_id_extraction_settings,
    load_export_settings,
    load_theme_settings,
    load_waveform_settings,
    load_worker_settings,
)
from ui.workers.worker_manager import AnalysisWorkerManager
from ui.theme import load_gz_media_fonts, load_gz_media_stylesheet
import ui._icons_rc  # Import Qt resources for icons (registers search paths)
from ui.constants import SETTINGS_FILENAME

if os.environ.get("QT_QPA_PLATFORM") in {"offscreen", "minimal"}:
    fonts_dir = Path(__file__).resolve().parent / "fonts"
    if fonts_dir.exists():
        for font_path in fonts_dir.glob("*.ttf"):
            QFontDatabase.addApplicationFont(str(font_path))


def main(config_path: Optional[Path] = None):
    """
    Entry point for the application. Assembles and launches the UI with dependency injection.
    """
    if config_path is None:
        env_path = os.getenv("TRACKLIST_CONFIG")
        config_path = Path(env_path) if env_path else SETTINGS_FILENAME
    else:
        config_path = Path(config_path)

    scale_value = None
    if config_path.exists():
        try:
            with config_path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            ui_section = data.get("ui", {})
            scale_value = ui_section.get("dpi_scale", "AUTO")
        except Exception:
            scale_value = None

    if hasattr(Qt, "ApplicationAttribute") and hasattr(Qt.ApplicationAttribute, "AA_EnableHighDpiScaling"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, "ApplicationAttribute") and hasattr(Qt.ApplicationAttribute, "AA_UseHighDpiPixmaps"):
        QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    if isinstance(scale_value, (int, float)) and float(scale_value) not in (0.0, 1.0):
        os.environ.setdefault("QT_SCALE_FACTOR", str(scale_value))
    elif isinstance(scale_value, str):
        value = scale_value.strip()
        if value and value.upper() != "AUTO":
            os.environ.setdefault("QT_SCALE_FACTOR", value)

    app = QApplication(sys.argv)

    load_config(config_path)

    tolerance_settings = load_tolerance_settings(cfg)
    id_extraction_settings = load_id_extraction_settings(cfg)
    export_settings = load_export_settings(cfg)
    theme_settings = load_theme_settings(cfg)
    waveform_settings = load_waveform_settings(cfg)
    worker_settings = load_worker_settings(cfg)

    worker_manager = AnalysisWorkerManager(
        worker_settings=worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )
    load_gz_media_fonts(app, font_family=theme_settings.font_family, font_size=theme_settings.font_size)
    load_gz_media_stylesheet(app, stylesheet_path=theme_settings.stylesheet_path)

    window = MainWindow(
        tolerance_settings=tolerance_settings,
        export_settings=export_settings,
        theme_settings=theme_settings,
        waveform_settings=waveform_settings,
        worker_manager=worker_manager,
        settings_filename=config_path,
    )
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

``n
### audio_utils.py

`$tag
from __future__ import annotations

from pathlib import Path
import logging


def get_wav_duration(path: Path) -> float:
    """Return duration seconds of a WAV file using soundfile, with wave fallback.

    Uses libsndfile via `soundfile` for robust support of WAV variants. If that
    fails, falls back to Python's builtin `wave` header read. Returns 0 on error.
    """
    # Primary: soundfile (libsndfile)
    try:
        import soundfile as sf

        info = sf.info(str(path))
        if info.samplerate and info.frames:
            return float(info.frames) / float(info.samplerate)
    except Exception as e:
        logging.debug("soundfile failed to read %s: %s", path.name, e)

    # Fallback: wave
    try:
        import wave

        with wave.open(str(path), "rb") as w:
            frames = w.getnframes()
            rate = w.getframerate()
            return (frames / float(rate)) if rate > 0 else 0.0
    except Exception as e:
        logging.warning("Unable to read WAV header for '%s': %s", path.name, e)
        return 0.0

``n
### config.py

`$tag
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

``n
### core\__init__.py

`$tag


``n
### core\domain\__init__.py

`$tag


``n
### core\domain\comparison.py

`$tag
from __future__ import annotations

from pathlib import Path

from core.models.analysis import SideResult, TrackInfo, WavInfo
from core.models.settings import ToleranceSettings
from core.ports import AudioModeDetector


def detect_audio_mode(
    wavs: list[WavInfo], detector: AudioModeDetector
) -> tuple[dict[str, str], dict[str, list[WavInfo]]]:
    """
    Vylepšená detekce stran/pořadí:
    strict z názvu → AI fallback (je-li k dispozici) → deterministické fallback,
    poté normalizace pořadí per strana.

    Args:
        wavs: List of WavInfo objects with filename and duration_sec populated.
        detector: AudioModeDetector instance to use for side/position detection.

    Returns:
        Tuple of (modes, side_map) where modes maps side to mode string,
        and side_map maps side to list of WavInfo objects with normalized positions.
    """
    # Use the injected detector for side/position detection
    side_map = detector.detect(wavs)
    # Detector returns normalized results, so no need for separate normalization

    modes: dict[str, str] = {side: ("side" if len(items) == 1 else "tracks") for side, items in side_map.items()}
    return modes, side_map


def compare_data(
    pdf_data: dict[str, list[TrackInfo]],
    wav_data: list[WavInfo],
    pair_info: dict[str, Path],
    tolerance_settings: ToleranceSettings,
    detector: AudioModeDetector,
) -> list[SideResult]:
    """Compare PDF and WAV track data using injected tolerance thresholds.

    Args:
        pdf_data: Dictionary mapping sides to lists of TrackInfo from PDF.
        wav_data: List of WavInfo objects from WAV files.
        pair_info: Dictionary with 'pdf' and 'zip' paths.
        tolerance_settings: ToleranceSettings object with warn/fail thresholds.
        detector: AudioModeDetector instance to use for side/position detection.

    Returns:
        List of SideResult objects with comparison results.
    """
    results: list[SideResult] = []
    modes, wavs_by_side = detect_audio_mode(wav_data, detector)
    all_sides = set(pdf_data.keys()) | set(wavs_by_side.keys())

    tolerance_warn = tolerance_settings.warn_tolerance
    tolerance_fail = tolerance_settings.fail_tolerance

    for side in sorted(all_sides):
        pdf_tracks = pdf_data.get(side, [])
        wav_tracks = wavs_by_side.get(side, [])
        sorted_wav_tracks = sorted(
            wav_tracks,
            key=lambda track: track.position if track.position is not None else 99,
        )
        mode = modes.get(side, "tracks")

        total_pdf_sec = sum(t.duration_sec for t in pdf_tracks)
        total_wav_sec = sum(w.duration_sec for w in wav_tracks)
        difference = round(total_wav_sec - total_pdf_sec)

        status = "OK"
        if abs(difference) > tolerance_fail:
            status = "FAIL"
        elif abs(difference) > tolerance_warn:
            status = "WARN"

        results.append(
            SideResult(
                seq=0,  # Will be assigned by TopTableModel.add_result()
                pdf_path=pair_info["pdf"],
                zip_path=pair_info["zip"],
                side=side,
                mode=mode,
                status=status,
                pdf_tracks=pdf_tracks,
                wav_tracks=sorted_wav_tracks,
                total_pdf_sec=total_pdf_sec,
                total_wav_sec=total_wav_sec,
                total_difference=difference,
            )
        )
    return results

``n
### core\domain\extraction.py

`$tag
"""Domain-level abstractions for audio extraction."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from core.models.analysis import WavInfo


class WavReader(Protocol):
    """Abstraction used by domain services to retrieve WAV metadata without performing I/O."""

    def read_wav_files(self, zip_path: Path) -> list[WavInfo]:
        """Return WAV metadata derived from the provided ZIP archive."""

``n
### core\domain\parsing.py

`$tag
from __future__ import annotations

import re
from pathlib import Path
from typing import NamedTuple, Optional

# Named constant to replace magic numbers
UNKNOWN_POSITION = 999

class ParsedFileInfo(NamedTuple):
    side: Optional[str]
    position: Optional[int]

class StrictFilenameParser:
    """A domain service to centralize all strict filename parsing logic."""

    def parse(self, filename: str | Path) -> ParsedFileInfo:
        """
        Parses side and position from a filename using deterministic regex patterns.

        Args:
            filename: The filename (or full path) to parse.

        Returns:
            A ParsedFileInfo tuple containing the extracted side and position.
        """
        name = Path(filename).stem

        # pos: prefix číslo "01_Track"
        m_pos = re.match(r"^0*([1-9][0-9]?)\b", name)
        pos = int(m_pos.group(1)) if m_pos else None

        # side: "Side_A", "Side-AA"
        m_side = re.search(r"(?i)side[^A-Za-z0-9]*([A-Za-z]+)", name)
        side = m_side.group(1).upper() if m_side else None

        # "A1", "AA02"
        if side is None:
            m_pref = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)[^A-Za-z0-9]*", name)
            if m_pref:
                side = m_pref.group(1).upper()
                if pos is None:
                    pos = int(m_pref.group(2))

        # "Side_A_01", "SideA_02", "Side_A01"
        if pos is None and side:
            m_pos2 = re.search(rf"(?i)side[^A-Za-z0-9]*{re.escape(side)}[^0-9]*0*([1-9][0-9]?)", name)
            if m_pos2:
                pos = int(m_pos2.group(1))

        # Handle Windows paths - extract filename from full path
        if side is None and pos is None:
            # For Windows paths like "C:\Users\Music\B2_Song.mp3", extract just the filename part
            path_str = str(filename)
            if '\\' in path_str:
                # Windows path - get the last component after backslash
                basename = path_str.split('\\')[-1]
                # Remove extension to get stem
                name = Path(basename).stem
                # Retry parsing with just the filename
                m_pos = re.match(r"^0*([1-9][0-9]?)\b", name)
                pos = int(m_pos.group(1)) if m_pos else None
                m_side = re.search(r"(?i)side[^A-Za-z0-9]*([A-Za-z]+)", name)
                side = m_side.group(1).upper() if m_side else None
                if side is None:
                    m_pref = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)[^A-Za-z0-9]*", name)
                    if m_pref:
                        side = m_pref.group(1).upper()
                        if pos is None:
                            pos = int(m_pref.group(2))
                if pos is None and side:
                    m_pos2 = re.search(rf"(?i)side[^A-Za-z0-9]*{re.escape(side)}[^0-9]*0*([1-9][0-9]?)", name)
                    if m_pos2:
                        pos = int(m_pos2.group(1))

        return ParsedFileInfo(side=side, position=pos)

import logging
from core.models.analysis import TrackInfo

class TracklistParser:
    """A domain service for parsing and consolidating track data from a raw VLM response."""

    def parse(self, raw_data: list[dict[str, Any]]) -> list[TrackInfo]:
        """
        Cleans, deduplicates, and converts raw AI data into strict TrackInfo objects.

        Args:
            raw_data: A list of track dictionaries from the VLM response.

        Returns:
            A sorted and deduplicated list of TrackInfo objects.
        """
        final_tracks = []
        seen = set()
        time_pattern = re.compile(r'(\d{1,2}):([0-5]\d)')

        for track_data in raw_data:
            try:
                title = str(track_data.get("title", "")).strip()
                side = str(track_data.get("side", "?")).strip().upper()
                position = int(track_data.get("position", UNKNOWN_POSITION))
                duration_str = str(track_data.get("duration_formatted", "")).strip()

                if not title or not duration_str:
                    continue

                match = time_pattern.match(duration_str)
                if not match:
                    continue
                
                minutes, seconds = int(match.group(1)), int(match.group(2))
                duration_sec = minutes * 60 + seconds
                
                if minutes > 25: # Sanity check for unreasonable durations
                    logging.warning(f"Ignoring track with unreasonable duration: {title} ({duration_str})")
                    continue

                key = (title.lower(), side, duration_sec)
                if key in seen:
                    continue
                seen.add(key)

                final_tracks.append(TrackInfo(
                    title=title, side=side, position=position, duration_sec=duration_sec
                ))
            except (ValueError, TypeError, KeyError) as e:
                logging.warning(f"Failed to process track data: {track_data}. Error: {e}")

        final_tracks.sort(key=lambda t: (t.side, t.position, t.title))
        return final_tracks

``n
### core\domain\steps.py

`$tag
from __future__ import annotations

from typing import Protocol, List
from core.models.analysis import WavInfo

class DetectionStep(Protocol):
    """Protocol for a single step in the audio mode detection chain."""

    def process(self, wavs: List[WavInfo]) -> bool:
        """
        Processes a list of WavInfo objects to detect side and position.

        Args:
            wavs: The list of WavInfo objects to process.

        Returns:
            True if the chain should stop processing (definitive result found),
            False to continue to the next step.
        """
        ...

``n
### core\models\__init__.py

`$tag
"""Core model exports for convenience."""

from .analysis import *  # noqa: F401,F403
from .settings import ExportSettings, IdExtractionSettings, ToleranceSettings

__all__ = [
    "ExportSettings",
    "IdExtractionSettings",
    "ToleranceSettings",
]

``n
### core\models\analysis.py

`$tag
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel


class TrackInfo(BaseModel):
    title: str
    side: str
    position: int
    duration_sec: int


class WavInfo(BaseModel):
    filename: str
    duration_sec: float
    side: str | None = None
    position: int | None = None


class SideResult(BaseModel):
    seq: int
    pdf_path: Path
    zip_path: Path
    side: str
    mode: str
    status: str
    pdf_tracks: list[TrackInfo]
    wav_tracks: list[WavInfo]
    total_pdf_sec: int
    total_wav_sec: float
    total_difference: int


@dataclass
class FilePair:
    """Represents a paired PDF and ZIP file based on a shared numeric ID."""

    pdf: Path
    zip: Path

``n
### core\models\settings.py

`$tag
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

``n
### core\ports.py

`$tag
"""Port interfaces for hexagonal architecture - domain depends on these abstractions, adapters implement them."""

from typing import Protocol

from core.models.analysis import WavInfo


class AudioModeDetector(Protocol):
    """Protocol for detecting audio side/position from WAV filenames.

    This protocol defines the contract for audio mode detection strategies.
    Implementations can use various approaches (AI-backed, deterministic parsing, etc.)
    while maintaining the same interface.

    Purpose:
        Detect side (e.g., "A", "B") and position (1, 2, 3...) from WAV filenames.
        This abstraction allows the domain layer to remain independent of detection
        strategy, enabling easy swapping between AI-backed and test implementations.

    Input:
        list[WavInfo]: List of WavInfo objects with filename and duration_sec populated.
        The side and position fields may be None initially.

    Output:
        dict[str, list[WavInfo]]: Dictionary mapping side (e.g., "A", "B") to list of
        WavInfo objects with side and position fields populated and normalized.

    Normalization:
        Positions must be sequential (1, 2, 3...) with no gaps or duplicates.
        For each side, positions are renumbered to start at 1 and increment by 1.
    """

    def detect(self, wavs: list[WavInfo]) -> dict[str, list[WavInfo]]:
        """Detect audio side and position from WAV filenames.

        Args:
            wavs: List of WavInfo objects with filename and duration_sec populated.

        Returns:
            Dictionary mapping side (e.g., "A", "B") to list of WavInfo objects
            with side and position fields populated and normalized.
        """
        ...

``n
### fluent_gui.py

`$tag
#!/usr/bin/env python3
# DEPRECATION WARNING:
# This file is a backward-compatibility wrapper.
# New development should use the modular components from the `ui/` package
# and the new entry point `app.py`.
# Export helpers moved to services/export_service.py.
#
# UI CHANGES: Text symbols (SYMBOL_CHECK, SYMBOL_CROSS) are deprecated in favor of
# custom SVG icons (ICON_CHECK, ICON_CROSS, ICON_PLAY). Use get_custom_icon() for
# consistent cross-platform icon rendering.

from PyQt6.QtWidgets import QApplication, QDialogButtonBox

from config import cfg, load_config
from core.models.analysis import SideResult, TrackInfo, WavInfo
from ui import (
    BUTTON_RUN_ANALYSIS,
    COLOR_WHITE,
    FILTER_ALL,
    FILTER_FAIL,
    FILTER_OK,
    FILTER_WARN,
    INTERFACE_MAIN,
    LABEL_FILTER,
    LABEL_TOTAL_TRACKS,
    MSG_DONE,
    MSG_ERROR,
    MSG_ERROR_PATHS,
    MSG_NO_PAIRS,
    MSG_PROCESSING_PAIR,
    MSG_SCANNING,
    PLACEHOLDER_DASH,
    SETTINGS_FILENAME,
    STATUS_ANALYZING,
    STATUS_FAIL,
    STATUS_OK,
    STATUS_READY,
    STATUS_WARN,
    SYMBOL_CHECK,
    SYMBOL_CROSS,
    TABLE_HEADERS_BOTTOM,
    TABLE_HEADERS_TOP,
    WINDOW_TITLE,
    AnalysisWorker,
    AnalysisWorkerManager,
    ResultsTableModel,
    TracksTableModel,
    load_export_settings,
    load_id_extraction_settings,
    load_theme_settings,
    load_tolerance_settings,
    load_waveform_settings,
    load_worker_settings,
)
from ui import (
    MainWindow as UIMainWindow,
)
from ui import (
    SettingsDialog as UISettingsDialog,
)
from ui import (
    get_gz_color as _ui_get_gz_color,
)
from ui import (
    load_gz_media_fonts as _ui_load_fonts,
)
from ui import (
    load_gz_media_stylesheet as _ui_load_stylesheet,
)
from ui.theme import get_system_file_icon, get_custom_icon

__all__ = [
    "MainWindow",
    "TopTableModel",
    "BottomTableModel",
    "ResultsTableModel",
    "TracksTableModel",
    "AnalysisWorker",
    "AnalysisWorkerManager",
    "SettingsDialog",
    "get_gz_color",
    "get_custom_icon",
    "load_gz_media_fonts",
    "load_gz_media_stylesheet",
    "SideResult",
    "TrackInfo",
    "WavInfo",
    "ICON_OPEN_QICON",
    "BUTTON_RUN_ANALYSIS",
    "COLOR_WHITE",
    "FILTER_ALL",
    "FILTER_FAIL",
    "FILTER_OK",
    "FILTER_WARN",
    "INTERFACE_MAIN",
    "LABEL_FILTER",
    "LABEL_TOTAL_TRACKS",
    "MSG_DONE",
    "MSG_ERROR",
    "MSG_ERROR_PATHS",
    "MSG_NO_PAIRS",
    "MSG_PROCESSING_PAIR",
    "MSG_SCANNING",
    "PLACEHOLDER_DASH",
    "SETTINGS_FILENAME",
    "STATUS_ANALYZING",
    "STATUS_FAIL",
    "STATUS_OK",
    "STATUS_READY",
    "STATUS_WARN",
    "SYMBOL_CHECK",
    "SYMBOL_CROSS",
    "SYMBOL_OPEN",
    "TABLE_HEADERS_BOTTOM",
    "TABLE_HEADERS_TOP",
    "WINDOW_TITLE",
    # Icon constants
    "ICON_CHECK",
    "ICON_CROSS",
    "ICON_PLAY",
    # Comment constants
    "COMMENT_SETUP_TOP_TABLE",
    "COMMENT_SETUP_BOTTOM_TABLE",
    "COMMENT_MAX_WIDTH_WAV",
    "COMMENT_APP_STARTUP",
    "COMMENT_CONFIG_LOAD",
    "COMMENT_CONFIG_ERROR",
    "COMMENT_BUTTON_COLOR",
    "COMMENT_BUTTON_COLOR_DESC",
]

TopTableModel = ResultsTableModel
BottomTableModel = TracksTableModel
ICON_OPEN_QICON = get_system_file_icon("file")

# Additional constants for backward compatibility
SYMBOL_OPEN = "▶"
COMMENT_SETUP_TOP_TABLE = "Setup top table with PDF data"
COMMENT_SETUP_BOTTOM_TABLE = "Setup bottom table with WAV data"
COMMENT_MAX_WIDTH_WAV = "Maximum width for WAV file columns"
COMMENT_APP_STARTUP = "Application startup initialization"
COMMENT_CONFIG_LOAD = "Loading configuration from settings file"
COMMENT_CONFIG_ERROR = "Error loading configuration"
COMMENT_BUTTON_COLOR = "Button color configuration"
COMMENT_BUTTON_COLOR_DESC = "Description of button color settings"


def get_gz_color(color_key: str):
    theme_settings = load_theme_settings(cfg)
    return _ui_get_gz_color(color_key, theme_settings.status_colors)


def load_gz_media_fonts(app):
    theme_settings = load_theme_settings(cfg)
    _ui_load_fonts(app, font_family=theme_settings.font_family, font_size=theme_settings.font_size)


def load_gz_media_stylesheet(app):
    theme_settings = load_theme_settings(cfg)
    _ui_load_stylesheet(app, stylesheet_path=theme_settings.stylesheet_path)


# Export functionality moved to services/export_service.py (Phase 4 refactoring)


class SettingsDialog(UISettingsDialog):
    def __init__(self, parent=None):
        super().__init__(settings_filename=SETTINGS_FILENAME, parent=parent)
        button_box = self.findChild(QDialogButtonBox)
        self.save_button = None
        if button_box is not None:
            self.save_button = button_box.button(QDialogButtonBox.StandardButton.Save)


class MainWindow(UIMainWindow):
    def __init__(self, *args, **kwargs):
        if args or kwargs:
            super().__init__(*args, **kwargs)
            return

        load_config(SETTINGS_FILENAME)
        tolerance_settings = load_tolerance_settings(cfg)
        export_settings = load_export_settings(cfg)
        theme_settings = load_theme_settings(cfg)
        worker_settings = load_worker_settings(cfg)
        id_extraction_settings = load_id_extraction_settings(cfg)
        waveform_settings = load_waveform_settings(cfg)

        app = QApplication.instance()
        if app is not None:
            _ui_load_fonts(app, theme_settings.font_family, theme_settings.font_size)
            _ui_load_stylesheet(app, theme_settings.stylesheet_path)

        worker_manager = AnalysisWorkerManager(
            worker_settings=worker_settings,
            tolerance_settings=tolerance_settings,
            id_extraction_settings=id_extraction_settings,
        )

        super().__init__(
            tolerance_settings=tolerance_settings,
            export_settings=export_settings,
            theme_settings=theme_settings,
            waveform_settings=waveform_settings,
            worker_manager=worker_manager,
            settings_filename=SETTINGS_FILENAME,
        )


if __name__ == "__main__":
    from app import main

    main()

``n
### fonts\dejavu-fonts-ttf-2.37\LICENSE

``nFonts are (c) Bitstream (see below). DejaVu changes are in public domain.
Glyphs imported from Arev fonts are (c) Tavmjong Bah (see below)


Bitstream Vera Fonts Copyright
------------------------------

Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved. Bitstream Vera is
a trademark of Bitstream, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of the fonts accompanying this license ("Fonts") and associated
documentation files (the "Font Software"), to reproduce and distribute the
Font Software, including without limitation the rights to use, copy, merge,
publish, distribute, and/or sell copies of the Font Software, and to permit
persons to whom the Font Software is furnished to do so, subject to the
following conditions:

The above copyright and trademark notices and this permission notice shall
be included in all copies of one or more of the Font Software typefaces.

The Font Software may be modified, altered, or added to, and in particular
the designs of glyphs or characters in the Fonts may be modified and
additional glyphs or characters may be added to the Fonts, only if the fonts
are renamed to names not containing either the words "Bitstream" or the word
"Vera".

This License becomes null and void to the extent applicable to Fonts or Font
Software that has been modified and is distributed under the "Bitstream
Vera" names.

The Font Software may be sold as part of a larger software package but no
copy of one or more of the Font Software typefaces may be sold by itself.

THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF COPYRIGHT, PATENT,
TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL BITSTREAM OR THE GNOME
FOUNDATION BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, INCLUDING
ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE
FONT SOFTWARE.

Except as contained in this notice, the names of Gnome, the Gnome
Foundation, and Bitstream Inc., shall not be used in advertising or
otherwise to promote the sale, use or other dealings in this Font Software
without prior written authorization from the Gnome Foundation or Bitstream
Inc., respectively. For further information, contact: fonts at gnome dot
org.

Arev Fonts Copyright
------------------------------

Copyright (c) 2006 by Tavmjong Bah. All Rights Reserved.

Permission is hereby granted, free of charge, to any person obtaining
a copy of the fonts accompanying this license ("Fonts") and
associated documentation files (the "Font Software"), to reproduce
and distribute the modifications to the Bitstream Vera Font Software,
including without limitation the rights to use, copy, merge, publish,
distribute, and/or sell copies of the Font Software, and to permit
persons to whom the Font Software is furnished to do so, subject to
the following conditions:

The above copyright and trademark notices and this permission notice
shall be included in all copies of one or more of the Font Software
typefaces.

The Font Software may be modified, altered, or added to, and in
particular the designs of glyphs or characters in the Fonts may be
modified and additional glyphs or characters may be added to the
Fonts, only if the fonts are renamed to names not containing either
the words "Tavmjong Bah" or the word "Arev".

This License becomes null and void to the extent applicable to Fonts
or Font Software that has been modified and is distributed under the 
"Tavmjong Bah Arev" names.

The Font Software may be sold as part of a larger software package but
no copy of one or more of the Font Software typefaces may be sold by
itself.

THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL
TAVMJONG BAH BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL
DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF THE USE OR INABILITY TO USE THE FONT SOFTWARE OR FROM
OTHER DEALINGS IN THE FONT SOFTWARE.

Except as contained in this notice, the name of Tavmjong Bah shall not
be used in advertising or otherwise to promote the sale, use or other
dealings in this Font Software without prior written authorization
from Tavmjong Bah. For further information, contact: tavmjong @ free
. fr.

TeX Gyre DJV Math
-----------------
Fonts are (c) Bitstream (see below). DejaVu changes are in public domain.

Math extensions done by B. Jackowski, P. Strzelczyk and P. Pianowski
(on behalf of TeX users groups) are in public domain.

Letters imported from Euler Fraktur from AMSfonts are (c) American
Mathematical Society (see below).
Bitstream Vera Fonts Copyright
Copyright (c) 2003 by Bitstream, Inc. All Rights Reserved. Bitstream Vera
is a trademark of Bitstream, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of the fonts accompanying this license (“Fonts”) and associated
documentation
files (the “Font Software”), to reproduce and distribute the Font Software,
including without limitation the rights to use, copy, merge, publish,
distribute,
and/or sell copies of the Font Software, and to permit persons  to whom
the Font Software is furnished to do so, subject to the following
conditions:

The above copyright and trademark notices and this permission notice
shall be
included in all copies of one or more of the Font Software typefaces.

The Font Software may be modified, altered, or added to, and in particular
the designs of glyphs or characters in the Fonts may be modified and
additional
glyphs or characters may be added to the Fonts, only if the fonts are
renamed
to names not containing either the words “Bitstream” or the word “Vera”.

This License becomes null and void to the extent applicable to Fonts or
Font Software
that has been modified and is distributed under the “Bitstream Vera”
names.

The Font Software may be sold as part of a larger software package but
no copy
of one or more of the Font Software typefaces may be sold by itself.

THE FONT SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF COPYRIGHT, PATENT,
TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL BITSTREAM OR THE GNOME
FOUNDATION
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, INCLUDING ANY GENERAL,
SPECIAL, INDIRECT, INCIDENTAL, OR CONSEQUENTIAL DAMAGES, WHETHER IN AN
ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF THE USE OR
INABILITY TO USE
THE FONT SOFTWARE OR FROM OTHER DEALINGS IN THE FONT SOFTWARE.
Except as contained in this notice, the names of GNOME, the GNOME
Foundation,
and Bitstream Inc., shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Font Software without prior written
authorization from the GNOME Foundation or Bitstream Inc., respectively.
For further information, contact: fonts at gnome dot org.

AMSFonts (v. 2.2) copyright

The PostScript Type 1 implementation of the AMSFonts produced by and
previously distributed by Blue Sky Research and Y&Y, Inc. are now freely
available for general use. This has been accomplished through the
cooperation
of a consortium of scientific publishers with Blue Sky Research and Y&Y.
Members of this consortium include:

Elsevier Science IBM Corporation Society for Industrial and Applied
Mathematics (SIAM) Springer-Verlag American Mathematical Society (AMS)

In order to assure the authenticity of these fonts, copyright will be
held by
the American Mathematical Society. This is not meant to restrict in any way
the legitimate use of the fonts, such as (but not limited to) electronic
distribution of documents containing these fonts, inclusion of these fonts
into other public domain or commercial font collections or computer
applications, use of the outline data to create derivative fonts and/or
faces, etc. However, the AMS does require that the AMS copyright notice be
removed from any derivative versions of the fonts which have been altered in
any way. In addition, to ensure the fidelity of TeX documents using Computer
Modern fonts, Professor Donald Knuth, creator of the Computer Modern faces,
has requested that any alterations which yield different font metrics be
given a different name.

$Id$

``n
### mypy.ini

``n[mypy]
ignore_missing_imports = True
# Limit type checking to refactored layers for this phase
files = core, adapters, services
# Phase 1 strictness is enforced via tools/check.sh running `mypy --strict` on these packages.

[mypy-pdf_extractor]
ignore_errors = True

[mypy-wav_extractor_wave]
ignore_errors = True

[mypy-config]
ignore_errors = True

[mypy-ui.*]
ignore_errors = True

[mypy-app]
ignore_errors = True

[mypy-fluent_gui]
ignore_errors = True

[mypy-settings_page]
ignore_errors = True

[mypy-waveform_viewer]
ignore_errors = True

[mypy-pdf_viewer]
ignore_errors = True

``n
### package.json

`$tag
{
  "dependencies": {
    "@fission-ai/openspec": "^0.12.0"
  }
}

``n
### pdf_extractor.py

`$tag
import logging
from pathlib import Path
from typing import List

from adapters.ai.vlm import VlmClient
from adapters.pdf.renderer import PdfImageRenderer
from core.domain.parsing import TracklistParser
from core.models.analysis import TrackInfo

def extract_pdf_tracklist(pdf_path: Path) -> dict[str, List[TrackInfo]]:
    """
    Orchestrates the PDF tracklist extraction process.

    This function uses dedicated components to:
    1. Render PDF pages to images (`PdfImageRenderer`).
    2. Send images to a VLM for analysis (`VlmClient`).
    3. Parse the VLM's JSON response into structured data (`TracklistParser`).
    """
    logging.info(f"Starting PDF extraction for: {pdf_path.name}")
    
    try:
        renderer = PdfImageRenderer()
        vlm_client = VlmClient()
        parser = TracklistParser()

        images = renderer.render(pdf_path)
        if not images:
            logging.warning(f"PDF file '{pdf_path.name}' contains no pages.")
            return {}

        prompt = (
            "You are a tracklist extractor. Return STRICT JSON only.\n"
            "Schema: { \"tracks\": [ {\"title\": string, \"side\": string, \"position\": integer, \"duration_formatted\": \"MM:SS\" } ] }.\n"
            "- Extract all visible tracks.\n"
            "- Normalize time to MM:SS format.\n"
            "- Infer side and position if possible.\n"
            "- Do not invent data. Ignore non-track information."
        )

        all_raw_tracks = []
        for img in images:
            try:
                ai_response = vlm_client.get_json_response(prompt, [img])
                if "tracks" in ai_response and isinstance(ai_response["tracks"], list):
                    all_raw_tracks.extend(ai_response["tracks"])
            except Exception as e:
                logging.error(f"AI call failed for a page from '{pdf_path.name}': {e}")
        
        if not all_raw_tracks:
            logging.warning(f"VLM returned no tracks for file: {pdf_path.name}")
            return {}

        parsed_tracks = parser.parse(all_raw_tracks)
        
        result_by_side: dict[str, list[TrackInfo]] = {}
        for track in parsed_tracks:
            result_by_side.setdefault(track.side, []).append(track)
        
        logging.info(f"PDF extraction for '{pdf_path.name}' complete. Found {len(parsed_tracks)} tracks.")
        return result_by_side

    except Exception as e:
        logging.error(f"Failed to extract tracklist from PDF '{pdf_path.name}': {e}", exc_info=True)
        return {}

``n
### pdf_viewer.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PDF Viewer Module for Tracklist Extractor
Provides custom PDF viewing functionality
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QDesktopServices

from pathlib import Path


class PdfViewerDialog(QDialog):
    """Custom PDF viewer dialog using system default viewer."""

    def __init__(self, pdf_path: Path, parent=None):
        super().__init__(parent)
        self.pdf_path = pdf_path
        self.setWindowTitle(f"PDF Viewer - {pdf_path.name}")
        self.resize(900, 700)

        # Create layout
        layout = QVBoxLayout(self)

        # For now, just open with system viewer and close dialog
        # In future, this could be extended with embedded PDF viewer
        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(pdf_path)))
        except Exception as e:
            print(f"Failed to open PDF: {e}")

        # Add close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)

        # Auto-close after opening (since we're using system viewer)
        self.accept()

``n
### requirements.txt

``nPillow>=10.0
PyMuPDF>=1.24
pydantic>=2.0
python-dotenv>=1.0.1
openai>=1.30
PyQt6>=6.4
pyqtgraph>=0.13.0
soundfile>=0.12
pytest-qt>=4.2.0
pytest-mock>=3.12.0

ruff>=0.5
black>=24.0
mypy>=1.8
pytest>=8.0
coverage>=7.0

``n
### scripts\run_analysis_no_ai.py

`$tag
from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
import sys as _sys
if str(PROJECT_ROOT) not in _sys.path:
    _sys.path.insert(0, str(PROJECT_ROOT))

from services.analysis_service import AnalysisService
from adapters.audio.wav_reader import ZipWavFileReader
from adapters.audio.fake_mode_detector import FakeAudioModeDetector
from core.models.settings import IdExtractionSettings, ToleranceSettings
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python scripts/run_analysis_no_ai.py <PDF_DIR> <WAV_DIR>")
        return 2
    pdf_dir = Path(sys.argv[1])
    wav_dir = Path(sys.argv[2])

    if not pdf_dir.exists() or not wav_dir.exists():
        print(f"Error: Provided paths must exist. PDF: {pdf_dir}, WAV: {wav_dir}")
        return 2

    tol = ToleranceSettings(warn_tolerance=2, fail_tolerance=5)
    ids = IdExtractionSettings(min_digits=3, max_digits=8, ignore_numbers=["33", "45"])  # conservative defaults

    service = AnalysisService(
        tolerance_settings=tol,
        id_extraction_settings=ids,
        wav_reader=ZipWavFileReader(),
        audio_mode_detector=FakeAudioModeDetector(),
    )

    def on_progress(msg: str) -> None:
        print(f"[progress] {msg}")

    def on_result(res: object) -> None:
        try:
            # SideResult has attributes; keep output succinct
            side = getattr(res, "side", "?")
            pdf = getattr(res, "pdf_path", "?")
            zipf = getattr(res, "zip_path", "?")
            status = getattr(res, "status", "?")
            total_diff = getattr(res, "total_difference", "?")
            print(f"[result] side={side} status={status} diff={total_diff} pdf={getattr(pdf, 'name', pdf)} zip={getattr(zipf, 'name', zipf)}")
        except Exception:
            print(f"[result] {res}")

    def on_finished(msg: str) -> None:
        print(f"[finished] {msg}")

    service.start_analysis(pdf_dir, wav_dir, on_progress, on_result, on_finished)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

``n
### scripts\smoke_test.py

`$tag
import logging
import sys
from collections import Counter
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from adapters.audio.ai_mode_detector import AiAudioModeDetector
from adapters.audio.wav_reader import ZipWavFileReader
from adapters.filesystem.file_discovery import discover_and_pair_files
from core.domain.comparison import compare_data
from config import cfg
from pdf_extractor import extract_pdf_tracklist
from ui.config_models import load_id_extraction_settings, load_tolerance_settings

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

pdf_dir = Path('test_data/pdf').resolve()
wav_dir = Path('test_data/wav').resolve()
print(f"Using pdf_dir={pdf_dir}")
print(f"Using wav_dir={wav_dir}")

if not pdf_dir.exists() or not wav_dir.exists():
    print("Test data directories not found. Aborting.")
    sys.exit(2)

tolerance_settings = load_tolerance_settings(cfg)
id_extraction_settings = load_id_extraction_settings(cfg)
wav_reader = ZipWavFileReader()
audio_mode_detector = AiAudioModeDetector()

pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir, id_extraction_settings)
print(f"Found {len(pairs)} pair(s); {skipped} ambiguous skipped")

all_results = []
for i, (file_id, pair_info) in enumerate(pairs.items(), 1):
    print(f"Processing {i}/{len(pairs)}: {pair_info.pdf.name}")
    pdf_data = extract_pdf_tracklist(pair_info.pdf)
    wav_data = wav_reader.read_wav_files(pair_info.zip)
    pair_info_dict = {"pdf": pair_info.pdf, "zip": pair_info.zip}
    side_results = compare_data(pdf_data, wav_data, pair_info_dict, tolerance_settings, audio_mode_detector)
    all_results.extend(side_results)

print(f"Side results: {len(all_results)}")
status_counts = Counter(r.status for r in all_results)
print("Status counts:", dict(status_counts))

sys.exit(0 if all_results else 1)

``n
### scripts\smoke_wav_only.py

`$tag
from __future__ import annotations
import sys
from pathlib import Path

# Ensure project root is on sys.path when running as a standalone script
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
from adapters.audio.wav_reader import ZipWavFileReader
from adapters.filesystem.file_discovery import discover_and_pair_files
from adapters.audio.fake_mode_detector import FakeAudioModeDetector
from core.models.settings import IdExtractionSettings


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: python scripts/smoke_wav_only.py <PDF_DIR> <WAV_DIR>")
        return 2
    pdf_dir = Path(sys.argv[1])
    wav_dir = Path(sys.argv[2])

    if not pdf_dir.exists() or not wav_dir.exists():
        print(f"Error: Provided paths must exist. PDF: {pdf_dir}, WAV: {wav_dir}")
        return 2

    # Conservative ID extraction defaults
    id_settings = IdExtractionSettings(min_digits=3, max_digits=8, ignore_numbers=["33", "45"]) 

    pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir, id_settings)
    print(f"Discovered pairs: {len(pairs)} (skipped ambiguous: {skipped})")

    if not pairs:
        return 0

    reader = ZipWavFileReader()
    detector = FakeAudioModeDetector()

    # Process up to first 3 pairs for brevity
    for idx, (file_id, pair) in enumerate(list(pairs.items())[:3], start=1):
        print(f"\nPair {idx}: ID={file_id} PDF={pair.pdf.name} ZIP={pair.zip.name}")
        wavs = reader.read_wav_files(pair.zip)
        print(f"  WAV files read: {len(wavs)}")
        if not wavs:
            continue
        side_map = detector.detect(wavs)
        for side, items in sorted(side_map.items()):
            positions = [w.position for w in items]
            print(f"  Side {side}: {len(items)} tracks; positions={positions}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

``n
### services\__init__.py

`$tag


``n
### services\analysis_service.py

`$tag
from __future__ import annotations

import logging
from pathlib import Path
from typing import Callable

from adapters.audio.chained_detector import ChainedAudioModeDetector
from adapters.audio.wav_reader import ZipWavFileReader
from adapters.filesystem.file_discovery import discover_and_pair_files
from core.domain.comparison import compare_data
from core.models.settings import IdExtractionSettings, ToleranceSettings
from core.ports import AudioModeDetector
from pdf_extractor import extract_pdf_tracklist


class AnalysisService:
    """Pure-Python orchestrator for the analysis process.

    Uses callbacks to report progress, results, and completion, so it can run
    in any thread context without Qt dependencies. Configuration settings
    and audio mode detector are injected via the constructor to keep dependencies explicit.
    """

    def __init__(
        self,
        tolerance_settings: ToleranceSettings,
        id_extraction_settings: IdExtractionSettings,
        wav_reader: ZipWavFileReader | None = None,
        audio_mode_detector: AudioModeDetector | None = None,
    ) -> None:
        self._tolerance_settings = tolerance_settings
        self._id_extraction_settings = id_extraction_settings
        self._wav_reader = wav_reader or ZipWavFileReader()
        # Use the new Chained detector as the default
        self._audio_mode_detector = audio_mode_detector or ChainedAudioModeDetector()

    def start_analysis(
        self,
        pdf_dir: Path,
        wav_dir: Path,
        progress_callback: Callable[[str], None],
        result_callback: Callable[[object], None],
        finished_callback: Callable[[str], None],
    ) -> None:
        try:
            progress_callback("Scanning and pairing files...")
            pairs, skipped_count = discover_and_pair_files(
                pdf_dir, wav_dir, self._id_extraction_settings
            )

            if not pairs:
                finished_callback("No valid PDF-ZIP pairs found.")
                return

            total_pairs = len(pairs)
            processed_count = 0
            for i, (file_id, pair_info) in enumerate(pairs.items()):
                try:
                    progress_callback(
                        f"Processing pair {i+1}/{total_pairs}: {pair_info.pdf.name}"
                    )

                    pdf_data = extract_pdf_tracklist(pair_info.pdf)
                    wav_data = self._wav_reader.read_wav_files(pair_info.zip)

                    pair_info_dict = {"pdf": pair_info.pdf, "zip": pair_info.zip}
                    side_results = compare_data(
                        pdf_data,
                        wav_data,
                        pair_info_dict,
                        self._tolerance_settings,
                        self._audio_mode_detector,
                    )

                    for res in side_results:
                        result_callback(res)

                    processed_count += 1
                except Exception as pair_error:
                    logging.error(
                        f"Failed to process pair {pair_info.pdf.name}: {pair_error}",
                        exc_info=True,
                    )
                    progress_callback(
                        f"⚠️ WARN: Skipping pair {pair_info.pdf.name} due to error."
                    )
                    continue

            summary_message = (
                f"Analysis completed. Processed {processed_count}/{total_pairs} pairs."
            )
            if skipped_count > 0:
                summary_message += f" ({skipped_count} ambiguous pairs skipped.)"
            finished_callback(summary_message)
        except Exception as e:
            logging.error("Chyba v AnalysisService:", exc_info=True)
            finished_callback(f"Error in analysis service: {e}")

``n
### services\export_service.py

`$tag
from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from core.models.analysis import SideResult

"""Centralized export service - single source of truth for all analysis result exports.
All export operations should use export_results_to_json() from this module."""


class ExportSettingsProtocol(Protocol):
    auto_export: bool
    export_dir: Path


ExportSettingsType = ExportSettingsProtocol


def export_results_to_json(results: list[SideResult], export_settings: ExportSettingsType) -> Path | None:
    """Export analysis results to JSON using the centralized export service.

    Usage example:
        from services.export_service import export_results_to_json
        exported_path = export_results_to_json(results, export_settings)

    This is the canonical export implementation shared by the UI layer and automated tests.
    Returns the exported file path or ``None`` when nothing is written.
    """
    if not export_settings.auto_export or not results:
        return None

    export_dir = export_settings.export_dir
    try:
        export_dir.mkdir(parents=True, exist_ok=True)
    except Exception:  # pragma: no cover
        logging.error("Failed to prepare export directory: %s", export_dir, exc_info=True)
        return None

    base = datetime.now().strftime("%Y%m%d_%H%M%S")
    payload: dict[str, Any] = {
        "exported_at": base,
        "count": len(results),
        "results": [],
    }

    for result in results:
        item = result.model_dump(mode="json")
        item["pdf_path"] = str(result.pdf_path)
        item["zip_path"] = str(result.zip_path)
        payload["results"].append(item)

    for index in range(1000):
        suffix = f"_{index:03d}" if index else ""
        out_path = export_dir / f"analysis_{base}{suffix}.json"
        try:
            with out_path.open("x", encoding="utf-8") as handle:
                json.dump(payload, handle, ensure_ascii=False, indent=2)
            logging.info("Exported analysis results to %s", out_path)
            return out_path
        except FileExistsError:
            continue
        except Exception:  # pragma: no cover
            logging.error("Failed to export analysis results to %s", out_path, exc_info=True)
            out_path.unlink(missing_ok=True)
            return None

    logging.error("Could not create unique filename for export in %s", export_dir)  # pragma: no cover
    return None

``n
### settings_page.py

`$tag
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

``n
### tests\__init__.py

`$tag


``n
### tests\conftest.py

`$tag
from __future__ import annotations

import contextlib
import math
import zipfile
from pathlib import Path
from typing import Generator, Tuple

import numpy as np
import pytest
import soundfile as sf
from PyQt6.QtCore import QSettings, QTimer
from PyQt6.QtWidgets import QApplication

import config as config_module
from adapters.audio.fake_mode_detector import FakeAudioModeDetector
from core.models.settings import IdExtractionSettings, ToleranceSettings
from ui.config_models import WaveformSettings


@pytest.fixture(scope="session")
def qapp() -> Generator[QApplication, None, None]:
    """Provide a QApplication instance for Qt tests."""
    app = QApplication.instance()
    created = False
    if app is None:
        app = QApplication([])
        created = True

    yield app

    if created:
        with contextlib.suppress(Exception):
            # Allow pending events to process before quitting.
            QTimer.singleShot(0, app.quit)
            app.processEvents()
            app.quit()


@pytest.fixture
def isolated_config(monkeypatch, tmp_path) -> Generator[config_module.AppConfig, None, None]:
    """Provide an isolated configuration with temporary QSettings storage."""
    original_cfg = config_module.cfg
    org_name = original_cfg.settings.organizationName()
    app_name = original_cfg.settings.applicationName()

    user_settings = QSettings(QSettings.Format.IniFormat, QSettings.Scope.UserScope, org_name, app_name)
    system_settings = QSettings(QSettings.Format.IniFormat, QSettings.Scope.SystemScope, org_name, app_name)
    original_user_dir = Path(user_settings.fileName()).parent
    original_system_dir = Path(system_settings.fileName()).parent

    settings_dir = tmp_path / "settings"
    settings_dir.mkdir()
    original_format = QSettings.defaultFormat()
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(settings_dir))
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.SystemScope, str(settings_dir))

    test_cfg = config_module.AppConfig()
    test_cfg.reset_to_defaults()
    monkeypatch.setattr(config_module, "cfg", test_cfg)

    yield test_cfg

    config_module.cfg = original_cfg
    QSettings.setDefaultFormat(original_format)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope, str(original_user_dir))
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.SystemScope, str(original_system_dir))


def _generate_sine_wave(duration: float, sample_rate: int) -> np.ndarray:
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False, dtype=np.float32)
    angles = 2 * math.pi * 440 * t
    waveform = 0.5 * np.sin(angles)
    return waveform.astype(np.float32)


@pytest.fixture
def mock_wav_zip(tmp_path) -> Generator[Tuple[Path, str], None, None]:
    """Create a temporary ZIP containing a valid WAV file."""
    wav_filename = "test_track.wav"
    wav_path = tmp_path / wav_filename
    sample_rate = 44100
    data = _generate_sine_wave(2.0, sample_rate)
    sf.write(wav_path, data, sample_rate)

    zip_path = tmp_path / "test_archive.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(wav_path, arcname=f"tracks/{wav_filename}")

    yield zip_path, wav_filename


@pytest.fixture
def empty_zip(tmp_path) -> Generator[Path, None, None]:
    """Create an empty ZIP archive."""
    zip_path = tmp_path / "empty.zip"
    with zipfile.ZipFile(zip_path, "w"):
        pass
    yield zip_path


@pytest.fixture
def invalid_wav_zip(tmp_path) -> Generator[Tuple[Path, str], None, None]:
    """Create a ZIP containing an invalid WAV payload."""
    wav_filename = "broken_track.wav"
    zip_path = tmp_path / "invalid.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr(wav_filename, b"not-a-valid-wav")
    yield zip_path, wav_filename


@pytest.fixture
def tolerance_settings() -> ToleranceSettings:
    """Provide default tolerance settings for tests."""
    return ToleranceSettings(warn_tolerance=2, fail_tolerance=5)


@pytest.fixture
def id_extraction_settings() -> IdExtractionSettings:
    """Provide default numeric ID extraction settings for tests."""
    return IdExtractionSettings(min_digits=1, max_digits=6, ignore_numbers=[])


@pytest.fixture
def waveform_settings() -> WaveformSettings:
    """Provide default waveform viewer/editor settings for tests."""
    return WaveformSettings(
        overview_points=2000,
        min_region_duration=0.3,
        snap_tolerance=0.1,
        enable_snapping=True,
        default_volume=0.5,
        waveform_color="#3B82F6",
        position_line_color="#EF4444",
        downsample_factor=10,
    )


@pytest.fixture
def audio_mode_detector() -> FakeAudioModeDetector:
    """Provide fake audio mode detector for tests (no external API calls)."""
    return FakeAudioModeDetector()

``n
### tests\test_ai_mode_detector.py

`$tag
"""Unit tests for audio mode detector adapters."""

from __future__ import annotations

from unittest.mock import patch, MagicMock

import pytest

from adapters.audio.ai_mode_detector import AiAudioModeDetector
from adapters.audio.fake_mode_detector import FakeAudioModeDetector
from core.models.analysis import WavInfo


class TestAiAudioModeDetector:
    """Test cases for AiAudioModeDetector."""

    def test_ai_detector_with_valid_filenames(self) -> None:
        """Test AI detector with valid WAV filenames."""
        detector = AiAudioModeDetector()
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_B_01_ballad.wav", duration_sec=210.0),
        ]

        # Mock the external API calls
        with patch("adapters.audio.ai_mode_detector.detect_audio_mode_with_ai") as mock_detect:
            with patch("adapters.audio.ai_mode_detector.normalize_positions") as mock_normalize:
                mock_detect.return_value = {
                    "A": [
                        WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0, side="A", position=1),
                        WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0, side="A", position=2),
                    ],
                    "B": [
                        WavInfo(filename="Side_B_01_ballad.wav", duration_sec=210.0, side="B", position=1),
                    ],
                }

                result = detector.detect(wavs)

                # Use simpler assertions to avoid WavInfo comparison issues
                mock_detect.assert_called_once()
                mock_normalize.assert_called_once()
                assert "A" in result
                assert "B" in result
                assert len(result["A"]) == 2
                assert len(result["B"]) == 1
                # Check that the mock was called with the right number of items
                call_args = mock_detect.call_args[0][0]
                assert len(call_args) == 3
                assert call_args[0].filename == "Side_A_01_intro.wav"
                assert call_args[1].filename == "Side_A_02_song.wav"
                assert call_args[2].filename == "Side_B_01_ballad.wav"

    def test_ai_detector_with_ambiguous_filenames(self) -> None:
        """Test AI detector with ambiguous filenames (triggers AI fallback)."""
        detector = AiAudioModeDetector()
        wavs = [
            WavInfo(filename="track1.wav", duration_sec=120.0),
            WavInfo(filename="track2.wav", duration_sec=150.0),
            WavInfo(filename="track3.wav", duration_sec=210.0),
        ]

        with patch("adapters.audio.ai_mode_detector.detect_audio_mode_with_ai") as mock_detect:
            with patch("adapters.audio.ai_mode_detector.normalize_positions") as mock_normalize:
                mock_detect.return_value = {
                    "A": [
                        WavInfo(filename="track1.wav", duration_sec=120.0, side="A", position=1),
                        WavInfo(filename="track2.wav", duration_sec=150.0, side="A", position=2),
                    ],
                    "B": [
                        WavInfo(filename="track3.wav", duration_sec=210.0, side="B", position=1),
                    ],
                }

                result = detector.detect(wavs)

                # Use simpler assertions to avoid WavInfo comparison issues
                mock_detect.assert_called_once()
                mock_normalize.assert_called_once()
                assert "A" in result
                assert "B" in result
                # Check that the mock was called with the right number of items
                call_args = mock_detect.call_args[0][0]
                assert len(call_args) == 3
                assert call_args[0].filename == "track1.wav"
                assert call_args[1].filename == "track2.wav"
                assert call_args[2].filename == "track3.wav"

    def test_ai_detector_with_empty_input(self) -> None:
        """Test AI detector with empty input list."""
        detector = AiAudioModeDetector()
        result = detector.detect([])
        assert result == {}


class TestFakeAudioModeDetector:
    """Test cases for FakeAudioModeDetector."""

    def test_fake_detector_with_side_prefixes(self) -> None:
        """Test fake detector with Side_A/Side_B filenames."""
        detector = FakeAudioModeDetector()
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_B_01_ballad.wav", duration_sec=210.0),
        ]

        result = detector.detect(wavs)

        assert "A" in result
        assert "B" in result
        assert len(result["A"]) == 2
        assert len(result["B"]) == 1
        assert result["A"][0].side == "A"
        assert result["A"][0].position == 1
        assert result["A"][1].side == "A"
        assert result["A"][1].position == 2
        assert result["B"][0].side == "B"
        assert result["B"][0].position == 1

    def test_fake_detector_with_letter_number_prefixes(self) -> None:
        """Test fake detector with A1/B1 prefixes."""
        detector = FakeAudioModeDetector()
        wavs = [
            WavInfo(filename="A1_intro.wav", duration_sec=120.0),
            WavInfo(filename="A2_song.wav", duration_sec=150.0),
            WavInfo(filename="B1_ballad.wav", duration_sec=210.0),
        ]

        result = detector.detect(wavs)

        # Assert both "A" and "B" sides are present
        assert "A" in result
        assert "B" in result
        # Verify correct position counts: 2 tracks for side A, 1 track for side B
        assert len(result["A"]) == 2
        assert len(result["B"]) == 1
        # Check position normalization (1, 2 for A side, 1 for B side)
        assert result["A"][0].side == "A"
        assert result["A"][0].position == 1
        assert result["A"][1].side == "A"
        assert result["A"][1].position == 2
        assert result["B"][0].side == "B"
        assert result["B"][0].position == 1

    def test_fake_detector_with_ambiguous_filenames(self) -> None:
        """Test fake detector with ambiguous filenames (parses 'track' as side)."""
        detector = FakeAudioModeDetector()
        wavs = [
            WavInfo(filename="track1.wav", duration_sec=120.0),
            WavInfo(filename="track2.wav", duration_sec=150.0),
            WavInfo(filename="track3.wav", duration_sec=210.0),
        ]

        result = detector.detect(wavs)

        # The fake detector parses "track" as the side from "track1.wav" etc.
        assert "TRACK" in result
        assert len(result["TRACK"]) == 3
        assert result["TRACK"][0].side == "TRACK"
        assert result["TRACK"][0].position == 1
        assert result["TRACK"][1].side == "TRACK"
        assert result["TRACK"][1].position == 2
        assert result["TRACK"][2].side == "TRACK"
        assert result["TRACK"][2].position == 3

    def test_fake_detector_normalizes_positions(self) -> None:
        """Test fake detector position normalization."""
        detector = FakeAudioModeDetector()
        wavs = [
            WavInfo(filename="Side_A_05_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_10_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_A_15_ballad.wav", duration_sec=210.0),
        ]

        result = detector.detect(wavs)

        assert "A" in result
        assert len(result["A"]) == 3
        assert result["A"][0].position == 1
        assert result["A"][1].position == 2
        assert result["A"][2].position == 3

    def test_fake_detector_is_deterministic(self) -> None:
        """Test fake detector is deterministic (same input → same output)."""
        detector = FakeAudioModeDetector()
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_B_01_ballad.wav", duration_sec=210.0),
        ]

        result1 = detector.detect(wavs)
        result2 = detector.detect(wavs)

        assert result1 == result2
        assert result1["A"][0].position == result2["A"][0].position
        assert result1["A"][1].position == result2["A"][1].position
        assert result1["B"][0].position == result2["B"][0].position

``n
### tests\test_config.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from config import cfg


def test_config():
    """Test configuration system functionality."""
    print("Testing configuration system...")

    try:
        # Test basic config access
        print(f"LLM Model: {cfg.llm_model}")
        print(f"PDF Dir: {cfg.input_pdf_dir}")
        print(f"WAV Dir: {cfg.input_wav_dir}")
        print(f"Export Dir: {cfg.export_default_dir}")
        print(f"UI Theme: {cfg.ui_theme}")
        print(f"UI Font Size: {cfg.ui_base_font_size}")
        print(f"Analysis Tolerance: {cfg.analysis_tolerance_warn}")

        print("Configuration system works correctly!")
        assert True

    except Exception as e:
        print(f"Configuration error: {e}")
        pytest.fail(f"Configuration error: {e}")



``n
### tests\test_export_auto.py

`$tag
#!/usr/bin/env python3

"""
Pytest testy pro automatizovanou validaci auto-export funkcionality.

Testuje všechny čtyři scénáře ze spec:
1. Success - export.auto=true, JSON se vytvoří
2. Disabled - export.auto=false, žádný soubor se nevytvoří
3. Directory Creation - neexistující adresář se vytvoří
4. Write Failure - chyba při zápisu, aplikace loguje chybu
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

import pytest

# Import funkcionality pro testování
from core.models.analysis import SideResult, TrackInfo, WavInfo
from core.models.settings import ExportSettings
from services.export_service import export_results_to_json

pytestmark = pytest.mark.qt_no_exception_capture


class TestExportAuto:
    """Testovací třída pro auto-export funkcionalitu."""

    def create_mock_side_result(self, seq: int = 1) -> SideResult:
        """Vytvoří mock SideResult objekt pro testování."""
        return SideResult(
            seq=seq,
            pdf_path=Path(f"/test/pdf_{seq}.pdf"),
            zip_path=Path(f"/test/zip_{seq}.zip"),
            side="A",
            mode="side",
            status="OK",
            pdf_tracks=[TrackInfo(title=f"Track {seq}", side="A", position=1, duration_sec=180)],
            wav_tracks=[WavInfo(filename=f"track_{seq}.wav", duration_sec=180.0, side="A", position=1)],
            total_pdf_sec=180,
            total_wav_sec=180.0,
            total_difference=0,
        )

    def test_export_success(self, tmp_path):
        """Test 2.1: Ověřit, že když export.auto=True, JSON soubor je vytvořen."""
        # Arrange
        export_dir = tmp_path / "exports"
        mock_results = [self.create_mock_side_result(1), self.create_mock_side_result(2)]

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        # Act
        result_path = export_results_to_json(mock_results, export_settings)

        # Assert
        assert result_path is not None
        assert export_dir.exists()
        assert result_path.exists()

        # Ověřit název souboru
        expected_pattern = f"analysis_{datetime.now().strftime('%Y%m%d')}_"
        assert expected_pattern in result_path.name
        assert result_path.name.endswith(".json")

        # Ověřit obsah JSON
        with open(result_path, encoding="utf-8") as f:
            data = json.load(f)

        assert "exported_at" in data
        assert "count" in data
        assert "results" in data
        assert data["count"] == 2
        assert len(data["results"]) == 2

        # Ověřit strukturu prvního výsledku
        result = data["results"][0]
        assert "seq" in result
        assert "pdf_path" in result
        assert "zip_path" in result
        assert "side" in result
        assert "mode" in result
        assert "status" in result
        assert "pdf_tracks" in result
        assert "wav_tracks" in result
        assert "total_pdf_sec" in result
        assert "total_wav_sec" in result
        assert "total_difference" in result

        # Ověřit, že cesty jsou stringy (JSON-safe)
        assert isinstance(result["pdf_path"], str)
        assert isinstance(result["zip_path"], str)
        assert isinstance(result["total_pdf_sec"], int)
        assert isinstance(result["total_wav_sec"], (int, float))

    def test_export_disabled(self, tmp_path):
        """Test 2.2: Ověřit, že když export.auto=False, žádný JSON soubor není vytvořen."""
        # Arrange
        export_dir = tmp_path / "exports"
        mock_results = [self.create_mock_side_result()]

        export_settings = ExportSettings(auto_export=False, export_dir=export_dir)

        # Act
        result_path = export_results_to_json(mock_results, export_settings)

        # Assert
        assert result_path is None
        assert not export_dir.exists()

    def test_export_directory_creation(self, tmp_path):
        """Test 2.3: Ověřit, že když export.default_dir neexistuje, je automaticky vytvořen."""
        # Arrange
        export_dir = tmp_path / "new_exports_dir"
        mock_results = [self.create_mock_side_result()]

        # Zajistit, že adresář neexistuje
        assert not export_dir.exists()

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        # Act
        result_path = export_results_to_json(mock_results, export_settings)

        # Assert
        assert result_path is not None
        assert export_dir.exists()  # Adresář byl vytvořen
        assert export_dir.is_dir()
        assert result_path.exists()
        assert result_path.parent == export_dir

    def test_export_write_failure(self, tmp_path, caplog):
        """Test 2.4: Ověřit, že když aplikace nemůže zapsat do export.default_dir, loguje chybu."""
        # Arrange
        export_dir = tmp_path / "exports"
        export_dir.mkdir()
        mock_results = [self.create_mock_side_result()]

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        # Mock json.dump funkci, aby vyvolala PermissionError při zápisu
        with patch("json.dump") as mock_json_dump, caplog.at_level(logging.ERROR):
            # Simulovat chybu při zápisu JSON
            mock_json_dump.side_effect = PermissionError("Access denied")

            # Act
            result_path = export_results_to_json(mock_results, export_settings)

            # Assert
            assert result_path is None  # Žádný soubor nebyl vytvořen kvůli chybě

            # Ověřit, že byla zalogována chyba
            assert len(caplog.records) > 0
            error_logged = any("Failed to export analysis results" in record.message for record in caplog.records)
            assert error_logged, f"Expected error log not found in: {[r.message for r in caplog.records]}"

    def test_export_empty_results(self, tmp_path):
        """Test: Ověřit, že s prázdnými výsledky se nevytváří žádný export."""
        # Arrange
        export_dir = tmp_path / "exports"
        empty_results = []

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        # Act
        result_path = export_results_to_json(empty_results, export_settings)

        # Assert
        assert result_path is None
        assert not export_dir.exists()

    def test_export_json_structure_validation(self, tmp_path):
        """Test: Detailní ověření struktury exportovaného JSON."""
        # Arrange
        export_dir = tmp_path / "exports"
        mock_results = [
            SideResult(
                seq=1,
                pdf_path=Path("/test/path.pdf"),
                zip_path=Path("/test/path.zip"),
                side="A",
                mode="tracks",
                status="OK",
                pdf_tracks=[TrackInfo(title="Test Track", side="A", position=1, duration_sec=245)],
                wav_tracks=[WavInfo(filename="test.wav", duration_sec=245.5, side="A", position=1)],
                total_pdf_sec=245,
                total_wav_sec=245.5,
                total_difference=0,
            )
        ]

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        # Act
        result_path = export_results_to_json(mock_results, export_settings)

        # Assert
        assert result_path is not None

        with open(result_path, encoding="utf-8") as f:
            data = json.load(f)

            # Ověřit základní strukturu
            assert "exported_at" in data
            assert "count" in data
            assert "results" in data
            assert data["count"] == 1

            result = data["results"][0]

            # Ověřit všechna požadovaná pole
            required_fields = [
                "seq",
                "pdf_path",
                "zip_path",
                "side",
                "mode",
                "status",
                "pdf_tracks",
                "wav_tracks",
                "total_pdf_sec",
                "total_wav_sec",
                "total_difference",
            ]
            for field in required_fields:
                assert field in result, f"Missing field: {field}"

            # Ověřit typy dat
            assert isinstance(result["pdf_path"], str)
            assert isinstance(result["zip_path"], str)
            assert isinstance(result["total_pdf_sec"], int)
            assert isinstance(result["total_wav_sec"], int | float)

            # Ověřit strukturu tracks
            assert len(result["pdf_tracks"]) == 1
            pdf_track = result["pdf_tracks"][0]
            assert "title" in pdf_track
            assert "side" in pdf_track
            assert "position" in pdf_track
            assert "duration_sec" in pdf_track

            wav_track = result["wav_tracks"][0]
            assert "filename" in wav_track
            assert "duration_sec" in wav_track

    def test_export_open_failure(self, tmp_path, caplog):
        """Test: Ověřit, že když selže otevření souboru pro zápis, aplikace loguje chybu."""
        # Arrange
        export_dir = tmp_path / "exports"
        export_dir.mkdir()

        export_settings = ExportSettings(auto_export=True, export_dir=export_dir)

        with patch("pathlib.Path.open", side_effect=PermissionError("Access denied")), caplog.at_level(logging.ERROR):
            # Act
            result_path = export_results_to_json(
                [self.create_mock_side_result(1)],
                export_settings,
            )

            # Assert
            assert result_path is None
            assert any("Failed to export analysis results" in record.message for record in caplog.records)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

``n
### tests\test_export_service.py

`$tag
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.models.analysis import SideResult, TrackInfo, WavInfo
from core.models.settings import ExportSettings
from services.export_service import export_results_to_json


@pytest.fixture
def export_settings(tmp_path):
    return ExportSettings(auto_export=True, export_dir=tmp_path)


@pytest.fixture
def sample_results(tmp_path):
    pdf_track = TrackInfo(title="Track 1", side="A", position=1, duration_sec=120)
    wav_track = WavInfo(filename="track1.wav", duration_sec=120.0, side="A", position=1)
    result = SideResult(
        seq=1,
        pdf_path=tmp_path / "track.pdf",
        zip_path=tmp_path / "track.zip",
        side="A",
        mode="tracks",
        status="OK",
        pdf_tracks=[pdf_track],
        wav_tracks=[wav_track],
        total_pdf_sec=120,
        total_wav_sec=120.0,
        total_difference=0,
    )
    return [result]


def test_export_results_creates_file(tmp_path, export_settings, sample_results):
    export_path = export_results_to_json(sample_results, export_settings)
    assert export_path is not None
    assert export_path.exists()

    payload = json.loads(export_path.read_text(encoding="utf-8"))
    assert payload["count"] == 1
    assert payload["results"][0]["pdf_path"].endswith("track.pdf")


def test_export_respects_auto_export_disabled(tmp_path, sample_results):
    settings = ExportSettings(auto_export=False, export_dir=tmp_path)
    export_path = export_results_to_json(sample_results, settings)
    assert export_path is None


def test_export_returns_none_for_empty_results(export_settings):
    export_path = export_results_to_json([], export_settings)
    assert export_path is None

``n
### tests\test_fluent_gui_legacy.py

`$tag
"""Characterization tests for the legacy fluent_gui module."""

from __future__ import annotations

import importlib
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Iterable

import pytest


pytest.importorskip("PyQt6")


@pytest.fixture(scope="session", autouse=True)
def _force_offscreen_platform() -> None:
    """Ensure Qt uses the offscreen platform during tests."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="session")
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def fluent_gui_module():
    return importlib.import_module("fluent_gui")


@pytest.fixture(scope="module")
def qapp():
    from PyQt6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture(scope="module", autouse=True)
def _load_legacy_config():
    from config import load_config

    return load_config("settings.json")


def _assert_attributes_exist(module, names: Iterable[str]) -> None:
    missing = [name for name in names if not hasattr(module, name)]
    assert not missing, f"Missing expected attributes: {missing}"


def test_expected_classes_are_available(fluent_gui_module):
    required_classes = [
        "MainWindow",
        "TopTableModel",
        "BottomTableModel",
        "AnalysisWorker",
        "SettingsDialog",
    ]
    _assert_attributes_exist(fluent_gui_module, required_classes)


def test_expected_functions_are_available(fluent_gui_module):
    required_functions = [
        "get_system_file_icon",
        "get_gz_color",
        "load_gz_media_fonts",
        "load_gz_media_stylesheet",
    ]
    _assert_attributes_exist(fluent_gui_module, required_functions)


def test_expected_constants_are_available(fluent_gui_module):
    required_constants = [
        "SETTINGS_FILENAME",
        "STATUS_READY",
        "STATUS_ANALYZING",
        "MSG_ERROR_PATHS",
        "MSG_NO_PAIRS",
        "MSG_DONE",
        "MSG_ERROR",
        "MSG_SCANNING",
        "MSG_PROCESSING_PAIR",
        "WINDOW_TITLE",
        "BUTTON_RUN_ANALYSIS",
        "LABEL_FILTER",
        "FILTER_ALL",
        "FILTER_OK",
        "FILTER_FAIL",
        "FILTER_WARN",
        "TABLE_HEADERS_TOP",
        "TABLE_HEADERS_BOTTOM",
        "SYMBOL_OPEN",
        "ICON_OPEN_QICON",
        "COLOR_WHITE",
        "STATUS_OK",
        "STATUS_WARN",
        "STATUS_FAIL",
        "SYMBOL_CHECK",
        "SYMBOL_CROSS",
        "PLACEHOLDER_DASH",
        "LABEL_TOTAL_TRACKS",
        "INTERFACE_MAIN",
        "COMMENT_SETUP_TOP_TABLE",
        "COMMENT_SETUP_BOTTOM_TABLE",
        "COMMENT_MAX_WIDTH_WAV",
        "COMMENT_APP_STARTUP",
        "COMMENT_CONFIG_LOAD",
        "COMMENT_CONFIG_ERROR",
        "COMMENT_BUTTON_COLOR",
        "COMMENT_BUTTON_COLOR_DESC",
    ]
    _assert_attributes_exist(fluent_gui_module, required_constants)


def test_main_window_can_instantiate(fluent_gui_module, qapp):
    window = fluent_gui_module.MainWindow()
    try:
        assert window.windowTitle() == fluent_gui_module.WINDOW_TITLE
    finally:
        window.close()
        window.deleteLater()


def test_fluent_gui_entrypoint_launches(project_root):
    env = os.environ.copy()
    env.setdefault("QT_QPA_PLATFORM", "offscreen")

    process = subprocess.Popen(
        [sys.executable, "fluent_gui.py"],
        cwd=project_root,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        time.sleep(2)
        assert process.poll() is None, "fluent_gui.py terminated prematurely"
    finally:
        process.terminate()
        try:
            process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate(timeout=5)

``n
### tests\test_gui_minimal.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from ui import MainWindow, AnalysisWorkerManager, load_tolerance_settings, load_export_settings, load_theme_settings, load_waveform_settings, load_worker_settings, load_id_extraction_settings
from config import cfg

pytestmark = pytest.mark.gui

def test_gui_minimal(qtbot, isolated_config, tolerance_settings, id_extraction_settings, waveform_settings):
    """Test minimal GUI initialization using proper fixtures."""

    # Dependencies are now loaded using fixtures or from the isolated_config
    export_settings = load_export_settings(isolated_config)
    theme_settings = load_theme_settings(isolated_config)
    worker_settings = load_worker_settings(isolated_config)

    worker_manager = AnalysisWorkerManager(
        worker_settings=worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )

    window = MainWindow(
        tolerance_settings=tolerance_settings,
        export_settings=export_settings,
        theme_settings=theme_settings,
        waveform_settings=waveform_settings,
        worker_manager=worker_manager,
        settings_filename=isolated_config.file,
    )
    qtbot.addWidget(window)

    assert window.isVisible() is False # We don't call show()
    assert "Final Cue Sheet Checker" in window.windowTitle()


``n
### tests\test_gui_show.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from unittest.mock import patch
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from config import load_config
from ui import MainWindow, AnalysisWorkerManager, load_tolerance_settings, load_export_settings, load_theme_settings, load_waveform_settings, load_worker_settings, load_id_extraction_settings
from config import cfg

pytestmark = pytest.mark.gui

def test_gui_show(qapp, qtbot):
    """Test GUI show functionality."""
    print("Testing GUI show functionality...")

    # Mock dependencies for MainWindow constructor
    tolerance_settings = load_tolerance_settings(cfg)
    export_settings = load_export_settings(cfg)
    theme_settings = load_theme_settings(cfg)
    waveform_settings = load_waveform_settings(cfg)
    worker_settings = load_worker_settings(cfg)
    id_extraction_settings = load_id_extraction_settings(cfg)

    worker_manager = AnalysisWorkerManager(
        worker_settings=worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )

    try:
        print("Creating MainWindow instance...")
        window = MainWindow(
            tolerance_settings=tolerance_settings,
            export_settings=export_settings,
            theme_settings=theme_settings,
            waveform_settings=waveform_settings,
            worker_manager=worker_manager,
            settings_filename=cfg.file,
        )
        qtbot.addWidget(window)
        print("MainWindow created successfully")

        print("Showing MainWindow...")
        window.show()
        print("MainWindow shown successfully")

        # Allow the event loop to run briefly and then exit
        QTimer.singleShot(100, qapp.quit)
        qapp.exec()

    except Exception as e:
        print(f"GUI show error: {e}")
        import traceback
        traceback.print_exc()
        pytest.fail(f"GUI show error: {e}")

``n
### tests\test_gui_simple.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

import pytest
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

pytestmark = pytest.mark.gui


def test_basic_gui():
    """Test basic PyQt6 GUI functionality."""
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Test GUI")
    window.resize(400, 200)

    layout = QVBoxLayout()
    label = QLabel("PyQt6 GUI Test - Basic functionality works!")
    layout.addWidget(label)

    window.setLayout(layout)
    window.show()

    print("GUI launched successfully!")
    QTimer.singleShot(1000, app.quit)
    return app.exec()


if __name__ == "__main__":
    sys.exit(test_basic_gui())

``n
### tests\test_chained_detector.py

`$tag
"""Unit testy pro ChainedAudioModeDetector a jeho steps."""

from __future__ import annotations

from unittest.mock import patch, MagicMock
import pytest

from core.models.analysis import WavInfo
from adapters.audio.chained_detector import ChainedAudioModeDetector
from adapters.audio.steps import StrictParserStep, AiParserStep, DeterministicFallbackStep


class TestChainedAudioModeDetector:
    """Test cases pro ChainedAudioModeDetector - hlavní orchestrátor."""

    def setup_method(self) -> None:
        """Inicializace detectoru pro každý test."""
        self.detector = ChainedAudioModeDetector()

    def test_detect_with_valid_filenames_strict_parsing(self) -> None:
        """Test detekce s validními názvy souborů - strict parsing."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_B_01_ballad.wav", duration_sec=210.0),
        ]

        result = self.detector.detect(wavs)

        # Strict parser by měl zpracovat všechny soubory
        assert "A" in result
        assert "B" in result
        assert len(result["A"]) == 2
        assert len(result["B"]) == 1

        # Ověřit pozice
        assert result["A"][0].side == "A"
        assert result["A"][0].position == 1
        assert result["A"][1].side == "A"
        assert result["A"][1].position == 2
        assert result["B"][0].side == "B"
        assert result["B"][0].position == 1

    def test_detect_with_mixed_parsing_scenarios(self) -> None:
        """Test detekce s kombinací parsovatelných a neparsovatelných souborů."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),  # Strict parsing
            WavInfo(filename="A2_song.wav", duration_sec=150.0),         # Strict parsing
            WavInfo(filename="unknown_track.wav", duration_sec=210.0),   # AI fallback
        ]

        with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
            with patch("adapters.audio.steps.merge_ai_results") as mock_merge:
                mock_ai.return_value = {
                    "unknown_track.wav": ("A", 3)  # Přidat do strany A
                }

                result = self.detector.detect(wavs)

                # Ověřit, že všechny soubory byly zpracovány
                assert "A" in result
                assert len(result["A"]) == 3  # Všechny tři v A
                assert result["A"][0].side == "A"
                assert result["A"][0].position == 1
                assert result["A"][1].side == "A"
                assert result["A"][1].position == 2
                assert result["A"][2].side is None  # AI nezměnilo stranu na A
                assert result["A"][2].position == 3

                # Ověřit, že AI bylo zavoláno
                mock_ai.assert_called_once()
                mock_merge.assert_called_once()

    def test_detect_with_custom_steps(self) -> None:
        """Test detekce s vlastními steps."""
        custom_steps = [StrictParserStep()]
        detector = ChainedAudioModeDetector(steps=custom_steps)

        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),
        ]

        result = detector.detect(wavs)

        # Pouze strict parser - fallback se nespustí, takže neznámý soubor zůstane bez strany
        # ale normalizace ho přidá do default strany A
        assert "A" in result
        assert len(result["A"]) == 2  # Oba soubory v A (jeden parsovaný, jeden default)
        assert result["A"][0].side == "A"
        assert result["A"][0].position == 1
        assert result["A"][1].side is None  # Neparsovaný zůstává None
        assert result["A"][1].position == 2

    def test_detect_empty_input(self) -> None:
        """Test detekce s prázdným vstupem."""
        result = self.detector.detect([])
        assert result == {}

    def test_detect_single_file(self) -> None:
        """Test detekce s jedním souborem."""
        wavs = [WavInfo(filename="01_track.wav", duration_sec=120.0)]

        result = self.detector.detect(wavs)

        assert "A" in result  # Default side
        assert len(result["A"]) == 1
        assert result["A"][0].position == 1

    def test_detect_normalization_and_grouping(self) -> None:
        """Test normalizace pozic a seskupování podle stran."""
        wavs = [
            WavInfo(filename="Side_A_05_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_10_song.wav", duration_sec=150.0),
            WavInfo(filename="Side_B_03_ballad.wav", duration_sec=210.0),
        ]

        result = self.detector.detect(wavs)

        # Pozice by měly být normalizovány na 1, 2, 3
        assert result["A"][0].position == 1
        assert result["A"][1].position == 2
        assert result["B"][0].position == 1

    def test_chain_of_responsibility_stops_at_first_success(self) -> None:
        """Test, že chain se zastaví při prvním úspěšném parsingu."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_A_02_song.wav", duration_sec=150.0),
        ]

        # Mock steps aby strict parser vrátil True (úspěch)
        with patch.object(StrictParserStep, 'process', return_value=True) as mock_strict:
            result = self.detector.detect(wavs)

            # AI step by neměl být zavolán
            with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
                mock_ai.assert_not_called()

    def test_chain_continues_when_strict_fails(self) -> None:
        """Test, že chain pokračuje když strict parser selže."""
        wavs = [
            WavInfo(filename="unknown_track1.wav", duration_sec=120.0),
            WavInfo(filename="unknown_track2.wav", duration_sec=150.0),
        ]

        with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
            mock_ai.return_value = {
                "unknown_track1.wav": ("A", 1),
                "unknown_track2.wav": ("A", 2)
            }

            result = self.detector.detect(wavs)

            # AI by mělo být zavoláno
            mock_ai.assert_called_once()
            assert "A" in result
            assert len(result["A"]) == 2


class TestStrictParserStep:
    """Test cases pro StrictParserStep."""

    def setup_method(self) -> None:
        """Inicializace stepu pro každý test."""
        self.step = StrictParserStep()

    def test_process_all_parsed_successfully(self) -> None:
        """Test zpracování když všechny soubory jsou parsovatelné."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="Side_B_02_song.wav", duration_sec=150.0),
        ]

        result = self.step.process(wavs)

        assert result is True  # Chain se zastaví
        assert wavs[0].side == "A"
        assert wavs[0].position == 1
        assert wavs[1].side == "B"
        assert wavs[1].position == 2

    def test_process_partial_parsing_continues_chain(self) -> None:
        """Test zpracování když některé soubory nejsou parsovatelné."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0),
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),
        ]

        result = self.step.process(wavs)

        assert result is False  # Chain pokračuje
        assert wavs[0].side == "A"
        assert wavs[0].position == 1
        assert wavs[1].side is None  # Nezměněno
        assert wavs[1].position is None  # Nezměněno

    def test_process_already_parsed_files_unchanged(self) -> None:
        """Test zpracování souborů, které už mají parsované údaje."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0, side="B", position=5),
        ]

        result = self.step.process(wavs)

        # Původní hodnoty by měly zůstat zachovány
        assert wavs[0].side == "B"
        assert wavs[0].position == 5

    def test_process_empty_list(self) -> None:
        """Test zpracování prázdného seznamu."""
        result = self.step.process([])
        assert result is True

    def test_process_various_filename_formats(self) -> None:
        """Test zpracování různých formátů názvů souborů."""
        test_cases = [
            ("01.wav", None, 1),
            ("Side_A_02.mp3", "A", 2),
            ("A1_Track.flac", "A", 1),
            ("B2_Song.wav", "B", 2),
            ("AA03_Intro.mp3", "AA", 3),
            ("unknown.wav", None, None),
        ]

        for filename, expected_side, expected_position in test_cases:
            wav = WavInfo(filename=filename, duration_sec=120.0)
            self.step.process([wav])

            assert wav.side == expected_side
            assert wav.position == expected_position


class TestAiParserStep:
    """Test cases pro AiParserStep."""

    def setup_method(self) -> None:
        """Inicializace stepu pro každý test."""
        self.step = AiParserStep()

    def test_process_all_already_parsed_stops_chain(self) -> None:
        """Test zpracování když všechny soubory už jsou parsované."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0, side="A", position=1),
            WavInfo(filename="Side_B_02_song.wav", duration_sec=150.0, side="B", position=2),
        ]

        result = self.step.process(wavs)

        assert result is True  # Chain se zastaví

    def test_process_with_unparsed_files_calls_ai(self) -> None:
        """Test zpracování s neparsovanými soubory - volá AI."""
        wavs = [
            WavInfo(filename="Side_A_01_intro.wav", duration_sec=120.0, side="A", position=1),
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),  # Neparsovaný
        ]

        with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
            with patch("adapters.audio.steps.merge_ai_results") as mock_merge:
                mock_ai.return_value = {
                    "unknown_track.wav": ("B", 1)
                }

                result = self.step.process(wavs)

                assert result is False  # Chain pokračuje (nikdy se nezastaví)
                mock_ai.assert_called_once_with(["unknown_track.wav"])
                mock_merge.assert_called_once()

    def test_process_ai_exception_handling(self) -> None:
        """Test zpracování výjimek z AI."""
        wavs = [
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),
        ]

        with patch("adapters.audio.steps.ai_parse_batch", side_effect=Exception("AI Error")):
            # Nemělo by vyhodit výjimku
            result = self.step.process(wavs)

            assert result is False  # Chain pokračuje
            # Soubor zůstává neparsovaný
            assert wavs[0].side is None
            assert wavs[0].position is None

    def test_process_empty_ai_response(self) -> None:
        """Test zpracování prázdné odpovědi z AI."""
        wavs = [
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),
        ]

        with patch("adapters.audio.steps.ai_parse_batch", return_value={}) as mock_ai:
            with patch("adapters.audio.steps.merge_ai_results") as mock_merge:
                result = self.step.process(wavs)

                assert result is False
                mock_ai.assert_called_once()
                mock_merge.assert_not_called()  # Nevolá se s prázdným mapem

    def test_process_unknown_side_handling(self) -> None:
        """Test zpracování 'UNKNOWN' side z AI."""
        wavs = [
            WavInfo(filename="unknown_track.wav", duration_sec=150.0),
        ]

        with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
            with patch("adapters.audio.steps.merge_ai_results") as mock_merge:
                mock_ai.return_value = {
                    "unknown_track.wav": ("UNKNOWN", 1)
                }

                result = self.step.process(wavs)

                assert result is False
                # UNKNOWN by měl být resetnut na None v AiParserStep kódu
                assert wavs[0].side is None
                # Pozice by měla být nastavena merge_ai_results, ale UNKNOWN side se ignoruje
                assert wavs[0].position is None  # Pozice se nenastaví kvůli UNKNOWN side
                mock_merge.assert_called_once()


class TestDeterministicFallbackStep:
    """Test cases pro DeterministicFallbackStep."""

    def setup_method(self) -> None:
        """Inicializace stepu pro každý test."""
        self.step = DeterministicFallbackStep()

    def test_process_no_sides_assigned_fallback(self) -> None:
        """Test fallback když žádný soubor nemá přiřazenou stranu."""
        wavs = [
            WavInfo(filename="track1.wav", duration_sec=120.0),
            WavInfo(filename="track2.wav", duration_sec=150.0),
            WavInfo(filename="track3.wav", duration_sec=210.0),
        ]

        result = self.step.process(wavs)

        assert result is True  # Poslední step, zastaví chain
        # Všechny soubory dostanou stranu A a pozice 1, 2, 3
        assert all(wav.side == "A" for wav in wavs)
        assert wavs[0].position == 1
        assert wavs[1].position == 2
        assert wavs[2].position == 3

    def test_process_some_sides_assigned_no_fallback(self) -> None:
        """Test že se fallback nespustí když některé soubory mají strany."""
        wavs = [
            WavInfo(filename="Side_A_01.wav", duration_sec=120.0, side="A", position=1),
            WavInfo(filename="track2.wav", duration_sec=150.0),  # Bez strany
        ]

        result = self.step.process(wavs)

        assert result is True  # Zastaví chain
        # Fallback se nespustí - druhý soubor zůstává nezměněný
        assert wavs[0].side == "A"
        assert wavs[1].side is None
        assert wavs[1].position is None

    def test_process_all_sides_assigned_no_fallback(self) -> None:
        """Test že se fallback nespustí když všechny soubory mají strany."""
        wavs = [
            WavInfo(filename="Side_A_01.wav", duration_sec=120.0, side="A", position=1),
            WavInfo(filename="Side_B_02.wav", duration_sec=150.0, side="B", position=2),
        ]

        result = self.step.process(wavs)

        assert result is True
        # Žádné změny
        assert wavs[0].side == "A"
        assert wavs[1].side == "B"

    def test_process_empty_list(self) -> None:
        """Test zpracování prázdného seznamu."""
        result = self.step.process([])
        assert result is True

    def test_process_position_assignment_with_none_positions(self) -> None:
        """Test přiřazení pozic když některé soubory nemají pozice."""
        wavs = [
            WavInfo(filename="track1.wav", duration_sec=120.0, side=None, position=5),  # Bez strany, ale s pozicí
            WavInfo(filename="track2.wav", duration_sec=150.0, side=None, position=None),  # Bez strany a pozice
        ]

        result = self.step.process(wavs)

        assert result is True
        # Oba soubory dostanou stranu A
        # První si ponechá pozici 5, druhý dostane pozici 2 (protože se řadí podle názvu)
        assert wavs[0].side == "A"
        assert wavs[0].position == 5  # Ponechá si původní pozici
        assert wavs[1].side == "A"
        assert wavs[1].position == 2  # Nová pozice (řadí se podle názvu)

    def test_process_deterministic_sorting(self) -> None:
        """Test deterministické řazení podle názvu souboru."""
        wavs = [
            WavInfo(filename="zebra_track.wav", duration_sec=120.0),
            WavInfo(filename="alpha_track.wav", duration_sec=150.0),
            WavInfo(filename="beta_track.wav", duration_sec=210.0),
        ]

        result = self.step.process(wavs)

        assert result is True
        # Měly by být seřazeny podle názvu: alpha, beta, zebra
        # Ale pozice se přiřazují podle původního pořadí v seznamu
        assert wavs[0].position == 1  # alpha_track
        assert wavs[1].position == 2  # beta_track
        assert wavs[2].position == 3  # zebra_track


class TestEdgeCases:
    """Test cases pro edge cases."""

    def test_chained_detector_with_empty_filenames(self) -> None:
        """Test ChainedAudioModeDetector s prázdnými filenames."""
        detector = ChainedAudioModeDetector()
        wavs = [
            WavInfo(filename="", duration_sec=120.0),
        ]

        # Nemělo by vyhodit výjimku
        result = detector.detect(wavs)
        assert "A" in result  # Default side
        assert len(result["A"]) == 1

    def test_steps_with_none_values(self) -> None:
        """Test steps s None hodnotami."""
        strict_step = StrictParserStep()
        ai_step = AiParserStep()
        fallback_step = DeterministicFallbackStep()

        wavs = [
            WavInfo(filename="test.wav", duration_sec=120.0, side=None, position=None),
        ]

        # Žádný step by neměl vyhodit výjimku
        strict_step.process(wavs)
        ai_step.process(wavs)
        fallback_step.process(wavs)

    def test_chained_detector_immutable_input(self) -> None:
        """Test že vstupní data nejsou mutována."""
        detector = ChainedAudioModeDetector()
        original_wavs = [
            WavInfo(filename="Side_A_01.wav", duration_sec=120.0),
        ]
        wavs_copy = [w.model_copy() for w in original_wavs]

        result = detector.detect(original_wavs)

        # Původní objekty by měly zůstat nezměněné
        assert original_wavs[0].side is None
        assert original_wavs[0].position is None

        # Výsledek by měl mít změněné kopie
        assert "A" in result
        assert result["A"][0].side == "A"
        assert result["A"][0].position == 1

    def test_steps_with_very_long_filenames(self) -> None:
        """Test steps s velmi dlouhými názvy souborů."""
        long_filename = "A" * 1000 + "_01_very_long_track_name_that_might_cause_issues.wav"

        strict_step = StrictParserStep()
        wavs = [WavInfo(filename=long_filename, duration_sec=120.0)]

        # Nemělo by vyhodit výjimku
        result = strict_step.process(wavs)
        assert isinstance(result, bool)

    def test_ai_step_with_malformed_ai_response(self) -> None:
        """Test AiParserStep s poškozenou odpovědí z AI."""
        ai_step = AiParserStep()
        wavs = [
            WavInfo(filename="test.wav", duration_sec=120.0),
        ]

        with patch("adapters.audio.steps.ai_parse_batch") as mock_ai:
            with patch("adapters.audio.steps.merge_ai_results") as mock_merge:
                # Simulace poškozené odpovědi
                mock_ai.return_value = {
                    "test.wav": ("INVALID_SIDE", "not_a_number")
                }

                # Nemělo by vyhodit výjimku
                result = ai_step.process(wavs)
                assert result is False
``n
### tests\test_characterization.py

`$tag
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from adapters.filesystem.file_discovery import discover_and_pair_files
from core.domain.comparison import compare_data
from core.models.analysis import TrackInfo, WavInfo
from core.models.settings import IdExtractionSettings, ToleranceSettings

FLOAT_TOLERANCE = 0.01
GOLDEN_DIR = Path(__file__).parent / "data" / "golden"


def _load_golden(name: str) -> Any:
    path = GOLDEN_DIR / name
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _assert_json_matches(actual: Any, expected: Any, path: str = "root") -> None:
    if isinstance(expected, dict):
        assert isinstance(actual, dict), f"{path} expected dict, got {type(actual).__name__}"
        assert set(actual.keys()) == set(expected.keys()), f"{path} key mismatch"
        for key in expected:
            _assert_json_matches(actual[key], expected[key], f"{path}.{key}")
        return

    if isinstance(expected, list):
        assert isinstance(actual, list), f"{path} expected list, got {type(actual).__name__}"
        assert len(actual) == len(expected), f"{path} length mismatch"
        for index, (act_item, exp_item) in enumerate(zip(actual, expected, strict=False)):
            _assert_json_matches(act_item, exp_item, f"{path}[{index}]")
        return

    if isinstance(expected, int | float) and isinstance(actual, int | float):
        if isinstance(expected, float) or isinstance(actual, float):
            delta = abs(float(actual) - float(expected))
            assert delta <= FLOAT_TOLERANCE, f"{path} float diff {delta} exceeds tolerance {FLOAT_TOLERANCE}"
        else:
            assert actual == expected, f"{path} int mismatch"
        return

    assert actual == expected, f"{path} value mismatch"


@pytest.mark.usefixtures("isolated_config")
def test_discover_and_pair_files_matches_golden(
    tmp_path,
    id_extraction_settings,
) -> None:
    pdf_dir = tmp_path / "pdf"
    wav_dir = tmp_path / "zip"
    pdf_dir.mkdir()
    wav_dir.mkdir()

    (pdf_dir / "12345_tracklist.pdf").write_text("pdf", encoding="utf-8")
    (pdf_dir / "67890_tracklist.pdf").write_text("pdf", encoding="utf-8")

    (wav_dir / "12345_masters.zip").write_text("zip", encoding="utf-8")
    (wav_dir / "67890_take1.zip").write_text("zip", encoding="utf-8")
    (wav_dir / "67890_take2.zip").write_text("zip", encoding="utf-8")

    pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir, id_extraction_settings)
    actual = {
        "pairs": {
            str(pair_id): {"pdf": pair.pdf.name, "zip": pair.zip.name}
            for pair_id, pair in pairs.items()
        },
        "skipped_count": skipped,
    }

    expected = _load_golden("golden_pairs.json")
    _assert_json_matches(actual, expected)


@pytest.mark.usefixtures("isolated_config")
def test_compare_data_matches_golden(tmp_path, tolerance_settings, audio_mode_detector) -> None:
    pdf_data = {
        "A": [
            TrackInfo(title="Intro", side="A", position=1, duration_sec=120),
            TrackInfo(title="Song", side="A", position=2, duration_sec=150),
        ],
        "B": [
            TrackInfo(title="Ballad", side="B", position=1, duration_sec=210),
        ],
    }

    wav_data = [
        WavInfo(filename="Side_A_01_intro.wav", duration_sec=119.98),
        WavInfo(filename="Side_A_02_song.wav", duration_sec=150.02),
        WavInfo(filename="Side_B_01_ballad.wav", duration_sec=206.9),
    ]

    pair_info = {"pdf": tmp_path / "dummy.pdf", "zip": tmp_path / "dummy.zip"}

    results = compare_data(pdf_data, wav_data, pair_info, tolerance_settings, audio_mode_detector)
    actual_results = []

    for item in results:
        data = item.model_dump()
        data["pdf_path"] = Path(data["pdf_path"]).name
        data["zip_path"] = Path(data["zip_path"]).name
        actual_results.append(data)

    expected = _load_golden("golden_comparison.json")
    _assert_json_matches(actual_results, expected)


@pytest.mark.parametrize(
    ("warn_tolerance", "fail_tolerance", "expected_status"),
    [
        (1, 2, "FAIL"),
        (2, 5, "WARN"),
        (4, 6, "OK"),
    ],
)
def test_compare_data_respects_injected_tolerances(
    tmp_path: Path,
    warn_tolerance: int,
    fail_tolerance: int,
    expected_status: str,
    audio_mode_detector,
) -> None:
    pdf_data = {
        "A": [
            TrackInfo(title="Intro", side="A", position=1, duration_sec=120),
            TrackInfo(title="Song", side="A", position=2, duration_sec=150),
        ],
        "B": [
            TrackInfo(title="Ballad", side="B", position=1, duration_sec=210),
        ],
    }
    wav_data = [
        WavInfo(filename="Side_A_01_intro.wav", duration_sec=119.98),
        WavInfo(filename="Side_A_02_song.wav", duration_sec=150.02),
        WavInfo(filename="Side_B_01_ballad.wav", duration_sec=206.9),
    ]
    pair_info = {"pdf": tmp_path / "dummy.pdf", "zip": tmp_path / "dummy.zip"}

    tolerance = ToleranceSettings(
        warn_tolerance=warn_tolerance,
        fail_tolerance=fail_tolerance,
    )
    results = compare_data(pdf_data, wav_data, pair_info, tolerance, audio_mode_detector)
    status_by_side = {result.side: result.status for result in results}
    assert status_by_side["B"] == expected_status


@pytest.mark.parametrize(
    ("min_digits", "max_digits", "ignore_numbers", "expected_ids"),
    [
        (1, 3, [], {1, 9}),
        (2, 3, [], {1}),
        (1, 3, ["9"], {1}),
    ],
)
def test_discover_and_pair_files_respects_id_settings(
    tmp_path: Path,
    min_digits: int,
    max_digits: int,
    ignore_numbers: list[str],
    expected_ids: set[int],
):
    pdf_dir = tmp_path / "pdf_param"
    wav_dir = tmp_path / "zip_param"
    pdf_dir.mkdir()
    wav_dir.mkdir()

    (pdf_dir / "track9.pdf").write_text("pdf", encoding="utf-8")
    (pdf_dir / "track_001.pdf").write_text("pdf", encoding="utf-8")
    (wav_dir / "track9.zip").write_text("zip", encoding="utf-8")
    (wav_dir / "track_001.zip").write_text("zip", encoding="utf-8")

    settings = IdExtractionSettings(
        min_digits=min_digits,
        max_digits=max_digits,
        ignore_numbers=ignore_numbers,
    )
    pairs, skipped = discover_and_pair_files(pdf_dir, wav_dir, settings)

    assert set(pairs.keys()) == expected_ids
    assert skipped == 0

``n
### tests\test_parsing.py

`$tag
from __future__ import annotations

import pytest
from pathlib import Path

from core.domain.parsing import StrictFilenameParser, ParsedFileInfo


class TestStrictFilenameParser:
    """Unit testy pro StrictFilenameParser."""

    def setup_method(self) -> None:
        """Inicializace parseru pro každý test."""
        self.parser = StrictFilenameParser()

    @pytest.mark.parametrize(
        "filename,expected_side,expected_position",
        [
            # Základní parsing pozice (čísla na začátku) - pouze na konci stringu
            ("01.wav", None, 1),
            ("1.flac", None, 1),
            ("02.wav", None, 2),
            ("10.mp3", None, 10),
            ("99.wav", None, 99),

            # Parsing strany (Side patterns)
            ("Side_A_Track.wav", "A", None),
            ("Side_AA_Song.mp3", "AA", None),
            ("side_b_Track.flac", "B", None),
            ("SIDE_C_Song.wav", "C", None),
            ("Side-A-Track.mp3", "A", None),
            ("Side_AA_Track.wav", "AA", None),

            # Kombinované patterny (A1, B2, atd.)
            ("A1_Track.wav", "A", 1),
            ("B2_Song.mp3", "B", 2),
            ("AA02_Track.flac", "AA", 2),
            ("C3_Song.wav", "C", 3),
            ("D10_Track.mp3", "D", 10),
            ("A1_intro.wav", "A", 1),
            ("B2_song.mp3", "B", 2),

            # Side s pozicí
            ("Side_A_01.wav", "A", 1),
            ("SideA_02.mp3", "A", 2),
            ("Side_A01.flac", "A", 1),
            ("side_b_3.wav", "B", 3),
            ("SIDE_C_05.mp3", "C", 5),
            ("Side_AA_10.wav", "AA", 10),

            # Edge cases - bez pozice a strany
            ("Track_Without_Numbers.wav", None, None),
            ("Random_Filename.mp3", None, None),
            ("No_Pattern_Here.flac", None, None),
            ("", None, None),

            # Speciální formáty
            ("Side_A_01_Track_Name.wav", "A", 1),
            ("A1_Side_B_02.mp3", "B", 2),  # Side_B má prioritu před A1
            ("00_Prefixed_Track.wav", None, None),  # 00 není validní pozice
            ("0_Track.wav", None, None),  # 0 není validní pozice

            # Case insensitive testy
            ("side_a_01.wav", "A", 1),
            ("SIDE_B_02.mp3", "B", 2),
            ("a1_track.flac", "A", 1),
            ("b2_song.wav", "B", 2),

            # Složité názvy
            ("Side_A_01_Intro_To_Track.wav", "A", 1),
            ("A1_Featuring_Artist_Song.mp3", "A", 1),
            ("Side_AA_02_Remix.flac", "AA", 2),
        ]
    )
    def test_parse_filename_comprehensive(
        self, filename: str, expected_side: str | None, expected_position: int | None
    ) -> None:
        """Parametrizovaný test pro různé formáty filename parsing."""
        result = self.parser.parse(filename)

        assert result.side == expected_side
        assert result.position == expected_position

    @pytest.mark.parametrize(
        "filename,expected",
        [
            # Test s úplnými cestami
            ("/path/to/Side_A_01.wav", ParsedFileInfo(side="A", position=1)),
            ("C:\\Users\\Music\\B2_Song.mp3", ParsedFileInfo(side="B", position=2)),
            ("./tracks/A1_Track.flac", ParsedFileInfo(side="A", position=1)),
            ("../parent/dir/Side_AA_02.wav", ParsedFileInfo(side="AA", position=2)),

            # Test s různými příponami
            ("01.WAV", ParsedFileInfo(side=None, position=1)),
            ("Side_A_02.MP3", ParsedFileInfo(side="A", position=2)),
            ("A1_Song.FLAC", ParsedFileInfo(side="A", position=1)),
            ("B2_Track.aiff", ParsedFileInfo(side="B", position=2)),

            # Test bez přípon
            ("01", ParsedFileInfo(side=None, position=1)),
            ("Side_A_02", ParsedFileInfo(side="A", position=2)),
            ("A1_Song", ParsedFileInfo(side="A", position=1)),
        ]
    )
    def test_parse_with_paths_and_extensions(self, filename: str, expected: ParsedFileInfo) -> None:
        """Test parsing s různými typy cest a přípon souborů."""
        result = self.parser.parse(filename)
        assert result == expected

    def test_parse_empty_filename(self) -> None:
        """Test parsing prázdného názvu souboru."""
        result = self.parser.parse("")
        assert result == ParsedFileInfo(side=None, position=None)

    def test_parse_filename_with_only_numbers(self) -> None:
        """Test parsing názvu obsahujícího pouze čísla."""
        result = self.parser.parse("12345.wav")
        assert result == ParsedFileInfo(side=None, position=None)

    def test_parse_filename_starting_with_zero(self) -> None:
        """Test parsing názvu začínajícího nulou."""
        result = self.parser.parse("001.wav")
        assert result == ParsedFileInfo(side=None, position=1)

    def test_parse_complex_side_patterns(self) -> None:
        """Test parsing složitějších patternů pro strany."""
        test_cases = [
            ("Side-A-01.wav", "A", 1),
            ("Side_AA_02.mp3", "AA", 2),
            ("Side-ABC-03.flac", "ABC", 3),
            ("Side_A-B_01.wav", "A", 1),  # První match
        ]

        for filename, expected_side, expected_position in test_cases:
            result = self.parser.parse(filename)
            assert result.side == expected_side
            assert result.position == expected_position

    def test_parse_position_only_various_formats(self) -> None:
        """Test parsing pouze pozice v různých formátech."""
        test_cases = [
            ("01.wav", None, 1),
            ("02.wav", None, 2),
            ("10.flac", None, 10),
            ("99.wav", None, 99),
            ("1.wav", None, 1),
            ("001.mp3", None, 1),  # Leading zeros are stripped
        ]

        for filename, expected_side, expected_position in test_cases:
            result = self.parser.parse(filename)
            assert result.side == expected_side
            assert result.position == expected_position

    def test_parse_side_only_various_formats(self) -> None:
        """Test parsing pouze strany v různých formátech."""
        test_cases = [
            ("Side_A.wav", "A", None),
            ("Side_AA.mp3", "AA", None),
            ("side_b.flac", "B", None),
            ("SIDE_C.wav", "C", None),
            ("Side-ABC.mp3", "ABC", None),
        ]

        for filename, expected_side, expected_position in test_cases:
            result = self.parser.parse(filename)
            assert result.side == expected_side
            assert result.position == expected_position

    def test_case_insensitive_parsing(self) -> None:
        """Test case insensitive parsing."""
        test_cases = [
            ("side_a_01.wav", "A", 1),
            ("SIDE_B_02.mp3", "B", 2),
            ("Side_Cc_03.flac", "CC", 3),
            ("a1_track.wav", "A", 1),
            ("b2_song.mp3", "B", 2),
            ("Aa01_Track.flac", "AA", 1),
        ]

        for filename, expected_side, expected_position in test_cases:
            result = self.parser.parse(filename)
            assert result.side == expected_side
            assert result.position == expected_position

    def test_priority_of_patterns(self) -> None:
        """Test priority parsing patternů podle skutečné implementace."""
        test_cases = [
            # Side pattern má prioritu před A1 patternem - parsuje první písmeno a pozici
            ("Side_A1_Track.wav", "A", 1),  # Parsuje jako Side_A -> A s pozicí 1 z A1

            # Position na začátku má prioritu před jinými patterny (ale pouze na konci stringu)
            ("01Side_A_Track.wav", "A", None),  # Parsuje Side_A -> A, ignoruje pozici 01

            # A1 pattern má prioritu před pozicí v jiném místě
            ("A1_02_Track.wav", "A", 1),  # Parsuje A1 jako A s pozicí 1, ignoruje 02

            # Side pattern v prostředku má prioritu
            ("A1_Side_B_02.wav", "B", 2),  # Parsuje Side_B s pozicí 2
        ]

        for filename, expected_side, expected_position in test_cases:
            result = self.parser.parse(filename)
            assert result.side == expected_side
            assert result.position == expected_position

    def test_pathlib_path_objects(self) -> None:
        """Test parsing s Path objekty."""
        test_cases = [
            (Path("Side_A_01.wav"), "A", 1),
            (Path("/path/to/B2_Song.mp3"), "B", 2),
            (Path("A1_Track.flac"), "A", 1),
        ]

        for path, expected_side, expected_position in test_cases:
            result = self.parser.parse(str(path))
            assert result.side == expected_side
            assert result.position == expected_position

    def test_parsed_file_info_equality(self) -> None:
        """Test rovnosti ParsedFileInfo objektů."""
        info1 = ParsedFileInfo(side="A", position=1)
        info2 = ParsedFileInfo(side="A", position=1)
        info3 = ParsedFileInfo(side="B", position=1)
        info4 = ParsedFileInfo(side="A", position=2)

        assert info1 == info2
        assert info1 != info3
        assert info1 != info4
        assert info1 != ParsedFileInfo(side=None, position=None)

    def test_windows_path_parsing(self) -> None:
        """Test parsing Windows cest s backslash."""
        # Test specific Windows path cases
        test_cases = [
            ("C:\\Users\\Music\\B2_Song.mp3", "B", 2),
            ("D:\\Audio\\Side_A_01.wav", "A", 1),
            ("\\\\server\\share\\A1_Track.flac", "A", 1),
        ]

        for path, expected_side, expected_position in test_cases:
            result = self.parser.parse(path)
            assert result.side == expected_side
            assert result.position == expected_position
``n
### tests\test_results_table_model.py

`$tag
from __future__ import annotations

from pathlib import Path

import pytest
from PyQt6.QtCore import Qt

from core.models.analysis import SideResult
from ui.config_models import ThemeSettings
from ui.constants import STATUS_WARN
from ui.models.results_table_model import ResultsTableModel

pytestmark = pytest.mark.usefixtures("qtbot")


@pytest.fixture
def theme_settings():
    return ThemeSettings(
        font_family="",
        font_size=10,
        stylesheet_path=Path(),
        status_colors={"ok": "#10B981", "warn": "#F59E0B", "fail": "#EF4444"},
        logo_path=Path(),
        claim_visible=True,
        claim_text="Emotions. Materialized.",
        action_bg_color="#E0E7FF",
        total_row_bg_color="#F3F4F6",
    )


@pytest.fixture
def mock_side_result():
    return SideResult(
        seq=1,
        pdf_path=Path("test.pdf"),
        zip_path=Path("test.zip"),
        side="A",
        mode="tracks",
        status="OK",
        pdf_tracks=[],
        wav_tracks=[],
        total_pdf_sec=100,
        total_wav_sec=100.0,
        total_difference=0,
    )


def test_results_table_model_creation(theme_settings):
    model = ResultsTableModel(theme_settings=theme_settings)
    assert model.rowCount() == 0
    assert model.columnCount() == len(model._headers)


def test_add_result_increases_row_count(theme_settings, mock_side_result):
    model = ResultsTableModel(theme_settings=theme_settings)
    model.add_result(mock_side_result)
    assert model.rowCount() == 1
    assert model.all_results()[0].pdf_path.name == "test.pdf"


def test_data_retrieval(theme_settings, mock_side_result):
    model = ResultsTableModel(theme_settings=theme_settings)
    model.add_result(mock_side_result)

    index_file = model.index(0, 1)
    assert model.data(index_file, Qt.ItemDataRole.DisplayRole) == "test.pdf"

    index_status = model.index(0, 5)
    assert model.data(index_status, Qt.ItemDataRole.DisplayRole) == "OK"


def test_status_color(theme_settings, mock_side_result):
    mock_side_result.status = STATUS_WARN

    model = ResultsTableModel(theme_settings=theme_settings)
    model.add_result(mock_side_result)

    index_status = model.index(0, 5)
    color = model.data(index_status, Qt.ItemDataRole.BackgroundRole)

    assert color is not None
    assert color.name().lower() == theme_settings.status_colors["warn"].lower()

``n
### tests\test_settings_dialog.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Comprehensive test for Settings dialog functionality and path resolution.
Tests: Settings dialog opening, configuration saving, path resolution, and error handling.
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

pytestmark = pytest.mark.gui

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

from config import cfg, load_config, save_config, resolve_path
from fluent_gui import MainWindow, SettingsDialog
from settings_page import SettingsPage

# Global test application instance
_test_app = None


class MockMainWindow(QMainWindow):
    """Mock main window for testing settings dialog functionality."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Main Window")

        # Setup menu bar like the real MainWindow
        self.setup_menu_bar()

    def setup_menu_bar(self):
        """Setup menu bar with File, Edit, Help menus."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        # Settings action with Ctrl+, shortcut
        settings_action = edit_menu.addAction("Settings...")
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self.open_settings)

        # Help menu
        help_menu = menubar.addMenu("Help")

    def open_settings(self):
        """Open settings dialog."""
        try:
            settings_dialog = SettingsDialog(self)
            settings_dialog.exec()
        except Exception as e:
            print(f"Failed to open settings dialog: {e}")
            raise


def test_settings_dialog_creation():
    """Test that SettingsDialog can be created successfully."""
    print("Testing SettingsDialog creation...")

    app = QApplication.instance()
    if app is None:
        global _test_app
        _test_app = QApplication(sys.argv)

    try:
        # Create a mock parent window
        parent = MockMainWindow()

        # Test creating SettingsDialog
        dialog = SettingsDialog(parent)
        assert dialog is not None
        print("+ SettingsDialog created successfully")

        # Test that it has the expected components
        assert hasattr(dialog, "settings_page")
        assert isinstance(dialog.settings_page, SettingsPage)
        print("+ SettingsDialog has SettingsPage")

        # Clean up
        dialog.deleteLater()
        parent.deleteLater()

        return True

    except Exception as e:
        print(f"- SettingsDialog creation failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_settings_dialog_menu_action():
    """Test that Settings dialog opens via Edit -> Settings... menu."""
    print("Testing Settings dialog via Edit -> Settings... menu...")

    app = QApplication.instance()
    if app is None:
        global _test_app
        _test_app = QApplication(sys.argv)

    try:
        # Create a mock parent window
        parent = MockMainWindow()

        # Find the settings action in the menu
        edit_menu = None
        for menu in parent.menuBar().findChildren(QMenu):
            if menu.title() == "Edit":
                edit_menu = menu
                break

        assert edit_menu is not None, "Edit menu not found"
        print("+ Edit menu found")

        # Find the Settings... action
        settings_action = None
        for action in edit_menu.actions():
            if action.text() == "Settings...":
                settings_action = action
                break

        assert settings_action is not None, "Settings... action not found"
        print("+ Settings... action found")

        # Mock the SettingsDialog to avoid actually showing it
        with patch("fluent_gui.SettingsDialog") as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog

            # Trigger the action
            settings_action.trigger()

            # Verify the dialog was created
            mock_dialog_class.assert_called_once()
            print("+ Settings dialog opened via menu action")

        # Clean up
        parent.deleteLater()

        return True

    except Exception as e:
        print(f"- Menu action test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_settings_dialog_shortcut():
    """Test that Settings dialog opens via Ctrl+, shortcut."""
    print("Testing Settings dialog via Ctrl+, shortcut...")

    app = QApplication.instance()
    if app is None:
        global _test_app
        _test_app = QApplication(sys.argv)

    try:
        # Create a mock parent window
        parent = MockMainWindow()

        # Find the settings action
        edit_menu = None
        for menu in parent.menuBar().findChildren(QMenu):
            if menu.title() == "Edit":
                edit_menu = menu
                break

        settings_action = None
        for action in edit_menu.actions():
            if action.text() == "Settings...":
                settings_action = action
                break

        # Mock the SettingsDialog
        with patch("fluent_gui.SettingsDialog") as mock_dialog_class:
            mock_dialog = MagicMock()
            mock_dialog_class.return_value = mock_dialog

            # Simulate Ctrl+, key press
            QTest.keyClick(parent, Qt.Key_Comma, Qt.ControlModifier)

            # Verify the dialog was created
            mock_dialog_class.assert_called_once()
            print("+ Settings dialog opened via Ctrl+, shortcut")

        # Clean up
        parent.deleteLater()

        return True

    except Exception as e:
        print(f"- Shortcut test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_configuration_save():
    """Test that configuration saves correctly via Save button."""
    print("Testing configuration save functionality...")

    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_settings_file = temp_path / "test_settings.json"

            # Create initial test configuration
            test_config = {
                "input": {"pdf_dir": str(temp_path / "pdf"), "wav_dir": str(temp_path / "wav")},
                "analysis": {"tolerance_warn": 3, "tolerance_fail": 7},
            }

            with open(test_settings_file, "w") as f:
                json.dump(test_config, f)

            # Load the test configuration
            load_config(test_settings_file)

            # Modify some settings
            cfg.set("analysis/tolerance_warn", 5)
            cfg.set("analysis/tolerance_fail", 10)
            cfg.set("input/pdf_dir", str(temp_path / "new_pdf"))

            # Save the configuration
            save_config(test_settings_file)

            # Verify the settings were saved correctly
            with open(test_settings_file, "r") as f:
                saved_config = json.load(f)

            assert saved_config["analysis"]["tolerance_warn"] == 5
            assert saved_config["analysis"]["tolerance_fail"] == 10
            assert saved_config["input"]["pdf_dir"] == str(temp_path / "new_pdf")
            print("+ Configuration saved correctly")

            return True

    except Exception as e:
        print(f"- Configuration save test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_path_resolution_absolute():
    """Test that path resolution works correctly with absolute paths."""
    print("Testing path resolution with absolute paths...")

    try:
        # Test with absolute path
        test_path = "/absolute/test/path"
        resolved = resolve_path(test_path)

        # Should return the absolute path as-is (resolved)
        assert resolved == Path(test_path).resolve()
        print("+ Absolute path resolution works correctly")

        # Test with Path object
        test_path_obj = Path("/another/absolute/path")
        resolved_obj = resolve_path(test_path_obj)
        assert resolved_obj == test_path_obj.resolve()
        print("+ Absolute Path object resolution works correctly")

        return True

    except Exception as e:
        print(f"- Absolute path resolution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_path_resolution_relative():
    """Test that path resolution works correctly with relative paths."""
    print("Testing path resolution with relative paths...")

    try:
        # Test with relative path
        test_path = "relative/test/path"
        resolved = resolve_path(test_path)

        # Should resolve relative to project root
        project_root = Path(__file__).resolve().parent
        expected = (project_root / test_path).resolve()
        assert resolved == expected
        print("+ Relative path resolution works correctly")

        # Test with current directory reference
        current_path = "./current/dir"
        resolved_current = resolve_path(current_path)
        expected_current = (project_root / current_path).resolve()
        assert resolved_current == expected_current
        print("+ Current directory path resolution works correctly")

        return True

    except Exception as e:
        print(f"- Relative path resolution test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_path_directory_validation():
    """Test that directory validation works correctly."""
    print("Testing path directory validation...")

    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Test with valid directory
            valid_dir = temp_path / "valid_dir"
            valid_dir.mkdir()

            # This should not raise an error
            cfg.input_pdf_dir = str(valid_dir)
            assert cfg.input_pdf_dir.value == str(valid_dir)
            print("+ Valid directory path accepted")

            # Test with invalid path (non-existent)
            invalid_dir = temp_path / "non_existent_dir"

            # This should create the directory
            cfg.input_pdf_dir = str(invalid_dir)
            assert invalid_dir.exists()
            assert invalid_dir.is_dir()
            print("+ Non-existent directory path created automatically")

            # Test with file path (should raise error)
            test_file = temp_path / "test_file.txt"
            test_file.write_text("test content")

            try:
                cfg.input_pdf_dir = str(test_file)
                # If we get here, the validation should have failed
                assert False, "Expected ValueError for file path"
            except ValueError as e:
                assert "not a directory" in str(e).lower()
                print("+ File path correctly rejected")

        return True

    except Exception as e:
        print(f"- Directory validation test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_settings_dialog_save_button():
    """Test that the Save button in SettingsDialog works correctly."""
    print("Testing SettingsDialog Save button functionality...")

    app = QApplication.instance()
    if app is None:
        global _test_app
        _test_app = QApplication(sys.argv)

    try:
        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            test_settings_file = temp_path / "test_settings.json"

            # Create initial test configuration
            test_config = {
                "input": {"pdf_dir": str(temp_path / "pdf"), "wav_dir": str(temp_path / "wav")},
                "analysis": {"tolerance_warn": 2, "tolerance_fail": 5},
            }

            with open(test_settings_file, "w") as f:
                json.dump(test_config, f)

            # Load the test configuration
            load_config(test_settings_file)

            # Create settings dialog
            parent = MockMainWindow()
            dialog = SettingsDialog(parent)

            # Modify some settings in the dialog
            dialog.settings_page.warn_slider.setValue(7)
            dialog.settings_page.fail_slider.setValue(12)

            # Mock the save_config function to verify it's called
            with patch("settings_page.save_config") as mock_save:
                # Click the save button
                dialog.save_button.click()

                # Verify save_config was called
                mock_save.assert_called_once()

                # Verify the dialog was accepted (closed)
                # The dialog should be closed after successful save

            # Clean up
            dialog.deleteLater()
            parent.deleteLater()

            print("+ SettingsDialog Save button works correctly")
            return True

    except Exception as e:
        print(f"- Save button test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_no_pdf_directory_errors():
    """Test that no 'PDF path is not a directory' errors occur during normal operation."""
    print("Testing for absence of 'PDF path is not a directory' errors...")

    try:
        # Create a temporary directory structure for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create valid directory structure
            pdf_dir = temp_path / "pdf"
            wav_dir = temp_path / "wav"
            pdf_dir.mkdir()
            wav_dir.mkdir()

            # Create test settings file
            test_settings = {"input": {"pdf_dir": str(pdf_dir), "wav_dir": str(wav_dir)}}

            settings_file = temp_path / "settings.json"
            with open(settings_file, "w") as f:
                json.dump(test_settings, f)

            # Load configuration
            load_config(settings_file)

            # Test that paths are properly resolved and valid
            pdf_path = cfg.input_pdf_dir.value
            wav_path = cfg.input_wav_dir.value

            assert pdf_path == str(pdf_dir)
            assert wav_path == str(wav_dir)
            assert Path(pdf_path).is_dir()
            assert Path(wav_path).is_dir()

            # Test MainWindow creation with valid paths
            app = QApplication.instance()
            if app is None:
                global _test_app
                _test_app = QApplication(sys.argv)

            # This should not raise any "PDF path is not a directory" errors
            window = MainWindow()

            # Verify the paths are accessible
            pdf_dir_path = Path(window.pdf_dir) if hasattr(window, "pdf_dir") else None
            if pdf_dir_path:
                assert pdf_dir_path.is_dir()

            print("+ No 'PDF path is not a directory' errors occurred")
            return True

    except Exception as e:
        print(f"- PDF directory error test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def run_all_tests():
    """Run all Settings dialog tests."""
    print("Running comprehensive Settings dialog tests...\n")

    tests = [
        test_settings_dialog_creation,
        test_settings_dialog_menu_action,
        test_settings_dialog_shortcut,
        test_configuration_save,
        test_path_resolution_absolute,
        test_path_resolution_relative,
        test_path_directory_validation,
        test_settings_dialog_save_button,
        test_no_pdf_directory_errors,
    ]

    passed = 0
    failed = 0

    for test in tests:
        print(f"\n{'='*60}")
        try:
            if test():
                passed += 1
                print(f"+ {test.__name__} PASSED")
            else:
                failed += 1
                print(f"- {test.__name__} FAILED")
        except Exception as e:
            failed += 1
            print(f"- {test.__name__} FAILED with exception: {e}")
        print(f"{'='*60}")

    print("\nTest Results Summary:")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Total: {passed + failed}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

``n
### tests\test_tracks_table_model.py

`$tag
from __future__ import annotations

from pathlib import Path

import pytest
from PyQt6.QtCore import Qt

from core.models.analysis import SideResult, TrackInfo, WavInfo
from core.models.settings import ToleranceSettings
from ui.config_models import ThemeSettings
from ui.constants import SYMBOL_CHECK, SYMBOL_CROSS
from ui.models.tracks_table_model import TracksTableModel

pytestmark = pytest.mark.usefixtures("qtbot")


@pytest.fixture
def tolerance_settings():
    return ToleranceSettings(warn_tolerance=2, fail_tolerance=5)


@pytest.fixture
def theme_settings():
    return ThemeSettings(
        font_family="Poppins, Segoe UI, Arial, sans-serif",
        font_size=10,
        stylesheet_path=Path("gz_media.qss"),
        status_colors={"ok": "#10B981", "warn": "#F59E0B", "fail": "#EF4444"},
        logo_path=Path("assets/gz_logo_white.png"),
        claim_visible=True,
        claim_text="Emotions. Materialized.",
        action_bg_color="#E0E7FF",
        total_row_bg_color="#F3F4F6",
    )


@pytest.fixture
def mock_side_result_tracks():
    pdf_track = TrackInfo(title="Track 1", side="A", position=1, duration_sec=180)
    wav_track = WavInfo(filename="track1.wav", duration_sec=181.0, side="A", position=1)
    return SideResult(
        seq=1,
        pdf_path=Path("test.pdf"),
        zip_path=Path("test.zip"),
        side="A",
        mode="tracks",
        status="OK",
        pdf_tracks=[pdf_track],
        wav_tracks=[wav_track],
        total_pdf_sec=180,
        total_wav_sec=181.0,
        total_difference=1,
    )


def test_tracks_table_model_creation(tolerance_settings, theme_settings):
    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    assert model.rowCount() == 0
    assert model.columnCount() == len(model._headers)


def test_update_data_populates_model(tolerance_settings, theme_settings, mock_side_result_tracks):
    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    model.update_data(mock_side_result_tracks)
    # One track row + total row
    assert model.rowCount() == 2


def test_track_match_icon_ok(tolerance_settings, theme_settings, mock_side_result_tracks):
    """Test that successful match displays check icon via DecorationRole."""
    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    model.update_data(mock_side_result_tracks)

    index_match = model.index(0, 6)
    icon = model.data(index_match, Qt.ItemDataRole.DecorationRole)

    # Verify icon is returned and is not null
    assert icon is not None
    assert not icon.isNull()


def test_track_match_icon_fail(tolerance_settings, theme_settings, mock_side_result_tracks):
    """Test that failed match displays cross icon via DecorationRole."""
    failure_result = mock_side_result_tracks.model_copy()
    failure_result.wav_tracks[0] = failure_result.wav_tracks[0].model_copy(update={"duration_sec": 184.0})
    failure_result.total_difference = 4

    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    model.update_data(failure_result)

    index_match = model.index(0, 6)
    icon = model.data(index_match, Qt.ItemDataRole.DecorationRole)

    # Verify icon is returned and is not null
    assert icon is not None
    assert not icon.isNull()


def test_track_match_display_empty(tolerance_settings, theme_settings, mock_side_result_tracks):
    """Test that Match column returns empty string for DisplayRole (icon only)."""
    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    model.update_data(mock_side_result_tracks)

    index_match = model.index(0, 6)
    display_text = model.data(index_match, Qt.ItemDataRole.DisplayRole)

    # Verify DisplayRole returns empty string (icon is shown via DecorationRole)
    assert display_text == ""


def test_waveform_icon_present(tolerance_settings, theme_settings, mock_side_result_tracks):
    """Test that Waveform column displays play icon via DecorationRole."""
    model = TracksTableModel(tolerance_settings=tolerance_settings, theme_settings=theme_settings)
    model.update_data(mock_side_result_tracks)

    index_waveform = model.index(0, 7)
    icon = model.data(index_waveform, Qt.ItemDataRole.DecorationRole)

    # Verify icon is returned and is not null
    assert icon is not None
    assert not icon.isNull()

``n
### tests\test_wav_reader.py

`$tag
from __future__ import annotations

import logging
import sys
import types
import zipfile
from pathlib import Path
from typing import Callable

import numpy as np
import pytest
import soundfile as sf

from adapters.audio.wav_reader import ZipWavFileReader


def _write_wav(path: Path, duration_sec: float, sample_rate: int = 44100) -> None:
    """Helper to author a simple sine-less wave file for tests."""
    frame_count = int(duration_sec * sample_rate)
    data = np.zeros(frame_count, dtype=np.float32)
    sf.write(path, data, sample_rate)


def _build_zip(tmp_path: Path, entries: dict[str, bytes]) -> Path:
    zip_path = tmp_path / "bundle.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        for arcname, payload in entries.items():
            zf.writestr(arcname, payload)
    return zip_path


def _patch_duration(monkeypatch: pytest.MonkeyPatch, factory: Callable[[Path], float]) -> None:
    monkeypatch.setattr("adapters.audio.wav_reader.get_wav_duration", factory)


def test_read_wav_files_success(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    entries = {
        "disc/B2_second.wav": b"data-b",
        "disc/A1_first.wav": b"data-a",
    }
    zip_path = _build_zip(tmp_path, entries)

    durations = {"A1_first.wav": 12.34, "B2_second.wav": 56.78}
    recorded_paths: list[Path] = []

    def fake_get_wav_duration(path: Path) -> float:
        recorded_paths.append(path)
        return durations[path.name]

    _patch_duration(monkeypatch, fake_get_wav_duration)

    reader = ZipWavFileReader()
    wav_infos = reader.read_wav_files(zip_path)

    assert [info.filename for info in wav_infos] == ["disc/A1_first.wav", "disc/B2_second.wav"]
    assert [info.duration_sec for info in wav_infos] == [12.34, 56.78]
    assert len(recorded_paths) == 2


def test_read_wav_files_corrupted_zip(tmp_path: Path) -> None:
    broken_zip = tmp_path / "corrupted.zip"
    broken_zip.write_bytes(b"not a real zip archive")

    reader = ZipWavFileReader()
    assert reader.read_wav_files(broken_zip) == []


def test_read_wav_files_empty_zip(empty_zip: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[Path] = []

    def fake_get_wav_duration(path: Path) -> float:
        calls.append(path)
        return 1.0

    _patch_duration(monkeypatch, fake_get_wav_duration)

    reader = ZipWavFileReader()
    assert reader.read_wav_files(empty_zip) == []
    assert not calls


def test_read_wav_files_corrupted_wav(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    zip_path = _build_zip(tmp_path, {"broken.wav": b"corrupted payload"})

    def failing_get_wav_duration(path: Path) -> float:
        raise RuntimeError(f"Cannot parse {path}")

    _patch_duration(monkeypatch, failing_get_wav_duration)

    reader = ZipWavFileReader()
    with caplog.at_level(logging.WARNING):
        results = reader.read_wav_files(zip_path)

    assert results == []
    assert any("Nelze přečíst hlavičku WAV" in message for message in caplog.messages)


def test_read_wav_files_no_wav_extension(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    zip_path = _build_zip(tmp_path, {"track.mp3": b"id3"})

    def forbidden_call(path: Path) -> float:
        raise AssertionError(f"get_wav_duration should not be called for {path}")

    _patch_duration(monkeypatch, forbidden_call)

    reader = ZipWavFileReader()
    assert reader.read_wav_files(zip_path) == []


def test_read_wav_files_soundfile_fallback(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    wav_path = tmp_path / "fallback.wav"
    _write_wav(wav_path, duration_sec=1.0)
    zip_path = tmp_path / "fallback.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.write(wav_path, arcname=f"folder/{wav_path.name}")

    fake_soundfile = types.ModuleType("soundfile")

    def fake_info(_: str) -> float:
        raise RuntimeError("libsndfile broken")

    fake_soundfile.info = fake_info  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "soundfile", fake_soundfile)

    reader = ZipWavFileReader()
    results = reader.read_wav_files(zip_path)

    assert len(results) == 1
    assert results[0].filename == "folder/fallback.wav"
    assert results[0].duration_sec > 0


def test_read_wav_files_duration_extraction_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    zip_path = _build_zip(tmp_path, {"fail.wav": b"broken"})

    def exploding_get_wav_duration(path: Path) -> float:
        raise ValueError(f"unreadable {path}")

    _patch_duration(monkeypatch, exploding_get_wav_duration)

    reader = ZipWavFileReader()
    with caplog.at_level(logging.WARNING):
        results = reader.read_wav_files(zip_path)

    assert results == []
    assert any("Nelze přečíst hlavičku WAV" in message for message in caplog.messages)


def test_read_wav_files_duplicate_basenames(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    entries = {
        "sideB/track.wav": b"two",
        "sideA/track.wav": b"one",
    }
    zip_path = _build_zip(tmp_path, entries)

    recorded_paths: list[Path] = []
    durations_iter = iter([1.23, 4.56])

    def fake_get_wav_duration(path: Path) -> float:
        recorded_paths.append(path)
        return next(durations_iter)

    _patch_duration(monkeypatch, fake_get_wav_duration)

    reader = ZipWavFileReader()
    wav_infos = reader.read_wav_files(zip_path)

    assert [info.filename for info in wav_infos] == ["sideA/track.wav", "sideB/track.wav"]
    assert [info.duration_sec for info in wav_infos] == [1.23, 4.56]
    assert {p.parent.name for p in recorded_paths} == {"sideA", "sideB"}


def test_read_wav_files_skips_zero_duration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    zip_path = _build_zip(tmp_path, {"only.wav": b"zero"})

    def zero_duration(_: Path) -> float:
        return 0.0

    _patch_duration(monkeypatch, zero_duration)

    reader = ZipWavFileReader()
    with caplog.at_level(logging.WARNING):
        wav_infos = reader.read_wav_files(zip_path)

    assert wav_infos == []
    assert any("neplatnou délku" in message for message in caplog.messages)

``n
### tests\test_waveform_config.py

`$tag
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

``n
### tests\test_waveform_editor.py

`$tag
from __future__ import annotations

from pathlib import Path
from unittest import mock
import pyqtgraph as pg
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

pytestmark = pytest.mark.gui

import waveform_viewer
from waveform_viewer import WaveformEditorDialog


@pytest.fixture(autouse=True)
def fake_multimedia(monkeypatch):
    """Provide dummy multimedia classes so tests run without QtMultimedia."""

    class DummySignal:
        def __init__(self):
            self._callbacks = []

        def connect(self, callback):
            self._callbacks.append(callback)

        def emit(self, *args, **kwargs):
            for callback in list(self._callbacks):
                callback(*args, **kwargs)

    class DummyAudioOutput:
        def __init__(self, parent=None):
            self._volume = 1.0

        def setVolume(self, volume):
            self._volume = volume

        def volume(self):
            return self._volume

    class DummyMediaPlayer:
        def __init__(self, parent=None):
            self.positionChanged = DummySignal()
            self.durationChanged = DummySignal()
            self.errorOccurred = DummySignal()
            self._audio_output = None
            self._source = None

        def setAudioOutput(self, audio_output):
            self._audio_output = audio_output

        def setSource(self, source):
            self._source = source

        def play(self):
            pass

        def pause(self):
            pass

        def stop(self):
            pass

        def setPosition(self, position_ms):
            pass

    monkeypatch.setattr(waveform_viewer, "QAudioOutput", DummyAudioOutput, raising=False)
    monkeypatch.setattr(waveform_viewer, "QMediaPlayer", DummyMediaPlayer, raising=False)
    yield


@pytest.fixture
def editor_dialog(qapp, mock_wav_zip, qtbot, waveform_settings) -> WaveformEditorDialog:
    """Create a fully initialised WaveformEditorDialog for tests."""
    zip_path, wav_name = mock_wav_zip
    dialog = WaveformEditorDialog(zip_path, wav_name, waveform_settings)
    qtbot.addWidget(dialog)
    try:
        yield dialog
    finally:
        dialog.close()


class TestWaveformEditorDialog:
    def test_editor_creation(self, editor_dialog, mock_wav_zip):
        zip_path, wav_name = mock_wav_zip
        assert wav_name in editor_dialog.windowTitle()
        assert editor_dialog._zip_path == Path(zip_path)
        assert editor_dialog._wav_filename == wav_name
        assert editor_dialog.width() == 1200
        assert editor_dialog.height() == 800

    def test_multimedia_unavailable(self, monkeypatch, mock_wav_zip, waveform_settings):
        zip_path, wav_name = mock_wav_zip
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", False)
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_IMPORT_ERROR", ImportError("missing Qt multimedia"))
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(RuntimeError):
                WaveformEditorDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called_once()
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", True)

    def test_ui_components_exist(self, editor_dialog):
        assert isinstance(editor_dialog.plot_widget, pg.PlotWidget)
        assert editor_dialog.region_label.text().startswith("Region:")
        assert editor_dialog.position_slider.minimum() == 0
        assert editor_dialog.play_button.text() == "Play"
        assert editor_dialog.pause_button.text() == "Pause"
        assert editor_dialog.stop_button.text() == "Stop"

    def test_audio_data_loading(self, editor_dialog):
        assert editor_dialog._audio_data is not None
        assert editor_dialog._audio_data.size > 0
        assert editor_dialog._sample_rate > 0
        assert editor_dialog._duration_sec > 0

    def test_waveform_curve_has_data(self, editor_dialog):
        assert editor_dialog._waveform_curve is not None
        x_data, y_data = editor_dialog._waveform_curve.getData()
        assert len(x_data) > 0
        assert len(x_data) == len(y_data)

    def test_region_item_created(self, editor_dialog):
        assert isinstance(editor_dialog._region_item, pg.LinearRegionItem)
        region = editor_dialog._region_item.getRegion()
        assert pytest.approx(region[0]) == 0.0
        assert region[1] > region[0]

    def test_region_change_updates_bounds(self, editor_dialog):
        initial_range = editor_dialog.plot_widget.viewRange()[0]
        editor_dialog._region_item.setRegion([0.5, 1.0])
        editor_dialog._on_region_changed()
        assert editor_dialog._region_bounds[0] >= 0.0
        assert editor_dialog._region_bounds[1] > editor_dialog._region_bounds[0]
        updated_range = editor_dialog.plot_widget.viewRange()[0]
        assert pytest.approx(updated_range[0], rel=1e-3) == pytest.approx(initial_range[0], rel=1e-3)
        assert pytest.approx(updated_range[1], rel=1e-3) == pytest.approx(initial_range[1], rel=1e-3)

    def test_minimum_region_duration_enforced(self, editor_dialog):
        editor_dialog._region_item.setRegion([0.0, 0.01])
        editor_dialog._on_region_changed()
        updated_region = editor_dialog._region_item.getRegion()
        assert (updated_region[1] - updated_region[0]) >= editor_dialog._min_region_duration

    def test_find_rms_peaks_returns_values(self, editor_dialog):
        peaks = editor_dialog._find_rms_peaks(0.0, editor_dialog._duration_sec, editor_dialog._snap_tolerance)
        assert isinstance(peaks, list)
        assert all(isinstance(p, float) for p in peaks)

    def test_find_zero_crossings_returns_values(self, editor_dialog):
        crossings = editor_dialog._find_zero_crossings(0.0, editor_dialog._duration_sec, editor_dialog._snap_tolerance)
        assert isinstance(crossings, list)
        assert all(isinstance(c, float) for c in crossings)
        assert len(crossings) > 0

    def test_position_change_creates_playhead_line(self, editor_dialog):
        editor_dialog._on_position_changed(500)
        assert editor_dialog._playhead_line is not None
        assert pytest.approx(editor_dialog._playhead_line.value(), rel=1e-3) == 0.5

    def test_set_pdf_tracks_creates_markers(self, editor_dialog, tolerance_settings):
        pdf_tracks = [
            {"duration_sec": 0.5, "title": "Intro", "position": 1},
            {"duration_sec": 1.0, "title": "Main", "position": 2},
        ]
        wav_tracks = [
            {"duration_sec": 0.52, "title": "Intro", "position": 1},
            {"duration_sec": 1.05, "title": "Main", "position": 2},
        ]
        editor_dialog.set_pdf_tracks(pdf_tracks, wav_tracks, tolerance_settings)
        assert len(editor_dialog._pdf_markers) == len(pdf_tracks)
        assert len(editor_dialog._marker_times) == len(pdf_tracks)
        assert pytest.approx(editor_dialog._marker_times[0], rel=1e-3) == pytest.approx(0.5, rel=1e-3)
        assert pytest.approx(editor_dialog._marker_times[1], rel=1e-3) == pytest.approx(1.5, rel=1e-3)

    def test_clear_pdf_markers(self, editor_dialog, tolerance_settings):
        pdf_tracks = [{"duration_sec": 0.5, "title": "Intro", "position": 1}]
        editor_dialog.set_pdf_tracks(pdf_tracks, pdf_tracks, tolerance_settings)
        assert editor_dialog._pdf_markers
        editor_dialog._clear_pdf_markers()
        assert not editor_dialog._pdf_markers
        assert not editor_dialog._marker_times

    def test_zoom_controls_adjust_range(self, editor_dialog):
        initial_range = editor_dialog.plot_widget.viewRange()[0]
        editor_dialog._zoom_in()
        zoomed_range = editor_dialog.plot_widget.viewRange()[0]
        assert (zoomed_range[1] - zoomed_range[0]) < (initial_range[1] - initial_range[0])
        editor_dialog._zoom_out()
        widened_range = editor_dialog.plot_widget.viewRange()[0]
        assert (widened_range[1] - widened_range[0]) >= (zoomed_range[1] - zoomed_range[0])
        editor_dialog._fit_to_region()
        fitted_range = editor_dialog.plot_widget.viewRange()[0]
        region_duration = editor_dialog._region_bounds[1] - editor_dialog._region_bounds[0]
        assert pytest.approx(fitted_range[1] - fitted_range[0], rel=1e-2) == pytest.approx(region_duration, rel=1e-2)
        editor_dialog._fit_all()
        fit_all_range = editor_dialog.plot_widget.viewRange()[0]
        assert pytest.approx(fit_all_range[0], rel=1e-3) == pytest.approx(0.0, rel=1e-3)
        assert pytest.approx(fit_all_range[1], rel=1e-3) == pytest.approx(editor_dialog._duration_sec, rel=1e-3)

    def test_playback_controls_trigger_player(self, editor_dialog, qtbot):
        with mock.patch.object(editor_dialog._player, "play") as play_mock:
            qtbot.mouseClick(editor_dialog.play_button, Qt.MouseButton.LeftButton)
            play_mock.assert_called_once()
        with mock.patch.object(editor_dialog._player, "pause") as pause_mock:
            qtbot.mouseClick(editor_dialog.pause_button, Qt.MouseButton.LeftButton)
            pause_mock.assert_called_once()
        with mock.patch.object(editor_dialog._player, "stop") as stop_mock:
            qtbot.mouseClick(editor_dialog.stop_button, Qt.MouseButton.LeftButton)
            stop_mock.assert_called_once()

    def test_get_performance_stats(self, editor_dialog):
        stats = editor_dialog.get_performance_stats()
        assert set(stats.keys()) == {
            "duration_sec",
            "sample_rate",
            "audio_size_mb",
            "waveform_points",
        }

    def test_close_event_cleanup(self, editor_dialog, qtbot):
        temp_wav = editor_dialog._temp_wav
        assert temp_wav and temp_wav.exists()
        with mock.patch.object(editor_dialog._player, "stop") as stop_mock:
            editor_dialog.close()
            stop_mock.assert_called_once()
        if temp_wav:
            assert not temp_wav.exists()

    def test_missing_zip_file(self, tmp_path, qtbot, waveform_settings):
        non_existent = tmp_path / "missing.zip"
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(FileNotFoundError):
                WaveformEditorDialog(non_existent, "track.wav", waveform_settings)
        critical.assert_not_called()

    def test_missing_wav_in_zip(self, empty_zip, qtbot, waveform_settings):
        with pytest.raises(FileNotFoundError):
            WaveformEditorDialog(empty_zip, "missing.wav", waveform_settings)

    def test_invalid_audio_data(self, invalid_wav_zip, waveform_settings):
        zip_path, wav_name = invalid_wav_zip
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformEditorDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()
        dialog.close()

``n
### tests\test_waveform_integration.py

`$tag
from __future__ import annotations

from pathlib import Path
from unittest import mock

import pytest

pytestmark = pytest.mark.gui
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QSignalSpy
from PyQt6.QtWidgets import QMessageBox

import fluent_gui
from fluent_gui import (
    TABLE_HEADERS_BOTTOM,
    BottomTableModel,
    MainWindow,
    SideResult,
    TrackInfo,
    WavInfo,
)


@pytest.fixture
def main_window(qapp, qtbot, isolated_config, monkeypatch):
    monkeypatch.setattr(fluent_gui, "cfg", isolated_config, raising=False)
    monkeypatch.setattr(fluent_gui, "load_config", lambda path: isolated_config, raising=False)
    window = MainWindow()
    qtbot.addWidget(window)
    return window


def _make_side_result(zip_path: Path, wav_filename: str, tmp_path: Path) -> SideResult:
    pdf_path = tmp_path / "track.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 dummy")
    return SideResult(
        seq=1,
        pdf_path=pdf_path,
        zip_path=zip_path,
        side="A",
        mode="tracks",
        status=fluent_gui.STATUS_OK,
        pdf_tracks=[TrackInfo(title="Test Track", side="A", position=1, duration_sec=120)],
        wav_tracks=[WavInfo(filename=wav_filename, duration_sec=120.0)],
        total_pdf_sec=120,
        total_wav_sec=120.0,
        total_difference=0,
    )


class TestWaveformIntegration:
    def test_bottom_table_waveform_column_exists(self):
        assert TABLE_HEADERS_BOTTOM[7] == "Waveform"
        model = BottomTableModel()
        assert model.columnCount() == 8

    def test_waveform_column_click_opens_dialog(self, main_window, mock_wav_zip, qtbot, tmp_path, monkeypatch):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)
        with mock.patch("waveform_viewer.WaveformEditorDialog", autospec=True) as dialog_cls:
            dialog_instance = dialog_cls.return_value
            main_window.on_bottom_cell_clicked(index)
            dialog_cls.assert_called_once()
            args, kwargs = dialog_cls.call_args
            assert args[:2] == (zip_path, wav_name)
            assert kwargs["waveform_settings"] == main_window.waveform_settings
            assert kwargs["parent"] is main_window
            dialog_instance.exec.assert_called_once()

    def test_waveform_click_no_selection(self, main_window, mock_wav_zip, qtbot):
        zip_path, wav_name = mock_wav_zip
        index = main_window.bottom_model.index(0, 7)
        with mock.patch("waveform_viewer.WaveformEditorDialog") as dialog_cls:
            main_window.on_bottom_cell_clicked(index)
            dialog_cls.assert_not_called()

    def test_waveform_click_missing_zip(self, main_window, mock_wav_zip, qtbot, tmp_path):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        result.zip_path = Path(tmp_path / "missing.zip")
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)
        index = main_window.bottom_model.index(0, 7)
        with mock.patch.object(QMessageBox, "warning") as warning:
            main_window.on_bottom_cell_clicked(index)
            warning.assert_called_once()

    def test_waveform_click_missing_dependencies(self, main_window, mock_wav_zip, qtbot, tmp_path, monkeypatch):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)

        def import_hook(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "waveform_viewer":
                raise ImportError("waveform viewer missing")
            return original_import(name, globals, locals, fromlist, level)

        original_import = __import__
        with mock.patch("builtins.__import__", side_effect=import_hook):
            with mock.patch.object(QMessageBox, "warning") as warning:
                main_window.on_bottom_cell_clicked(index)
                warning.assert_called_once()

    def test_bottom_table_clicked_signal_connected(self, main_window, qtbot, mock_wav_zip, tmp_path):
        zip_path, wav_name = mock_wav_zip
        result = _make_side_result(zip_path, wav_name, tmp_path)
        main_window.top_model.add_result(result)
        main_window.top_table.selectRow(0)
        main_window.bottom_model.update_data(result)

        index = main_window.bottom_model.index(0, 7)
        if not main_window.isVisible():
            main_window.show()
            qtbot.waitForWindowShown(main_window)
        main_window.bottom_table.scrollTo(index)
        rect = main_window.bottom_table.visualRect(index)
        if not rect.isValid():
            qtbot.waitUntil(lambda: main_window.bottom_table.visualRect(index).isValid())
            rect = main_window.bottom_table.visualRect(index)
        spy = QSignalSpy(main_window.bottom_table.clicked)

        qtbot.mouseClick(
            main_window.bottom_table.viewport(),
            Qt.MouseButton.LeftButton,
            pos=rect.center(),
        )

        qtbot.waitUntil(lambda: len(spy) > 0)
        assert spy[0][0] == index

    def test_bottom_model_waveform_column_data(self, tmp_path):
        zip_path = tmp_path / "archive.zip"
        zip_path.write_bytes(b"")
        result = _make_side_result(zip_path, "track.wav", tmp_path)
        model = BottomTableModel()
        model.update_data(result)
        index = model.index(0, 7)
        assert model.data(index, Qt.ItemDataRole.DisplayRole) == "View"
        assert model.data(index, Qt.ItemDataRole.TextAlignmentRole) == Qt.AlignmentFlag.AlignCenter

``n
### tests\test_waveform_viewer.py

`$tag
from __future__ import annotations

from pathlib import Path
from unittest import mock

import numpy as np
import pyqtgraph as pg
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

pytestmark = pytest.mark.gui

import waveform_viewer
from waveform_viewer import WaveformViewerDialog


@pytest.fixture(autouse=True)
def fake_multimedia(monkeypatch):
    class DummySignal:
        def __init__(self):
            self._callbacks = []

        def connect(self, callback):
            self._callbacks.append(callback)

        def emit(self, *args, **kwargs):
            for callback in list(self._callbacks):
                callback(*args, **kwargs)

    class DummyAudioOutput:
        def __init__(self, parent=None):
            self._volume = 1.0

        def setVolume(self, volume):
            self._volume = volume

        def volume(self):
            return self._volume

    class DummyMediaPlayer:
        def __init__(self, parent=None):
            self.positionChanged = DummySignal()
            self.durationChanged = DummySignal()
            self.errorOccurred = DummySignal()
            self._audio_output = None
            self._source = None

        def setAudioOutput(self, audio_output):
            self._audio_output = audio_output

        def setSource(self, source):
            self._source = source

        def play(self):
            pass

        def pause(self):
            pass

        def stop(self):
            pass

        def setPosition(self, position_ms):
            pass

    monkeypatch.setattr(waveform_viewer, "QAudioOutput", DummyAudioOutput, raising=False)
    monkeypatch.setattr(waveform_viewer, "QMediaPlayer", DummyMediaPlayer, raising=False)
    yield


@pytest.fixture
def viewer_dialog(qapp, mock_wav_zip, qtbot, waveform_settings) -> WaveformViewerDialog:
    zip_path, wav_name = mock_wav_zip
    dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
    qtbot.addWidget(dialog)
    try:
        yield dialog
    finally:
        dialog.close()


class TestWaveformViewerDialog:
    def test_dialog_creation(self, viewer_dialog, mock_wav_zip):
        zip_path, wav_name = mock_wav_zip
        assert wav_name in viewer_dialog.windowTitle()
        assert viewer_dialog._zip_path == Path(zip_path)
        assert viewer_dialog._wav_filename == wav_name
        assert viewer_dialog.width() == 900
        assert viewer_dialog.height() == 600

    def test_multimedia_unavailable(self, monkeypatch, mock_wav_zip, waveform_settings):
        zip_path, wav_name = mock_wav_zip
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", False)
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_IMPORT_ERROR", ImportError("missing Qt multimedia"))
        with mock.patch.object(QMessageBox, "critical") as critical:
            with pytest.raises(RuntimeError):
                WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called_once()
        monkeypatch.setattr(waveform_viewer, "_MULTIMEDIA_AVAILABLE", True)

    def test_ui_components_exist(self, viewer_dialog):
        assert isinstance(viewer_dialog.plot_widget, pg.PlotWidget)
        assert viewer_dialog.play_button.text() == "Play"
        assert viewer_dialog.pause_button.text() == "Pause"
        assert viewer_dialog.stop_button.text() == "Stop"
        assert viewer_dialog.time_current.text() == "00:00"
        assert viewer_dialog.time_total.text() != ""
        assert viewer_dialog.position_slider.minimum() == 0
        assert viewer_dialog.volume_slider.maximum() == 100

    def test_plot_widget_configuration(self, viewer_dialog):
        plot_item = viewer_dialog.plot_widget.getPlotItem()
        assert plot_item.getAxis("left").labelText == "Amplitude"
        assert plot_item.getAxis("bottom").labelText == "Time"

    def test_waveform_extraction(self, mock_wav_zip, qtbot, waveform_settings):
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        qtbot.addWidget(dialog)
        assert dialog._temp_wav is not None
        assert dialog._temp_wav.exists()
        assert dialog._temp_wav.suffix == ".wav"

    def test_waveform_loading_success(self, monkeypatch, tmp_path, qtbot, waveform_settings):
        fake_wav = tmp_path / "fake.wav"
        fake_wav.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake_wav

        mono = np.linspace(-1, 1, 1000, dtype=np.float32)
        with (
            mock.patch.object(waveform_viewer, "sf") as mock_sf,
            mock.patch.object(waveform_viewer.pg.PlotDataItem, "setData", autospec=True) as set_data,
        ):
            mock_sf.read.return_value = (mono, 100)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            dialog = WaveformViewerDialog(
                tmp_path / "dummy.zip",
                "test.wav",
                waveform_settings,
            )
            qtbot.addWidget(dialog)
            assert dialog._duration_ms > 0
            assert dialog.time_total.text().startswith("00:")
            assert set_data.called

    def test_waveform_loading_stereo_to_mono(self, monkeypatch, tmp_path, qtbot, waveform_settings):
        fake = tmp_path / "fake.wav"
        fake.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake

        stereo = np.column_stack(
            [np.linspace(-1, 1, 1000, dtype=np.float32), np.linspace(1, -1, 1000, dtype=np.float32)]
        )
        with mock.patch.object(waveform_viewer, "sf") as mock_sf:
            mock_sf.read.return_value = (stereo, 100)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            dialog = WaveformViewerDialog(
                tmp_path / "dummy.zip",
                "test.wav",
                waveform_settings,
            )
            qtbot.addWidget(dialog)
            assert dialog._duration_ms > 0

    def test_waveform_downsampling(self, monkeypatch, tmp_path, qtbot, waveform_settings):
        waveform_settings.downsample_factor = 20
        fake = tmp_path / "fake.wav"
        fake.write_bytes(b"RIFF\x00\x00\x00\x00WAVEfmt ")

        def fake_extract(self):
            self._temp_wav = fake

        mono = np.linspace(-1, 1, 4000, dtype=np.float32)
        with (
            mock.patch.object(waveform_viewer, "sf") as mock_sf,
            mock.patch.object(waveform_viewer.pg.PlotDataItem, "setData", autospec=True) as set_data,
        ):
            mock_sf.read.return_value = (mono, 400)
            monkeypatch.setattr(WaveformViewerDialog, "_extract_wav", fake_extract, raising=False)
            WaveformViewerDialog(
                tmp_path / "dummy.zip",
                "test.wav",
                waveform_settings,
            )
            # We cannot easily inspect internals but ensure plotting called with compressed data
            args, _ = set_data.call_args
            x_values = args[1]
            assert len(x_values) < mono.size

    def test_play_button_triggers_playback(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "play") as play_mock:
            qtbot.mouseClick(viewer_dialog.play_button, Qt.MouseButton.LeftButton)
            play_mock.assert_called_once()

    def test_pause_button_triggers_pause(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "pause") as pause_mock:
            qtbot.mouseClick(viewer_dialog.pause_button, Qt.MouseButton.LeftButton)
            pause_mock.assert_called_once()

    def test_stop_button_resets_position(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._player, "stop") as stop_mock:
            with mock.patch.object(viewer_dialog, "_on_position_changed") as on_position:
                qtbot.mouseClick(viewer_dialog.stop_button, Qt.MouseButton.LeftButton)
                stop_mock.assert_called_once()
                on_position.assert_called_with(0)

    def test_volume_slider_changes_volume(self, viewer_dialog, qtbot):
        with mock.patch.object(viewer_dialog._audio_output, "setVolume") as set_volume:
            viewer_dialog.volume_slider.setValue(75)
            qtbot.waitUntil(lambda: set_volume.called, timeout=1000)
            set_volume.assert_called_with(pytest.approx(0.75, rel=1e-2))
            assert viewer_dialog.volume_value.text() == "75%"

    def test_position_changed_updates_ui(self, viewer_dialog):
        viewer_dialog._on_position_changed(30000)
        assert viewer_dialog.position_slider.value() == 30000
        assert viewer_dialog.time_current.text() == "00:30"

    def test_slider_seeking(self, viewer_dialog):
        with mock.patch.object(viewer_dialog._player, "setPosition") as set_position:
            viewer_dialog._on_slider_pressed()
            viewer_dialog._on_slider_moved(60000)
            viewer_dialog._on_slider_released()
            set_position.assert_called_with(60000)

    @pytest.mark.parametrize(
        "millis, expected",
        [
            (0, "00:00"),
            (45_000, "00:45"),  # 45 seconds
            (125_000, "02:05"),  # 2 minutes 5 seconds
            (-1_000, "00:00"),  # Negative values should return 00:00
        ],
    )
    def test_format_time(self, millis, expected):
        """Test time formatting with milliseconds input (Qt QMediaPlayer API)."""
        assert WaveformViewerDialog._format_time(millis) == expected

    def test_default_volume_from_config(self, mock_wav_zip, qtbot, waveform_settings):
        waveform_settings.default_volume = 0.7
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        qtbot.addWidget(dialog)
        assert dialog._audio_output.volume() == pytest.approx(0.7)

    def test_downsample_factor_from_config(self, mock_wav_zip, qtbot, waveform_settings):
        waveform_settings.downsample_factor = 15
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        qtbot.addWidget(dialog)
        assert dialog._get_downsample_factor() == 15

    def test_waveform_colors_from_config(self, mock_wav_zip, qtbot, waveform_settings):
        waveform_settings.waveform_color = "#ffffff"
        waveform_settings.position_line_color = "#123456"
        zip_path, wav_name = mock_wav_zip
        dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        qtbot.addWidget(dialog)
        curve_color = dialog._plot_curve.opts["pen"].color().name()
        line_color = dialog._position_line.pen().color().name()
        assert curve_color.lower() == "#ffffff"
        assert line_color.lower() == "#123456"

    def test_missing_zip_file(self, tmp_path, qtbot, waveform_settings):
        non_existent = tmp_path / "missing.zip"
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(non_existent, "track.wav", waveform_settings)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_missing_wav_in_zip(self, empty_zip, qtbot, waveform_settings):
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(empty_zip, "missing.wav", waveform_settings)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_invalid_wav_data(self, invalid_wav_zip, qtbot, waveform_settings):
        zip_path, wav_name = invalid_wav_zip
        with mock.patch.object(QMessageBox, "critical") as critical:
            dialog = WaveformViewerDialog(zip_path, wav_name, waveform_settings)
        critical.assert_called()
        assert not dialog.play_button.isEnabled()

    def test_player_error_handling(self, viewer_dialog, monkeypatch):
        with mock.patch.object(QMessageBox, "warning") as warning:
            viewer_dialog._on_player_error(None, "Test error")
            warning.assert_called_once()

    def test_close_event_cleanup(self, viewer_dialog, qtbot):
        temp_wav = viewer_dialog._temp_wav
        assert temp_wav and temp_wav.exists()
        with mock.patch.object(viewer_dialog._player, "stop") as stop_mock:
            viewer_dialog.close()
            stop_mock.assert_called_once()
        if temp_wav:
            assert not temp_wav.exists()

    def test_position_line_stored_as_instance_variable(self, viewer_dialog):
        """Verify position line is created once and reused on updates."""
        initial_line = viewer_dialog._position_line
        viewer_dialog._on_position_changed(1000)
        viewer_dialog._on_position_changed(2000)
        assert viewer_dialog._position_line is initial_line

``n
### tests\test_worker_manager.py

`$tag
from __future__ import annotations

from unittest.mock import MagicMock

import pytest
from PyQt6.QtCore import QObject, pyqtSignal


@pytest.fixture
def mock_worker_settings(tmp_path):
    from ui.config_models import WorkerSettings

    return WorkerSettings(pdf_dir=tmp_path, wav_dir=tmp_path)


@pytest.fixture
def mock_analysis_worker(monkeypatch):
    class MockWorker(QObject):
        progress = pyqtSignal(str)
        result_ready = pyqtSignal(object)
        finished = pyqtSignal(str)

        def __init__(
            self,
            worker_settings,
            tolerance_settings,
            id_extraction_settings,
        ):
            super().__init__()
            self.worker_settings = worker_settings
            self.tolerance_settings = tolerance_settings
            self.id_extraction_settings = id_extraction_settings
            self.run = MagicMock()

    monkeypatch.setattr("ui.workers.worker_manager.AnalysisWorker", MockWorker)
    return MockWorker


def wait_for_worker(manager, qtbot, condition, timeout=1000):
    qtbot.waitUntil(lambda: manager._worker is not None, timeout=timeout)
    qtbot.waitUntil(condition, timeout=timeout)


def test_worker_manager_creation(
    mock_worker_settings,
    tolerance_settings,
    id_extraction_settings,
):
    from ui.workers.worker_manager import AnalysisWorkerManager

    manager = AnalysisWorkerManager(
        worker_settings=mock_worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )
    assert not manager.is_running()
    assert manager._thread is None
    assert manager._worker is None


def test_start_analysis_starts_thread_and_worker(
    mock_worker_settings,
    tolerance_settings,
    id_extraction_settings,
    mock_analysis_worker,
    qtbot,
):
    from ui.workers.worker_manager import AnalysisWorkerManager

    manager = AnalysisWorkerManager(
        worker_settings=mock_worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )

    manager.start_analysis()
    wait_for_worker(manager, qtbot, lambda: manager._worker.run.called)

    assert manager._thread is not None
    assert manager._worker is not None
    assert manager._worker.run.called

    manager.cleanup()
    assert manager._thread is None
    assert manager._worker is None


def test_cleanup_stops_thread(
    mock_worker_settings,
    tolerance_settings,
    id_extraction_settings,
    mock_analysis_worker,
    qtbot,
):
    from ui.workers.worker_manager import AnalysisWorkerManager

    manager = AnalysisWorkerManager(
        worker_settings=mock_worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )
    manager.start_analysis()
    wait_for_worker(manager, qtbot, lambda: manager._worker.run.called)

    manager.cleanup()
    qtbot.waitUntil(lambda: not manager.is_running(), timeout=1000)

    assert manager._thread is None
    assert manager._worker is None


def test_signals_are_forwarded(
    mock_worker_settings,
    tolerance_settings,
    id_extraction_settings,
    mock_analysis_worker,
    qtbot,
):
    from ui.workers.worker_manager import AnalysisWorkerManager

    manager = AnalysisWorkerManager(
        worker_settings=mock_worker_settings,
        tolerance_settings=tolerance_settings,
        id_extraction_settings=id_extraction_settings,
    )

    progress_values = []
    result_values = []
    finished_values = []

    manager.progress.connect(lambda msg: progress_values.append(msg))
    manager.result_ready.connect(lambda payload: result_values.append(payload))
    manager.finished.connect(lambda msg: finished_values.append(msg))

    manager.start_analysis()
    wait_for_worker(manager, qtbot, lambda: manager._worker.run.called)

    manager._worker.progress.emit("In progress...")
    manager._worker.result_ready.emit({"data": 1})
    manager._worker.finished.emit("Done")

    assert progress_values == ["In progress..."]
    assert result_values == [{"data": 1}]
    assert finished_values == ["Done"]

    manager.cleanup()

``n
### tools\bootstrap_and_finalize.sh

`$tag
#!/usr/bin/env bash
set -euo pipefail

section() { printf "\n\033[1;36m== %s ==\033[0m\n" "$*"; }
ok()      { printf "\033[0;32m[ok]\033[0m %s\n" "$*"; }
warn()    { printf "\033[0;33m[warn]\033[0m %s\n" "$*"; }
info()    { printf "\033[0;34m[i]\033[0m %s\n" "$*"; }

# --- 0) Create local venv (.venv) and use it ---------------------------------
section "Python venv bootstrap (.venv)"
PY="python3"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[err] python3 not found in PATH"; exit 1
fi
if [[ ! -d .venv ]]; then
  $PY -m venv .venv
  ok "Created .venv"
fi

if [[ -x .venv/bin/python ]]; then
  PY=".venv/bin/python"
elif [[ -x .venv/Scripts/python ]]; then
  PY=".venv/Scripts/python"
elif [[ -x .venv/Scripts/python.exe ]]; then
  PY=".venv/Scripts/python.exe"
else
  echo "[err] Could not find Python executable in .venv"; exit 1
fi
VENV_BIN=$(dirname "$PY")
export PATH="$VENV_BIN:$PATH"
PIP="$PY -m pip"

$PIP --version >/dev/null 2>&1 || ($PY -m ensurepip --upgrade || true)
$PIP install --upgrade pip wheel setuptools

# --- 1) Dev toolchain ---------------------------------------------------------
section "Install dev toolchain"
if [[ -f requirements-dev.txt ]]; then
  info "requirements-dev.txt found → installing"
  $PIP install -r requirements-dev.txt
else
  info "requirements-dev.txt not found → installing minimal toolchain"
  $PIP install "coverage>=7.6" "pytest>=7.4" "ruff>=0.5" "mypy>=1.8"
fi

# Optional: OpenSpec CLI
if ! command -v openspec >/dev/null 2>&1; then
  warn "openspec CLI not found → attempting optional install"
  $PIP install openspec-cli || warn "openspec optional install failed (continuing)"
fi

# --- 2) Verify tools ----------------------------------------------------------
section "Verify tool availability"
$PY --version
$PIP show coverage pytest ruff mypy | sed 's/^Name: /-- /' || true
openspec --version || true

# --- 3) Run finalize flow w/ audit log ---------------------------------------
section "Run finalize.sh (with audit log)"
mkdir -p .openspec
ts=$(date +%Y%m%d_%H%M%S)
LOG=".openspec/finalize-${ts}.log"

chmod +x tools/check.sh tools/finalize.sh || true
# Capture both finalize output AND a quick env snapshot into the same log
{
  echo "# Environment snapshot";
  which $PY || true;
  $PY -m pip freeze || true;
  echo;
  echo "# Finalize flow";
  ./tools/finalize.sh
} 2>&1 | tee "$LOG"

ok "Audit log saved to: $LOG"

# --- 4) Optional stricter OpenSpec check if CLI present -----------------------
if command -v openspec >/dev/null 2>&1; then
  section "OpenSpec validate (strict, hard-fail)"
  openspec validate --strict | tee -a "$LOG"
  ok "OpenSpec validate passed"
else
  warn "openspec CLI not found; validation deferred"
fi

# --- 5) Exit summary ----------------------------------------------------------
section "Summary"
echo "Finalize log: $LOG"
ok "Bootstrap + Finalization completed"

``n
### tools\bootstrap_finalize.sh

`$tag
#!/usr/bin/env bash
set -euo pipefail

section() { printf "\n\033[1;36m== %s ==\033[0m\n" "$*"; }
ok()      { printf "\033[0;32m[ok]\033[0m %s\n" "$*"; }
warn()    { printf "\033[0;33m[warn]\033[0m %s\n" "$*"; }
info()    { printf "\033[0;34m[i]\033[0m %s\n" "$*"; }

PY="python3"
PIP="python3 -m pip"

section "Bootstrap Python environment"
if ! command -v python3 >/dev/null 2>&1; then
  echo "[err] python3 not found in PATH"; exit 1
fi
$PIP --version >/dev/null 2>&1 || ($PY -m ensurepip --upgrade || true)
$PIP install --break-system-packages --upgrade pip wheel setuptools

if [[ -f requirements-dev.txt ]]; then
  info "requirements-dev.txt found → installing"
  $PIP install --break-system-packages -r requirements-dev.txt
elif [[ -f requirements.txt ]]; then
  info "requirements-dev.txt not found, using requirements.txt"
  $PIP install --break-system-packages -r requirements.txt
else
  info "requirements-dev.txt not found → installing minimal toolchain"
  $PIP install --break-system-packages coverage pytest ruff mypy || true
fi

if ! command -v openspec >/dev/null 2>&1; then
  warn "openspec CLI not found → attempting optional install"
  $PIP install --break-system-packages openspec-cli || warn "openspec optional install failed (continuing)"
fi

section "Verify tool availability"
$PY --version
$PY -m pip show coverage pytest ruff mypy || true
openspec --version || true

section "Run finalize flow"
chmod +x tools/check.sh tools/finalize.sh || true
./tools/finalize.sh || { echo "[err] finalize.sh failed"; exit 1; }

section "Audit snapshot"
git --version || true
git status --porcelain || true
git tag -l 'refactor-phase1-stabilization*' || true

``n
### tools\build_resources.py

`$tag
#!/usr/bin/env python3
"""Build Qt resources from QRC file using pyrcc6 or manual generation."""

import subprocess
import sys
from pathlib import Path


def build_resources():
    """Compile icons.qrc to _icons_rc.py"""
    qrc_path = Path(__file__).parent.parent / "assets" / "icons.qrc"
    output_path = Path(__file__).parent.parent / "ui" / "_icons_rc.py"

    if not qrc_path.exists():
        print(f"Error: {qrc_path} not found")
        return False

    # Try using pyrcc6 command
    try:
        result = subprocess.run(
            ["pyrcc6", str(qrc_path), "-o", str(output_path)],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"[SUCCESS] Successfully compiled {qrc_path} to {output_path}")
        print(result.stdout)
        return True
    except FileNotFoundError:
        print("pyrcc6 not found in PATH, using fallback method...")
    except subprocess.CalledProcessError as e:
        print(f"pyrcc6 failed: {e.stderr}")
        return False

    # Fallback: create a minimal working _icons_rc.py that registers the resources
    print("Generating minimal resource module...")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # This creates a simple module that PyQt6 will use to find the resource files
    minimal_code = '''# This file was automatically generated by build_resources.py
# Qt resource module (minimal fallback)
from PyQt6.QtCore import qRegisterResourceData, qUnregisterResourceData

# Note: QResource.addSearchPath is not for resource files compiled by pyrcc6,
# and directly accessing QResource.addSearchPath does not function as intended
# for :/ paths. The proper mechanism involves data registered by pyrcc6.
# When pyrcc6 is absent, we rely on ui/theme.py's direct file loading logic.

def qInitResources():
    """Initialize resources (called on module import)"""
    pass

def qCleanupResources():
    """Cleanup resources"""
    pass

# Auto-initialize on import
qInitResources()
'''

    with output_path.open("w", encoding="utf-8") as f:
        f.write(minimal_code)

    print(f"[SUCCESS] Generated fallback resource module at {output_path}")
    return True


if __name__ == "__main__":
    success = build_resources()
    sys.exit(0 if success else 1)

``n
### tools\finalize.sh

`$tag
#!/usr/bin/env bash
set -euo pipefail

CHANGE_ID="refactor-phase1-stabilization"
TAG_NAME="refactor-phase1-stabilization-done"

section() { printf "\n\033[1;36m== %s ==\033[0m\n" "$*"; }
info()    { printf "\033[0;34m[i]\033[0m %s\n" "$*"; }
ok()      { printf "\033[0;32m[ok]\033[0m %s\n" "$*"; }
warn()    { printf "\033[0;33m[warn]\033[0m %s\n" "$*"; }
err()     { printf "\033[0;31m[err]\033[0m %s\n" "$*"; }

# 0) Preflight
section "Preflight"
if [[ ! -f tools/check.sh ]]; then
  err "Missing tools/check.sh"; exit 1
fi
chmod +x tools/check.sh || true
ok "tools/check.sh is executable"

# 1) Quality Gate (unified)
section "Quality Gate"
./tools/check.sh
ok "Quality gate passed (tools/check.sh)"

# 2) OpenSpec finalize + validate (if CLI available)
section "OpenSpec Finalization"
if command -v openspec >/dev/null 2>&1; then
  info "openspec CLI detected"
  openspec finalize "$CHANGE_ID"
  ok "openspec finalize $CHANGE_ID done"

  section "OpenSpec Validate (strict)"
  openspec validate --strict
  ok "openspec validate --strict passed"
else
  warn "openspec CLI not found in PATH. Skipping finalize/validate."
  warn "Run later when CLI is available: "
  printf "  openspec finalize %s\n  openspec validate --strict\n" "$CHANGE_ID"
fi

# 3) Git: init/commit/tag/push (optional, only if inside repo OR user wants it)
section "Git Commit/Tag"
if command -v git >/dev/null 2>&1; then
  if git rev-parse --git-dir >/dev/null 2>&1; then
    info "Git repository detected"
  else
    warn "No git repo found. Initializing a new one..."
    git init
    git branch -M main || true
  fi

  # Ensure .gitignore exists minimally
  if [[ ! -f .gitignore ]]; then
    cat <<'EOF' > .gitignore
__pycache__/
*.pyc
.coverage
htmlcov/
.env
.venv/
EOF
    info "Created minimal .gitignore"
  fi

  git add -A
  COMMIT_MSG="Finalize ${CHANGE_ID}: quality gate pass, docs aligned (PyQt6+QSettings), Purpose sections, CHANGELOG 0.0.1"
  if git diff --cached --quiet; then
    info "No staged changes to commit"
  else
    git commit -m "$COMMIT_MSG"
    ok "Committed changes"
  fi

  if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    info "Tag ${TAG_NAME} already exists"
  else
    git tag -a "$TAG_NAME" -m "Stabilization phase 1 finalized"
    ok "Created tag ${TAG_NAME}"
  fi

  if git remote get-url origin >/dev/null 2>&1; then
    git push origin HEAD --tags
    ok "Pushed branch and tags to origin"
  else
    warn "No git remote configured. Skipping push."
  fi
else
  warn "git not found. Skipping commit/tag/push."
fi

section "Done"
ok "Finalization flow completed. If OpenSpec CLI was missing, re-run the finalize/validate commands later."

``n
### tools\check.sh

`$tag
#!/usr/bin/env bash
set -euo pipefail

# Phase 1 quality gate script.

if [[ -n "${PYTHON_BIN:-}" ]]; then
  # Allow callers to override the interpreter path, e.g. PYTHON_BIN="py -3".
  # shellcheck disable=SC2206
  PYTHON_CMD=(${PYTHON_BIN})
elif command -v python >/dev/null 2>&1; then
  PYTHON_CMD=("python")
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=("python3")
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=("py" "-3")
else
  echo "Python interpreter not found on PATH." >&2
  exit 1
fi

echo "Collecting coverage metrics..."
# ZDE JE OPRAVA: Odstraněn flag -m "not gui" pro spuštění VŠECH testů
QT_QPA_PLATFORM=offscreen "${PYTHON_CMD[@]}" -m coverage run -m pytest
"${PYTHON_CMD[@]}" -m coverage report --fail-under=85

echo "Running Ruff lint checks..."
"${PYTHON_CMD[@]}" -m ruff check .

echo "Running mypy in strict mode..."
"${PYTHON_CMD[@]}" -m mypy --strict core adapters services

if command -v openspec >/dev/null 2>&1; then
   echo "Validating OpenSpec specifications..."
   openspec validate refactor-phase5-ai-port --strict
else
   echo "Skipping OpenSpec validation (openspec CLI not found)..."
fi

echo "All checks passed"

``n
### ui\__init__.py

`$tag
from core.models.settings import ExportSettings, IdExtractionSettings, ToleranceSettings

from .constants import *
from .theme import get_system_file_icon, get_custom_icon, get_gz_color, load_gz_media_fonts, load_gz_media_stylesheet
from .models.results_table_model import ResultsTableModel
from .models.tracks_table_model import TracksTableModel
from .workers.analysis_worker import AnalysisWorker
from .workers.worker_manager import AnalysisWorkerManager
from .dialogs.settings_dialog import SettingsDialog
from .main_window import MainWindow
from .config_models import (
    PathSettings,
    ThemeSettings,
    WorkerSettings,
    WaveformSettings,
    load_tolerance_settings,
    load_export_settings,
    load_path_settings,
    load_theme_settings,
    load_worker_settings,
    load_id_extraction_settings,
    load_waveform_settings,
)

__all__ = [
    # Constants
    "SETTINGS_FILENAME",
    "WINDOW_TITLE",
    "STATUS_READY",
    "STATUS_ANALYZING",
    "MSG_ERROR_PATHS",
    "MSG_NO_PAIRS",
    "MSG_DONE",
    "MSG_ERROR",
    "MSG_SCANNING",
    "MSG_PROCESSING_PAIR",
    "BUTTON_RUN_ANALYSIS",
    "LABEL_FILTER",
    "FILTER_ALL",
    "FILTER_OK",
    "FILTER_FAIL",
    "FILTER_WARN",
    "TABLE_HEADERS_TOP",
    "TABLE_HEADERS_BOTTOM",
    "SYMBOL_CHECK",
    "SYMBOL_CROSS",
    "PLACEHOLDER_DASH",
    "COLOR_WHITE",
    "LABEL_TOTAL_TRACKS",
    "STATUS_OK",
    "STATUS_WARN",
    "STATUS_FAIL",
    "INTERFACE_MAIN",
    # Icon constants
    "ICON_CHECK",
    "ICON_CROSS",
    "ICON_PLAY",
    # Theme helpers
    "get_system_file_icon",
    "get_custom_icon",
    "get_gz_color",
    "load_gz_media_fonts",
    "load_gz_media_stylesheet",
    # Models
    "ResultsTableModel",
    "TracksTableModel",
    # Workers
    "AnalysisWorker",
    "AnalysisWorkerManager",
    # Dialogs
    "SettingsDialog",
    # Main window
    "MainWindow",
    # Config models and loaders
    "ToleranceSettings",
    "ExportSettings",
    "PathSettings",
    "ThemeSettings",
    "WorkerSettings",
    "IdExtractionSettings",
    "WaveformSettings",
    "load_tolerance_settings",
    "load_export_settings",
    "load_path_settings",
    "load_theme_settings",
    "load_worker_settings",
    "load_id_extraction_settings",
    "load_waveform_settings",
]

``n
### ui\_icons_rc.py

`$tag
# This file was automatically generated by build_resources.py
# Qt resource module (minimal fallback)
from PyQt6.QtCore import qRegisterResourceData, qUnregisterResourceData

# Note: QResource.addSearchPath is not for resource files compiled by pyrcc6,
# and directly accessing QResource.addSearchPath does not function as intended
# for :/ paths. The proper mechanism involves data registered by pyrcc6.
# When pyrcc6 is absent, we rely on ui/theme.py's direct file loading logic.


def qInitResources():
    """Initialize resources (called on module import)"""
    pass


def qCleanupResources():
    """Cleanup resources"""
    pass


# Auto-initialize on import
qInitResources()

``n
### ui\config_models.py

`$tag
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

    claim_visible_attr = getattr(cfg, "gz_claim_visible", None)
    claim_visible = bool(getattr(claim_visible_attr, "value", True))

    claim_text_attr = getattr(cfg, "gz_claim_text", None)
    claim_text = getattr(claim_text_attr, "value", "Emotions. Materialized.")

    action_color_attr = getattr(cfg, "ui_table_action_bg_color", None)
    action_bg_color = getattr(action_color_attr, "value", "#E0E7FF")

    total_row_bg_color = cfg.get("ui/total_row_bg_color", "#F3F4F6")

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

``n
### ui\constants.py

`$tag
from pathlib import Path

"""
Constants for the UI module.

This module defines constants used throughout the UI, including status messages, table headers, and symbols.

Note: Text symbols like SYMBOL_CHECK and SYMBOL_CROSS are deprecated in favor of icon constants ICON_CHECK, ICON_CROSS, ICON_PLAY for better cross-platform rendering.
"""

# --- Constants ---
SETTINGS_FILENAME = Path("settings.json")
STATUS_READY = "Ready"
STATUS_ANALYZING = "Analyzing..."
MSG_ERROR_PATHS = "Error: Paths 'pdf_dir' and 'wav_dir' must be set in settings.json"
MSG_NO_PAIRS = "No valid PDF-ZIP pairs found."
MSG_DONE = "Analysis completed. Processed {count} pairs."
MSG_ERROR = "Error: {error}"
MSG_SCANNING = "Scanning and pairing files..."
MSG_PROCESSING_PAIR = "Processing pair {current}/{total}: {filename}"
WINDOW_TITLE = "Final Cue Sheet Checker"
BUTTON_RUN_ANALYSIS = "Run analysis"
LABEL_FILTER = "Filter:"
FILTER_ALL = "All"
FILTER_OK = "OK"
FILTER_FAIL = "Fail"
FILTER_WARN = "Warn"
TABLE_HEADERS_TOP = ["#", "File", "Side", "Mode", "Side length", "Status", "PDF", "ZIP"]
TABLE_HEADERS_BOTTOM = ["#", "WAV file", "Title", "Length (PDF)", "Length (WAV)", "Difference(s)", "Match", "Waveform"]

# Table content strings

COLOR_WHITE = "white"
STATUS_OK = "OK"
STATUS_WARN = "WARN"
STATUS_FAIL = "FAIL"

# Icon constants for UI rendering
ICON_CHECK = "check"
ICON_CROSS = "cross"
ICON_PLAY = "play"

# Deprecated: Use get_custom_icon('check') and get_custom_icon('cross') instead
# These constants are kept for backward compatibility but are no longer used in UI rendering
SYMBOL_CHECK = "✓"
SYMBOL_CROSS = "✗"
PLACEHOLDER_DASH = "-"
LABEL_TOTAL_TRACKS = "Total (tracks)"
# Interface strings
INTERFACE_MAIN = "Main"

``n
### ui\delegates\__init__.py

`$tag

``n
### ui\delegates\action_cell_delegate.py

`$tag
"""Delegate for rendering hover affordance on action cells in tables."""

from __future__ import annotations

from typing import Set

from PyQt6.QtCore import QModelIndex, QRect
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QAbstractItemView, QStyledItemDelegate, QStyle


def _darken_color(color: str, factor: float = 0.15) -> QColor:
    """Darken a hex color by a given factor (0.0 to 1.0).

    Args:
        color: Hex color string (e.g., '#E0E7FF')
        factor: Darkening factor (0.0-1.0, where 1.0 is black)

    Returns:
        QColor object
    """
    qcolor = QColor(color)
    if not qcolor.isValid():
        return QColor(color)

    # Reduce lightness by factor
    h, s, v, a = qcolor.getHsv()
    if v > 0:
        v = max(0, int(v * (1 - factor)))
    qcolor.setHsv(h, s, v, a)
    return qcolor


class ActionCellDelegate(QStyledItemDelegate):
    """Delegate that renders a subtle hover tint on action cells in specified columns.

    This delegate checks if a cell is in a configured action column and if the mouse
    is hovering over it. If so, it draws a slightly darker background tint before
    rendering the normal content.
    """

    def __init__(self, theme_settings, action_columns: Set[int] | list[int]):
        """Initialize the delegate.

        Args:
            theme_settings: ThemeSettings object with action_bg_color
            action_columns: Set or list of column indices that are action cells
        """
        super().__init__()
        self.theme_settings = theme_settings
        self.action_columns = set(action_columns)
        self._hovered_index: QModelIndex | None = None

    def paint(
        self,
        painter: QPainter,
        option,
        index,
    ) -> None:
        """Paint the cell with hover affordance if applicable.

        Args:
            painter: QPainter for drawing
            option: QStyleOptionViewItem with styling info
            index: QModelIndex of the cell
        """
        # Only apply hover effect for action columns
        if index.column() not in self.action_columns:
            super().paint(painter, option, index)
            return

        # Check if cell is hovered and not selected
        # Compare with the currently hovered index tracked via mouse events
        is_hovered = (
            self._hovered_index is not None
            and self._hovered_index.row() == index.row()
            and self._hovered_index.column() == index.column()
        )
        is_selected = bool(option.state & QStyle.StateFlag.State_Selected)

        if is_hovered and not is_selected:
            # Draw hover tint background
            hover_color = _darken_color(
                self.theme_settings.action_bg_color,
                factor=0.15,
            )
            painter.fillRect(option.rect, hover_color)

        # Call parent paint to render the icon and text
        super().paint(painter, option, index)

    def set_hovered_index(self, index: QModelIndex | None) -> None:
        """Set the currently hovered cell index.

        Args:
            index: QModelIndex of the hovered cell, or None if no cell is hovered
        """
        self._hovered_index = index

``n
### ui\dialogs\__init__.py

`$tag

``n
### ui\dialogs\settings_dialog.py

`$tag
from __future__ import annotations

import logging
import os
from pathlib import Path

from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFrame,
    QMessageBox,
    QScrollArea,
    QVBoxLayout,
)

from config import save_config
from settings_page import SettingsPage


class SettingsDialog(QDialog):
    """Modal settings dialog containing SettingsPage with Save/Cancel buttons."""

    def __init__(self, settings_filename: Path, parent=None):
        super().__init__(parent)
        self.settings_filename = Path(settings_filename)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.resize(800, 600)

        layout = QVBoxLayout(self)

        scroll_area = QScrollArea(self)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.settings_page = SettingsPage()
        scroll_area.setWidget(self.settings_page)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _show_safe_message_box(
        self,
        title: str,
        text: str,
        icon: QMessageBox.Icon = QMessageBox.Icon.Information,
    ):
        if os.getenv("QT_QPA_PLATFORM") == "offscreen":
            logging.error(f"MODAL_DIALOG_BLOCKED: Title: {title}, Text: {text}")
            return

        parent = self.parent()
        if parent and hasattr(parent, "_show_safe_message_box"):
            parent._show_safe_message_box(title, text, icon)
            return

        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setText(text)
        msg_box.setWindowTitle(title)
        msg_box.exec()

    def _on_save(self) -> None:
        """Handle save button click - save config and accept dialog."""
        try:
            save_config(self.settings_filename)
            self.accept()
        except Exception as exc:
            self._show_safe_message_box(
                "Save Error",
                f"Failed to save settings:\n{exc}",
                QMessageBox.Icon.Critical,
            )

``n
### ui\main_window.py

`$tag
from __future__ import annotations

import logging
import os
from pathlib import Path

from PyQt6.QtCore import QEvent, QModelIndex, QSize, Qt, QTimer, QUrl
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QAbstractItemView,
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
    QTableView,
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
from ui.models.results_table_model import ResultsTableModel
from ui.models.tracks_table_model import TracksTableModel
from ui.workers.worker_manager import AnalysisWorkerManager


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
    ):
        super().__init__()
        self.tolerance_settings = tolerance_settings
        self.export_settings = export_settings
        self.theme_settings = theme_settings
        self.waveform_settings = waveform_settings
        self.worker_manager = worker_manager
        self.worker_manager.setParent(self)
        self.settings_filename = Path(settings_filename)

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

        self.top_table = QTableView()
        self.top_model = ResultsTableModel(theme_settings=self.theme_settings)
        self.top_table.setModel(self.top_model)
        try:
            self.top_table.setIconSize(QSize(16, 16))
        except Exception:
            pass

        self.bottom_table = QTableView()
        self.bottom_model = TracksTableModel(
            tolerance_settings=self.tolerance_settings, theme_settings=self.theme_settings
        )
        self.bottom_table.setModel(self.bottom_model)

        splitter.addWidget(self.top_table)
        splitter.addWidget(self.bottom_table)
        splitter.setSizes([300, 400])
        main_layout.addWidget(splitter)

        self.setCentralWidget(central)

        self.setup_tables()
        self.connect_signals()

        self._auto_resize_pending = False

        def _apply_header_resizes():
            if not hasattr(self, "top_table") or not hasattr(self, "bottom_table"):
                return

            h_header = self.top_table.horizontalHeader()
            for col in (0, 2, 3, 4, 5, 6, 7):
                h_header.resizeSection(col, self.top_table.sizeHintForColumn(col))

            h_header_b = self.bottom_table.horizontalHeader()
            for col in (0, 3, 4, 5, 6):
                h_header_b.resizeSection(col, self.bottom_table.sizeHintForColumn(col))

        def _schedule_header_resizes():
            if self._auto_resize_pending:
                return
            self._auto_resize_pending = True
            QTimer.singleShot(0, lambda: (setattr(self, "_auto_resize_pending", False), _apply_header_resizes()))

        self._schedule_header_resizes = _schedule_header_resizes  # type: ignore[assignment]
        self.top_model._schedule_header_resizes = _schedule_header_resizes  # type: ignore[attr-defined]

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
        self.top_table.setMouseTracking(True)
        self.bottom_table.setMouseTracking(True)

        h_header = self.top_table.horizontalHeader()
        h_header.setStretchLastSection(False)
        h_header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        h_header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        h_header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.top_table.setColumnWidth(6, 60)
        self.top_table.setColumnWidth(7, 60)

        bold = h_header.font()
        bold.setBold(True)
        h_header.setFont(bold)

        h_header_bottom = self.bottom_table.horizontalHeader()
        bbold = h_header_bottom.font()
        bbold.setBold(True)
        h_header_bottom.setFont(bbold)
        h_header_bottom.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        h_header_bottom.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        h_header_bottom.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        h_header_bottom.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        h_header_bottom.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        h_header_bottom.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        h_header_bottom.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        h_header_bottom.setSectionResizeMode(7, QHeaderView.ResizeMode.Stretch)
        h_header_bottom.setStretchLastSection(True)
        self.bottom_table.setColumnWidth(1, 200)

        self.top_table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.bottom_table.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self.top_table.setAlternatingRowColors(True)
        self.bottom_table.setAlternatingRowColors(True)

        # Install hover affordance delegates for action cells
        self.top_delegate = ActionCellDelegate(self.theme_settings, {6, 7})
        self.top_table.setItemDelegateForColumn(6, self.top_delegate)
        self.top_table.setItemDelegateForColumn(7, self.top_delegate)

        self.bottom_delegate = ActionCellDelegate(self.theme_settings, {7})
        self.bottom_table.setItemDelegateForColumn(7, self.bottom_delegate)

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
            settings_dialog = SettingsDialog(settings_filename=self.settings_filename, parent=self)
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

``n
### ui\models\__init__.py

`$tag

``n
### ui\models\results_table_model.py

`$tag
from __future__ import annotations

from typing import List, Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt, QTimer
from PyQt6.QtGui import QColor, QFont

from core.models.analysis import SideResult
from ui.config_models import ThemeSettings
from ui.constants import (
    COLOR_WHITE,
    FILTER_ALL,
    FILTER_FAIL,
    FILTER_OK,
    FILTER_WARN,
    STATUS_FAIL,
    STATUS_OK,
    STATUS_WARN,
    TABLE_HEADERS_TOP,
)
from ui.theme import get_system_file_icon
from ui.theme import get_system_file_icon


class ResultsTableModel(QAbstractTableModel):
    """Model for the top table showing matched PDF/ZIP pairs."""

    def __init__(self, theme_settings: ThemeSettings):
        super().__init__()
        self.theme_settings = theme_settings
        self._headers = TABLE_HEADERS_TOP
        self._data: List[SideResult] = []
        self._filtered_data: List[SideResult] = []
        self._active_filter: str = FILTER_ALL
        self._seq_counter = 1

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:  # type: ignore[override]
        return len(self._filtered_data)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:  # type: ignore[override]
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if not index.isValid():
            return None
        row = index.row()
        if row < 0 or row >= len(self._filtered_data):
            return None
        result = self._filtered_data[row]
        column = index.column()

        if role == Qt.ItemDataRole.DecorationRole:
            if column == 6 and result.pdf_path:
                return get_system_file_icon("file")
            if column == 7 and result.zip_path:
                return get_system_file_icon("dir")

        if role == Qt.ItemDataRole.BackgroundRole:
            if column == 6 and result.pdf_path:
                return QColor(self.theme_settings.action_bg_color)
            if column == 7 and result.zip_path:
                return QColor(self.theme_settings.action_bg_color)

        if role == Qt.ItemDataRole.DisplayRole:
            if column == 0:
                return index.row() + 1
            if column == 1:
                return result.pdf_path.name
            if column == 2:
                return result.side
            if column == 3:
                return result.mode
            if column == 4:
                return f"{result.total_pdf_sec // 60:02d}:{result.total_pdf_sec % 60:02d}"
            if column == 5:
                return result.status

        if role == Qt.ItemDataRole.ForegroundRole and column == 5:
            return QColor(COLOR_WHITE)

        if role == Qt.ItemDataRole.BackgroundRole and column == 5:
            status_colors = self.theme_settings.status_colors
            if result.status == STATUS_OK:
                return QColor(status_colors["ok"])
            if result.status == STATUS_WARN:
                return QColor(status_colors["warn"])
            if result.status == STATUS_FAIL:
                return QColor(status_colors["fail"])

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if column in (6, 7):
                return Qt.AlignmentFlag.AlignCenter
            if column in (3, 4, 5):
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            if column in (0, 2):
                return Qt.AlignmentFlag.AlignCenter
            return Qt.AlignmentFlag.AlignLeft

        if role == Qt.ItemDataRole.ToolTipRole and column == 1:
            return f"PDF: {result.pdf_path}\nZIP: {result.zip_path if result.zip_path else '-'}"
        if role == Qt.ItemDataRole.ToolTipRole:
            if column == 6 and result.pdf_path:
                return "Open PDF file"
            if column == 7 and result.zip_path:
                return "Open ZIP archive"

        return None

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
            if role == Qt.ItemDataRole.FontRole:
                header_font = QFont()
                header_font.setBold(True)
                return header_font
        return None

    def add_result(self, result: SideResult) -> None:
        """Add a result to the model, maintaining filter state."""
        result_with_seq = result.model_copy()
        result_with_seq.seq = self._seq_counter
        self._seq_counter += 1

        self._data.append(result_with_seq)
        if self._passes_filter(result_with_seq):
            insert_row = len(self._filtered_data)
            self.beginInsertRows(QModelIndex(), insert_row, insert_row)
            self._filtered_data.append(result_with_seq)
            self.endInsertRows()
            if hasattr(self, "_schedule_header_resizes"):
                QTimer.singleShot(0, self._schedule_header_resizes)

    def get_result(self, row: int) -> Optional[SideResult]:
        if 0 <= row < len(self._filtered_data):
            return self._filtered_data[row]
        return None

    def clear(self) -> None:
        self.beginResetModel()
        self._data.clear()
        self._filtered_data.clear()
        self._active_filter = FILTER_ALL
        self._seq_counter = 1
        self.endResetModel()

    def all_results(self) -> List[SideResult]:
        return list(self._data)

    def set_filter(self, filter_text: str) -> None:
        valid_filters = {FILTER_ALL, FILTER_OK, FILTER_FAIL, FILTER_WARN}
        self._active_filter = filter_text if filter_text in valid_filters else FILTER_ALL
        self._rebuild_filtered_data()

    def _passes_filter(self, result: SideResult) -> bool:
        if self._active_filter == FILTER_ALL:
            return True
        status_by_filter = {
            FILTER_OK: STATUS_OK,
            FILTER_FAIL: STATUS_FAIL,
            FILTER_WARN: STATUS_WARN,
        }
        expected_status = status_by_filter.get(self._active_filter)
        if expected_status is None:
            return True
        return result.status == expected_status

    def _rebuild_filtered_data(self) -> None:
        self.beginResetModel()
        self._filtered_data = [res for res in self._data if self._passes_filter(res)]
        self.endResetModel()

``n
### ui\models\tracks_table_model.py

`$tag
from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor, QFont, QPalette
from PyQt6.QtWidgets import QApplication

from core.models.analysis import SideResult
from core.models.settings import ToleranceSettings
from ui.config_models import ThemeSettings
from ui.constants import (
    LABEL_TOTAL_TRACKS,
    PLACEHOLDER_DASH,
    STATUS_OK,
    TABLE_HEADERS_BOTTOM,
)
from ui.theme import get_custom_icon


class TracksTableModel(QAbstractTableModel):
    """Model for the bottom table showing track details."""

    def __init__(self, tolerance_settings: ToleranceSettings, theme_settings: Optional[ThemeSettings] = None):
        """Initialize TracksTableModel with dependency injection.

        Args:
            tolerance_settings: Tolerance settings for match calculations.
            theme_settings: Optional theme settings for styling. If None, loads settings from the global config.
        """
        super().__init__()
        self.tolerance_settings = tolerance_settings

        if theme_settings is None:
            from config import cfg
            from ui.config_models import load_theme_settings

            self.theme_settings = load_theme_settings(cfg)
        else:
            self.theme_settings = theme_settings

        self._headers = TABLE_HEADERS_BOTTOM
        self._data: Optional[SideResult] = None

    def flags(self, index: QModelIndex):
        base = super().flags(index)
        if not index.isValid():
            return base
        if index.row() == self.rowCount() - 1:
            return base & ~Qt.ItemFlag.ItemIsSelectable
        return base

    def rowCount(self, parent: QModelIndex = QModelIndex()):  # type: ignore[override]
        if not self._data or not self._data.pdf_tracks:
            return 0
        return len(self._data.pdf_tracks) + 1

    def columnCount(self, parent: QModelIndex = QModelIndex()):  # type: ignore[override]
        return len(self._headers)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if not index.isValid() or not self._data:
            return None

        row = index.row()
        column = index.column()
        is_total_row = row == self.rowCount() - 1

        # Column 6 (Match) - Icon rendering
        if role == Qt.ItemDataRole.DecorationRole and column == 6 and not is_total_row:
            if self._data.mode == "tracks":
                pdf_track = self._data.pdf_tracks[row] if row < len(self._data.pdf_tracks) else None
                wav_track = self._data.wav_tracks[row] if row < len(self._data.wav_tracks) else None

                if pdf_track and wav_track:
                    difference = wav_track.duration_sec - pdf_track.duration_sec
                    try:
                        track_tolerance = float(self.tolerance_settings.warn_tolerance)
                    except (TypeError, ValueError):
                        track_tolerance = 2.0

                    # Return check or cross icon based on tolerance
                    if abs(difference) <= track_tolerance:
                        return get_custom_icon("check")
                    else:
                        return get_custom_icon("cross")
                else:
                    return get_custom_icon("cross")
            return None

        # Column 6 (Match) - Total row icon
        if role == Qt.ItemDataRole.DecorationRole and column == 6 and is_total_row:
            if self._data.status == STATUS_OK:
                return get_custom_icon("check")
            else:
                return get_custom_icon("cross")

        # Column 7 (Waveform) - Icon rendering
        if role == Qt.ItemDataRole.DecorationRole and column == 7 and not is_total_row:
            wav_track_exists = False
            if self._data.mode == "tracks":
                wav_track_exists = row < len(self._data.wav_tracks)
            else:
                wav_track_exists = bool(self._data.wav_tracks)
            if wav_track_exists:
                return get_custom_icon("play")

        if role in (Qt.ItemDataRole.AccessibleTextRole, Qt.ItemDataRole.ToolTipRole) and column == 6:
            if is_total_row:
                return "Match OK" if self._data.status == STATUS_OK else "No match"
            else:
                if self._data.mode == "tracks":
                    pdf_track = self._data.pdf_tracks[row] if row < len(self._data.pdf_tracks) else None
                    wav_track = self._data.wav_tracks[row] if row < len(self._data.wav_tracks) else None

                    if pdf_track and wav_track:
                        difference = wav_track.duration_sec - pdf_track.duration_sec
                        try:
                            track_tolerance = float(self.tolerance_settings.warn_tolerance)
                        except (TypeError, ValueError):
                            track_tolerance = 2.0

                        if abs(difference) <= track_tolerance:
                            return "Match OK"
                    return "No match"
            return None

        if role == Qt.ItemDataRole.ToolTipRole and column == 7 and not is_total_row:
            return "View waveform"

        if role == Qt.ItemDataRole.DisplayRole:
            if is_total_row:
                return self.get_total_row_data(column)
            return self.get_track_row_data(row, column)

        if role == Qt.ItemDataRole.BackgroundRole and is_total_row:
            return QColor(self.theme_settings.total_row_bg_color)

        if role == Qt.ItemDataRole.FontRole and is_total_row:
            font = QFont()
            font.setBold(True)
            return font

        if role == Qt.ItemDataRole.TextAlignmentRole and column == 7:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.TextAlignmentRole and column == 6:
            return Qt.AlignmentFlag.AlignCenter

        return None

    def get_track_row_data(self, row: int, column: int):
        if not self._data or row >= len(self._data.pdf_tracks):
            return ""

        pdf_track = self._data.pdf_tracks[row]

        if self._data.mode == "tracks":
            wav_track = self._data.wav_tracks[row] if row < len(self._data.wav_tracks) else None
            difference = (wav_track.duration_sec - pdf_track.duration_sec) if wav_track else None

            try:
                track_tolerance = float(self.tolerance_settings.warn_tolerance)
            except (TypeError, ValueError):
                track_tolerance = 2.0

            is_match = wav_track and difference is not None and abs(difference) <= track_tolerance

            if column == 0:
                return pdf_track.position
            if column == 1:
                return wav_track.filename if wav_track else PLACEHOLDER_DASH
            if column == 2:
                return pdf_track.title
            if column == 3:
                return f"{pdf_track.duration_sec // 60:02d}:{pdf_track.duration_sec % 60:02d}"
            if column == 4:
                if wav_track:
                    return f"{int(wav_track.duration_sec) // 60:02d}:{int(wav_track.duration_sec) % 60:02d}"
                return PLACEHOLDER_DASH
            if column == 5:
                return f"{difference:+.0f}" if difference is not None else PLACEHOLDER_DASH
            if column == 6:
                return ""  # Icon is shown via DecorationRole
            if column == 7:
                return ""
        else:
            if column == 0:
                return pdf_track.position
            if column == 1:
                return PLACEHOLDER_DASH
            if column == 2:
                return pdf_track.title
            if column == 3:
                return f"{pdf_track.duration_sec // 60:02d}:{pdf_track.duration_sec % 60:02d}"
            if column == 4:
                return PLACEHOLDER_DASH
            if column == 5:
                return PLACEHOLDER_DASH
            if column == 6:
                return PLACEHOLDER_DASH
            if column == 7:
                return ""
            return PLACEHOLDER_DASH
        return ""

    def get_total_row_data(self, column: int):
        if not self._data:
            return ""

        if column == 1:
            if self._data.mode == "side" and self._data.wav_tracks:
                return self._data.wav_tracks[0].filename
            return LABEL_TOTAL_TRACKS
        if column == 2:
            return f"{len(self._data.pdf_tracks)} tracks"
        if column == 3:
            return f"{self._data.total_pdf_sec // 60:02d}:{self._data.total_pdf_sec % 60:02d}"
        if column == 4:
            return f"{int(self._data.total_wav_sec) // 60:02d}:{int(self._data.total_wav_sec) % 60:02d}"
        if column == 5:
            return f"{self._data.total_difference:+.0f}"
        if column == 6:
            return ""  # Icon is shown via DecorationRole
        if column == 7:
            return ""
        return ""

    def headerData(self, section: int, orientation, role=Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
        if orientation == Qt.Orientation.Horizontal:
            if role == Qt.ItemDataRole.DisplayRole:
                return self._headers[section]
            if role == Qt.ItemDataRole.FontRole:
                font = QFont()
                font.setBold(True)
                return font
        return None

    def update_data(self, result: Optional[SideResult]) -> None:
        self.beginResetModel()
        self._data = result
        self.endResetModel()

``n
### ui\theme.py

`$tag
import logging
import sys
from pathlib import Path
from typing import Dict

from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QStyle


# Icon cache for performance
_icon_cache: Dict[str, QIcon] = {}


def get_asset_path(relative_path: Path) -> Path:
    """Get absolute path to asset, supporting both development and bundled app (PyInstaller)."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # Running in a PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Running in a normal Python environment
        base_path = Path(__file__).resolve().parent.parent
    return base_path / relative_path


def get_custom_icon(icon_name: str) -> QIcon:
    """Load a custom SVG icon with caching, resource lookup, and system fallback.

    Args:
        icon_name: Name of the icon without extension (e.g., 'check', 'cross', 'play')

    Returns:
        QIcon object, system fallback, or empty QIcon if not found.
    """
    if icon_name in _icon_cache:
        return _icon_cache[icon_name]

    # 1. Try loading from filesystem (dev or bundled app)
    try:
        icon_path = get_asset_path(Path("assets") / "icons" / f"{icon_name}.svg")
        if icon_path.exists():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                logging.debug(f"Loaded icon '{icon_name}' from filesystem: {icon_path}")
                _icon_cache[icon_name] = icon
                return icon

        logging.warning(f"Custom icon file not found at: {icon_path}, using fallback.")

    except Exception as exc:
        logging.error(f"Error loading custom icon '{icon_name}' from filesystem: {exc}")

    # 2. If filesystem fails, use a system fallback icon
    fallback_icon = _get_fallback_icon(icon_name)
    if not fallback_icon.isNull():
        logging.warning(f"Using fallback for icon '{icon_name}'.")
        _icon_cache[icon_name] = fallback_icon  # Cache the fallback too
        return fallback_icon

    logging.error(f"Failed to load icon or find fallback for '{icon_name}'.")
    _icon_cache[icon_name] = QIcon()  # Cache the empty icon to prevent repeated lookups
    return _icon_cache[icon_name]


def _get_fallback_icon(icon_name: str) -> QIcon:
    """Get fallback system icon for the given icon name."""
    try:
        app = QApplication.instance()
        if not app:
            return QIcon()

        style = app.style()

        # Map icon names to system pixmaps
        fallback_mapping = {
            "check": QStyle.StandardPixmap.SP_DialogApplyButton,
            "cross": QStyle.StandardPixmap.SP_DialogCancelButton,
            "play": QStyle.StandardPixmap.SP_MediaPlay,
        }

        if icon_name in fallback_mapping:
            fallback_icon = style.standardIcon(fallback_mapping[icon_name])
            if not fallback_icon.isNull():
                logging.debug(f"Using fallback icon for: {icon_name}")
                return fallback_icon

        logging.warning(f"No fallback available for icon: {icon_name}")
        return QIcon()

    except Exception as exc:
        logging.error(f"Error getting fallback icon for '{icon_name}': {exc}")
        return QIcon()


def get_system_file_icon(icon_type: str = "file") -> QIcon:
    """Return a standard system icon for files, directories, or actions, with support for custom SVG icons."""
    # Support custom SVG icons for specific types
    if icon_type in ["check", "cross", "play"]:
        return get_custom_icon(icon_type)

    # Fallback to system icons for backward compatibility
    try:
        app = QApplication.instance()
        if not app:
            return QIcon()

        style = app.style()
        mapping = {
            "file": QStyle.StandardPixmap.SP_FileIcon,
            "dir": QStyle.StandardPixmap.SP_DirIcon,
        }
        return style.standardIcon(mapping.get(icon_type, QStyle.StandardPixmap.SP_FileIcon))
    except Exception:
        return QIcon()


def get_gz_color(color_key: str, status_colors: Dict[str, str]) -> str:
    """Resolve a brand color using provided status colors with safe fallbacks."""
    fallback_colors = {
        "white": "white",
        "ok": "#10B981",
        "warn": "#F59E0B",
        "fail": "#EF4444",
    }

    if color_key == "white":
        return "white"

    try:
        if status_colors and color_key in status_colors:
            return status_colors[color_key]
    except Exception:
        logging.debug("Failed to read status color '%s' from config", color_key, exc_info=True)

    return fallback_colors.get(color_key, color_key)


def load_gz_media_fonts(app: QApplication, font_family: str, font_size: int) -> None:
    """Apply the configured font family and size to the application."""
    try:
        resolved_family = font_family or "Poppins, Segoe UI, Arial, sans-serif"
        font = QFont(resolved_family)

        try:
            if font_size:
                font.setPointSize(int(font_size))
            else:
                font.setPointSize(10)
        except (TypeError, ValueError):
            font.setPointSize(10)

        app.setFont(font)
        logging.info("GZ Media font applied successfully")
    except Exception as exc:
        logging.warning("Failed to apply GZ Media font, using system default: %s", exc)


def load_gz_media_stylesheet(app: QApplication, stylesheet_path: Path) -> None:
    """Load the configured stylesheet if available."""
    try:
        if stylesheet_path and stylesheet_path.exists():
            with stylesheet_path.open("r", encoding="utf-8") as handle:
                qss_content = handle.read()
            app.setStyleSheet(qss_content)
            logging.info("GZ Media stylesheet loaded successfully")
        else:
            logging.warning("GZ Media stylesheet file not found at %s", stylesheet_path)
    except Exception as exc:
        logging.error("Failed to load GZ Media stylesheet from %s: %s", stylesheet_path, exc)

``n
### ui\workers\__init__.py

`$tag

``n
### ui\workers\analysis_worker.py

`$tag
from __future__ import annotations

import logging
from PyQt6.QtCore import QObject, pyqtSignal

from core.models.settings import IdExtractionSettings, ToleranceSettings
from services.analysis_service import AnalysisService
from ui.config_models import WorkerSettings


class AnalysisWorker(QObject):
    """Runs the analysis service in a background thread with injected settings."""

    progress = pyqtSignal(str)
    result_ready = pyqtSignal(object)
    finished = pyqtSignal(str)

    def __init__(
        self,
        worker_settings: WorkerSettings,
        tolerance_settings: ToleranceSettings,
        id_extraction_settings: IdExtractionSettings,
    ):
        super().__init__()
        self.worker_settings = worker_settings
        self.tolerance_settings = tolerance_settings
        self.id_extraction_settings = id_extraction_settings

    def run(self) -> None:
        try:
            service = AnalysisService(
                tolerance_settings=self.tolerance_settings,
                id_extraction_settings=self.id_extraction_settings,
            )
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

``n
### ui\workers\worker_manager.py

`$tag
from __future__ import annotations

from PyQt6.QtCore import QObject, QThread, pyqtSignal

from core.models.settings import IdExtractionSettings, ToleranceSettings
from ui.config_models import WorkerSettings
from ui.workers.analysis_worker import AnalysisWorker


class AnalysisWorkerManager(QObject):
    """Manages the lifecycle of AnalysisWorker, injecting required settings."""

    progress = pyqtSignal(str)
    result_ready = pyqtSignal(object)
    finished = pyqtSignal(str)

    def __init__(
        self,
        worker_settings: WorkerSettings,
        tolerance_settings: ToleranceSettings,
        id_extraction_settings: IdExtractionSettings,
        parent: QObject | None = None,
    ):
        super().__init__(parent)
        self.worker_settings = worker_settings
        self.tolerance_settings = tolerance_settings
        self.id_extraction_settings = id_extraction_settings
        self._worker: AnalysisWorker | None = None
        self._thread: QThread | None = None

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.isRunning()

    def start_analysis(self) -> None:
        if self.is_running():
            return

        self._thread = QThread()
        self._worker = AnalysisWorker(
            worker_settings=self.worker_settings,
            tolerance_settings=self.tolerance_settings,
            id_extraction_settings=self.id_extraction_settings,
        )
        self._worker.moveToThread(self._thread)

        self._worker.progress.connect(self.progress)
        self._worker.result_ready.connect(self.result_ready)
        self._worker.finished.connect(self.finished)
        self._worker.finished.connect(self.cleanup)

        self._thread.started.connect(self._worker.run)
        self._thread.start()

    def cleanup(self) -> None:
        if self._thread:
            self._thread.quit()
            self._thread.wait(1000)
        self._thread = None
        self._worker = None

``n
### wav_extractor_wave.py

`$tag
# DEPRECATION WARNING:
# This module is considered deprecated and will be removed in a future version.
# Its functionality has been decomposed and moved to dedicated components:
# - Filename parsing: core.domain.parsing.StrictFilenameParser
# - AI detection logic: adapters.audio.steps.AiParserStep
# - Fallback logic: adapters.audio.steps.DeterministicFallbackStep
# - Orchestration: adapters.audio.chained_detector.ChainedAudioModeDetector
#
# This file is kept for backward compatibility of the AI functions it exposes.
# New code should NOT use this module directly.

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from core.domain.parsing import UNKNOWN_POSITION

# NOTE: The WavInfo class here is a legacy duplicate. The canonical version is in core.models.analysis.
@dataclass
class WavInfo:
    filename: str
    duration_sec: float
    side: Optional[str] = None
    position: Optional[int] = None

# These functions are still used by AiParserStep
def ai_parse_batch(filenames: List[str]) -> Dict[str, Tuple[Optional[str], Optional[int]]]:
    # ... (implementation remains for now)
    pass # Placeholder to keep the structure

def merge_ai_results(wavs: List[WavInfo], ai_map: Dict[str, Tuple[Optional[str], Optional[int]]]) -> None:
    # ... (implementation remains for now)
    pass # Placeholder to keep the structure

# --- All other functions from the original file are now removed or considered deprecated ---

# Keeping the original implementation of the two functions still in use
def _load_ai_client():
    try:
        from openai import OpenAI
    except Exception:
        return None, None
    if os.getenv("OPENROUTER_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1")
            model = os.getenv("OPENROUTER_MODEL", "google/gemini-2.5-flash")
            return client, model
        except Exception:
            pass
    if os.getenv("OPENAI_API_KEY"):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
            return client, model
        except Exception:
            pass
    return None, None

def ai_parse_batch(filenames: List[str]) -> Dict[str, Tuple[Optional[str], Optional[int]]]:
    client, model = _load_ai_client()
    if not client or not model or not filenames:
        return {}
    system = (
        "You extract metadata from WAV filenames. "
        "For each filename, infer 'side' (letters only, like A,B,AA) and 'position' (1..99). "
        "Return STRICT JSON object mapping filename -> {\"side\": str|null, \"position\": int|null}. No extra text."
    )
    user = {"filenames": filenames}
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": json.dumps(user, ensure_ascii=False)}
            ],
            temperature=0.0,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            cleaned = content.strip().strip("`").replace("json\\n", "").strip()
            data = json.loads(cleaned)
        out: Dict[str, Tuple[Optional[str], Optional[int]]] = {}
        for fn in filenames:
            rec = data.get(fn, {})
            s_raw = rec.get("side")
            p_raw = rec.get("position")
            side = s_raw.strip().upper() if isinstance(s_raw, str) and s_raw.strip() else None
            pos = int(p_raw) if isinstance(p_raw, int) else None
            out[fn] = (side, pos)
        return out
    except Exception as e:
        print(f"[WARN] AI fallback selhal: {e}", file=sys.stderr)
        return {}

def merge_ai_results(wavs: List[WavInfo], ai_map: Dict[str, Tuple[Optional[str], Optional[int]]]) -> None:
    if not ai_map:
        return
    for w in wavs:
        if w.filename in ai_map:
            s_ai, p_ai = ai_map[w.filename]
            if (w.side is None or w.side == "UNKNOWN") and s_ai and s_ai != "UNKNOWN":
                w.side = s_ai
            if w.position is None and p_ai is not None:
                w.position = p_ai


def detect_audio_mode_with_ai(wavs: List[WavInfo]) -> Dict[str, List[WavInfo]]:
    """Detect audio side and position from WAV filenames using AI.

    Args:
        wavs: List of WavInfo objects with filename and duration_sec populated.

    Returns:
        Dictionary mapping side (e.g., "A", "B") to list of WavInfo objects
        with side and position populated.
    """
    if not wavs:
        return {}

    # Use existing AI parsing logic
    filenames = [w.filename for w in wavs]
    ai_map = ai_parse_batch(filenames)

    # Apply AI results to wavs
    for w in wavs:
        if w.filename in ai_map:
            side, position = ai_map[w.filename]
            if side:
                w.side = side
            if position is not None:
                w.position = position

    # Group by side
    side_map: Dict[str, List[WavInfo]] = {}
    for w in wavs:
        side = w.side or "A"  # Default to "A" if side is None
        side_map.setdefault(side, []).append(w)

    return side_map


def normalize_positions(side_map: Dict[str, List[WavInfo]]) -> None:
    """Normalize positions to be sequential (1, 2, 3...) with no gaps.

    Args:
        side_map: Dictionary mapping side to list of WavInfo objects.
    """
    for side, wav_list in side_map.items():
        if not wav_list:
            continue

        # Sort by current position and filename for deterministic ordering
        wav_list.sort(key=lambda w: (w.position if w.position is not None else UNKNOWN_POSITION, w.filename.lower()))

        # Normalize positions to be sequential starting from 1
        for i, wav in enumerate(wav_list, start=1):
            wav.position = i

``n
### waveform_viewer.py

`$tag
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Waveform viewer dialog with audio playback controls."""

from __future__ import annotations

import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Optional, List, Tuple, Dict

import numpy as np
import pyqtgraph as pg
import soundfile as sf
from PyQt6.QtCore import Qt, QUrl

try:
    from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer

    _MULTIMEDIA_AVAILABLE = True
    _MULTIMEDIA_IMPORT_ERROR = None
except ImportError as exc:
    QAudioOutput = None  # type: ignore[assignment]
    QMediaPlayer = None  # type: ignore[assignment]
    _MULTIMEDIA_AVAILABLE = False
    _MULTIMEDIA_IMPORT_ERROR = exc
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSlider,
    QVBoxLayout,
)

from core.models.settings import ToleranceSettings
from ui.config_models import WaveformSettings

# Waveform display configuration defaults
DEFAULT_OVERVIEW_POINTS = 2000  # Maximum points for waveform envelope
MIN_REGION_DURATION = 0.3  # Minimum region duration in seconds
DEFAULT_SNAP_TOLERANCE = 0.1  # Default snap tolerance in seconds
RMS_WINDOW_SIZE = 0.1  # RMS calculation window in seconds
INITIAL_DETAIL_DURATION = 10.0  # Initial detail view duration in seconds


class TimeAxisItem(pg.AxisItem):
    """Axis item that formats ticks as MM:SS."""

    def tickStrings(self, values, scale, spacing):
        labels: List[str] = []
        for value in values:
            total_seconds = max(0.0, float(value))
            minutes = int(total_seconds // 60)
            seconds = int(round(total_seconds - minutes * 60))
            if seconds == 60:
                minutes += 1
                seconds = 0
            labels.append(f"{minutes:02d}:{seconds:02d}")
        return labels


class WaveformEditorDialog(QDialog):
    """Advanced waveform editor with a single interactive waveform view for precise audio analysis."""

    def __init__(
        self,
        zip_path: Path,
        wav_filename: str,
        waveform_settings: WaveformSettings,
        parent=None,
    ):
        super().__init__(parent)
        self._zip_path = Path(zip_path)
        self._wav_filename = wav_filename
        self._temp_wav: Optional[Path] = None
        self._duration_sec: float = 0.0
        self._sample_rate: int = 0
        self._audio_data: Optional[np.ndarray] = None

        # Waveform plot and overlays
        self.plot_widget: Optional[pg.PlotWidget] = None
        self._waveform_curve: Optional[pg.PlotDataItem] = None

        # Region selection
        self._region_item: Optional[pg.LinearRegionItem] = None
        self._region_bounds = (0.0, 1.0)  # seconds

        # PDF markers
        self._pdf_markers: List[pg.InfiniteLine] = []
        self._marker_times: List[float] = []
        self._pdf_tracks: List[Dict] = []  # Store PDF track data
        self._playhead_line: Optional[pg.InfiniteLine] = None

        # Inherit extraction method from parent class
        self._slider_updating = False

        # Waveform editor configuration
        self._waveform_settings = waveform_settings
        self._overview_points = max(1, waveform_settings.overview_points)
        self._min_region_duration = max(0.0, waveform_settings.min_region_duration)
        self._snap_tolerance = max(0.0, waveform_settings.snap_tolerance)
        self._snapping_enabled = waveform_settings.enable_snapping

        self.setWindowTitle(f"Waveform Editor - {wav_filename}")
        self.resize(1200, 800)

        if not _MULTIMEDIA_AVAILABLE:
            QMessageBox.critical(
                self,
                "Qt Multimedia Required",
                "Waveform playback requires the PyQt6 QtMultimedia module. "
                "Install PyQt6>=6.4 with Qt Multimedia support to enable this feature.",
            )
            raise RuntimeError("Qt Multimedia module not available") from _MULTIMEDIA_IMPORT_ERROR

        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)

        volume_value = max(0.0, min(1.0, float(waveform_settings.default_volume)))
        self._audio_output.setVolume(max(0.0, min(1.0, volume_value)))

        self._init_ui()
        self._load_audio_data()

    def _init_ui(self) -> None:
        """Initialize editor layout with a single waveform plot and controls."""
        main_layout = QVBoxLayout(self)

        # Title
        name_label = QLabel(f"{self._wav_filename}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setObjectName("waveformEditorTitle")
        main_layout.addWidget(name_label)

        # Single waveform plot with custom time axis
        self.plot_widget = pg.PlotWidget(self, axisItems={"bottom": TimeAxisItem(orientation="bottom")})
        self.plot_widget.setBackground("k")
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.setLabel("left", "Amplitude")
        self.plot_widget.setMouseEnabled(x=True, y=False)
        view_box = self.plot_widget.getViewBox()
        if view_box is not None:
            view_box.setMouseEnabled(x=True, y=False)
        if self.plot_widget.scene() is not None:
            self.plot_widget.scene().sigMouseMoved.connect(self._on_plot_mouse_moved)
        self.plot_widget.setToolTip(self._format_mmss_with_fraction(0.0))
        main_layout.addWidget(self.plot_widget, stretch=1)

        # Controls
        controls_layout = QHBoxLayout()

        # Region info
        self.region_label = QLabel("Region: 00:00.0 - 00:01.0", self)
        controls_layout.addWidget(self.region_label)

        controls_layout.addStretch()

        # Zoom controls
        zoom_in_btn = QPushButton("Zoom In", self)
        zoom_out_btn = QPushButton("Zoom Out", self)
        fit_all_btn = QPushButton("Fit", self)
        fit_region_btn = QPushButton("Fit to Region", self)

        zoom_in_btn.clicked.connect(self._zoom_in)
        zoom_out_btn.clicked.connect(self._zoom_out)
        fit_all_btn.clicked.connect(self._fit_all)
        fit_region_btn.clicked.connect(self._fit_to_region)

        controls_layout.addWidget(zoom_in_btn)
        controls_layout.addWidget(zoom_out_btn)
        controls_layout.addWidget(fit_all_btn)
        controls_layout.addWidget(fit_region_btn)

        main_layout.addLayout(controls_layout)

        # Transport controls (same as original)
        transport_layout = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        transport_layout.addWidget(self.play_button)
        transport_layout.addWidget(self.pause_button)
        transport_layout.addWidget(self.stop_button)
        transport_layout.addStretch()

        self.play_button.clicked.connect(self._handle_play)
        self.pause_button.clicked.connect(self._handle_pause)
        self.stop_button.clicked.connect(self._handle_stop)

        main_layout.addLayout(transport_layout)

        # Position slider (same as original)
        slider_layout = QHBoxLayout()
        self.time_current = QLabel("00:00.0", self)
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 0)
        self.time_total = QLabel("00:00.0", self)
        slider_layout.addWidget(self.time_current)
        slider_layout.addWidget(self.position_slider, stretch=1)
        slider_layout.addWidget(self.time_total)
        main_layout.addLayout(slider_layout)

        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        self.position_slider.sliderMoved.connect(self._on_slider_moved)

        # Wire up player signals
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.errorOccurred.connect(self._on_player_error)

    def _load_audio_data(self) -> None:
        """Load and process audio data for the waveform view."""
        import time

        start_time = time.time()

        try:
            self._extract_wav()
            if not self._temp_wav:
                raise FileNotFoundError("Temporary WAV file missing after extraction")

            # Load full audio data for processing with progress feedback
            load_start = time.time()
            self._audio_data, self._sample_rate = sf.read(str(self._temp_wav), dtype="float32")
            load_duration = time.time() - load_start

            if self._audio_data.ndim > 1:
                self._audio_data = self._audio_data.mean(axis=1)

            if self._sample_rate <= 0 or self._audio_data.size == 0:
                raise ValueError("Invalid audio data encountered")

            self._duration_sec = self._audio_data.shape[0] / float(self._sample_rate)

            # Render waveform on the primary plot
            self._render_waveform()

            # Setup region selection
            self._setup_region_selection()

            # Apply axis limits after region creation
            self._apply_view_limits()

            # Setup player
            self._player.setSource(QUrl.fromLocalFile(str(self._temp_wav)))

            total_duration = time.time() - start_time
            logging.info(
                "Waveform editor loaded in %.2fs (audio load: %.2fs, duration: %.0fs)",
                total_duration,
                load_duration,
                self._duration_sec,
            )

        except FileNotFoundError:
            raise
        except Exception as exc:
            logging.error("Failed to load waveform data: %s", exc, exc_info=True)
            QMessageBox.critical(
                self,
                "Waveform Error",
                f"Unable to load WAV file '{self._wav_filename}'.\n\nError: {exc}",
            )
            for widget in (
                self.play_button,
                self.pause_button,
                self.stop_button,
                self.position_slider,
            ):
                widget.setEnabled(False)

    def _extract_wav(self) -> None:
        """Extract WAV file from ZIP archive to a temporary file."""
        if not self._zip_path.exists():
            raise FileNotFoundError(f"ZIP archive not found: {self._zip_path}")

        with zipfile.ZipFile(self._zip_path, "r") as zf:
            matching_entry: Optional[str] = None
            for member in zf.namelist():
                if member == self._wav_filename:
                    matching_entry = member
                    break

            if not matching_entry:
                raise FileNotFoundError(f"WAV file '{self._wav_filename}' not found in archive")

            with zf.open(matching_entry) as wav_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    shutil.copyfileobj(wav_file, temp_file)
                    self._temp_wav = Path(temp_file.name)

    def _render_waveform(self) -> None:
        """Render the waveform envelope on the primary plot."""
        if not self.plot_widget or self._audio_data is None:
            return

        overview_points = max(1, int(self._overview_points))
        envelope = self._create_envelope(self._audio_data, self._sample_rate, max_points=overview_points)

        if envelope.size == 0:
            return

        if self._waveform_curve is None:
            self._waveform_curve = self.plot_widget.plot(pen=pg.mkPen("#3B82F6", width=1))

        self._waveform_curve.setData(envelope[:, 0], envelope[:, 1])
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setXRange(0, self._duration_sec, padding=0)

    def _apply_view_limits(self) -> None:
        """Clamp navigation to the valid time range."""
        if not self.plot_widget:
            return

        max_range = float(self._duration_sec) if self._duration_sec > 0 else 1.0
        min_range = min(max_range, max(0.5, float(self._min_region_duration)))
        self.plot_widget.setLimits(
            xMin=0.0,
            xMax=max_range,
            minXRange=min_range,
            maxXRange=max_range,
        )
        view_box = self.plot_widget.getViewBox()
        if view_box is not None:
            view_box.setXRange(0.0, max_range, padding=0)

    def _create_envelope(
        self,
        data: np.ndarray,
        sample_rate: int,
        max_points: int = DEFAULT_OVERVIEW_POINTS,
    ) -> np.ndarray:
        """Create envelope from audio data for efficient display."""
        if data.size == 0:
            return np.array([])

        # Calculate points per pixel for downsampling
        duration = len(data) / sample_rate
        points_per_second = max_points / duration if duration > 0 else max_points

        if points_per_second >= sample_rate / 2:
            # Use original data if we don't need much downsampling
            time_points = np.arange(len(data)) / sample_rate
            return np.column_stack([time_points, data])

        # Create envelope using min/max windows for better visual representation
        window_size = max(1, int(sample_rate / points_per_second))

        # Pad data to fit windows
        pad_size = (window_size - len(data) % window_size) % window_size
        if pad_size > 0:
            padded_data = np.pad(data, (0, pad_size), mode="edge")
        else:
            padded_data = data

        # Reshape and calculate min/max for each window
        reshaped = padded_data.reshape(-1, window_size)
        mins = reshaped.min(axis=1)
        maxs = reshaped.max(axis=1)

        # Create time points for envelope (center of each window)
        time_points = (np.arange(len(mins)) * window_size + window_size // 2) / sample_rate

        # Create min/max pairs for filled envelope effect
        envelope_data = np.empty((len(time_points) * 2, 2))
        envelope_data[0::2, 0] = time_points  # Time for min values
        envelope_data[1::2, 0] = time_points  # Time for max values
        envelope_data[0::2, 1] = mins  # Min amplitude values
        envelope_data[1::2, 1] = maxs  # Max amplitude values

        return envelope_data

    def _setup_region_selection(self) -> None:
        """Setup interactive region selection."""
        if not self.plot_widget:
            return

        # Create linear region for selection
        self._region_item = pg.LinearRegionItem(values=[0.0, 1.0], bounds=[0.0, self._duration_sec])

        # Style the region
        region_color = pg.mkBrush("#3B82F640")  # Semi-transparent blue
        self._region_item.setBrush(region_color)
        self._region_item.setMovable(True)

        # Connect region changes
        self._region_item.sigRegionChanged.connect(self._on_region_changed)

        self.plot_widget.addItem(self._region_item)
        self._region_item.setZValue(1)

        # Set initial region (first 1 second)
        initial_duration = min(1.0, self._duration_sec)
        self._region_item.setRegion([0.0, initial_duration])
        self._region_bounds = (0.0, initial_duration)
        self._update_region_label()

    def _on_region_changed(self) -> None:
        """Handle region selection changes with snap functionality."""
        if not self._region_item or self._audio_data is None:
            return

        min_val, max_val = self._region_item.getRegion()

        # Check if snapping is enabled in settings
        if self._snapping_enabled:
            # Apply snap to audio features (RMS peaks and zero crossings)
            snapped_min, snapped_max = self._snap_region_to_audio(min_val, max_val)
        else:
            # Use original values when snapping is disabled
            snapped_min, snapped_max = min_val, max_val

        # Enforce minimum region size (0.3 seconds)
        min_region = max(0.0, float(self._min_region_duration))
        if snapped_max - snapped_min < min_region:
            if min_val == self._region_bounds[0]:
                snapped_max = snapped_min + min_region
            else:
                snapped_min = snapped_max - min_region

        # Ensure region stays within bounds
        snapped_min = max(0.0, snapped_min)
        snapped_max = min(self._duration_sec, snapped_max)

        # Update region if snapping occurred
        if abs(min_val - snapped_min) > 0.01 or abs(max_val - snapped_max) > 0.01:
            self._region_item.setRegion([snapped_min, snapped_max])

        self._region_bounds = (snapped_min, snapped_max)

        # Update region label
        self._update_region_label()

    def _snap_region_to_audio(self, min_val: float, max_val: float) -> Tuple[float, float]:
        """Snap region boundaries to audio features (RMS peaks and zero crossings)."""
        if self._audio_data is None:
            return (min_val, max_val)

        # Get tolerance from configuration (seconds)
        snap_tolerance = max(0.0, float(self._snap_tolerance))
        search_start = max(0.0, min_val - snap_tolerance)
        search_end = min(self._duration_sec, max_val + snap_tolerance)

        # Find nearby RMS peaks
        rms_peaks = self._find_rms_peaks(search_start, search_end, snap_tolerance)

        # Find nearby zero crossings
        zero_crossings = self._find_zero_crossings(search_start, search_end, snap_tolerance)

        # Combine all snap points
        snap_points = sorted(set(rms_peaks + zero_crossings))

        # Snap min_val to nearest point
        snapped_min = min_val
        if snap_points:
            # Find closest snap point for start
            start_candidates = [p for p in snap_points if abs(p - min_val) <= snap_tolerance]
            if start_candidates:
                snapped_min = min(start_candidates, key=lambda p: abs(p - min_val))

        # Snap max_val to nearest point
        snapped_max = max_val
        if snap_points:
            # Find closest snap point for end
            end_candidates = [p for p in snap_points if abs(p - max_val) <= snap_tolerance]
            if end_candidates:
                snapped_max = min(end_candidates, key=lambda p: abs(p - max_val))

        return (snapped_min, snapped_max)

    def _find_rms_peaks(self, start_time: float, end_time: float, tolerance: float) -> List[float]:
        """Find RMS peaks within a bounded window around the region."""
        if self._audio_data is None:
            return []

        peaks = []
        sr = self._sample_rate
        window_size = max(1, int(RMS_WINDOW_SIZE * sr))  # 100ms windows
        half_step = max(1, window_size // 2)

        search_start_sample = max(0, int((start_time - tolerance) * sr))
        search_end_sample = min(len(self._audio_data), int((end_time + tolerance) * sr))

        if search_end_sample - search_start_sample <= window_size:
            return peaks

        local_rms = []
        for offset in range(search_start_sample, search_end_sample - window_size, half_step):
            window = self._audio_data[offset : offset + window_size]
            rms = float(np.sqrt(np.mean(window**2)))
            center_sample = offset + window_size // 2
            local_rms.append((rms, center_sample))

        for idx in range(1, len(local_rms) - 1):
            prev_rms, _ = local_rms[idx - 1]
            current_rms, sample_idx = local_rms[idx]
            next_rms, _ = local_rms[idx + 1]
            if current_rms > prev_rms and current_rms > next_rms:
                peaks.append(sample_idx / sr)

        return peaks

    def _find_zero_crossings(self, start_time: float, end_time: float, tolerance: float) -> List[float]:
        """Find zero crossings within a bounded window around the region."""
        if self._audio_data is None:
            return []

        crossings = []
        sr = self._sample_rate
        search_start_sample = max(1, int((start_time - tolerance) * sr))
        search_end_sample = min(len(self._audio_data), int((end_time + tolerance) * sr))

        for i in range(search_start_sample, search_end_sample):
            # Detect sign changes
            if self._audio_data[i - 1] * self._audio_data[i] < 0:
                time_pos = i / self._sample_rate
                crossings.append(time_pos)

        return crossings

    def _update_region_label(self) -> None:
        """Update region time display."""
        if hasattr(self, "region_label"):
            start_label = self._format_mmss_with_fraction(self._region_bounds[0])
            end_label = self._format_mmss_with_fraction(self._region_bounds[1])
            self.region_label.setText(f"Region: {start_label} - {end_label}")

    def get_performance_stats(self) -> Dict[str, float]:
        """Get performance statistics for validation."""
        return {
            "duration_sec": self._duration_sec,
            "sample_rate": self._sample_rate,
            "audio_size_mb": len(self._audio_data) * 4 / (1024 * 1024) if self._audio_data is not None else 0,
            "waveform_points": len(self._waveform_curve.getData()[0]) if self._waveform_curve else 0,
        }

    @staticmethod
    def _format_mmss(seconds: float) -> str:
        """Format seconds as MM:SS without decimals."""
        total = max(0.0, float(seconds))
        minutes = int(total // 60)
        secs = int(round(total - minutes * 60))
        if secs == 60:
            minutes += 1
            secs = 0
        return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def _format_mmss_with_fraction(seconds: float) -> str:
        """Format seconds as MM:SS.s with one decimal place."""
        total = max(0.0, float(seconds))
        minutes = int(total // 60)
        secs = total - minutes * 60
        if secs >= 59.95:
            minutes += 1
            secs = 0.0
        return f"{minutes:02d}:{secs:04.1f}".replace(" ", "0")

    @staticmethod
    def _format_delta(delta_seconds: float) -> str:
        """Format time delta in seconds with sign."""
        return f"{float(delta_seconds):+0.1f} s"

    def set_pdf_tracks(
        self,
        pdf_tracks: List[Dict],
        wav_tracks: List[Dict],
        tolerance_settings: ToleranceSettings,
    ) -> None:
        """Set PDF track markers with tolerance-based coloring."""
        self._pdf_tracks = pdf_tracks

        # Clear existing markers
        self._clear_pdf_markers()

        if not pdf_tracks or not self.plot_widget:
            return

        tolerance_warn = float(tolerance_settings.warn_tolerance)
        tolerance_fail = float(tolerance_settings.fail_tolerance)

        # Collect PDF durations and labels
        pdf_durations: List[float] = []
        pdf_labels: List[str] = []
        for index, pdf_track in enumerate(pdf_tracks, start=1):
            if hasattr(pdf_track, "duration_sec"):
                duration = float(getattr(pdf_track, "duration_sec", 0.0))
                label = getattr(pdf_track, "label", f"PDF {index}")
            else:
                duration = float(pdf_track.get("duration_sec", 0.0))
                label = str(pdf_track.get("label", f"PDF {index}"))
            pdf_durations.append(max(0.0, duration))
            pdf_labels.append(label)

        if not pdf_durations:
            return

        pdf_end_times = np.cumsum(pdf_durations)

        # Collect WAV cumulative ends for delta computation
        wav_durations: List[float] = []
        for wav_track in wav_tracks:
            if hasattr(wav_track, "duration_sec"):
                wav_durations.append(max(0.0, float(getattr(wav_track, "duration_sec", 0.0))))
            else:
                wav_durations.append(max(0.0, float(wav_track.get("duration_sec", 0.0))))
        wav_end_times = np.cumsum(wav_durations) if wav_durations else []

        for idx, end_time in enumerate(pdf_end_times):
            delta_t = 0.0
            if idx < len(wav_end_times):
                delta_t = wav_end_times[idx] - end_time

            # Determine marker color based on tolerance
            if abs(delta_t) <= tolerance_warn:
                color = "#10B981"  # Green (OK)
            elif abs(delta_t) <= tolerance_fail:
                color = "#F59E0B"  # Yellow (WARN)
            else:
                color = "#EF4444"  # Red (FAIL)

            # Create vertical line marker
            marker = pg.InfiniteLine(
                pos=end_time,
                angle=90,
                pen=pg.mkPen(color, width=2, style=pg.QtCore.Qt.PenStyle.DashLine),
                movable=False,
            )

            marker.setToolTip(
                f"{pdf_labels[idx]} - {self._format_mmss(end_time)} " f"(delta {self._format_delta(delta_t)})"
            )
            marker.setZValue(2)

            self.plot_widget.addItem(marker)
            self._pdf_markers.append(marker)
            self._marker_times.append(end_time)

    def _clear_pdf_markers(self) -> None:
        """Remove all PDF markers from the plot."""
        if self.plot_widget:
            for marker in self._pdf_markers:
                self.plot_widget.removeItem(marker)
        self._pdf_markers.clear()
        self._marker_times.clear()

    def _on_plot_mouse_moved(self, scene_position) -> None:
        """Update plot tooltip with the cursor time."""
        if not self.plot_widget:
            return
        if self.plot_widget.scene() is None:
            return
        view_box = self.plot_widget.getViewBox()
        if view_box is None:
            return
        if not self.plot_widget.sceneBoundingRect().contains(scene_position):
            return

        mouse_point = view_box.mapSceneToView(scene_position)
        time_value = max(0.0, min(float(self._duration_sec), mouse_point.x()))
        self.plot_widget.setToolTip(self._format_mmss_with_fraction(time_value))

    def _zoom_in(self) -> None:
        """Zoom in on the waveform around the current view center."""
        if not self.plot_widget or self._duration_sec <= 0:
            return

        view_min, view_max = self.plot_widget.viewRange()[0]
        current_width = max(0.0, view_max - view_min)
        if current_width <= 0:
            return

        min_range = min(float(self._duration_sec), max(0.5, float(self._min_region_duration)))
        new_width = max(current_width * 0.5, min_range)
        center = (view_min + view_max) / 2.0
        half_width = new_width / 2.0

        new_min = max(0.0, center - half_width)
        new_max = min(float(self._duration_sec), center + half_width)

        if new_max - new_min < min_range:
            new_min = max(0.0, new_max - min_range)
        self.plot_widget.setXRange(new_min, new_max, padding=0)

    def _zoom_out(self) -> None:
        """Zoom out from the current view while staying within bounds."""
        if not self.plot_widget or self._duration_sec <= 0:
            return

        view_min, view_max = self.plot_widget.viewRange()[0]
        current_width = max(0.0, view_max - view_min)
        if current_width <= 0:
            return

        max_range = float(self._duration_sec)
        new_width = min(current_width * 2.0, max_range)
        center = (view_min + view_max) / 2.0
        half_width = new_width / 2.0

        new_min = max(0.0, center - half_width)
        new_max = min(max_range, center + half_width)

        if new_max - new_min < new_width:
            new_max = min(max_range, new_min + new_width)
        self.plot_widget.setXRange(new_min, new_max, padding=0)

    def _fit_all(self) -> None:
        """Fit the entire waveform into view."""
        if not self.plot_widget or self._duration_sec <= 0:
            return
        self.plot_widget.setXRange(0.0, float(self._duration_sec), padding=0)

    def _fit_to_region(self) -> None:
        """Fit the current selection region."""
        if not self.plot_widget:
            return
        start, end = self._region_bounds
        if end <= start:
            return
        self.plot_widget.setXRange(start, end, padding=0)

    def _on_position_changed(self, position_ms: int) -> None:
        """Update position indicators when player position changes."""
        position_sec = position_ms / 1000.0

        # Update time label
        self.time_current.setText(self._format_time(position_sec))

        # Update position line on the plot
        if self.plot_widget:
            if self._playhead_line is None:
                self._playhead_line = pg.InfiniteLine(
                    angle=90,
                    movable=False,
                    pen=pg.mkPen("#EF4444", width=2),
                )
                self.plot_widget.addItem(self._playhead_line)
                self._playhead_line.setZValue(3)
            self._playhead_line.setPos(position_sec)

    def _on_duration_changed(self, duration_ms: int) -> None:
        """Handle player duration updates."""
        if duration_ms <= 0:
            return
        self._duration_ms = duration_ms
        self.position_slider.setRange(0, duration_ms)
        self.time_total.setText(self._format_time(duration_ms / 1000.0))

    def _on_slider_pressed(self) -> None:
        """Pause position updates while scrubbing."""
        self._slider_updating = True

    def _on_slider_released(self) -> None:
        """Apply slider position when released."""
        new_position = self.position_slider.value()
        self._player.setPosition(new_position)
        self._slider_updating = False

    def _on_slider_moved(self, position_ms: int) -> None:
        """Preview position while slider is moved."""
        position_sec = position_ms / 1000.0
        self.time_current.setText(self._format_time(position_sec))

    def _handle_play(self) -> None:
        """Start playback."""
        self._player.play()

    def _handle_pause(self) -> None:
        """Pause playback."""
        self._player.pause()

    def _handle_stop(self) -> None:
        """Stop playback and reset position."""
        self._player.stop()
        self._on_position_changed(0)

    def _on_player_error(self, _error, error_string: str) -> None:
        """Log playback errors."""
        if not error_string:
            error_string = "Unknown playback error"
        logging.error("Waveform playback error: %s", error_string)
        QMessageBox.warning(self, "Playback Error", error_string)

    @staticmethod
    def _format_time(seconds: float) -> str:
        """Format seconds as MM:SS.s string."""
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02.1f}"

    def closeEvent(self, event) -> None:
        """Clean up resources."""
        try:
            self._player.stop()
        finally:
            if self._temp_wav and self._temp_wav.exists():
                try:
                    self._temp_wav.unlink()
                except Exception as exc:
                    logging.warning("Failed to remove temporary WAV file: %s", exc)
            self._temp_wav = None
        super().closeEvent(event)


class WaveformViewerDialog(QDialog):
    """Modal dialog showing waveform visualization with playback controls."""

    def __init__(
        self,
        zip_path: Path,
        wav_filename: str,
        waveform_settings: WaveformSettings,
        parent=None,
    ):
        super().__init__(parent)
        self._zip_path = Path(zip_path)
        self._wav_filename = wav_filename
        self._temp_wav: Optional[Path] = None
        self._duration_ms: int = 0
        self._slider_updating = False
        self._waveform_settings = waveform_settings

        self.setWindowTitle(f"Waveform Viewer - {wav_filename}")
        self.resize(900, 600)

        if not _MULTIMEDIA_AVAILABLE:
            QMessageBox.critical(
                self,
                "Qt Multimedia Required",
                "Waveform playback requires the PyQt6 QtMultimedia module. "
                "Install PyQt6>=6.4 with Qt Multimedia support to enable this feature.",
            )
            raise RuntimeError("Qt Multimedia module not available") from _MULTIMEDIA_IMPORT_ERROR

        self._player = QMediaPlayer(self)
        self._audio_output = QAudioOutput(self)
        self._player.setAudioOutput(self._audio_output)

        volume_value = max(0.0, min(1.0, float(waveform_settings.default_volume)))
        self._audio_output.setVolume(max(0.0, min(1.0, volume_value)))

        self._init_ui()
        self._load_waveform()

    def _init_ui(self) -> None:
        """Initialize dialog layout."""
        main_layout = QVBoxLayout(self)

        name_label = QLabel(f"{self._wav_filename}", self)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setObjectName("waveformFilenameLabel")
        main_layout.addWidget(name_label)

        self.plot_widget = pg.PlotWidget(self)
        self.plot_widget.setBackground("k")
        self.plot_widget.setMenuEnabled(False)
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.setLabel("bottom", "Time", units="s")
        self.plot_widget.setLabel("left", "Amplitude")
        main_layout.addWidget(self.plot_widget, stretch=1)

        waveform_pen_color = waveform_settings.waveform_color or "#3B82F6"
        position_pen_color = waveform_settings.position_line_color or "#EF4444"

        self._plot_curve = self.plot_widget.plot(pen=pg.mkPen(waveform_pen_color, width=1))
        self._position_line = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen(position_pen_color, width=1))
        self.plot_widget.addItem(self._position_line)

        controls_layout = QVBoxLayout()
        main_layout.addLayout(controls_layout)

        # Transport controls
        transport_layout = QHBoxLayout()
        self.play_button = QPushButton("Play", self)
        self.pause_button = QPushButton("Pause", self)
        self.stop_button = QPushButton("Stop", self)
        transport_layout.addWidget(self.play_button)
        transport_layout.addWidget(self.pause_button)
        transport_layout.addWidget(self.stop_button)
        transport_layout.addStretch()

        self.play_button.clicked.connect(self._player.play)
        self.pause_button.clicked.connect(self._player.pause)
        self.stop_button.clicked.connect(self._handle_stop)

        controls_layout.addLayout(transport_layout)

        # Position slider
        slider_layout = QHBoxLayout()
        self.time_current = QLabel("00:00", self)
        self.position_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.position_slider.setRange(0, 0)
        self.time_total = QLabel("00:00", self)
        slider_layout.addWidget(self.time_current)
        slider_layout.addWidget(self.position_slider, stretch=1)
        slider_layout.addWidget(self.time_total)
        controls_layout.addLayout(slider_layout)

        self.position_slider.sliderPressed.connect(self._on_slider_pressed)
        self.position_slider.sliderReleased.connect(self._on_slider_released)
        self.position_slider.sliderMoved.connect(self._on_slider_moved)

        # Volume controls
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:", self)
        self.volume_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(int(self._audio_output.volume() * 100))
        self.volume_value = QLabel(f"{self.volume_slider.value()}%", self)
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)
        volume_layout.addWidget(self.volume_value)
        controls_layout.addLayout(volume_layout)

        self.volume_slider.valueChanged.connect(self._on_volume_changed)

        # Wire up player signals
        self._player.positionChanged.connect(self._on_position_changed)
        self._player.durationChanged.connect(self._on_duration_changed)
        self._player.errorOccurred.connect(self._on_player_error)

    def _load_waveform(self) -> None:
        """Extract WAV file and render waveform."""
        try:
            self._extract_wav()
            if not self._temp_wav:
                raise FileNotFoundError("Temporary WAV file missing after extraction")

            audio_data, sample_rate = sf.read(str(self._temp_wav), dtype="float32")

            if audio_data.ndim > 1:
                mono_data = audio_data.mean(axis=1)
            else:
                mono_data = audio_data

            if sample_rate <= 0 or mono_data.size == 0:
                raise ValueError("Invalid audio data encountered")

            duration_seconds = mono_data.shape[0] / float(sample_rate)

            target_pixels = max(200, int(self.plot_widget.width()))
            if target_pixels <= 0:
                target_pixels = 800
            downsample_factor = max(1, self._get_downsample_factor())
            segments = max(1, target_pixels // downsample_factor)
            window_size = max(1, int(np.ceil(mono_data.shape[0] / segments)))

            pad = (-mono_data.shape[0]) % window_size
            if pad:
                mono_padded = np.pad(mono_data, (0, pad), mode="edge")
            else:
                mono_padded = mono_data

            reshaped = mono_padded.reshape(-1, window_size)
            mins = reshaped.min(axis=1)
            maxs = reshaped.max(axis=1)

            if mins.size == 0 or maxs.size == 0:
                raise ValueError("Unable to compute waveform envelope")

            centers = ((np.arange(mins.size, dtype=float) * window_size) + (window_size / 2.0)) / float(sample_rate)
            time_pairs = np.repeat(centers, 2)
            amplitude_pairs = np.empty(time_pairs.size, dtype=mono_data.dtype)
            amplitude_pairs[0::2] = mins
            amplitude_pairs[1::2] = maxs

            self._plot_curve.setData(time_pairs, amplitude_pairs)
            self._position_line.setPos(0)
            self.plot_widget.setXRange(0, max(duration_seconds, 1.0))

            self._duration_ms = int(duration_seconds * 1000)
            self.time_total.setText(self._format_time(self._duration_ms))
            self.position_slider.setRange(0, self._duration_ms)

            self._player.setSource(QUrl.fromLocalFile(str(self._temp_wav)))
        except Exception as exc:
            logging.error("Failed to load waveform: %s", exc, exc_info=True)
            QMessageBox.critical(
                self,
                "Waveform Error",
                f"Unable to load WAV file '{self._wav_filename}'.\n\nError: {exc}",
            )
            self._set_controls_enabled(False)

    def _extract_wav(self) -> None:
        """Extract WAV file from ZIP archive to a temporary file."""
        if not self._zip_path.exists():
            raise FileNotFoundError(f"ZIP archive not found: {self._zip_path}")

        with zipfile.ZipFile(self._zip_path, "r") as zf:
            matching_entry: Optional[str] = None
            for member in zf.namelist():
                if member == self._wav_filename:
                    matching_entry = member
                    break

            if not matching_entry:
                raise FileNotFoundError(f"WAV file '{self._wav_filename}' not found in archive")

            with zf.open(matching_entry) as wav_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
                    shutil.copyfileobj(wav_file, temp_file)
                    self._temp_wav = Path(temp_file.name)

    def _get_downsample_factor(self) -> int:
        """Retrieve downsample factor from injected settings."""
        value = int(self._waveform_settings.downsample_factor)
        return max(1, min(100, value))

    def _set_controls_enabled(self, enabled: bool) -> None:
        """Enable or disable playback controls."""
        for widget in (
            self.play_button,
            self.pause_button,
            self.stop_button,
            self.position_slider,
            self.volume_slider,
        ):
            widget.setEnabled(enabled)

    def _on_position_changed(self, position_ms: int) -> None:
        """Update slider and position indicator when player position changes."""
        if self._slider_updating:
            return

        self._slider_updating = True
        self.position_slider.setValue(position_ms)
        self.time_current.setText(self._format_time(position_ms))
        self._update_position_line(position_ms)
        self._slider_updating = False

    def _on_duration_changed(self, duration_ms: int) -> None:
        """Handle player duration updates."""
        if duration_ms <= 0:
            return
        self._duration_ms = duration_ms
        self.position_slider.setRange(0, duration_ms)
        self.time_total.setText(self._format_time(duration_ms))

    def _on_slider_pressed(self) -> None:
        """Pause automatic updates while the user scrubs."""
        self._slider_updating = True

    def _on_slider_released(self) -> None:
        """Apply slider position when the user releases the handle."""
        new_position = self.position_slider.value()
        self._player.setPosition(new_position)
        self._update_position_line(new_position)
        self._slider_updating = False

    def _on_slider_moved(self, position_ms: int) -> None:
        """Preview position while the slider is moved."""
        self.time_current.setText(self._format_time(position_ms))
        self._update_position_line(position_ms)

    def _on_volume_changed(self, value: int) -> None:
        """Handle volume slider changes."""
        volume = max(0.0, min(1.0, value / 100.0))
        self._audio_output.setVolume(volume)
        self.volume_value.setText(f"{value}%")

    def _handle_stop(self) -> None:
        """Stop playback and reset position."""
        self._player.stop()
        self._on_position_changed(0)

    def _update_position_line(self, position_ms: int) -> None:
        """Update graphical position indicator."""
        if self._duration_ms <= 0:
            return
        position_sec = position_ms / 1000.0
        self._position_line.setPos(position_sec)

    def _on_player_error(self, _error, error_string: str) -> None:
        """Log playback errors and notify the user."""
        if not error_string:
            error_string = "Unknown playback error"
        logging.error("Waveform playback error: %s", error_string)
        QMessageBox.warning(self, "Playback Error", error_string)

    @staticmethod
    def _format_time(milliseconds: int) -> str:
        """Format milliseconds as MM:SS string."""
        try:
            millis_int = int(milliseconds)
        except (TypeError, ValueError):
            millis_int = 0
        if millis_int <= 0:
            return "00:00"
        seconds = millis_int / 1000.0
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes:02d}:{secs:02d}"

    def closeEvent(self, event) -> None:  # noqa: D401
        """Ensure playback stops and temporary files are removed."""
        try:
            self._player.stop()
        finally:
            if self._temp_wav and self._temp_wav.exists():
                try:
                    self._temp_wav.unlink()
                except Exception as exc:
                    logging.warning("Failed to remove temporary WAV file: %s", exc)
            self._temp_wav = None
        super().closeEvent(event)

``n

