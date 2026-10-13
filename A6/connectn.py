"""
connectn.py

This contains the main controller for the command line version of
ConnectN.  To use it, type at the command line:

    python connectn rows cols streak

where

    * 3 <= rows,cols <= 10
    * 3 <= streak <= min(rows,cols)
    
"""

import sys

import a6board
import a6game
import a6player
import cornellasserts
from consts import *


def _collectDimensions():
    """
    Grabs the board dimensions and minimum win length from the command line, if
    any were specified.  If none were specified, or if the specified values are
    invalid, we leave the original value, instead.

    RETURN:  a tuple (<rows>,<cols>,<winlength>) containing the board dimensions
    and minimum win length for a game.
    """

    rows,cols,streak = DEFAULT_ROWS,DEFAULT_COLS,DEFAULT_STREAK

    try:
        value = int(sys.argv[1])
        if value >= MIN_DIMENSION and value <= MAX_DIMENSION:
            rows = value
    except:
        pass # Use original value

    try:
        value = int(sys.argv[2])
        if value >= MIN_DIMENSION and value <= MAX_DIMENSION:
            cols = value
    except:
        pass # Use original value

    try:
        value = int(sys.argv[3])
        if value >= MIN_DIMENSION and value <= min(min(rows,cols),MAX_STREAK):
            streak = value
        elif streak >= min(rows,cols):
            streak = min(rows,cols)
    except:
        if streak >=  min(rows,cols):
            streak = min(rows,cols)
        # Else use original value

    return (rows,cols,streak)


#############################
if __name__ == '__main__':

    rows,cols,streak = _collectDimensions()

    gc = a6game.Game(cols,rows,streak)

    symbols = ['x','o']

    for sym in symbols:
        gc.addPlayer(a6player.Player(sym))

    print("\n****************** READY! ******************")

    try:
        gc.run()
        gc.reportFinalResults()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass

    print("\nGoodbye!")
