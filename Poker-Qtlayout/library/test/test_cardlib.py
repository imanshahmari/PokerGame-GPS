from cardlib import *


# This test assumes you call your suit class "Suit" and the colours "Hearts and "Spades"
def test_cards():
    h5 = NumberedCard(Suit.Hearts,4)
    assert isinstance(h5.suit, IntEnum)
    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13

    ph = AceCard(Suit.Spades)

    assert ph.get_value() == 14
    assert ph > sk
    assert h5 < sk
    assert h5 == h5


# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_StandardDeck():
    d = StandardDeck()
    c1 = d.take_card()
    c2 = d.take_card()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    assert not d == d2

    d3 = StandardDeck()
    a = d3.cards.copy()
    d3.shuffle()
    b = d3.cards
    assert not a == b


# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_new_card(d.take_card())
    h.add_new_card(d.take_card())
    h.add_new_card(d.take_card())
    h.add_new_card(d.take_card())
    h.add_new_card(d.take_card())
    assert len(h.cards) == 5

    h.sort_cards()
    for i in range(3):
        assert h.cards[i] < h.cards[i+1] or h.cards[i] == h.cards[i+1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]


def test_pokerhands():
    "Test PokerHand types"
    pokerhand_1 = PokerHand([NumberedCard(Suit.Spades,8),NumberedCard(Suit.Spades,7),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Spades,6),NumberedCard(Suit.Spades,8),])
    pokerhand_2 = PokerHand([NumberedCard(Suit.Spades,8),NumberedCard(Suit.Hearts,8),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Clubs,8),NumberedCard(Suit.Diamonds,8),])
    assert pokerhand_1 < pokerhand_2

    "Test highcard"
    h1 = Hand()
    h1.add_new_card(QueenCard(Suit.Diamonds))
    h1.add_new_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_new_card(QueenCard(Suit.Hearts))
    h2.add_new_card(AceCard(Suit.Hearts))

    cl = [NumberedCard(Suit.Diamonds,10), NumberedCard(Suit.Diamonds,9),
          NumberedCard(Suit.Clubs,8), NumberedCard(Suit.Spades,6)]

    ph1 = h1.best_poker_hand(cl)

    assert isinstance(ph1, PokerHand)
    ph2 = h2.best_poker_hand(cl)
    # assert ph1 == PokerHand( <insert your handtype class and data here> )
    # assert ph2 == PokerHand( <insert your handtype class and data here> )

    assert ph1 < ph2

    "Test one pair"
    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert ph3 < ph4
    assert ph1 < ph2

    "Test two pairs"
    pokerhand_3 = PokerHand([NumberedCard(Suit.Spades,8),NumberedCard(Suit.Spades,9),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Hearts,8),NumberedCard(Suit.Hearts,9),])
    pokerhand_4 = PokerHand([NumberedCard(Suit.Diamonds,8),NumberedCard(Suit.Diamonds,9),AceCard(Suit.Spades)
                    ,NumberedCard(Suit.Clubs,8),NumberedCard(Suit.Clubs,9)])
    assert pokerhand_3 == pokerhand_4

    "Test three of a kind"
    pokerhand_5 = PokerHand([NumberedCard(Suit.Spades,8),NumberedCard(Suit.Spades,9),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Hearts,8),NumberedCard(Suit.Hearts,8),])
    pokerhand_6 = PokerHand([NumberedCard(Suit.Spades,7),NumberedCard(Suit.Spades,9),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Hearts,7),NumberedCard(Suit.Hearts,7),])
    assert pokerhand_5 > pokerhand_6

    "Test straight"
    pokerhand_7 = PokerHand([NumberedCard(Suit.Spades,2),NumberedCard(Suit.Spades,3),AceCard(Suit.Clubs)
                    ,NumberedCard(Suit.Hearts,4),NumberedCard(Suit.Hearts,5)])
    pokerhand_8 = PokerHand([KingCard(Suit.Spades),AceCard(Suit.Clubs),JackCard(Suit.Hearts)
                    ,QueenCard(Suit.Clubs),NumberedCard(Suit.Hearts,10)])
    pokerhand_9 = PokerHand([KingCard(Suit.Diamonds), AceCard(Suit.Spades), JackCard(Suit.Spades)
                                , QueenCard(Suit.Spades), NumberedCard(Suit.Spades, 10), NumberedCard(Suit.Hearts, 9)])
    assert pokerhand_8 > pokerhand_7
    assert pokerhand_9 > pokerhand_7

    "Test flush"
    pokerhand_10 = PokerHand([NumberedCard(Suit.Spades, 7), NumberedCard(Suit.Spades, 3), AceCard(Suit.Spades)
                  , NumberedCard(Suit.Spades, 4), NumberedCard(Suit.Spades, 5)])
    pokerhand_10_1 = PokerHand([NumberedCard(Suit.Spades, 7), NumberedCard(Suit.Spades, 3), KingCard(Suit.Spades)
                  , NumberedCard(Suit.Spades, 4), NumberedCard(Suit.Spades, 5)])
    assert pokerhand_10.highest_value == [14,7,5,4,3]
    assert pokerhand_10.type == Handtype.flush
    assert pokerhand_10 > pokerhand_10_1


    "Test fullhouse"
    pokerhand_11 = PokerHand([NumberedCard(Suit.Spades, 8), NumberedCard(Suit.Spades, 9), NumberedCard(Suit.Diamonds, 9)
                                , NumberedCard(Suit.Hearts, 8), NumberedCard(Suit.Diamonds, 8) ])
    pokerhand_11_1 = PokerHand([NumberedCard(Suit.Spades, 8), NumberedCard(Suit.Spades, 7), NumberedCard(Suit.Diamonds, 7)
                                , NumberedCard(Suit.Hearts, 8), NumberedCard(Suit.Diamonds, 8) ])
    assert pokerhand_11.type == Handtype.full_house
    assert pokerhand_11.highest_value == [8,9]
    assert pokerhand_11_1 < pokerhand_11


    "Test four of a kind"
    pokerhand_12 = PokerHand([NumberedCard(Suit.Spades, 8), NumberedCard(Suit.Spades, 9), NumberedCard(Suit.Diamonds, 9)
                                , NumberedCard(Suit.Hearts, 9), NumberedCard(Suit.Clubs, 9) ])

    assert pokerhand_12.type == Handtype.four_of_a_kind
    assert pokerhand_12.highest_value == [9,8]


    "Test straight flush"
    pokerhand_13 = PokerHand([NumberedCard(Suit.Spades, 2), NumberedCard(Suit.Spades, 3), AceCard(Suit.Spades)
                  , NumberedCard(Suit.Spades, 4), NumberedCard(Suit.Spades, 5)])
    assert pokerhand_13.highest_value == 5
    assert pokerhand_13.type == Handtype.straight_flush

