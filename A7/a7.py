import dice

class Rules():
    """ A class to store some of the basic assumptions and rules of the game. """

    NUM_DICE = 5

    # Numbers for each of the 13 categories
    CHANCE = 0
    ONES = 1
    TWOS = 2
    THREES = 3
    FOURS = 4
    FIVES = 5
    SIXES = 6
    THREE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 9
    SM_STRAIGHT = 10
    LG_STRAIGHT = 11
    YAHTZEE = 12
    NUM_CATEGORIES = 13
    FULL_HOUSE_PTS = 25
    SM_STRAIGHT_PTS = 30
    LG_STRAIGHT_PTS = 40
    YAHTZEE_PTS = 50

    names = ["Chance", "Ones", "Twos", "Threes", "Fours", "Fives", "Sixes",\
             "3 of a kind", "4 of a kind", "Full House", "Small Straight",\
             "Large Straight", "Yahtzee (5x!)"]

    descriptions = [" -- sum all 5 dice ",
                    "   -- sum 1s only    ",
                    "   -- sum 2s only    ",
                    " -- sum 3s only    ",
                    "  -- sum 4s only    ",
                    "  -- sum 5s only    ",
                    "  -- sum 6s only    ",
                    " -- sum all 5 ",
                    " -- sum all 5 ",
                    "      -- "+str(FULL_HOUSE_PTS)+" pts",
                    " -- "+str(SM_STRAIGHT_PTS)+" pts",
                    " -- "+str(LG_STRAIGHT_PTS)+" pts",
                    "  -- "+str(YAHTZEE_PTS)+" pts"]


# Do not modify Category and Chance!
class Category():
    """
    This is the Category class. You will need to create its subclasses to
    represent the different categories in Yahtzee. The Chance class is an
    example of one way to implement a category. You may choose to implement
    the categories differently, but you must have a way to represent each
    category and its associated score.
    """

    def __init__(self, index):
        """
        Creates an instance of a Category with the following attributes:

        index:      [int] which scorecard entry this is associated with
        is_filled:  [bool] whether a hand has been assigned to this category
                    (this is always False in the beginning)
        points:     [int] once a hand as been associated with this category,
                    the points attribute will reflect the score
        max_points: [int] the best score one can get with this category. this
                    field will be used for the scoreboard to let users know
                    how many points they stand to earn under this category

        Precondition: index is a valid category index (0-12)
        """
        assert index >= 0, "index must be a positive integer"
        assert index <= Rules.YAHTZEE, \
            "index must be no larger than "+str(Rules.YAHTZEE)
        self.index = index
        self.is_filled = False
        self.points = 0
        self.max_points = Rules.NUM_DICE * dice.Die.NUM_SIDES

    def score(self, hand):
        """
        Default score implementation that can be overridden by subclasses.

        This method does the following:
        1. Set the `is_filled` attribute to True
        2. Set the `points` attribute to the appropriate number of points,
            given the hand and category

        Returns None

        Default behavior: set points to 0.
        Subclasses must override this method for category-specific scoring.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        self.is_filled = True
        self.points = 0

    def __str__(self):
        """ Returns a human-readable string representation of the Category. """
        end = "/"+str(self.max_points)+"]"
        if not self.is_filled:
            scoretext = " [ "+end
        else:
            scoretext = " ["+str(self.points)+end
        return str(self.index) + ": "+ Rules.names[self.index]+\
            Rules.descriptions[self.index] + scoretext


class Chance(Category):
    """
    Chance is the simplest category in Yahtzee. Any 5-dice hand meets the
    criteria to count for Chance. The score is the sum of the values of all
    the dice in the hand.
    """

    def __init__(self, index):
        assert index == Rules.CHANCE, "index must be " + str(Rules.CHANCE)
        super().__init__(index)


    def score(self, hand):
        """
        When Chance is scored, simply sum the value of all dice in the hand.
        Also mark the category as filled. Each category can only be used once.
        """
        self.points = hand.score()
        self.is_filled = True

class UpperSection(Category):
    """
    UpperSection is the one of the two major categories in Yahtzee. Any 5-dice
    hand meets the criteria to count for UpperSection. The score is the sum
    of dice that matches the target number. The target number ranges from
    1-6(inclusive).
    """

    def __init__(self, index, target):
        """
        Creates an UpperSection category.

        index:  [int] which scorecard entry this is
        target: [int] the die face value to sum

        Precondition: index is between Rules.ONES and Rules.SIXES inclusive
                  target is between 1 and dice.Die.NUM_SIDES inclusive
        """
        assert Rules.ONES <= index <= Rules.SIXES, \
        "index must be between" + str(Rules.ONES) + ' and ' + str(Rules.SIXES)
        super().__init__(index)
        self.target = target
        self.max_points = Rules.NUM_DICE * target


    def score(self, hand):
        """
        Sums only the dice whose value equals self.target.
        Sets is_filled to True.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        self.is_filled = True
        total = 0
        for die in hand.get_dice():
            if die.value == self.target:
                total += die.value
        self.points = total


class LowerSection(Category):
    """
    LowerSection is the one of the two major categories in Yahtzee. Any 5-dice
    hand meets the criteria to count for LowerSection. The base class that
    includes Three of a Kind, Four of a Kind, Full House, Small
    Straight, Large Straight, and Yahtzee in the LowerSection of the game.
    """

    def __init__(self, index):
        """
        Creates a LowerSection category.

        index: [int] which scorecard entry this is

        Precondition: index is between Rules.THREE_OF_A_KIND and
                  Rules.YAHTZEE inclusive
        """
        assert Rules.THREE_OF_A_KIND <= index <= Rules.YAHTZEE
        super().__init__(index)


    def _rep(self,hand):
        """
        Returns a dict mapping die value -> count for all dice in hand.

        Precondition: hand is a Hand object
        """
        rep = {}
        for die in hand.get_dice():
            if die.value in rep:
                rep[die.value] += 1
            else:
                rep[die.value] = 1
        return rep


class FixedPoints(LowerSection):
    """
    Represents lower section categories that award a fixed number of
    points if the hand meets the category criteria, or 0 otherwise.
    Handles Full House, Small Straight, Large Straight, and Yahtzee.

    Attributes:
        fixed_score: [int] the number of points awarded when the criteria is met
    """
    def __init__(self, index, fixed_score):
        """
        Creates a FixedPoints category.

        index:       [int] which scorecard entry this is
        fixed_score: [int] points awarded when criteria is met

        Precondition: index is one of Rules.FULL_HOUSE, Rules.SM_STRAIGHT,
                      Rules.LG_STRAIGHT, or Rules.YAHTZEE
                      fixed_score is a positive integer
        """
        assert Rules.FULL_HOUSE <= index <= Rules.YAHTZEE
        assert type(fixed_score) == int and fixed_score > 0
        super().__init__(index)
        self.fixed_score = fixed_score
        self.max_points = fixed_score


    def _criteria(self, hand):
        """
        Returns True if hand meets this category's criteria.
        Default to False so subclasses must override

        Precondition: hand is a Hand object
        """
        return False


    def score(self, hand):
        """
        Sets points to fixed_score if _criteria(hand) is True, else 0.
        Sets is_filled to True.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        self.is_filled = True
        if self._criteria(hand):
            self.points = self.fixed_score
        else:
            self.points = 0


class FullHouse(FixedPoints):
    """
    Full House: exactly 3 dice of one value and 2 of another.
    Awards Rules.FULL_HOUSE_PTS if criteria met, else 0.
    """
    def __init__(self, index):
        """
        Initializes a Full House category.

        Precondition: index == Rules.FULL_HOUSE
        """
        assert index == Rules.FULL_HOUSE
        super().__init__(index, Rules.FULL_HOUSE_PTS)


    def _criteria(self, hand):
        """
        Returns True if hand has exactly two distinct values where one
        appears 2 times and the other appears 3 times.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        dic = self._rep(hand)
        if len(dic) != 2:
            return False
        else:
            acc = 0
            nlist = [2,3]
            for value in dic:
                if dic[value] in nlist:
                    acc += 1
                else:
                    acc += 0
            if acc == 2:
                return True
            else:
                return False


class SmStraight(FixedPoints):
    """
    Small Straight: hand contains any sequence of four consecutive numbers.
    Awards Rules.SM_STRAIGHT_PTS if criteria met, else 0.
    """
    def __init__(self, index):
        """
        Initializes a Small Straight category.

        Precondition: index == Rules.SM_STRAIGHT
        """
        assert index == Rules.SM_STRAIGHT
        super().__init__(index, Rules.SM_STRAIGHT_PTS)


    def _criteria(self, hand):
        """
        Returns True if hand contains any sequence of four consecutive
        numbers (1-2-3-4, 2-3-4-5, or 3-4-5-6).

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        dlist = self._rep(hand)
        if 1 in dlist and 2 in dlist and 3 in dlist and 4 in dlist:
            return True
        if 2 in dlist and 3 in dlist and 4 in dlist and 5 in dlist:
            return True
        if 3 in dlist and 4 in dlist and 5 in dlist and 6 in dlist:
            return True
        return False


class LgStraight(FixedPoints):
    """
    Large Straight: hand contains any sequence of five consecutive numbers.
    Awards Rules.LG_STRAIGHT_PTS if criteria met, else 0.
    """
    def __init__(self, index):
        """
        Initializes a Large Straight category.

        Precondition: index == Rules.LG_STRAIGHT
        """
        assert index == Rules.LG_STRAIGHT
        super().__init__(index, Rules.LG_STRAIGHT_PTS)


    def _criteria(self, hand):
        """
        Returns True if hand contains any sequence of five consecutive
        numbers (1-2-3-4-5 or 2-3-4-5-6).

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        dlist = self._rep(hand)
        if 1 in dlist and 2 in dlist and 3 in dlist and 4 in dlist and 5 in dlist:
            return True
        if 2 in dlist and 3 in dlist and 4 in dlist and 5 in dlist and 6 in dlist:
            return True
        return False


class Yahtzee(FixedPoints):
    """
    Yahtzee: All 5 dice have the same value.
    Awards Rules.YAHTZEE if criteria met, else 0.
    """
    def __init__(self, index):
        """
        Initializes a Yahtzee category.

        Precondition: index == Rules.YAHTZEE
        """
        assert index == Rules.YAHTZEE
        super().__init__(index, Rules.YAHTZEE_PTS)


    def _criteria(self, hand):
        """
        Returns True if hand has all five of the same values.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        dic = self._rep(hand)
        if len(dic) != 1:
            return False
        else:
            return True


class SumHand(LowerSection):
    """
    Represents Three of a Kind and Four of a Kind.
    If at least n dice share the same value, score = sum of all 5 dice.
    Otherwise score = 0.
    """
    def __init__(self, index, n):
        """
        Creates a SumHand category.

        index: [int] which scorecard entry this is
        n:     [int] minimum number of matching dice required

        Precondition: index is Rules.THREE_OF_A_KIND or Rules.FOUR_OF_A_KIND
                      n is 3 or 4
        """
        assert index == Rules.THREE_OF_A_KIND or index == Rules.FOUR_OF_A_KIND
        assert type(n) == int
        assert n == 3 or n == 4
        super().__init__(index)
        self.n = n


    def score(self, hand):
        """
        Sets points to sum of all 5 dice if any value appears >= n times.
        Otherwise sets points to 0. Sets is_filled to True.

        Precondition: hand is a Hand object
        """
        assert isinstance(hand, dice.Hand)
        self.is_filled = True
        rep = self._rep(hand)
        for value in rep:
            if rep[value] >= self.n:
                self.points = hand.score()
                return
        self.points = 0


class Scorecard():
    """
    The scorecard tells you what categories there are, what points can be
    earned, which ones have been filled, and what your total score is so far.
    """

    def __init__(self):
        """
        Instance attributes:
          total_score: [int] tells you how  many points have been earned
          categories: [list of Category] there are 13 categories in the game
                  and this list keeps track of each of them
        """
        self.total_score = 0
        self.categories = [None]*Rules.NUM_CATEGORIES
        self.categories[Rules.CHANCE] = Chance(Rules.CHANCE)
        self.categories[Rules.ONES] = UpperSection(Rules.ONES, 1)
        self.categories[Rules.TWOS] = UpperSection(Rules.TWOS, 2)
        self.categories[Rules.THREES] = UpperSection(Rules.THREES, 3)
        self.categories[Rules.FOURS] = UpperSection(Rules.FOURS, 4)
        self.categories[Rules.FIVES] = UpperSection(Rules.FIVES, 5)
        self.categories[Rules.SIXES] = UpperSection(Rules.SIXES, 6)
        self.categories[Rules.THREE_OF_A_KIND] = SumHand(Rules.THREE_OF_A_KIND, 3)
        self.categories[Rules.FOUR_OF_A_KIND] = SumHand(Rules.FOUR_OF_A_KIND, 4)
        self.categories[Rules.FULL_HOUSE] = FullHouse(Rules.FULL_HOUSE)
        self.categories[Rules.SM_STRAIGHT] = SmStraight(Rules.SM_STRAIGHT)
        self.categories[Rules.LG_STRAIGHT] = LgStraight(Rules.LG_STRAIGHT)
        self.categories[Rules.YAHTZEE] = Yahtzee(Rules.YAHTZEE)

    # --------- Do not modify any of the code below ---------

    def cat_prompt(self):
        print(self)
        print("How would you like to categorize these dice?")

    def set_hand(self, hand, choice):
        """ Associates a hand with one of the game categories. """
        self.categories[choice].score(hand)
        s = self.categories[choice].points
        print("You just earned "+str(s)+" points!\n")
        self.total_score += s

    def __str__(self):
        """ Prints out the scorecard, one category (row) at a time. """
        result = ""
        for c in self.categories:
            result += str(c)+"\n"
        return result

    def choice_okay(self, choice):
        """
        Makes the game more usable by not letting the user select a category
        that has already been chosen or that is not valid.
        """
        if not choice.isnumeric():
            print("Please enter a number.")
            return False
        choice = int(choice)
        if (choice < 0):
            print("category index must be a positive integer.")
            return False
        if (choice > Rules.YAHTZEE):
            print("The largest category index in Yahtzee is "+str(Rules.YAHTZEE))
            return False
        if (self.categories[choice] == None):
            print("This category has not been implemented yet.")
            return False
        if (self.categories[choice].is_filled):
            print("That category has already been filled.")
            return False
        return True

    def get_choice(self):
        """
        Prompts the user to pick a category that they wish apply
        their current hand to.
        """
        choice = input("Your choice: ")
        while(not self.choice_okay(choice)):
            choice = input("Your choice: ")
        return int(choice)

def get_hand():
    """ Rolls the dice and allows the user to re-roll up to 2 more times. """
    print("Rolling the dice...")
    hand = dice.Hand(Rules.NUM_DICE)
    if hand.initiate_reroll():
        hand.initiate_reroll()
    return hand

if __name__=='__main__':
    sc = Scorecard()
    print("Welcome to Yahtzee!")
    print(sc)
    n_turns = Rules.NUM_CATEGORIES - sc.categories.count(None)

    while (n_turns > 0):
        print("You have "+str(n_turns)+" turns left.")
        hand = get_hand()
        sc.cat_prompt()
        choice = sc.get_choice()
        sc.set_hand(hand, choice)
        print(sc)
        print("Current score = "+str(sc.total_score))
        print("--------------------------------------------")
        n_turns -= 1

    print("FINAL SCORE = "+str(sc.total_score)+"\nThanks for playing!")
