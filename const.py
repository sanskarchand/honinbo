import os

TOTAL_DIM = (1280, 960)     # (640, 480)
FPS = 60
DEBUG_DRAW = True

GUI_P = 80              # GUI sizing param; just for convenience

POS_UNDEF = (-1, -1)    # position param for container children

CELL_SIZE = 40
STONE_SIZE = 40
HOR_LABELS = list(map(str, range(1, 20)))
VERT_LABELS = HOR_LABELS
#VERT_LABELS = ['一', '二', '三', '四', '五']
STAR_POINTS = [
    (4, 4), (10, 4), (16, 4),
    (4, 10), (10, 10), (16, 10),
    (4, 16), (10, 16), (16, 16)
]

FONT =  "Envy Code R Regular"
FONT_SIZE = 24
FONT_COLOR = (0, 0, 0)
LINE_GAP = 5    # vertical gap; text rendering newline handling

BLACK_STONE_IMGPATH = os.path.join("res", "black_stone_128pxsq.png")
WHITE_STONE_IMGPATH = os.path.join("res", "white_stone_128pxsq.png")
#GOBAN_TILE_IMGPATH = os.path.join("res", "goban_tile.png")
GOBAN_TILE_IMGPATH = os.path.join("res", "goban_tile_blue.png")

