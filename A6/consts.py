"""
Constants for Connect-N

To reduce errors, we like to replace commonly occurring values with
variable names.  This allows us to centralize our commitments to
various hard-coded values.  In turn, this reduces the maintenance
burden if we ever want to change one of these values, and it reduces
the chances that we'll introduce new bugs when we do.

"""


# The constant representing an empty board piece
NOBODY = " "

### BOARD SIZE ###
# Number of rows in the board
DEFAULT_ROWS   = 6
# Number of columns in the board
DEFAULT_COLS   = 7
# Number of pieces needed to win
DEFAULT_STREAK = 4

# smallest valid number of rows,columns, and minimum win winlength
MIN_DIMENSION = 3
# largest valid number of rows,columns, and minimum win winlength
MAX_DIMENSION = 10
# longest valid minimum win length requirement
MAX_STREAK = 10

# Move directions for the consecutive run checks:
MV_LEFT = -1
MV_RIGHT = 1
MV_UP = 1
MV_DOWN = -1
NO_MOVE = 0
