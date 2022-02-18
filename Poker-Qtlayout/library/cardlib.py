""" Playing card library for texas poker game
Authors: Iman Shahmari Khalid Barkhad"""

version = "1.0"  # Module global variable
from enum import IntEnum
from collections import Counter


# Creating super class PlayingCard

class PlayingCard:
    """
    Base class for creating playing cards
    """

    def __init__(self, suit):
        self.suit = suit

    def __lt__(self, other):
        """
                overload < operator between self value and other value
                :param other:
                :return: True or False
                """
        if self.get_value() == other.get_value():
            return self.suit < other.suit
        else:
            return self.get_value() < other.get_value()

    def __eq__(self, other):
        """
        Return True if two cards are equal
        :param other: other cards
        :return: True
        """

        return self.get_value() == other.get_value() and self.suit == other.suit

    def __str__(self):
        """
        stringify card attributes
        :return: string of cards attributes
        """
        return str(self.suit) + ',' + str(self.get_value())

    def get_value(self):
        """A super class for poker game containing subclasses Numbered,Jack,Queen,King cards

        """
        raise NotImplementedError("missing")


# sub class numbered cards
class NumberedCard(PlayingCard):
    """
        Class for numbered playing cards, inherits from parent abstract class PlayingCard
        """

    def __init__(self, suit, value):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        return self.value


# sub class Jackcard
class JackCard(PlayingCard):
    def get_value(self):
        return 11


# sub class QueenCard
class QueenCard(PlayingCard):
    def get_value(self):
        return 12


# sub class KingCard
class KingCard(PlayingCard):
    def get_value(self):
        return 13


# sub class AceCard
class AceCard(PlayingCard):
    def get_value(self):
        return 14


# Creating class for suits
class Suit(IntEnum):
    """
        class that defines suits,
        enumerated for later purposes although the values are random and not important
        """
    Clubs = 0
    Diamonds = 1
    Hearts = 2
    Spades = 3


class StandardDeck:
    """
        create deck class
        """

    def __init__(self):
        """
                for loops that construct the deck
                """
        cards = []
        for i in range(2, 11):
            for suit in Suit:
                cards.append(NumberedCard(suit, i))
        cards_pic = []
        for suit in Suit:
            cards_pic.append(JackCard(suit))
            cards_pic.append(QueenCard(suit))
            cards_pic.append(KingCard(suit))
            cards_pic.append(AceCard(suit))
        self.cards = cards + cards_pic

    def shuffle(self):
        """
                method that shuffles the deck randomly
                :return: shuffled deck
                """
        import random
        random.shuffle(self.cards)

    def take_card(self):
        """
                method that takes the top card and removes it from deck
                :return: the top card
                """
        mycard = self.cards[0]
        del self.cards[0]
        return mycard


class Hand:
    """
        class Hand that defines the cards on the table
        """

    def __init__(self):
        self.cards = []

    def add_new_card(self, newcard):
        """
        add new card to Hand

        :param newcard: card to be added
        :return: append card list in hand
                """
        self.cards.append(newcard)

    def drop_cards(self, indexes):
        """
                drop cards from hand based on input index

                :param indexes: int
                :return:
                """
        for index in sorted(indexes, reverse=True):
            del self.cards[index]

    def sort_cards(self):
        """
                method that sorts cards in hand
                :return: sorted card list
                """
        self.cards.sort()

    def best_poker_hand(self, Deck_cards=[]):  # change to cards
        """
                method that computes best poker hand based on cards in hand and cards in input argument
                :param Deck_cards: card object
                :return: PokerHand object
                """
        all_cards = self.cards + Deck_cards
        best_combo = PokerHand(all_cards)
        return best_combo


class Handtype(IntEnum):
    """
        class that ranks the different hand types based on relative strength
        """
    high_card = 0
    one_pair = 1
    two_pair = 2
    three_of_a_kind = 3
    straight = 4
    flush = 5
    full_house = 6
    four_of_a_kind = 7
    straight_flush = 8


class PokerHand:
    """
        class PokerHand that creates PokerHand objects based on cards in input argument
        """

    def __init__(self, cards_combined):
        self.cards_combined = cards_combined
        self.type = []
        self.high_card()
        self.one_pair()
        self.two_pair()
        self.three_of_a_kind()
        self.straight()
        self.check_flush()
        self.check_full_house()
        self.four_of_a_kind()
        self.check_straight_flush()

    def __lt__(self, other):
        """
        overload < operator to compare PokerHand objects
        :param other:
        :return: True or False
                """
        if self.type == other.type:
            if isinstance(self.highest_value, list):
                return tuple(self.highest_value) < tuple(other.highest_value)
            elif isinstance(self.highest_value, int):
                return self.highest_value < other.highest_value
        else:
            return self.type < other.type

    def __eq__(self, other):

        if self.type == other.type:
            if self.highest_value == other.highest_value:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return "(" + str(self.type) + ',' + str(self.highest_value) + ")"

    def straight(self):
        """
                def straight HandType
                check for straight
                :return: highest value
                """
        values = []
        cards = self.cards_combined
        cards.sort(reverse=True)

        for card in cards:
            values.append(card.get_value())

        for card in cards:
            if card.get_value() == 14:
                values.append(1)

        for card in cards:
            found_straight = True

            for k in range(1, 5):
                if (card.get_value() - k) not in values:
                    found_straight = False
                    break
            if found_straight:
                self.type = Handtype.straight
                self.highest_value = card.get_value()

    def check_straight_flush(self):
        """
        Checks for the best straight flush in a list of cards (may be more than just 5)

        :param cards: A list of playing cards.
        :return: None if no straight flush is found, else the value of the top card.
                    """
        vals = [(c.get_value(), c.suit) for c in self.cards_combined] \
               + [(1, c.suit) for c in self.cards_combined if c.get_value() == 14]  # Add the aces!
        for c in reversed(self.cards_combined):  # Starting point (high card)
            # Check if we have the value - k in the set of cards:
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                self.highest_value = c.get_value()
                self.type = Handtype.straight_flush

    def check_full_house(self):
        from collections import Counter
        """
        Checks for the best full house in a list of cards (may be more than just 5)

        :param cards: A list of playing cards
        :return: None if no full house is found, else a tuple of the values of the triple and pair.
        """
        value_count = Counter()
        for c in self.cards_combined:
            value_count[c.get_value()] += 1
        # Find the card ranks that have at least three of a kind
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        # Find the card ranks that have at least a pair
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()

        # Threes are dominant in full house, lets check that value first:
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    self.type = Handtype.full_house
                    self.highest_value = [three, two]

    def check_flush(self):
        """
                check for flush HandType
                :return: values in flush
                """

        suit_count = Counter()
        for k in self.cards_combined:
            suit_count[k.suit] += 1
        # Only suits matter in flush, checks if all suits are the same
        suits_number = [c[0] for c in suit_count.items() if c[1] >= 5]
        if len(suits_number) == 1:
            self.type = Handtype.flush
            print(suits_number[0])
            values = [item.get_value() for item in self.cards_combined if item.suit == suits_number[0]]
            self.highest_value = values

    def four_of_a_kind(self):
        """
            check for four of a kind HandType

            :return: values in four of a kind
                        """
        from collections import Counter
        value_count = Counter()
        for c in self.cards_combined:
            value_count[c.get_value()] += 1
        fours = [v[0] for v in value_count.items() if v[1] >= 4]
        fours.sort()
        ones = [v[0] for v in value_count.items() if v[1] >= 1]
        ones.sort()
        for four in reversed(fours):
            for one in reversed(ones):
                if one != four:
                    self.type = Handtype.four_of_a_kind
                    self.highest_value = [four]

                    values = [c.get_value() for c in self.cards_combined]
                    values.sort()
                    values = list(set(values))
                    values.remove(four)
                    self.highest_value.append(values[-1])

    def three_of_a_kind(self):
        """
            check for three of a kind HandType

            :return: values in three of a kind
                            """
        from collections import Counter
        value_count = Counter()
        for c in self.cards_combined:
            value_count[c.get_value()] += 1
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        zeros = [v[0] for v in value_count.items() if v[1] >= 0]
        zeros.sort()
        for three in reversed(threes):
            for zero in reversed(zeros):
                if zero != three:
                    self.type = Handtype.three_of_a_kind
                    self.highest_value = [three]

                    values = [c.get_value() for c in self.cards_combined]
                    values.sort()
                    values = list(set(values))
                    values.remove(three)
                    values.sort(reverse=True)
                    print(values)
                    for v in values:
                        self.highest_value.append(v)


    def two_pair(self):
        """
            check for two pair HandType

            :return: high values in two pairs
                            """

        from collections import Counter
        value_count = Counter()
        for c in self.cards_combined:
            value_count[c.get_value()] += 1
        twos_1 = [v[0] for v in value_count.items() if v[1] >= 2]
        twos_1.sort()
        twos_2 = [v[0] for v in value_count.items() if v[1] >= 2]
        twos_2.sort()
        for two_1 in reversed(twos_1):
            for two_2 in reversed(twos_2):
                if two_2 != two_1:
                    self.type = Handtype.two_pair
                    self.highest_value = [two_2, two_1]

                    values = [c.get_value() for c in self.cards_combined]
                    values.sort()
                    values = list(set(values))
                    values.remove(two_1)
                    values.remove(two_2)
                    values.sort(reverse=True)
                    for v in values:
                        self.highest_value.append(v)

    def one_pair(self):
        """
            check for one pair HandType

            :return: high value in one pair
                                    """
        from collections import Counter
        value_count = Counter()
        for c in self.cards_combined:
            value_count[c.get_value()] += 1
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()
        zeros = [v[0] for v in value_count.items() if v[1] >= 0]
        zeros.sort()
        for two in reversed(twos):
            for zero in reversed(zeros):
                if zero != two:
                    self.type = Handtype.one_pair
                    other_values = [c.get_value() for c in self.cards_combined]
                    self.highest_value = [two]
                    other_values.remove(two)
                    self.highest_value = self.highest_value + other_values

    def high_card(self):
        """
            check for high card HandType

            :return: high card as well as the cards coming after
                                    """
        all_values = [c.get_value() for c in self.cards_combined]
        all_values.sort(reverse=True)
        self.type = Handtype.high_card
        self.highest_value = all_values
