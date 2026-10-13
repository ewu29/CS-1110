"""
This class represents a player.

"""
import random

import a6board
# STUDENTS: Do NOT change these import statements
import cornellasserts
from consts import *


#### TASK 1 ####
class Player():
    """
    A class representing a human player.
    """

    # INSTANCE ATTRIBUTES
    #
    # Attribute name: The player name
    # Invariant: name is a nonempty string
    #
    # Attribute symbol: The player symbol
    # Invariant: symbol is a 1-letter string of a lower case letter ('a'-'z')
    #
    # Read the class invariants above before implementing this class.

    # Hint: call setPlayerSymbol(sym) from here so you do not duplicate name/symbol logic.
    def __init__(self,sym):
        """
        Initializes a player with the given player symbol.

        The name will be set to 'Player <Sym>', where the `sym`
        value is capitalized. For example, if `sym` is 'x', the name
        will be set to 'Player X'

        Parameter sym: the symbol that will be used for this player on the board
        Precondition: sym is a 1-letter string of a lower case letter ('a'-'z')
        """
        # TODO: implement me (task 1)
        self.setPlayerSymbol(sym)


    # ---------- GETTERS ----------
    # Hint: each getter returns the corresponding instance attribute.

    def getName(self):
        """
        Returns the player name
        """
        # TODO: implement me (task 1)
        return self.name


    def getPlayerSymbol(self):
        """
        Returns the player symbol
        """
        # TODO: implement me (task 1)
        return self.symbol


    # ---------- SETTERS ----------
    # Hint: assert the symbol precondition with a6board.Board.assert_valid_player_symbol(sym), then set both symbol and name as described in the docstring below.

    def setPlayerSymbol(self, sym):
        """
        Given a 1-letter lowercase string `s` sets the player symbol

        Because a player name is a function of the symbol, this method
        also sets the player name.

        attribute symbol will be the value of parameter `sym`
        attribute name will be "Player <capital sym>"

        For example, if `sym` has the value 'x', symbol will be set to 'x'
           and name will be set to "Player X"

        Parameter sym: the new symbol
        Precondition: sym is a 1-letter, lowercase string

        """
        # TODO: implement me (task 1)
        a6board.Board.assert_valid_player_symbol(sym)
        self.symbol = sym
        self.name = 'Player ' + sym.upper()


    # WE HAVE IMPLEMENTED THIS METHOD FOR YOU
    # DO NOT MODIFY THIS METHOD
    def chooseMove(self,bd):
        """
        Returns the current move for this player

        Parameter board: The board to choose from
        Precondition: board is an a6board.Board object that is not full
        """
        """ from get Choice
        Displays the current board state and prompts for a column number.
        Since 0-based indices are more useful internally, this is a value
        between 0 and the numbers of columns on the board - 1, inclusive.

        Return value is guaranteed to be a valid play in a non-full column
        """
        assert type(bd) == a6board.Board
        assert not bd.isFullBoard()
        # THIS IS HOW A HUMAN PLAYER MAKES A CHOICE

        a6board.Board.assert_valid_player_symbol(self.symbol)
        print(bd)

        msg = self.name + "'s turn: "
        msg += ("pick a column (0 .. " + str(bd.getNCols()-1) + "):  ")

        validMove = False
        while not validMove:
            try:
                move = int(input(msg))
                if 0 <= move <= (bd.getNCols()-1):
                    if bd.isFullColumn(move):
                        print("Column " + str(move) + " is full.")
                    else:
                        validMove = True
                else:
                    print("Not a valid column for this board.")
            except ValueError:
                print("Invalid input. Please enter an integer value.")

        return move
