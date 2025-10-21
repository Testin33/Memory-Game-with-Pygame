from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class Tile:
    row: int
    col: int

    @property
    def coord(self) -> Tuple[int, int]:
        return (self.row, self.col)

# E3: visual helpers
def is_highlight_state(state: str) -> bool:
    """Return True if tile should be drawn highlighted."""
    return state in {"lit", "picked", "correct"}
