import pygame as pg
import const

class Board:
    """
    Represents a go board, and is intended to be a 
    pluggable component. Its interface is provided through
    the following functions:
        -
        -
        -
    """

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen
        self.move_idx = 0
        self.black_stone_img = pg.image.load(const.BLACK_STONE_IMGPATH)
        self.white_stone_img = pg.image.load(const.WHITE_STONE_IMGPATH)

    def next_move(self):
        self.move_idx += 1
        self.move_idx = min(self.move_idx, len(self.game.move_seq)-1)
        #self.update_or_sth

    def prev_move(self):
        self.move_idx -= 1
        self.move_idx = max(self.move_idx, 0)


    def draw(self):
        pass

