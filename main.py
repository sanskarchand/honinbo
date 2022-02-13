from core.game import Game
from utils import parser 


def main():

    g = parser.parse_from_file('cho_chikun_v_tanaka_go4go.sgf')
    print(g)

if __name__ == '__main__':
    main()
