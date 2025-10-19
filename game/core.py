from __future__ import annotations

import random
import time
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Tuple


class GameState(Enum):
    SHOWING = auto()
    PLAYING = auto()
    WON = auto()
    LOST = auto()


Coord = Tuple[int, int]


@dataclass
class GameConfig:
    rows: int
    cols: int
    total_seconds: int
    # Optional fixed pattern length. If None, use default rule.
    pattern_length: int | None = None
    # Max wrong clicks allowed before losing
    max_wrong: int = 5


class GameLogic:
    """Pure game logic, render-agnostic.

    - Generates a random pattern as a list of coordinates
    - SHOWING: advance through pattern automatically over time
    - HIDE/flip visual is handled by renderer; logic only exposes phase timestamps
    - PLAYING: user must click the same sequence
    - Tracks timer and transitions to WON/LOST
    """

    def __init__(self, config: GameConfig, seed: int | None = None) -> None:
        self.config = config
        self.random = random.Random(seed)

        self.state: GameState = GameState.SHOWING
        self.pattern: List[Coord] = self._generate_pattern()
        self.show_index: int = 0
        self.user_index: int = 0
        self.start_time_s: float = time.monotonic()
        self.wrong_count: int = 0

    # ---------- setup ----------
    def _generate_pattern(self) -> List[Coord]:
        cells = [(r, c) for r in range(self.config.rows) for c in range(self.config.cols)]
        # If a fixed pattern length is provided, honor it (clamped to bounds).
        if self.config.pattern_length is not None:
            length = min(len(cells), max(1, int(self.config.pattern_length)))
        else:
            length = max(3, min(len(cells), (self.config.rows * self.config.cols) // 2))
        self.random.shuffle(cells)
        return cells[:length]

    # ---------- time ----------
    def seconds_left(self, now_s: float | None = None) -> int:
        now = time.monotonic() if now_s is None else now_s
        remaining = int(self.config.total_seconds - (now - self.start_time_s))
        return max(0, remaining)

    def is_time_over(self, now_s: float | None = None) -> bool:
        return self.seconds_left(now_s) <= 0

    # ---------- update loop (driven by scene) ----------
    def update_showing(self) -> None:
        if self.state is not GameState.SHOWING:
            return
        self.show_index += 1
        if self.show_index >= len(self.pattern):
            self.state = GameState.PLAYING

    def input_click(self, coord: Coord) -> None:
        if self.state is not GameState.PLAYING:
            return
        expected = self.pattern[self.user_index]
        if coord != expected:
            self.wrong_count += 1
            if self.wrong_count >= self.config.max_wrong:
                self.state = GameState.LOST
            return
        self.user_index += 1
        if self.user_index == len(self.pattern):
            self.state = GameState.WON

    def tick(self, now_s: float | None = None) -> None:
        if self.state in (GameState.WON, GameState.LOST):
            return
        if self.is_time_over(now_s):
            self.state = GameState.LOST


"""Compatibility exports for alternate import styles.

These aliases allow importing symbols as:
    from game.core import GameCore, SHOWING, PLAYING, WON, LOST

without changing the rest of the codebase that uses GameLogic/GameState.
"""

# Class alias
GameCore = GameLogic

# State aliases
SHOWING = GameState.SHOWING
PLAYING = GameState.PLAYING
WON = GameState.WON
LOST = GameState.LOST
