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


