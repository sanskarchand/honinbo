from core.game import Game
from utils import parser 
from graphics.display_game import DisplayWindow

def main():

    g = parser.parse_from_file('ShusakuvsInseki_EarReddening.sgf')
    print(g)
    #print(g.move_seq)

    dw = DisplayWindow(g)
    dw.set_title()
    dw.mainloop()



if __name__ == '__main__':
    main()
