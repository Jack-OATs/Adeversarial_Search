# from Game import *
# from Players import *
#from BasicAshbyAgent import BasicAgent

from reversi.Game import *
from reversi.Players import *

if __name__ == "__main__":
    game = Game(AIAgent(1), Human(2), time_per_turn=1, gui=True)
    game.start_game()
