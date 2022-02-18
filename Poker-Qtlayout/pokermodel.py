from cardlib import *
from PyQt5.QtCore import *

class GameModel(QObject):
    """
    Class that contains the game state variables
    """
    pot_signal = pyqtSignal()
    add_card_signal = pyqtSignal()
    def __init__(self,players):
        super().__init__()
        self.deck = None
        self.pot = 0
        self.pot_before = 0
        self.pot_after = 0
        self.players = players
        self.active_player = 0
        self.table = Table()
        self.bet_sum = 0
        self.bet_sum_input = 0
        self.round_winner = "Hen vann"
        self.call_number = 0
        self.new_round()

    def call(self):
        """
        method for call game function

        """

        call_sum = self.pot_after - self.pot_before
        print(call_sum)
        self.pot = self.pot + call_sum
        self.pot_signal.emit()
        self.players[self.active_player].call(call_sum)
        self.active_player = (self.active_player + 1) % 2
        self.add_card_signal.emit()
        self.call_number += 1
        if self.call_number == 4:
            self.winner()


    def bet(self):
        """
        method for bet game function

        """
        bet_sum= self.bet_sum_input

        self.bet_sum = self.bet_sum + bet_sum
        self.pot_before = self.pot
        self.pot = self.pot + bet_sum
        self.pot_signal.emit()
        self.pot_after=self.pot
        self.players[self.active_player].bet(bet_sum)
        self.active_player = (self.active_player + 1) % 2


    def fold(self):

        """
        method for fold game function

        """
        pot_sum=self.pot
        self.active_player = (self.active_player + 1) % 2
        self.round_winner=self.players[self.active_player].name
        print(self.round_winner)


        self.players[self.active_player].fold(pot_sum)
        self.new_round()

    def winner(self):
        """
        method that defines winner game state, when a player wins in the fifth round.(not fold)

        """
        pot_sum = self.pot
        winner = 0
        if len(self.table.hand.cards) == 5:

            best_poker_hand_0 = self.table.hand.best_poker_hand(self.players[0].hand.cards)
            #best_poker_hand_0 = self.players[0].hand.best_poker_hand(self.table.hand)

            best_poker_hand_1 = self.table.hand.best_poker_hand(self.players[1].hand.cards)
            #best_poker_hand_1 = self.players[1].hand.best_poker_hand(self.table.hand)

            if best_poker_hand_0 > best_poker_hand_1:
                winner= self.players[0]
            else:
                winner = self.players[1]

        winner.money = winner.money + pot_sum

        winner.stash_signal.emit()
        self.new_round()


    def new_round(self):
        self.pot = 0
        self.pot_signal.emit()
        self.deck = StandardDeck()
        self.deck.shuffle()
        self.table.hand.cards = []
        self.add_card_signal.emit()
        for player in self.players:
            player.hand = Hand()
            player.hand.cards = []
            #player.cards.append(self.deck.take_card())
            player.hand.cards.append(self.deck.take_card())
            #player.cards.append(self.deck.take_card())
            player.hand.cards.append(self.deck.take_card())
            player.player_card_signal.emit()

        self.call_number = 0
    def add_3_cards(self):
        """
        adds three cards to the table when number of cards is zero (beginning of round)

        """
        if len(self.table.hand.cards) == 0:
            self.table.hand.add_new_card(self.deck.take_card())
            self.table.hand.add_new_card(self.deck.take_card())
            self.table.hand.add_new_card(self.deck.take_card())

    def add_card(self):
        """
        adds consecutive cards after the first three are dealt, until five cards are on the table.
        :return:
        """
        if len(self.table.hand.cards) < 5 and len(self.table.hand.cards) >= 3 :
            self.table.hand.add_new_card(self.deck.take_card())


class Player(QObject):
    """
    class that defines variables and methods pertaining to the player
    """
    stash_signal = pyqtSignal()
    player_card_signal = pyqtSignal()

    def __init__(self,player_name):
        super().__init__()
        self.name = player_name
        self.hand = Hand()
        self.cards = []
        self.money = 500

    def bet(self,bet_sum):
        """
        method for bet player function
        :param bet_sum: inputed bet sum from player
        :return:
        """
        self.money = self.money - bet_sum
        self.stash_signal.emit()

    def call(self,call_sum):
        """
        method for call player function
        :param call_sum: call sum calculated in the game state class
        :return:
        """
        self.money = self.money - call_sum
        self.stash_signal.emit()

    def fold(self,pot_sum):
        """
         method for fold player function
        :param pot_sum: total pot sum from the game state, awarded to the winner
        :return:
        """
        self.money = self.money + pot_sum
        self.stash_signal.emit()




class Table():
    """
    Class that holds the hand
    """
    def __init__(self):
        hand = Hand()
        self.hand = hand
