from core.game import Game, Move, Result
import const
from gui.gui import GUI, Color, Orientation
from graphics.board import Board
import pygame as pg


def callback_sample(string):
    print(string)

class DisplayWindow:

    def __init__(self, game):
        self.running = True
        self.cur_move_idx = -1
        self.clock = None
        self.gui = None
        self.game = game
        self.board = None
        
        # upper 12
        self.board_rect = pg.Rect(0, 0, const.TOTAL_DIM[0]-80, const.TOTAL_DIM[1]-80)
        # lower 1280 x 80 rectangle
        self.bh_rect = pg.Rect(0, const.TOTAL_DIM[1] - 80, const.TOTAL_DIM[0], 80)

        self.init_pygame()
        self.init_gui()

        self.board = Board(self.game, self.screen, self.board_rect)
   
    # unnecessary right now
    def set_game(self, game):
        self.game = game
        self.board = Board(self.game, self.screen, self.board_rect)

    def init_gui(self):
        #assert self.screen is not None, "self.screen cannot be None"
        self.gui = GUI(self.screen)

        cont = self.gui.make_horizontal_container((self.bh_rect.x, self.bh_rect.y), self.bh_rect.w, self.bh_rect.h)
        cont.margin = (0, 20)

        but = self.gui.make_text_button((200, 200), 160, 40, "PREV", self.game.prev_move, ())
        but.style.set_border((0, 0, 0), 1)
        but.set_font("Envy Code R Regular")
        
        but2 = self.gui.make_text_button((900, 200), 160, 40, "NEXT", self.game.next_move, ())
        but2.style.set_border((0, 0, 0), 1)
        but2.set_font("Envy Code R Regular", font_bold=False, font_italic=False)

        cont.push_items(but, but2)
        self.gui.add_elem(cont)

    
    def draw_gui_extras(self):
        pg.draw.rect(self.screen, (47, 152, 127), self.bh_rect)

    def init_pygame(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode(const.TOTAL_DIM)
        pg.display.set_caption("Honinbo - SGF viewer")
        self.clock = pg.time.Clock()

    def set_title(self):
        vs_string = self.game.player_names[0] + " vs " + self.game.player_names[1]
        pg.display.set_caption("Honinbo : " + vs_string)


    def mainloop(self):
        assert self.game is not None, "DisplayWindow: no game set"

        while self.running:

            mouse_pos = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                else:
                    self.gui.update(event, mouse_pos)

            ## drawing section ##
            self.screen.fill((248, 255, 184))

            
            self.draw_gui_extras()
            self.gui.draw()
            self.board.draw()

            pg.display.update()
            self.clock.tick(const.FPS)


