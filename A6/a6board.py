"""
This class defines the gameboard for the Connect-N game.

This module keeps the board state of the game. This game supports R rows, C columns, and
a requirement of N in a line to win.   Traditionally, all of these values are fixed to:

    R == 6 (DEFAULT_ROWS)
    C == 7 (DEFAULT_COLS)
    N == 4 (DEFAULT_STREAK)

(These default values can be found in a6consts.py)

Our version of the game allows variations on some or all of these parameters.

"""
import cornellasserts
from consts import *


class Board:
    """
    A class to represent a game board.

    This class stores the current state of the game board, namely what pieces
    are filled in, as well as the state of the game. Game pieces are represented
    as symbols (lowercase letters).  An empty board location corresponds to NOBODY.
    """

    @staticmethod
    def assert_valid_player_symbol(sym):
        """
        Static helper method
        Asserts that sym can represent a player in the game.
        sym needs to be a 1-letter lowercase string ('a'-'z')

        Preconditions: none!
        """
        assert type(sym) == str
        assert len(sym) == 1
        assert sym.isalpha()
        assert sym.islower()

    @staticmethod
    def assert_valid_board_values(rows, cols, streak):
        """
        Static helper method
        Asserts that the rows, cols, and streak values meet the class
        invariant, namely:

        cols is an int > 0
        rows is an int > 0
        streak is an int > 0 and <= min(nrows,ncols)

        Preconditions: none!
        """
        assert type(rows) == int and type(cols) == int and type(streak) == int
        assert rows > 0 and cols > 0
        assert streak > 0 and streak <= min(rows,cols)


    # INSTANCE ATTRIBUTES
    # Attribute ncols: The number of columns in the game board
    # Invariant: ncols is an int > 0
    #
    # Attribute nrows: The number of rows in the game board
    # Invariant: nrows is an int > 0
    #
    # Attribute: streak: Minimum-length run of same symbol-pieces needed to win
    # Invariant: streak is an int > 0 and <= min(nrows,ncols)
    #
    # Attribute grid: a 2d table storing the game pieces.
    # Invariant: grid is a 2d table of size nrows by ncols,
    #            where the first dimension is row and the second is column.
    #            It contains strings. These strings are NOBODY or 'a'-'z'
    #
    # Attribute moves: The saved moves in the game
    # Invariant: moves is a list of (int,int) tuples and has length
    #            less than ncols*nrows. It's length is equal to the number
    #            of non-empty places in the board.
    #
    # Read the class invariants above before implementing Board.

    def __init__(self,rows=DEFAULT_ROWS,cols=DEFAULT_COLS,streak=DEFAULT_STREAK):
        """
        Initializes a board with the given dimensions and win-streak.

        The board should be initialized as empty, meaning that the symbol for
        all board locations is NOBODY. There are NO saved moves at
        the beginning, so that list is empty.

        The default values define a traditional Connect 4 setup.

        Parameter rows: The number of rows in the board (DEFAULT 6)
        Precondition: rows is an int > 0

        Parameter cols: The number of columns in the board (DEFAULT 7)
        Precondition: cols is an int > 0

        Parameter streak: number of pieces in a line needed to win (DEFAULT 4)
        Precondition: streak is an int > 0 and <= min(rows,cols)
        """
        Board.assert_valid_board_values(rows, cols, streak)
        self.nrows = rows
        self.ncols = cols
        self.streak = streak
        self.clear()


    # ---------- GETTERS ----------

    def getNCols(self):
        """
        Returns the number of columns in this board.
        """
        return self.ncols


    def getNRows(self):
        """
        Returns the number of rows in this board.
        """
        return self.nrows


    def getStreak(self):
        """
        Returns the number of pieces in a row necessary to win

        The pieces can be horizontal, vertical, or diagonal, but they must all
        be the same symbol.
        """
        return self.streak


    def getSymbolAt(self,r,c):
        """
        Returns the symbol stored in the board at (r,c).

        The value returned is a 1 letter string. If no piece
        occupies (r,c), this method will return NOBODY

        Parameter r: The row
        Precondition: r is an int and a valid row position in board

        Parameter c: The column
        Precondition: c is an int and a valid column position in board
        """
        assert self.in_range(r,c)
        return self.grid[r][c]


    def getMoveCount(self):
        """
        Returns the number of moves that have been made so far.

        This is equal to the number of pieces in the board.
        """
        return len(self.moves)


    def getLastMove(self):
        """
        Returns the last move made.

        The value will be in the format (row,column)
        """
        if len(self.moves) == 0:
            return None
        else:
            return self.moves[-1]


    def clear(self):
        """
        Clears the board of all pieces.

        The board will be rebuilt so that all locations are set to NOBODY
        In addition, the list of moves will be reset to the empty list.
        """
        self.moves = []
        self.grid = []
        for i in range(self.nrows):
            row = [NOBODY] * self.ncols
            self.grid.append(row)


    def setSymbolAt(self,r,c,s):
        """
        Sets the symbol stored in the board at (r,c) to the value s

        Parameter r: The row
        Precondition: r is an int and a valid row position in board

        Parameter c: The column
        Precondition: c is an int and a valid column position in board

        Parameter s: the symbol to write to the specified location
        Precondition: a 1 letter string or NOBODY
        """
        assert self.in_range(r,c)
        assert type(s) == str
        assert len(s) == 1 or s == NOBODY
        self.grid[r][c] = s

    def findAvailableRow(self,col):
        """
        Returns the lowest row in column col that has no piece in it.

        If this column is full, this method returns the value of getNRows().

        Parameter col: The column
        Precondition: col is an int and a valid column in this board.
        """
        assert type(col) == int
        assert col < self.getNCols() and col>=0
        for x in range(self.getNRows()):
            if self.grid[x][col] == NOBODY:
                return x
        return self.getNRows()


    def isFullColumn(self,col):
        """
        Returns True if there is no available row in column col, False otherwise

        Parameter col: The column
        Precondition: col is an int and a valid column in this board.
        """
        assert type(col) == int
        assert col < self.getNCols() and col>=0
        if self.findAvailableRow(col) == self.getNRows():
            return True
        else:
            return False


    def isFullBoard(self):
        """
        Returns True if every location on the board is full, False otherwise.

        The board is full is every location stores a non-NOBODY string.
        """
        value = True
        for i in range(self.getNCols()):
            if self.isFullColumn(i) == False:
                value = False
        return value

    def place(self,column,symbol):
        """
        Returns the row that this symbol was placed in the given column.

        This is an interesting method that is both modifies the board AND
        returns a value to the caller. It attempts to place the given symbol
        at the specified column.  If successful, it updates the board and
        returns the row in which it was placed.
        But if that column is full, the board is not updated and this
        method returns -1 instead.

        When a piece is sucessfully placed (so this method does not
        return -1), we add (row,column) to the list of moves.

        Parameter column: The column to place the piece
        Precondition: column is an int and a valid column in this board.

        Parameter symbol: The piece symbol
        Precondition: symbol is a 1-letter string
        """
        assert type(column) == int
        assert type(symbol) == str
        assert 0 <= column < self.getNCols()
        assert len(symbol) == 1
        if self.isFullBoard() == True:
            return -1
        if self.findAvailableRow(column) == self.getNRows():
            return -1
        else:
            value = self.findAvailableRow(column)
            self.setSymbolAt(value,column,symbol)
            self.moves.append((value,column))
            return value

    def undoPlace(self):
        """
        Removes the last piece placed in the board.

        This method looks at the last element in the moves list. It erases that
        symbol from the board (by setting that position to NOBODY) and
        removes it from the move list.  If no moves have yet been made, this
        method does nothing.

        Calling this method multiple times will undo the entire board.
        """
        if self.getMoveCount() == 0:
            return None
        value = self.getLastMove()
        self.setSymbolAt(value[0],value[1],NOBODY)
        self.moves.remove(value)

    # DO NOT MODIFY THIS METHOD
    def __str__(self):
        """
        Returns the string representation of this board

        The string should be displayed as a 2D list of symbols in row-major
        order STARTING FROM THE TOP ROW.  The left brackets of each row should
        be aligned, and every entry should be padded to ensure a uniform width
        in the display.

        For example, suppose we have a 3x3 board with the following state:

            [['x','o','x'],[' ','o','x'],[' ','x','o']]

        Then the string should be

            "[[' ', 'x ','o'],\n [' ','o','x'],\n ['x','o','x']]"

        Note the newlines (\n) after each row. That is because when you print
        this string, it will look like this:

            [[' ','x','o'],
             [' ','o','x'],
             ['x','o','x']]

        This is useful for debugging, since it allows us to see each row of the
        board on its own line.

        There should be no spaces after the commas or brackets.
        """

        # Print, with last row at the top, to match the visuals of
        # a physical board
        indent = '\t'
        longline =  indent + '-' * (self.ncols * 4 + 6) + '\n'
        result = "\n"
        for row in range(self.nrows-1,-1,-1):
            result += indent + str(row)+ ' || '
            for col in range(self.ncols):
                result += self.getSymbolAt(row,col)
                result += ' | '
            result = result[:-1] + '|\n'
        result += longline
        result += indent + "  || "
        for col in range(self.ncols):
            result += str(col)
            result += ' | '
        result = result[:-1] + '|\n'

        return result

    def runFrom(self,r,c, r_step, c_step):
        """
        From (r,c), walk one step at a time in direction (r_step, c_step) while
        cells match the symbol at (r,c).

        This method returns the far endpoint of the matching run on that ray:
        the last in-bounds cell reached that still has the same symbol. If the
        very first step is off the board or lands on a different symbol, then
        the matching run in that direction has length 1 and this method returns
        (r,c).

        Example: to look downward, use r_step=MV_DOWN and c_step=NO_MOVE so each
        step stays in the same column.

        Parameter r: row of the piece (int, on board)
        Parameter c: column of the piece (int, on board)
        Parameter r_step: MV_DOWN, MV_UP, or NO_MOVE
        Parameter c_step: MV_LEFT, MV_RIGHT, or NO_MOVE
        Precondition: (r,c) holds a player symbol; r_step and c_step are not both NO_MOVE
        """
        assert self.in_range(r,c)
        assert self.getSymbolAt(r,c) != NOBODY
        assert not (r_step == NO_MOVE and c_step == NO_MOVE)
        sym = self.getSymbolAt(r,c)
        cr= r
        cc = c
        for x in range(max(self.getNRows(),self.getNCols())):
                nr = cr + r_step
                nc = cc + c_step
                if not self.in_range(nr,nc):
                    return (cr,cc)
                if self.getSymbolAt(nr,nc) != sym:
                    return (cr,cc)
                cr = nr
                cc = nc
        return (cr,cc)


    def detectRun(self, min_len,r,c,r1_move, c1_move, r2_move=NO_MOVE, c2_move=NO_MOVE):
        """
        If there is a straight run of matching symbols through (r,c) with length
        at least min_len, return (r1,c1,r2,c2), the two endpoints of that run.
        Otherwise return None.

        Preconditions: min_len is a positive int; (r,c) is on board with a piece;
        each move is in {MV_LEFT, MV_RIGHT, MV_UP, MV_DOWN, NO_MOVE}; the tuple
        forms one valid line (use is_valid_line).
        """
        assert type(min_len) == int
        assert min_len > 0
        assert self.in_range(r,c)
        assert is_valid_line(r1_move,c1_move,r2_move,c2_move)
        endpt1 = self.runFrom(r,c,r1_move,c1_move)
        r1 = endpt1[0]
        c1 = endpt1[1]
        if r2_move == NO_MOVE and c2_move == NO_MOVE:
            r2 = r
            c2 = c
        else:
            endpt2 = self.runFrom(r,c,r2_move,c2_move)
            r2 = endpt2[0]
            c2 = endpt2[1]
        if self.dist(r1, c1, r2, c2) >= min_len:
            return (r1,c1,r2,c2)
        return None

    def findWins(self,r,c):
        """
        Return a list of wins that include (r,c). Each win is (r1,c1,r2,c2), the
        endpoints of a streak of length at least getStreak(). Order of wins in the
        list does not matter; use [] if none.

        Parameter r: row of the last placed piece (precondition: on board, occupied)
        Parameter c: column of the last placed piece (precondition: on board, occupied)
        """
        assert self.in_range(r,c)
        assert self.getSymbolAt(r,c) != NOBODY
        final = []
        number = self.getStreak()
        for check in _VALID_LINE_MOVES:
            r1_move = check[0]
            c1_move = check[1]
            r2_move = check[2]
            c2_move = check[3]
            result = self.detectRun(number,r,c,r1_move, c1_move, r2_move, c2_move)
            if result != None:
                final.append(result)
        return final


    #### HELPER FUNCTIONS ####
    # DO NOT MODIFY
    def in_range(self,r=0,c=0):
        """
        Returns True if (r,c) is a valid board position, False otherwise.

        Parameter board: The game board
        Precondition: board is a Board object

        Parameter r: The candidate row
        Precondition: r is an int

        Parameter c: The candidate column
        Precondition: c is an int
        """
        assert type(r) == int
        assert type(c) == int
        return 0 <= r < self.getNRows() and 0 <= c < self.getNCols()


    def dist(self, r1,c1,r2,c2):
        """
        Returns the number of board positions between (r1,c1) and (r2,c2)

        The number computed includes those endpoints. Assuming the arguments are
        valid board coordinates, the smallest value that can be returned is 1, when
        (r1,c1) == (r2,c2).

        Distance is computed in all directions, horizontally, vertically, and
        diagonally. This is necessary for checking wins. However, if the endpoints
        do not form a valid diagonal (say (1,1) to (2,3)) then the number received
        may be unexpected.

        The positions that lie between the two endpoints do not have to be filled.

        Parameter board: The game board
        Precondition: board is a Board object

        Parameter r1: The initial row
        Precondition: r1 is an int and a valid row position in board

        Parameter c1: The initial column
        Precondition: c1 is an int and a valid column position in board

        Parameter r2: The final row
        Precondition: r2 is an int and a valid row position in board

        Parameter c2: The final column
        Precondition: c2 is an int and a valid column position in board
        """
        assert self.in_range(r1,c1) and self.in_range(r2,c2)
        if (r1 != r2):
            return abs(r1-r2) + 1
        else:
            return abs(c1-c2) + 1


    def is_valid_run(self, run):
        """
        Returns True if run is a valid run in board, False otherwise

        A valid run is one where run is None or run is a tuple (r1,c1,r2,c2) of ints
        where (r1,c1) and (r2,c2) are valid board positions.

        Parameter run: The run to score
        Precondition: NONE (run can be anything)
        """
        if run is None:
            return True
        if type(run) != tuple:
            return False
        if len(run) != 4:
            return False

        r1 = run[0]
        c1 = run[1]
        r2 = run[2]
        c2 = run[3]
        if type(r1) != int or type(c1) != int or type(r2) != int or type(c2) != int:
            return False

        return self.in_range(r1,c1) and self.in_range(r2,c2)


#### HELPER FUNCTION ####
# The four direction-tuples used for vertical-only, horizontal, and the two diagonals.
_VALID_LINE_MOVES = frozenset({
    (MV_DOWN, NO_MOVE, NO_MOVE, NO_MOVE),
    (NO_MOVE, MV_LEFT, NO_MOVE, MV_RIGHT),
    (MV_UP, MV_LEFT, MV_DOWN, MV_RIGHT),
    (MV_DOWN, MV_LEFT, MV_UP, MV_RIGHT),
})


def is_valid_line(r1_move, c1_move, r2_move, c2_move):
    """
    Returns True if and only if the "move directions" form two straight
    lines that are segments of the same line (horizontal, vertical, or
    diagonal), moving in opposite directions.  Only four segment
    combinations are valid:

        * down + no movement upwards
        * left + right
        * SE to NW + NW to SE (northwest/southeast diagonal)
        * NE to SW + SW to NE (southwest/northeast diagonal)

    Parameters r1_move & c1_move: The direction to check in one direction
                from (r,c)
    Precondition: none

    Parameters r2_move & c2_move: The direction to check in the other direction
                from (r,c)
    Precondition: none
    """
    for mv in (r1_move, c1_move, r2_move, c2_move):
        if type(mv) != int or mv not in (MV_LEFT, MV_RIGHT, MV_UP, MV_DOWN, NO_MOVE):
            return False
    if r1_move == c1_move == NO_MOVE:
        return False
    return (r1_move, c1_move, r2_move, c2_move) in _VALID_LINE_MOVES
