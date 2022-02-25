import pygame as pg
from const import (
    BLACK_STONE_IMGPATH, WHITE_STONE_IMGPATH,
    GOBAN_TILE_IMGPATH,
    CELL_SIZE, STONE_SIZE,
    FONT, FONT_SIZE, FONT_COLOR,
    HOR_LABELS, VERT_LABELS,
    STAR_POINTS,
)


class Board:
    """
    Represents a go board, and is intended to be a 
    pluggable component. Its interface is provided through
    the following functions:
        -
        -
        -
    """

    def __init__(self, game, screen, board_rect):

        assert pg.font.get_init(), "Board: font subsystem not initialized"

        self.game = game
        self.screen = screen
        self.board_rect = board_rect
        self.actual_board_rect = board_rect     # after margins are accounted for 

        self.move_idx = 0

        self.black_stone_img = pg.image.load(BLACK_STONE_IMGPATH)
        self.white_stone_img = pg.image.load(WHITE_STONE_IMGPATH)
        self.goban_tile_img = pg.image.load(GOBAN_TILE_IMGPATH)
        self.goban_tile_rect = self.goban_tile_img.get_rect()

        self.font = pg.font.SysFont(FONT, FONT_SIZE)

        self.margin = 50
        self.calc_everything()

    def calc_everything(self):
        '''
        self.full_width = self.board_rect.width - self.margin * 2
        self.full_height = self.board_rect.height - self.margin * 2

        self.lower_dim = self.full_width if self.full_width < self.full_height else self.full_height
        self.cell_size = self.lower_dim // 20
        '''

        self.actual_board_rect = pg.Rect(self.margin, self.margin, 
                                        CELL_SIZE * 18, CELL_SIZE * 18)
        
    def set_margin(margin):
        self.margin = margin
        self.calc_everything()

    def next_move(self):
        self.move_idx += 1
        self.move_idx = min(self.move_idx, len(self.game.move_seq)-1)
        #self.update_or_sth

    def prev_move(self):
        self.move_idx -= 1
        self.move_idx = max(self.move_idx, 0)


    def game_to_screen_coords(self, pos):
        i = pos[0] - 1
        j = pos[1] - 1
        return (self.margin + i * CELL_SIZE, self.margin + j * CELL_SIZE)


    def draw(self):
        # draw the board first, then the grid, and then the stones
        # add coordinate labels too
        # 50 to 
        '''
        print("total dim = ", self.cell_size * 19)
        for i in range(19):
            for j in range(19):
                x = self.margin + i * self.cell_size
                y = self.margin + j * self.cell_size
                pos_rect = pg.Rect(x, y, self.cell_size, self.cell_size)
                self.screen.blit(self.goban_tile_img, pos_rect)
                pg.draw.rect(self.screen, (255, 0, 0), pos_rect)
        '''

        # draw board
        pg.draw.rect(self.screen, (165,42,42), self.actual_board_rect)

        #draw rect around board
        pg.draw.rect(self.screen, (0, 0, 0), self.actual_board_rect, 2)

        
        # draw lines
        pos_x = pos_y = self.margin
        end_y = self.margin + 18 * CELL_SIZE
        end_x = self.margin + 18 * CELL_SIZE
                
        # draw vertical lines
        self.cell_size = CELL_SIZE
        for i in range(18):
            start_pos = (pos_x + i * self.cell_size, pos_y)
            end_pos = (pos_x + i * self.cell_size, end_y)
            pg.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)

        # draw horizontal lines
        for j in range(18):
            start_pos = (pos_x, pos_y + j * self.cell_size)
            end_pos = (end_x, pos_y + j * self.cell_size)

            pg.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 2)


        # draw star points
        for coord in STAR_POINTS:
            real_pos = self.game_to_screen_coords(coord)
            pg.draw.circle(self.screen, (0,0,0), real_pos, CELL_SIZE//6)

        # draw coordinate labels
        # (1, 1) is top left, japanese style
        # draw horizontal labels (columns)
        pos_x = self.margin - 5
        pos_y = self.margin/2
        for i, label_x in enumerate(HOR_LABELS):
            pos = (pos_x + i * CELL_SIZE, pos_y)
            text_img = self.font.render(label_x, True, FONT_COLOR)
            self.screen.blit(text_img, pos) 
        
        pos_y = self.margin - 5
        pos_x = self.margin/2
        # draw vertical labels (ranks)
        for j, label_y in enumerate(VERT_LABELS):
            pos = (pos_x, pos_y + j * CELL_SIZE)
            text_img = self.font.render(label_y, True, FONT_COLOR)
            self.screen.blit(text_img, pos)

