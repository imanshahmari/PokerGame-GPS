from pokerview import *


player1 = Player("Hen 1")
player2 = Player("Hen 2")
game = GameModel([player1, player2])

qt_app = QApplication(sys.argv)

win = WholeWindow(game)
win.show()
qt_app.exec_()
