from core.game import Game
from utils import parser 
from graphics.display_game import DisplayWindow

def main():

    g = parser.parse_from_file('cho_chikun_v_tanaka_go4go.sgf')
    print(g)
    #print(g.move_seq)

    dw = DisplayWindow()
    dw.set_game(g)
    dw.mainloop()



if __name__ == '__main__':
    main()
