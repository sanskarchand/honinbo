class Evaluator:
    """
    A class for handling strategic and
    full-board evaluation. 
    Terminology src: https://senseis.xmp.net/?EssayOnComputerGoByDavidFotland

    Since there are no plans to include an AI opponent in honinbo,
    this evaluator will focus mainly on:
        - detecting atari, capture, illegal moves etc.
        - counting points and territory

    That being said, the inclusion of an AI in the future is a
    distinct possiblity, and so this class will be as general as
    possible
    """
