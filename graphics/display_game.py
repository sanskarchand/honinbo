from core.game import Game, Move, Result
import const
from gui.gui import GUI, Color, Orientation
import pygame as pg


def callback_sample(string):
    print(string)

class DisplayWindow:

    def __init__(self):
        self.running = True
        self.cur_move_idx = 0
        self.clock = None
        self.gui = None
        self.game = None
        
        self.board_rect = pg.Rect(0, 0, const.TOTAL_DIM[0]-80, const.TOTAL_DIM[1]-80)
        self.bh_rect = pg.Rect(0, const.TOTAL_DIM[1] - 80, const.TOTAL_DIM[0], 80)

        self.init_pygame()
        self.init_gui()

    def set_game(self, game):
        self.game = game

    def init_gui(self):
        #assert self.screen is not None, "self.screen cannot be None"
        self.gui = GUI(self.screen)

        cont = self.gui.make_horizontal_container((self.bh_rect.x, self.bh_rect.y), self.bh_rect.w, self.bh_rect.h)
        cont.margin = (0, 20)

        but = self.gui.make_text_button((200, 200), 160, 40, "CLICK!", callback_sample, ("click!",))
        but.style.set_border((0, 0, 244), 8)
        but.set_font("Envy Code R Regular", True, True)
        
        but2 = self.gui.make_text_button((900, 200), 160, 40, "AHOY!", callback_sample, ("ahoy!",))
        but2.style.bg_color = Color(200, 40, 0)
        but2.style.set_border((0, 0, 244), 2)
        but2.set_font("Envy Code R Regular", True, True)

        cont.push_items(but, but2)
        self.gui.add_elem(cont)

    
    def draw_gui_extras(self):
        pg.draw.rect(self.screen, (155, 155, 155), self.bh_rect)

    def init_pygame(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode(const.TOTAL_DIM)
        pg.display.set_caption("Honinbo - SGF viewer")
        self.clock = pg.time.Clock()

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

            pg.display.update()
            self.clock.tick(const.FPS)


