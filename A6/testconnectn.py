"""
Test cases for Connect-N

You will want to run this script to test out your code. The advantage of this script over
the connectn program is that you can run it on the early classes, before the class Game
is complete. Passing this test suite does not mean full credit.

"""

import a6board
import a6game
import a6player
import connectn
from consts import *
from cornellasserts import (assert_equals, assert_error, assert_false,
                            assert_not_equals, assert_true)

#### CHANGE THIS TO MATCH YOUR TASK LEVEL (1-4)                 ####
#### OR RUN WITH A COMMAND-LINE ARGUMENT (python a6test.py 4)   ####
TASK_LEVEL = 4

def testPlayer():
    """
    Test function to verify the (human) Player class
    """
    print('Testing the Player class (Task 1)')
    # Test a simple red player
    p = a6player.Player('x')
    assert_equals('Player X',p.getName())
    assert_equals('x',p.getPlayerSymbol())

    # Set the name
    p.setPlayerSymbol('a')
    assert_equals('Player A',p.getName())

    # Verify that we enforce preconditions
    assert_error(a6player.Player, '1')
    assert_error(a6player.Player,'xx')
    assert_error(a6player.Player,'B')
    assert_error(a6player.Player, 0)
    assert_error(p.setPlayerSymbol,'1')
    assert_error(p.setPlayerSymbol,'xx')
    assert_error(p.setPlayerSymbol,'B')
    assert_error(p.setPlayerSymbol,0)


def testBoardA():
    """
    Test function to verify part A of the Board class.
    """
    print('- Part A: Testing the board initialization')
    # Test the board
    b = a6board.Board(3,4,2)
    assert_equals(3,b.getNRows())
    assert_equals(4,b.getNCols())
    assert_equals(2,b.getStreak())

    # Test the defaults
    b = a6board.Board()
    assert_equals(6,b.getNRows())
    assert_equals(7,b.getNCols())
    assert_equals(4,b.getStreak())

    # Verify that we enforce preconditions
    assert_error(a6board.Board,-1,2,1)
    assert_error(a6board.Board,2,-1,1)
    assert_error(a6board.Board,2,2,3)

    # Verify that clear works
    b.setSymbolAt(0,1,'x')
    b.setSymbolAt(1,0,'o')
    b.moves = [(0,1),(1,0)]

    b.clear()
    for r in range(b.getNRows()):
        for c in range(b.getNCols()):
            assert_equals(NOBODY,b.getSymbolAt(r,c))
    assert_equals(0,b.getMoveCount())

    # Let's verify that new board is empty
    b = a6board.Board(10,12,7)
    assert_equals(10,b.getNRows())
    assert_equals(12,b.getNCols())
    assert_equals(7,b.getStreak())

    for r in range(b.getNRows()):
        for c in range(b.getNCols()):
            assert_equals(NOBODY,b.getSymbolAt(r,c))
    assert_equals(0,b.getMoveCount())


def testBoardB():
    """
    Test function to verify part B of the Board class.
    """
    print('- Part B: Testing the board capacity')
    # Fill up the board a bit
    b = a6board.Board(4,6,3)
    tops = [4,3,2,0,1,4]
    for c in range(6):
        for r in range(tops[c]):
            b.setSymbolAt(r,c,'x')

    # Let's see what is available
    for c in range(6):
        full = tops[c] == 4
        assert_equals(tops[c],b.findAvailableRow(c))
        assert_equals(full,b.isFullColumn(c))
    assert_equals(False,b.isFullBoard())

    # Fill the entire board
    for r in range(b.getNRows()):
        for c in range(b.getNCols()):
            b.setSymbolAt(r,c,'x')
    assert_equals(True,b.isFullBoard())

    # And clear it
    b.clear()
    for r in range(b.getNRows()):
        for c in range(b.getNCols()):
            assert_equals(NOBODY,b.getSymbolAt(r,c))
    assert_equals(0,b.getMoveCount())


def testBoardC():
    """
    Test function to verify part C of the Board class.
    """
    print('- Part C: Testing board placement')
    b = a6board.Board(4,6,3)

    # Time to place a piece
    b.place(0,'x')
    assert_equals('x',b.getSymbolAt(0,0))
    assert_equals(1,b.getMoveCount())
    assert_equals((0,0),b.getLastMove())

    b.place(1,'o')
    assert_equals('o',b.getSymbolAt(0,1))
    assert_equals(2,b.getMoveCount())
    assert_equals((0,1),b.getLastMove())

    b.place(0,'y')
    assert_equals('y',b.getSymbolAt(1,0))
    assert_equals(3,b.getMoveCount())
    assert_equals((1,0),b.getLastMove())

    # Check move undo:

    b.undoPlace()
    assert_equals(NOBODY,b.getSymbolAt(1,0))
    assert_equals(2,b.getMoveCount())
    assert_equals((0,1),b.getLastMove())

    # And clear it
    b.clear()
    for r in range(b.getNRows()):
        for c in range(b.getNCols()):
            assert_equals(NOBODY,b.getSymbolAt(r,c))
    assert_equals(0,b.getMoveCount())


def testBoardD():
    """
    Test function to verify part D of the Board class.
    """
    print('- Part D: Testing detectRun in all possible directions')
    b = play_game1()

    # [[ , , , , , , x],
    #  [ , , , , , , x],
    #  [ , , x,o, ,o, x],
    #  [ , ,o, x,o,o, x],
    #  [o,o,o,o, x, x,o],
    #  [ x, x,o, x,o, x, x]]

    # test detectRun looking across
    assert_equals((2, 2, 2, 2),b.detectRun(1,2,2,NO_MOVE,MV_LEFT,NO_MOVE,MV_RIGHT))
    assert_equals(None,b.detectRun(2,2,2,NO_MOVE,MV_LEFT,NO_MOVE,MV_RIGHT))
    assert_equals((1, 0, 1, 3),b.detectRun(2,1,1,NO_MOVE,MV_LEFT,NO_MOVE,MV_RIGHT))
    assert_equals((1, 0, 1, 3),b.detectRun(2,1,0,NO_MOVE,MV_LEFT,NO_MOVE,MV_RIGHT))
    assert_equals((3, 5, 3, 5),b.detectRun(1,3,5,NO_MOVE,MV_LEFT,NO_MOVE,MV_RIGHT))

    # test findNWSE
    assert_equals((3, 5, 3, 5),b.detectRun(1,3,5,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))
    assert_equals(None,b.detectRun(2,3,5,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))

    assert_equals(None,b.detectRun(5,3,2,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))
    assert_equals((3, 2, 0, 5),b.detectRun(4,3,2,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))
    assert_equals((3, 2, 0, 5),b.detectRun(4,2,3,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))
    assert_equals((3, 2, 0, 5),b.detectRun(4,0,5,MV_UP,MV_LEFT,MV_DOWN,MV_RIGHT))

    #test findSWNE
    assert_equals((3, 2, 3, 2),b.detectRun(1,3,2,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))

    assert_equals(None,b.detectRun(2,3,2,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))
    assert_equals(None,b.detectRun(5,3,5,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))
    assert_equals((0, 2, 3, 5),b.detectRun(4,3,5,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))
    assert_equals((0, 2, 3, 5),b.detectRun(4,2,4,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))
    assert_equals((0, 2, 3, 5),b.detectRun(4,0,2,MV_DOWN,MV_LEFT,MV_UP,MV_RIGHT))


def testBoardE():
    """
    Test function to verify part E of the Board class.
    """
    print('- Part E: Testing findWins')

    b = play_game2()
    # [[ , , , , , , ],
    #  [ , , , , , , ],
    #  [ ,x,x, ,x, , ],
    #  [o,o,x,x,x,o,o],
    #  [o,x,o,x,o,x,o],
    #  [x,o,o,x,o,o,x]]

    assert_equals(len(b.findWins(2,3)), 0)

    b.place(3,b.getSymbolAt(2,3))

    endpts = [(3, 3, 0, 3),(3, 1, 3, 4),(0, 0, 3, 3),(3, 3, 0, 6)]
    altEndpts = [(0, 3, 3, 3),(3, 4, 3, 1),(3, 3, 0, 0),(0, 6, 3, 3)]

    wins = b.findWins(3,3)

    assert_true(len(wins) == 4)

    foundAll = True
    for w in zip(endpts,altEndpts):
        foundNext = w[0] in wins or w[1] in wins
        foundAll = foundAll and foundNext

    assert_true(foundAll)


def testBoard():
    """
    Test function to verify the Board class.

    This only tests the Board methods implemented in Tasks 2 and 4.
    """
    if TASK_LEVEL < 2:
        return

    if TASK_LEVEL < 4:
        task = 2
    else:
        task = 4

    print('Testing the Board class (Task '+str(task)+')')
    testBoardA()
    testBoardB()
    testBoardC()

    if TASK_LEVEL >= 4:
        testBoardD()
        testBoardE()


def testGameA():
    """
    Test function to verify the Game class.

    This tests everything but the run() method in Game:

    getBoard, getPlayers, getWinner, __init__, advance, takeTurn
    """
    print('- Part A: Testing the game initialization')

    # Verify that we enforce preconditions
    assert_error(a6game.Game,-1,2,1)
    assert_error(a6game.Game,2,-1,1)
    assert_error(a6game.Game,2,2,3)

    # Valid setup:
    g = a6game.Game(8,5,3)

    # dimensions used correctly?
    b = g.getBoard()
    assert_equals(5,b.getNRows())
    assert_equals(8,b.getNCols())
    assert_equals(3,b.getStreak())

    # _winner attribute defined, but currently None?

    assert_equals(None,g.getWinner())

    # make sure we start with no players
    players = g.getPlayers()
    assert_equals(list,type(players))
    assert_equals(0,len(players))

    # Every player distinct, and advance reaches each one?
    g.addPlayer(a6player.Player('x'))
    g.addPlayer(a6player.Player('o'))
    p0 = g.getCurrent()

    # Make sure the first player is the x player
    assert_equals(a6player.Player,type(p0))
    assert_equals('x',p0.getPlayerSymbol())

    # Make sure all symbols are distinct
    p1 = a6player.Player('x')
    assert_error(g.addPlayer,p1)


def testGameB():
    """
    Test function to verify the Game class.

    This tests version of the Game class completed in Task 3,
    """
    print('- Part B: Testing human players with no win condition')
    # Test that advance works correctly
    g = a6game.Game(4,3,3)
    g.addPlayer(a6player.Player('x'))
    g.addPlayer(a6player.Player('o'))
    p0 = g.getCurrent()
    players = g.getPlayers()

    plast = p0
    for _ in range(len(players[1:])):
        g.advance()
        p1 = plast
        p2 = g.getCurrent()
        assert_not_equals(p1.getPlayerSymbol(),p2.getPlayerSymbol())
        plast = p2

    # Make sure we loop around to beginning
    g.advance()
    assert_equals(p0,g.getCurrent())

    # control for testing takeTurn and run:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('x')
    g.addPlayer(p1)
    p2 = a6player.Player('o')
    g.addPlayer(p2)

    # testing takeTurn and advance
    # inject automatic moves play into p1, p2
    setAutoMoves(p1,[2,2,1,0,1,3,3])

    # This is one move too many for the board.  If run stops correctly on a
    # full board, we'll never reach the last move.
    setAutoMoves(p2,[3,2,1,0,0,3])

    # play these five moves:

    c1 = g.takeTurn(p1)
    g.advance()
    c2 = g.takeTurn(p2)

    assert_equals(2,c1)
    assert_equals(3,c2)

    assert_equals('x',g.getBoard().getSymbolAt(0,2))
    assert_equals('o',g.getBoard().getSymbolAt(0,3))

    # The board so far:
    # [[ , , , ],
    #  [ , , , ],
    #  [ , ,x,o]]

    # test run():  should stop when the rest board has filled
    try:
        g.run()
        # print('DEBUG (testGameB):  full board?\n' + str(g.getBoard()))
    except StopIteration:
        # This means that the game loop ran at least one extra move
        assert_false(True, message='run() did not quit on full game board.')

    assert_true(g.getBoard().isFullBoard())


def testGameC():
    """
    Test function to verify the Game class.

    This tests version of the Game class completed in Task 4.
    """
    print('- Part C: Testing human players with a win condition')
    # control for testing takeTurn and run:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('x')
    g.addPlayer(p1)
    p2 = a6player.Player('o')
    g.addPlayer(p2)

    # testing takeTurn and advance
    # inject automatic moves play into p1, p2
    setAutoMoves(p1,[2,2,1,0,1,3,3])
    setAutoMoves(p2,[3,2,1,0,0,3])

    # Same move set as in testGameB.  X wins on its 4th move (column 0), so
    # the game should stop there.

    # test run():  should stop after p1's 4th move, which wins the game
    g.run()
    # print('DEBUG (testGameB):  did X win?\n' + str(g.getBoard()))
    assert_equals((0,0),g.getBoard().getLastMove())
    assert_equals(p1,g.getWinner())
    assert_equals(7, g.getBoard().getMoveCount())
    assert_false(g.getBoard().isFullBoard())

    ### Test win detection on a full board:
    g = a6game.Game(4,3,3)
    p1 = a6player.Player('x')
    g.addPlayer(p1)
    p2 = a6player.Player('o')
    g.addPlayer(p2)

    assert_true(g.getWinner() == None)
    # This time, the board should fill, with o winning on the final move
    setAutoMoves(p1,[1, 3, 1, 0, 3, 0])
    setAutoMoves(p2,[2, 1, 0, 2, 3, 2])

    g.run()
    # print('DEBUG (testGameB):  did O win?\n' + str(g.getBoard()))

    assert_equals((2,2),g.getBoard().getLastMove())
    assert_true(g.getBoard().isFullBoard())
    assert_equals(p2,g.getWinner())


def testGame():
    """
    Test function to verify the Game class.

    This game varies its tests to match the appropriate Task
    """
    if TASK_LEVEL < 3:
        return

    print('Testing the Game class (Task '+str(TASK_LEVEL)+')')
    testGameA()
    testGameB()
    if TASK_LEVEL >= 4:
        testGameC()

#### Test Utility Functions ####
# You do not need to undersand anything below this line

def setAutoMoves(player,moves,restore=False):
    """
    Injects moves into an object of the Player class.

    This function temporarily overrides the chooseMove method in player. It
    causes that player to run through an iteration of moves until the last
    one is played.

    If restore is true, it restores the original chooseMove method once the
    moves are exhausted.  Otherwise, calls to chooseMove beyond the injected
    moves will result in an error.

    Parameter player: The player to override
    Precondition: player is an instance of Player

    Parameter moves: The moves (columns) to inject
    Precondition: moves is a list of ints

    Parameter restore: Whether to restore chooseMove when done
    Precondition: restore is a bool
    """
    oldChooseFn = player.chooseMove
    moves_id = '_automoves_' + str(id(player))
    moves = iter(moves)
    setattr(player,moves_id,moves)

    def autoChoose(bd):
        """
        Local closure to replace chooseMove

        Parameter board: The board to choose from
        Precondition: board is a Board object that is not full
        """
        assert type(bd) == a6board.Board
        try:
            m = next(getattr(player,moves_id))
            return m
        except StopIteration as e:
            if restore:
                delattr(player,moves_id)
                delattr(player,'chooseMove')
                setattr(player,'chooseMove',oldChooseFn)

                assert not hasattr(player,moves_id)
                return a6player.chooseMove(bd)
            else:
                raise e

    setattr(player,'chooseMove',autoChoose)

    return oldChooseFn


def zzip(z):
    """
    Returns a flattened zip of the list z.

    Zip is used to combine lists of the same length into a single list of
    tuples. This function performs zip on a nested list of lists all of the
    same length.

    The result of this function can be undone with unzip.

    Parameter z: The nested list to zip
    Precondition: z is a list of lists all of the same length
    """
    return list(zip(*z))


def unzzip(u):
    """
    Returns a nested list of lists from a zip flattened list.

    This function undoes the result of zzip.

    Parameter u: The list to unzip
    Precondition: u is a list of tuples, all of the same length
    """
    if len(u) == 0:
        return []

    result = []
    for item in u:
        for p in range(len(item)):
            while p >= len(result):
                result.append([])
            result[p].append(item[p])
    return result


def place_game(board,p1,p2,moves):
    """
    Plays the list of p1/p2 moves in the board.

    This function assumes that it is has to be possible to play every move.
    There is no check for a win, but preconditions prevent playing past a
    full board

    Parameter board: The board to fill
    Precondition: board is a Board object

    Parameter p1: The symbol of the first player
    Precondition: p1 is a symbol string

    Parameter p2: The symbol of the first player
    Precondition: p2 is a symbol string

    Parameter moves: The moves for each player
    Precondition: moves is a two-element tuple of lists of ints
    """
    for i,j in zzip(moves):
        assert board.place(i,p1) >= 0
        assert board.place(j,p2) >= 0

    if len(moves[0]) > len(moves[1]):  # one more p1 move to make
        assert board.place(moves[0][-1],p1)

    return board


def make_game_moves(p1,p2,state,moves):
    """
    Uses state to create a game between p1 and p2, which it plays with moves

    Parameter p1: The symbol of the first player
    Precondition: p1 is a symbol string

    Parameter p2: The symbol of the first player
    Precondition: p2 is a symbol string

    Parameter state: The state necessary to initialize the game board
    Precondition: state is a tuple (width,height,streak)

    Parameter moves: The moves for each player
    Precondition: moves is a two-element tuple of lists of ints
    """
    b = a6board.Board(*state)

    return place_game(b,p1,p2,moves)

#### Some sample, Board-only "games" ####
GAME_SIZE = (6,7,4)
GAME_1_MOVES = ([3, 6, 5, 4, 5, 6], [2, 6, 4, 3, 5, 5])
GAME_2_MOVES = ([3, 3, 3, 4, 1, 2, 0, 1, 2, 6, 5, 4],
                [2, 4, 4, 1, 2, 1, 0, 0, 5, 6, 6, 5])


def play_game0():
    """
    Creates the following game:

    [[ , , , , , , ],
     [ , , , , , , ],
     [ , , , , ,o, ],
     [ , , , , ,o,x],
     [ , , ,o,x,x,o],
     [ , ,o,x,o,x,x]]
    """
    return make_game_moves('x','o',GAME_SIZE,GAME_1_MOVES)


def play_game1():
    """
    Creates the following game:

    [[ , , , , , ,x],
     [ , , , , , ,x],
     [ , ,x,o, ,o,x],
     [ , ,o,x,o,o,x],
     [o,o,o,o,x,x,o],
     [x,x,o,x,o,x,x]]
    """
    p1,p2 = 'x', 'o'
    bd = play_game0()

    nextMoves = ([3,1,0,2,6,6,6],[2,1,2,4,0,3])
    return place_game(bd,p1,p2,nextMoves)


def play_game2():
    """
    Creates the following game:

    [[ , , , , , , ],
     [ , , , , , , ],
     [ ,x,x, ,x, , ],
     [o,o,x,x,x,o,o],
     [o,x,o,x,o,x,o],
     [x,o,o,x,o,o,x]]

    This one will have four wins after x plays (3,3)
    """

    return make_game_moves('x','o',GAME_SIZE,GAME_2_MOVES)


def set_task_level():
    """
    Sets the active TASK_LEVEL
    """
    global TASK_LEVEL
    import sys
    if len(sys.argv) > 1:
        try:
            level = int(sys.argv[1])
            if 1 <= level <= 5:
                TASK_LEVEL = level
            else:
                raise ValueError("TASK_LEVEL must be 1-4:", level)
        except ValueError:
            pass
        print('TASK_LEVEL is currently',TASK_LEVEL)


if __name__ == '__main__':
    set_task_level()
    testPlayer()
    testBoard()
    testGame()
    print('Assignment 6 passed all tests up to Task',TASK_LEVEL)
