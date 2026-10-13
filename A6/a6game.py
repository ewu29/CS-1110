"""
This class runs the game.

This module provides the class that handles the basic game loop. Once this
class is completed, you can start to play with the connectn program.

"""
# STUDENTS: Do NOT change these import statements
import a6board
import a6player


#### TASK 3 ####
class Game:
    """
    A class representing a game of Connect-N.
    Instances of this class contain a board and a list of players. Game instances
    play the game by calling chooseMove() for each player and making the
    corresponding play in the game board. They also check for wins or ties.
    """
    # INSTANCE ATTRIBUTES
    # Attribute board: a6board.Board object - The game board
    # Invariant: board != None
    #
    # Attribute players:(a6player.Player list) -  The game players
    # Invariant: players is a (possibly empty) list of Player objects, each
    #            with a distinct symbol
    #
    # Attribute current: The index of the current player
    # Invariant: current is an int >= 0 and < len(players), or -1 if players
    #            is empty
    #
    # Attribute winner: The winner of the game
    # Invariant: winner is None (no winner) OR one of the Players in players
    #
    # Read the class invariants above before implementing Game.

    #### PART A ####
    # Task 3 Part A: __init__ creates the Board, starts with no players, current=-1, winner=None.
    # addPlayer: use isinstance(..., Player) and is_new_player(self.players, p).
    def getBoard(self):
        """
        Returns the game board
        """
        return self.board


    def getPlayers(self):
        """
        Returns a list of players in the game
        """
        return self.players


    def addPlayer(self, p):
        """
        Adds the given player to the game.

        If the list of players was currently empty, this makes this player the
        current player.

        Parameter p: the Player to add
        Precondition: player is a Player object with a different symbol than
        any of the current players.
        """
        # Note: when you assert this precondition, use isinstance() and not
        # type so that all Players and its subclasses can pass the assertion.

        assert isinstance(p,a6player.Player)
        assert is_new_player(self.players,p)
        if len(self.getPlayers()) == 0:
            self.players.append(p)
            self.current = 0
        else:
            self.players.append(p)


    def clearPlayers(self):
        """
        Removes all the players from the game
        """
        self.players = []
        self.current = -1


    def getCurrent(self):
        """
        Returns the current player object in the game. If there are no players,
        it returns None.
        """
        if len(self.players) == 0:
            return None
        else:
            return self.players[self.current]


    def getWinner(self):
        """
        Returns the winner of the game (or None if there is no winner)
        """
        return self.winner


    def __init__(self,width,height,streak):
        """
        Initializes a new game with the given width, height, and streak.

        Parameter width: The board width
        Precondition: width is an int > 0

        Parameter height: The board height
        Precondition: height is an int > 0

        Parameter streak: The number of pieces in a line necessary to win
        Precondition: streak is an int > 0 and <= min(width,height)
        """
        # NOTE #1: This method should start out with no players.
        # NOTE #2: After this initializer returns, there must be a call to setView(), before using the object further.

        a6board.Board.assert_valid_board_values(height, width, streak)
        self.board = a6board.Board(height,width,streak)
        self.players = []
        self.current = -1
        self.winner = None


    #### PART B ####
    # Task 3 Part B: takeTurn asks chooseMove then board.place; advance rotates current;
    # run loops until full board or win (after Task 4, detect wins via findWins).
    def advance(self):
        """
        Advances the game to the next player.

        This increments the current player index by 1 (or resets it to 0 when
        all players have had a chance).
        """
        self.current = (self.current + 1) % len(self.getPlayers())


    def run(self):
        """
        Runs the game until completion.

        If there are no players, this method stops immediately. Otherwise, the game proceeds until a player wins or the board is full.
        """

        if len(self.getPlayers()) == 0:
            return None
        while not self.getBoard().isFullBoard():
            self.takeTurn(self.getCurrent())
            last = self.getBoard().getLastMove()
            wins = self.getBoard().findWins(last[0],last[1])
            if len(wins) > 0:
                self.winner = self.getCurrent()
                return
            self.advance()


    def takeTurn(self, player):
        """
        Returns the column chosen by the given player.

        This method processes a turn for the current player. That means choosing a
        column AND placing the player's symbol in that column on the board.

        If the player is unable to make a move, this method returns -1.

        Parameter player: The current player
        Precondition: player is a Player object
        """
        assert isinstance(player,a6player.Player)
        if self.getBoard().isFullBoard() == True:
            return -1
        col = player.chooseMove(self.getBoard())
        self.getBoard().place(col,player.getPlayerSymbol())
        return col


    def reportFinalResults(self):
        """
        Reports the final result of the game, either the winner or tie.
        """

        if (self.getWinner() != None):
            banner = "*****************************************\n"
            msg = self.getWinner().getName() + " WINS!"
            print ("\n" + banner + str(self.board)+"\n" + msg + "\n" + banner)
        else:
            print("Game is drawn.")


#### HELPER FUNCTIONS ####
# DO NOT MODIFY
def is_new_player(players,p):
    """
    Returns True if p is a different symbol than the players in p

    Parameter players: The existing players
    Precondition: players is a list of Player objects

    Parameter p: The player to test
    Precondition: p is a Player object
    """
    result = True
    for opponent in players:
        if opponent.getPlayerSymbol() == p.getPlayerSymbol():
            return False
    return True
