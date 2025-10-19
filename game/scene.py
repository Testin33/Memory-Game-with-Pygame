from __future__ import annotations

import pygame

from typing import Tuple
import sys

# Import style requested; works when running from project root
from game.core import GameCore, GameConfig, SHOWING, PLAYING, WON, LOST
from models.tile import Tile  # not strictly required for current scene logic
from settings import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    FPS,
    GRID_ROWS,
    GRID_COLS,
    CELL_SIZE,
    GRID_MARGIN,
    COLOR_BG,
    COLOR_GRID,
    COLOR_TILE,
    COLOR_TILE_HL,
    COLOR_TEXT,
    SHOW_TIME_PER_STEP_MS,
    HIDE_FLIP_MS,
    TOTAL_TIME_SECONDS,
    BOARD_WIDTH,
    BOARD_HEIGHT,
)


class GameScene:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Memory Game")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 28)

        self.logic = GameCore(
            GameConfig(
                GRID_ROWS,
                GRID_COLS,
                total_seconds=TOTAL_TIME_SECONDS,
                pattern_length=3,
            )
        )

        # Center grid within window (reserve ~120px HUD at bottom)
        self.hud_height = 120
        self.origin_x = (WINDOW_WIDTH - BOARD_WIDTH) // 2
        self.origin_y = ((WINDOW_HEIGHT - self.hud_height) - BOARD_HEIGHT) // 2

        # Click feedback
        self.feedback_text: str | None = None
        self.feedback_until_ms: int = 0

        self.last_show_ms = pygame.time.get_ticks()
        self.in_hide_flip: bool = False
        self.hide_flip_started_ms: int = 0

    # ---------- helpers ----------
    def grid_rect(self, r: int, c: int) -> pygame.Rect:
        x = self.origin_x + GRID_MARGIN + c * (CELL_SIZE + GRID_MARGIN)
        y = self.origin_y + GRID_MARGIN + r * (CELL_SIZE + GRID_MARGIN)
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def draw_board(self) -> None:
        self.screen.fill(COLOR_BG)
        # grid background
        board_rect = pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_GRID, board_rect, 0)

        # tiles
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect = self.grid_rect(r, c)
                color = COLOR_TILE
                if self.logic.state == SHOWING and not self.in_hide_flip:
                    idx = self.logic.show_index
                    if idx < len(self.logic.pattern) and (r, c) == self.logic.pattern[idx]:
                        color = COLOR_TILE_HL
                pygame.draw.rect(self.screen, color, rect, border_radius=12)

        # flip overlay (simple dark mask) to indicate hiding
        if self.in_hide_flip:
            elapsed = pygame.time.get_ticks() - self.hide_flip_started_ms
            t = min(1.0, elapsed / HIDE_FLIP_MS)
            alpha = int(180 * t)
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            self.screen.blit(overlay, (0, 0))

        # HUD
        remaining = self.logic.seconds_left()
        text = f"Estado: {self.logic.state.name}  Tiempo: {remaining:02d}s"
        surf = self.font.render(text, True, COLOR_TEXT)
        self.screen.blit(surf, (16, WINDOW_HEIGHT - 48))

        # Wrong attempts bar (Errores X/Max)
        max_wrong = self.logic.config.max_wrong
        wrong = getattr(self.logic, "wrong_count", 0)
        bar_w = 240
        bar_h = 16
        bar_x = 16
        bar_y = WINDOW_HEIGHT - 72
        # background bar
        pygame.draw.rect(self.screen, COLOR_GRID, pygame.Rect(bar_x, bar_y, bar_w, bar_h), border_radius=6)
        # filled portion
        fill_w = int(bar_w * min(1.0, wrong / max_wrong))
        if fill_w > 0:
            pygame.draw.rect(self.screen, COLOR_TILE_HL, pygame.Rect(bar_x, bar_y, fill_w, bar_h), border_radius=6)
        # numeric label
        label = self.font.render(f"Errores: {wrong}/{max_wrong}", True, COLOR_TEXT)
        self.screen.blit(label, (bar_x + bar_w + 12, bar_y - 6))

        # Feedback (show briefly above HUD)
        now = pygame.time.get_ticks()
        if self.feedback_text and now <= self.feedback_until_ms:
            fb = self.font.render(self.feedback_text, True, COLOR_TEXT)
            self.screen.blit(fb, (16, WINDOW_HEIGHT - 80))
        else:
            self.feedback_text = None

    def update_show_sequence(self) -> None:
        if self.logic.state != SHOWING:
            return
        now = pygame.time.get_ticks()
        if not self.in_hide_flip and now - self.last_show_ms >= SHOW_TIME_PER_STEP_MS:
            # advance to next tile and start flip
            self.logic.update_showing()
            self.last_show_ms = now
            self.in_hide_flip = True
            self.hide_flip_started_ms = now
        elif self.in_hide_flip and now - self.hide_flip_started_ms >= HIDE_FLIP_MS:
            self.in_hide_flip = False

    def handle_click(self, pos: Tuple[int, int]) -> None:
        if self.logic.state != PLAYING:
            return
        x, y = pos
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                if self.grid_rect(r, c).collidepoint(x, y):
                    # Determine and show feedback
                    try:
                        expected = self.logic.pattern[self.logic.user_index]
                    except IndexError:
                        expected = None
                    clicked = (r, c)
                    if expected is not None and clicked == expected:
                        self.feedback_text = "Correcto"
                    else:
                        self.feedback_text = "Incorrecto"
                    self.feedback_until_ms = pygame.time.get_ticks() + 900

                    self.logic.input_click(clicked)
                    return

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.logic.tick()
            self.update_show_sequence()
            # Exit immediately if reached max wrong attempts
            if getattr(self.logic, "wrong_count", 0) >= self.logic.config.max_wrong:
                pygame.quit()
                sys.exit(0)
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
