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
            filename=wav.filename,
            duration_sec=wav.duration_sec,
            side=wav.side,
            position=wav.position
        )

    def _convert_to_core_wavinfo(self, wav: ExtractorWavInfo) -> WavInfo:
        """Convert wav_extractor_wave WavInfo to core WavInfo format.
        
        Args:
            wav: ExtractorWavInfo object to convert.
            
        Returns:
            Core WavInfo object with identical field values.
        """
        return WavInfo(
            filename=wav.filename,
            duration_sec=wav.duration_sec,
            side=wav.side,
            position=wav.position
        )
