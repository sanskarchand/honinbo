from dataclasses import dataclass
import datetime

# NOTE: intentionally omitting player id/indication (e.g. Black).
# rationale: we know black goes first always (so odd seq id => white)
#. Even were that not the case, a recording of the first player 
# to make a move would be enough
@dataclass
class Move:
    """Records an individual move (e.g. black at 3x4 komoku).

       value => location | action,
           location: pq, cd(3x4), etc.
           action: !! for pass
    """

    # real moves have non-negative seq_id values
    # for 'virtual moves', the author will use negative integers
    seq_id: int  = -1   # sequence number in moveset
    value: str  = '00'  # e.g. cd for 3x4 komoku, !! for pass
    
  
    def __repr__(self):
        pl = ('B', 'W')[self.seq_id % 2]

        return f'M<{self.seq_id},{pl},{self.value}>'
        
@dataclass
class Result:
    """
    Records the result of a game
    """
    winner = 'W'    # 'W' | 'B'
    resignation = False     # True if won by resignation
    points = -1     # > 0. Valid only if resignation is false

    def __repr__(self):
        ret = ('White' if self.winner == 'W' else 'Black') + ' wins by'

        if self.resignation:
            return ret + " resignation"

        return f"{ret} {self.points} points"



class Game:
    """
    This class represents a Game of go.
    The representation consists of 
    the sequence of moves, the outcome, and some
    metadata (e.g. players' names, ranks, etc.)
    """
    
    # parsed from a file, normally
    # so the values are all set after utils.parser is done
    def __init__(self):
        self.move_seq = []
        self.event = ''
        self.date = datetime.datetime(1970, 1, 1)
        self.player_names = ['PB', 'PW']
        self.komi = -1
        self.result = Result()

        self.cur_move_id = -1
        self.current_stones = []

        self.captured_moves = {}    # seq_id -> Move


    def next_move(self):
        if self.cur_move_id != len(self.move_seq) - 1:
            self.cur_move_id += 1
            self.current_stones.append(self.move_seq[self.cur_move_id])
            # evalute dead stones here

    def prev_move(self):
        if self.cur_move_id > 0:
            self.cur_move_id -= 1
            self.current_stones.pop()
            # evaluate stones

    def remove_dead_stones(self):
        pass


    def __repr__(self):
        return '\n'.join([
            f"<Game>",
            f"Event: {self.event}",
            f"Black: {self.player_names[0]}",
            f"White: {self.player_names[1]}",
            f"Moves: {len(self.move_seq)}",
            f"Result: {self.result}",
            f"</Game>"
        ])


    
    '''
    # NOTE: effectively replacing self. This is okay right?
    @classmethod
    def from_file(cls, sgf_file_path):
        return parse_from_file(sgf_file_path)
    '''
