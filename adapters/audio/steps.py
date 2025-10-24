from __future__ import annotations

import logging

from core.domain.parsing import StrictFilenameParser
from core.models.analysis import WavInfo
from wav_extractor_wave import WavInfo as WavExtractorWavInfo, ai_parse_batch, merge_ai_results


class StrictParserStep:
    """First step: attempts to parse side/position using strict regex rules."""
    def __init__(self) -> None:
        self._parser = StrictFilenameParser()

    def process(self, wavs: list[WavInfo]) -> bool:
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
    def process(self, wavs: list[WavInfo]) -> bool:
        unparsed_wavs = [w for w in wavs if w.side is None or w.position is None]
        if not unparsed_wavs:
            return True  # Chain can stop, everything is parsed

        try:
            filenames = [w.filename for w in unparsed_wavs]
            ai_map = ai_parse_batch(filenames)
            if ai_map:
                # Convert to WavExtractorWavInfo format for merge_ai_results
                extractor_wavs = [
                    WavExtractorWavInfo(
                        filename=w.filename,
                        duration_sec=w.duration_sec,
                        side=w.side,
                        position=w.position
                    ) for w in wavs
                ]

                # The merge_ai_results function expects side to be 'UNKNOWN'
                for w in extractor_wavs:
                      if w.side is None:
                         w.side = "UNKNOWN"
                merge_ai_results(extractor_wavs, ai_map)

                # Copy results back to original WavInfo objects
                for orig_w, ext_w in zip(wavs, extractor_wavs):
                    if ext_w.side is not None:
                        orig_w.side = ext_w.side
                    if ext_w.position is not None:
                        orig_w.position = ext_w.position

                # Reset 'UNKNOWN' back to None if AI didn't find anything
                for w in wavs:  # type: ignore
                    if w.side == "UNKNOWN":
                        w.side = None
        except Exception as e:
            logging.warning(f"AI parser step failed: {e}", exc_info=True)

        # Never stop the chain here; always allow fallback
        return False

class DeterministicFallbackStep:
    """Final step: assigns default side/position if all else fails."""
    def process(self, wavs: list[WavInfo]) -> bool:
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