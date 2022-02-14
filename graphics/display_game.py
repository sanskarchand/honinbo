from core.game import Game, Move, Result
import const
from gui.gui import GUI
import pygame as pg


def callback_sample():
    print("HEYA!")

class DisplayWindow:

    def __init__(self):
        self.running = True
        self.cur_move_idx = 0
        self.clock = None
        self.gui = None

        self.init_pygame()
        self.init_gui()

    def init_gui(self):
        #assert self.screen is not None, "self.screen cannot be None"
        self.gui = GUI(self.screen)
        but = self.gui.add_text_button((200, 200), 160, 40, "CLICK!", callback_sample, ())
        but.style.set_border((0, 0, 244), 2)
        but.set_font("Envy Code R Regular", True, True)

    def init_pygame(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode(const.TOTAL_DIM)
        pg.display.set_caption("Honinbo - SGF viewer")
        self.clock = pg.time.Clock()

    def mainloop(self):
        while self.running:

            mouse_pos = pg.mouse.get_pos()
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                else:
                    self.gui.update(event, mouse_pos)

            ## drawing section ##
            self.screen.fill((248, 255, 184))

            self.gui.draw()

            pg.display.update()
            self.clock.tick(const.FPS)


