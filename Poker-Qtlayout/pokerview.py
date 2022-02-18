from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from pokermodel import *



class PlayerWidget(QWidget):
    """
    creates player widget with variables from the model
    """

    def __init__(self,player):
        super().__init__()
        self.player=player

        hbox = QHBoxLayout()

        player_label = QLabel(f"player name:{player.name}")

        self.stash_label = QLabel()
        self.update_stash_label()
        player.stash_signal.connect(self.update_stash_label)

        hbox.addWidget(player_label)

        self.player_cards = QLabel()
        self.update_player_cards()
        player.player_card_signal.connect(self.update_player_cards)


        vbox = QVBoxLayout()
        vbox.addWidget(self.player_cards)
        vbox.addWidget(self.stash_label)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    def update_stash_label(self):
        """
        method that updates player stash (money) label

        """
        self.stash_label.setText("Player stash: " + str(self.player.money))

    def update_player_cards(self):
        """
        method updates players cards

        """
        self.player_cards.setText(str([c.__str__() for c in self.player.hand.cards]))

class Buttons(QWidget):
    """
    button class that holds all the clickable buttons in the GUI presented to the players
    """

    def __init__(self,model):
        super().__init__()  # Call the QWidget initialization as well!

        self.round_winner=model.round_winner
        self.model=model
        self.call_number=0


        call = QPushButton("Call")
        bet = QPushButton("Bet")
        fold = QPushButton("Fold")

        call.clicked.connect(model.add_3_cards)
        call.clicked.connect(model.call)
        call.clicked.connect(model.add_card)




        bet.clicked.connect(self.showDialog)
        bet.clicked.connect(model.bet)


        fold.clicked.connect(model.fold)
        fold.clicked.connect(self.foldclickMethod)


        hbox = QHBoxLayout()

        hbox.addWidget(call)
        hbox.addWidget(bet)
        hbox.addWidget(fold)


        self.setLayout(hbox)
    def foldclickMethod(self):
        """
        display winner when a player folds

        """

        QMessageBox.about(self, "Congrats!", self.model.round_winner + " is the round winner!")

    def showDialog(self):
        """
        input box presented to player when a player bets, to get bet sum

        """
        bet_sum_gui = QInputDialog.getInt(self, 'input dialog', 'Enter bet sum')
        self.model.bet_sum_input = int(bet_sum_gui[0])




class CardDisplay(QWidget):
    """
    class that displays the cards in the GUI
    """
    def __init__(self,label,model):
        super().__init__()
        self.model =model
        str_cards = [c.__str__() for c in model.table.hand.cards]
        self.str_cards = str_cards
        vbox = QVBoxLayout()
        self.card_label = QLabel(str(str_cards))
        model.add_card_signal.connect(self.update_card_label)
        vbox.addWidget(self.card_label)

        self.setLayout(vbox)

    def update_card_label(self):
        """
        method that updates card labels for the cards on the table
        :return:
        """
        self.card_label.setText(str([c.__str__() for c in self.model.table.hand.cards]))



class WholeWindow(QGroupBox):
    """
    Class for the whole window that is displayed, all the previous widgets are displayed here
    """
    def __init__(self,model):
        self.model=model

        super().__init__()
        hbox = QHBoxLayout()


        hbox.addWidget(PlayerWidget(model.players[0]))
        hbox.addWidget(PlayerWidget(model.players[1]))
        hbox.addWidget(Buttons(model))



        self.pot_label = QLabel("Pot: " + str(model.pot))
        model.pot_signal.connect(self.update_pot_label)
        hbox.addWidget(self.pot_label)

        vbox = QVBoxLayout()
        vbox.addWidget(CardDisplay('CARDS PLACEHOLDER', model))

        vbox.addLayout(hbox)



        self.setLayout(vbox)
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Poker Game')
        self.setWindowIcon(QIcon("jack-of-spade-554355.png"))

    def update_pot_label(self):
        """
        method that updates pot label

        """
        self.pot_label.setText("Pot: " + str(self.model.pot))