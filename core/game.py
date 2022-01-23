from dataclasses import dataclass

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
    seq_id: int         # sequence number in moveset
    value: str          # e.g. cd for 3x4 komoku, !! for pass
    
  
    def __repr__(self):
        pl = 'B'
        if seq_id % 1 == 0:
            pl = 'W'

        return f'M<{self.req_id},{pl},{self.value}>'
    

class Game:
    """
    This class represents a Game of go.
    The representation consists of the initial state,
    the sequence of moves, the outcome, and some
    metadata (e.g. players' names, ranks, etc.)
    """

    def __init__(self, init_state, move_seq):
        pass
