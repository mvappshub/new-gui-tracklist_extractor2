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

    def parse(self, filename: str) -> ParsedFileInfo:
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
            m_pref = re.match(r"^([A-Za-z]+)0*([1-9][0-9]?)\b", name)
            if m_pref:
                side = m_pref.group(1).upper()
                if pos is None:
                    pos = int(m_pref.group(2))

        # "Side_A_01", "SideA_02", "Side_A01"
        if pos is None and side:
            m_pos2 = re.search(rf"(?i)side[^A-Za-z0-9]*{re.escape(side)}[^0-9]*0*([1-9][0-9]?)", name)
            if m_pos2:
                pos = int(m_pos2.group(1))
        
        return ParsedFileInfo(side=side, position=pos)