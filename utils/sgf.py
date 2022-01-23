class ParsedSGF:
    """
    Parses SGF (v4) format files into a native format 
    """
    __version__ = '4'

    def __init__(self, data):
        self.parsed_ = None
