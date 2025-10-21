from __future__ import annotations

# Window
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 720
FPS = 60

# Board
GRID_ROWS = 4
GRID_COLS = 4
CELL_SIZE = 120
GRID_MARGIN = 16

# Gameplay
SHOW_TIME_PER_STEP_MS = 450  # how long each tile stays highlighted when showing pattern
HIDE_FLIP_MS = 350           # visual flip duration after showing
TOTAL_TIME_SECONDS = 40

# Colors
COLOR_BG = (69, 69, 69)
COLOR_GRID = (40, 46, 52)
COLOR_TILE = (63, 81, 181)
COLOR_TILE_HL = (255, 215, 64)
COLOR_TEXT = (130, 240, 100)

# Derived
BOARD_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS + 1) * GRID_MARGIN
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS + 1) * GRID_MARGIN

assert BOARD_WIDTH <= WINDOW_WIDTH, "Board wider than window"
assert BOARD_HEIGHT + 120 <= WINDOW_HEIGHT, "Board plus HUD taller than window"


