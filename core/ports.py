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
