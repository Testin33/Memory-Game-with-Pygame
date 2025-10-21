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
#changes made for experiment 2 trial 
COLOR_ERROR = (255,85,85) #Bright red for error
COLOR_WARNING = (255,165,0)  # Orange for warnings

COLOR_BG = (69, 69, 69)
COLOR_GRID = (30, 36, 22)
COLOR_TILE = (63, 81, 181)
COLOR_TILE_HL = (255, 215, 64)
COLOR_TEXT = (130, 240, 100)

THEME = "dark"  # opciones: "dark" o "light"

if THEME == "light":
    COLOR_BG = (245, 245, 245)
    COLOR_GRID = (200, 200, 200)
    COLOR_TILE = (100, 149, 237)
    COLOR_TILE_HL = (255, 215, 0)
    COLOR_TEXT = (20, 20, 20)


# Derived
BOARD_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS + 1) * GRID_MARGIN
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS + 1) * GRID_MARGIN

assert BOARD_WIDTH <= WINDOW_WIDTH, "Board wider than window"
assert BOARD_HEIGHT + 120 <= WINDOW_HEIGHT, "Board plus HUD taller than window"


