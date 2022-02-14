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
        self.gui.add_button((0, 0), 200, 100, callback_sample, ())

    def init_pygame(self):
        pg.init()
        pg.font.init()

        self.screen = pg.display.set_mode(const.TOTAL_DIM)
        pg.display.set_caption("Honinbo - SGF viewer")
        self.clock = pg.time.Clock()

    def mainloop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
            
            mouse_pos = pg.mouse.get_pos()
            if self.gui:
                self.gui.update(event, mouse_pos)
                self.gui.draw()


