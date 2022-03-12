from core.game import Game, Move, Result
import const
from gui.gui import GUI, Color, Orientation
from graphics.board import Board
import pygame as pg


GUI_P = const.GUI_P


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

        self.move_label = None
        
        # upper 12
        self.board_rect = pg.Rect(0, 0, const.TOTAL_DIM[0]-GUI_P, const.TOTAL_DIM[1]-GUI_P)
        # lower 12GUI_P x GUI_P rectangle
        self.bh_rect = pg.Rect(0, const.TOTAL_DIM[1] - GUI_P, const.TOTAL_DIM[0], GUI_P)
        # right part
        self.bv_rect = pg.Rect(const.TOTAL_DIM[0] - 3 * GUI_P, 0, 3 * GUI_P, const.TOTAL_DIM[1] - GUI_P)

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
        cont.margin = (10, 10)


        but = self.gui.make_text_button((200, 200), 160, 40, "PREV", self.prev_move, ())
        but.style.set_border((0, 0, 0), 1)
        but.set_font("Envy Code R Regular")
        
        but2 = self.gui.make_text_button((900, 200), 160, 40, "NEXT", self.next_move, ())
        but2.style.set_border((0, 0, 0), 1)
        but2.set_font("Envy Code R Regular", font_bold=False, font_italic=False)

        text_input = self.gui.make_text_input(const.POS_UNDEF, 160, 40)

        cont.push_items(but, but2, text_input)

        label_cont = self.gui.make_vertical_container(self.bv_rect.topleft, *self.bv_rect.size)
        label_cont.margin = (20, 0)

        label_1 = self.gui.make_label(const.POS_UNDEF, 80, 40, "Go\nis\nAwesome")
        self.move_label = self.gui.make_label(const.POS_UNDEF, 80, 40, "Move: 0")
        label_cont.push_items(label_1, self.move_label)


        self.gui.add_elem(cont)
        self.gui.add_elem(label_cont)

    def next_move(self):
        self.game.next_move()
        self.move_label.set_text(f"Move: {self.game.cur_move_id + 1}")

    def prev_move(self):
        self.game.prev_move()
        self.move_label.set_text(f"Move: {self.game.cur_move_id + 1}")

    
    def draw_gui_extras(self):
        pg.draw.rect(self.screen, (47, 152, 127), self.bh_rect)
        pg.draw.rect(self.screen, (222, 222, 222), self.bv_rect)

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


