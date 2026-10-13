# dice.py

""" A module that supports rolling and displaying lone dice."""

import random

random.seed(11)

""" Helper class that prints messages."""
class Printer():
    print_f = True

    @staticmethod
    def print_bad_mask_len(n):
        """ Precondition: n is an int """
        if Printer.print_f:
            print("Mask should be "+str(n)+" characters long.")

    @staticmethod
    def print_bad_mask_01():
        if Printer.print_f:
            print("Mask can contain only 0 or 1.")

    @staticmethod
    def print_rerolling(n):
        """ Precondition: n is an int """
        if Printer.print_f:
            print("re-rolling die "+str(n))

    @staticmethod
    def print_it(thing):
        """ Precondition: thing is anything that can be printed """
        if Printer.print_f:
            print(thing)

    @staticmethod
    def prompt_roll(n):
        """ Precondition: n is an int indicating how big a Hand is. """
        if Printer.print_f:
            print("Which dice would you like to re-roll?")
            print("For each die, 0 means keep, 1 means re-roll.")
            print("Press Return for '"+"0"*n+"'.")

    @staticmethod
    def print_score(n):
        """ Precondition: n is an int """
        if Printer.print_f:
            print("Your current score is "+str(n))

    @staticmethod
    def print_tally(i, b):
        """ Precondition: i is an int representing a Die value
                        b is a bool indicating whether that value is in the hand
        """
        if Printer.print_f:
            print("Got "+str(i)+"s? "+str(b))

    @staticmethod
    def print_thanks():
        if Printer.print_f:
            print("Thanks for playing!")

""" Helper class that simplifies the ascii art stringification of a die."""
class Dots():

    NUM_ROWS = 5    # ascii art dice are 5 rows tall

    # all ascii art dice begin and end with line.
    # the middle rows are a combination of these other 5 strings
    line = ".-------."
    nada = "|       |"
    one  = "|   O   |"
    two  = "| O   O |"
    left = "| O     |"
    right= "|     O |"

    """Below is a list of lists. Each list contains the strings needed to
    print out each of the possible dice you might want to draw.

    Example: a dice with value 4 is:
        ".-------."   line
        "| O   O |"   two
        "|       |"   nada
        "| O   O |"   two
        ".-------."   line
    so below you'll see art[4] set to [line,two,nada,two,line]
    """
    art = [[line,nada,nada,nada,line], # the empty Die
           [line,nada,one,nada,line],  # a Die with value 1
           [line,left,nada,right,line],# a Die with value 2
           [line,left,one,right,line], # a Die with value 3
           [line,two,nada,two,line],   # a Die with value 4
           [line,two,one,two,line],    # a Die with value 5
           [line,two,two,two,line]]    # a Die with value 6

class Die():
    """Instances are 6-sided dice.

    This is a somewhat simplified version of the Die introduced in lecture.
    This is all you need for A7.
    """

    NUM_SIDES = 6

    def __init__(self, val=None):
        """ Initializer: makes a new Die
            Precondition: val must be an integer from 1 to 6
                          if no val provided, value will be chosen randomly
        """
        if val != None:
            assert type(val)== int, "die value must be an int"
            assert val > 0, "die value must be greater than 0"
            assert val <= Die.NUM_SIDES, "die value can be at most " + \
                str(Die.NUM_SIDES)
            self.value = val
        else:
            self.roll()

    def __str__(self):
        """Returns: the ascii art string version of the die"""
        mystring = ""
        for row in range(Dots.NUM_ROWS):
            mystring += Dots.art[self.value][row]+"\n"
        return mystring

    def roll(self):
        """ Picks a new random integer to be the new value of the Die """
        self.value = random.randint(1,Die.NUM_SIDES) # invariant maintained

class Hand():
    """ An instance is a list of dice. The dice can be rolled, re-rolled, and
    printed in a cool ASCII art format. The hand can also add up all the values
    of its dice and state whether or not the hand has a particular number
    in it or not. (e.g., "Does this hand have any 3s?")
    """

    """ The standard terminal is 80 characters wide. Each ASCII art Die
    requires 9 characters, so we limit the number of dice in a hand to 8.

    A hand must have at least MIN_DICE dice and at most MAX_DICE dice.
    If the user asks for too many dice, they get MAX_DICE instead.
    If the user asks for too few dice, the get MIN_DICE instead.
    """
    MIN_DICE = 1
    MAX_DICE = 8

    def __init__(self, n_dice=1, dice_list=None):
        """
        Initializes the hand in one of two possible ways:
        * using the dice_list provided
        * constructing a list of dice that is n_dice long

        Prints the hand after it's been initialized.

        Precondition: n_dice == len(dice_list) (if dice_list is not None)
                      MIN_DICE <= len(dice_list) <= MAX_DICE (if not None)
        """
        if dice_list != None:
            assert len(dice_list) >= Hand.MIN_DICE, \
                "dice_list must have at least "+str(Hand.MIN_DICE)+" dice"
            assert len(dice_list) <= Hand.MAX_DICE, \
                "dice_list must have at most "+str(Hand.MAX_DICE)+" dice"
            assert n_dice == len(dice_list), \
                "if dice_list is not None, its length must be n_dice"
        self.n_dice = min(max(n_dice, Hand.MIN_DICE),Hand.MAX_DICE)
        if dice_list is None:
            self.mydice = []
            for i in range(0, self.n_dice):
                self.mydice.append(Die())
        else:
            self.mydice = dice_list
        Printer.print_it(self)

    def get_n_dice(self):
        """ At various times, a user will need to know how many dice are in
        the Hand. So the user can call this method and be told.

        Returns: an int that represents how many dice are in the hand.
        """
        return self.n_dice

    def get_dice(self):
        """ At various times, a user will need access to the dice list
        So the user can call this method and be given a list of dice.

        Returns: a list of Die that represents the hand.
        """
        return self.mydice

    def mask_valid(self, mask):
        """ A valid mask must be either:
        * the empty string
        OR
        * a string of length equal to the number of dice in the hand.
          the string must contain only 0's and/or 1's

        If the mask is the wrong length, use the helper function
        print_bad_mask_len() to inform the user.

        If the mask contains anything besides a 0 or a 1, use the helper
        function print_bad_mask_01() to inform the user.

        Returns True if the mask is valid by this definition. Otherwise False.
        """
        if (mask == ""):
            return True
        if len(mask) != self.get_n_dice():
            Printer.print_bad_mask_len(self.get_n_dice())
            return False
        for c in mask:
            if c != '0' and c != '1':
                Printer.print_bad_mask_01()
                return False
        return True

    def contains(self, value):
        """ Checks every die in the hand, looking for `value`

            Returns True if any die in the hand has the value `value`
            Otherwise, returns False.
        """
        for d in self.mydice:
            if d.value == value:
                return True
        return False

    def score(self):
        """Sums up the values of all the dice in the Hand.

        Example:
        if the hand has 4 dice and all of them have the value 2, Return 8
        """
        total = 0
        for d in self.mydice:
            total += d.value
        return total

    def reroll(self, mask):
        """Given a mask, rerolls the die in the hand where the mask
        has a 1

        Example: if the hand has 4 dice,
           - the mask "1000" will reroll only the first die
           - the mask "1111" will reroll all the dice
           - the mask "0000" will reroll none of the dice

        A Die knows how to roll itself. Make use of that instance method.

        Returns True if any dice were rerolled. False if the mask directed
        that no die be rerolled.

        Precondition: mask is a string of exclusively 0s and 1s
                      len(mask) == number of dice in this hand
        """
        if "1" in mask:
            for i in range(0, len(mask)):
                if mask[i] == "1":
                    Printer.print_rerolling(i)
                    self.mydice[i].roll()
            Printer.print_it(self)
            return True
        return False

    def __str__(self):
        """Returns the string that represents the Hand. The pseudo code will
        help you return something like:
        6, 5, 2, 1, 4
        but ultimately, you'll need to return the ASCII art version that
        will print:
        .-------..-------..-------..-------..-------.
        | O   O || O   O || O     ||       || O   O |
        | O   O ||   O   ||       ||   O   ||       |
        | O   O || O   O ||     O ||       || O   O |
        .-------..-------..-------..-------..-------.
        """
        mystring = ""
        for i in range(0, Dots.NUM_ROWS):
            one_row = ""
            for one_die in self.mydice:
                one_row += Dots.art[one_die.value][i]
            mystring += one_row +"\n"
        return mystring

    def initiate_reroll(self):
        Printer.prompt_roll(self.get_n_dice())
        mask = self.get_mask()
        return self.reroll(mask)

    def get_mask(self):
        """Prompts the user for a mask. Keeps prompting the
        user until the mask is valid. returns the valid
        Mask. If the user enters the empty string, converts
        this to all 0s. """
        choice = input("Your reroll mask: ")
        while not self.mask_valid(choice):
            choice = input("Your reroll mask: ")
        if choice == "":
            choice = "0"*self.get_n_dice()
        return choice

if __name__=='__main__':
    n = int(input("How many dice would you like to roll? "))
    hand = Hand(n)
    Printer.print_score(hand.score())
    while hand.initiate_reroll():
        Printer.print_score(hand.score())
    for i in range(1, Die.NUM_SIDES+1):
        Printer.print_tally(i, hand.contains(i))
    Printer.print_thanks()
