"""Fake audio mode detector adapter for tests.

Implements the AudioModeDetector protocol with deterministic filename parsing.
No external API calls - guarantees consistent results for same inputs.
"""

from __future__ import annotations

import re
from typing import Optional

from core.models.analysis import WavInfo
from core.ports import AudioModeDetector


class FakeAudioModeDetector(AudioModeDetector):
    """Fake audio mode detector for tests.

    Uses deterministic filename parsing with no external API calls.
    Guarantees consistent results for same inputs.
    """

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
        # Handle empty input
        if not wavs:
            return {}

        # Parse side and position from each filename
        parsed_wavs = []
        for wav in wavs:
            side, position = self._parse_filename(wav.filename)
            parsed_wavs.append(WavInfo(
                filename=wav.filename,
                duration_sec=wav.duration_sec,
                side=side,
                position=position
            ))

        # Group by side (ensure side is not None)
        side_map: dict[str, list[WavInfo]] = {}
        for wav in parsed_wavs:
            side = wav.side or "A"  # Default to "A" if side is None
            side_map.setdefault(side, []).append(wav)

        # Sort each group by position (or filename if position missing)
        for side, wav_list in side_map.items():
            wav_list.sort(key=lambda x: (x.position if x.position is not None else 999, x.filename.lower()))

        # Normalize positions to be sequential (1, 2, 3...) with no gaps
        self._normalize_positions(side_map)

        return side_map

    def _parse_filename(self, filename: str) -> tuple[str, Optional[int]]:
        """Parse side and position from filename using deterministic regex patterns.
        
        Args:
            filename: The WAV filename to parse.
            
        Returns:
            Tuple of (side, position) where side is a string and position is an int or None.
        """
        # Parse side using regex pattern for "Side_A", "Side-AA", etc.
        side_match = re.search(r"(?i)side[_-]?([A-Za-z]+)", filename)
        if side_match:
            side = side_match.group(1).upper()
        else:
            # Try letter-number prefix like "A1", "AA02"
            prefix_match = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)\b", filename)
            if prefix_match:
                side = prefix_match.group(1).upper()
            else:
                # Default to side "A" if no pattern matches
                side = "A"

        # Parse position using regex patterns
        position = None
        
        # Try prefix number like "01_Track"
        pos_match = re.match(r"^0*([1-9][0-9]?)\b", filename)
        if pos_match:
            position = int(pos_match.group(1))
        else:
            # Try letter-number pattern like "A1", "AA02"
            letter_num_match = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)\b", filename)
            if letter_num_match:
                position = int(letter_num_match.group(2))
            else:
                # Try side-specific pattern like "Side_A_01", "SideA_02"
                if side_match:
                    side_pos_match = re.search(rf"(?i)side[^A-Za-z0-9]*{re.escape(side)}[^0-9]*0*([1-9][0-9]?)", filename)
                    if side_pos_match:
                        position = int(side_pos_match.group(1))

        return side, position

    def _normalize_positions(self, side_map: dict[str, list[WavInfo]]) -> None:
        """Normalize positions to be sequential (1, 2, 3...) with no gaps or duplicates.
        
        Args:
            side_map: Dictionary mapping sides to lists of WavInfo objects.
        """
        for side, wav_list in side_map.items():
            if not wav_list:
                continue
            
            # Check if we need to renumber (missing positions, duplicates, or non-sequential)
            positions = [w.position for w in wav_list if w.position is not None]
            has_missing = any(w.position is None for w in wav_list)
            has_duplicates = len(positions) != len(set(positions))
            is_sequential = not has_missing and not has_duplicates and positions == list(range(min(positions), max(positions) + 1)) if positions else False
            
            if has_missing or has_duplicates or not is_sequential:
                # Renumber sequentially starting from 1
                for i, wav in enumerate(wav_list, start=1):
                    wav.position = i
            else:
                # Already sequential, just ensure they're sorted
                wav_list.sort(key=lambda x: x.position or 0)