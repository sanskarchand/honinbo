from core.game import Game, Result, Move
import logging

logging.basicConfig(
    filename=f'{__name__}.log', 
    format='%(asctime)s %(message)s',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def parse_property(game, my_data):
    '''
    Parses a key[value] property, and fills it in
    _game_ appropriately

    Return value; my_data, sans the string
    containing the key-val data. The file_data
    string is crunched from the front.

    The idea is to allow continuous feeding into this
    function
    '''
    
    # _data_ starts with [ i.e. the beginning of the property value
    # return (property_value, crunched_string)
    def crunch_value(data):

        assert data[0] == '[', "Parsing error: property value missing '['. \nData = " + data
        prop_val = ''

        for idx, char in enumerate(data):
            if char == ']':
                break

        prop_val = data[1:idx]
        crunched_str = data[idx+1:]         # crunching upto ']'

        return (prop_val, crunched_str)
    
    # return (property_key, crunched_string)
    def crunch_key(data):
        if data[1] == '[':
            return data[0], data[1:]

        return data[:2], data[2:]

    def parse_result(value):
        res = Result()
        res.winner = value[0]
        if value[2] == 'R':
            res.resignation = True
        else:
            res.points = float(value[2:])

        return res
            
    key, my_data = crunch_key(my_data)
    #logger.info("Key = " + key)
    val, my_data = crunch_value(my_data)
    #logger.info("Val = " + val)

    if key == 'EV':
        game.event = val
    elif key == 'PB':
        game.player_names[0] = val
    elif key == 'PW':
        game.player_names[1] = val
    elif key == 'KM':
        game.komi = float(val)
    elif key == 'RE':
        game.result  = parse_result(val)
    
    # game moves
    elif key in ['B', 'W']:
        move = Move()
        move.value = val
        move.seq_id = len(game.move_seq) 
        game.move_seq.append(move)



    return my_data


def parse(file_data):
    '''
    Parse the data of SGF (v4) files.

    Params: file_data, a string
    Return value: a filled Game object

    Resillience: low
    Method: Naive. Look for (property, value) pairs.
    Errors out on incorrect syntax.
    '''

    game = Game()

    # skip first two chars  - (;
    file_data = file_data[2:]

    cur_data = file_data

    
    while cur_data: 
        cur_data = parse_property(game, cur_data)
        char = cur_data[0]
        
        # next independent char is semicolon
        # that's a game node -> semicolon + property
        if char == ';':
            cur_data = cur_data[1:]

        # next independent char is close param
        # effectively, we've reached EOF
        elif char == ')':
            cur_data = ''
    
    logger.info('Parsing finished for ' + game.player_names[0] + ' vs ' +  game.player_names[1])

    return game


def parse_from_file(file_path):
    with open(file_path) as f:
        data = ''.join([line.strip() for line in f.readlines()])
        return parse(data)
