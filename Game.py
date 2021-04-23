from GameBoard import *
from Players import *
from reversi.GUIGameboard import GUIGameboard
import time

from reversi.GameBoard import *
from reversi.Players import *


class Game:
    def __init__(self, player1, player2, time_per_turn=-1, gui=False):
        self.player1 = player1
        self.player2 = player2
        self.__gameboard = GameBoard()
        self.__whos_turn = 1
        self.__gui_game = gui
        self.__time_per_turn = time_per_turn

    def __gui_select_square(self, player, time_limit):
        if isinstance(player, Human):
            possible_moves = self.__gameboard.get_current_moves(self.__whos_turn)
            gui_board = GUIGameboard(self.__gameboard, possible_moves)
            selection = gui_board.get_clicked_squares()
            # print("selected {}".format(selection))
            return selection
        return player.select_square(self.__gameboard, time_limit)

    def start_game(self):
        game_over = False
        skip_count = 0

        count = 0
        while not game_over:  # and count < 3:
            count += 1
            # print("----------------------------------START of TURN {}-----------------------------------".format(count))
            # print(self.__gameboard)
            if False:#not self.__gui_game:
                print(self.__gameboard)
                print("Player {}'s turn with squares {}".format(self.__whos_turn,
                                                                self.__gameboard.get_current_moves(self.__whos_turn)))
            st_time = time.perf_counter()
            human_player = False
            if self.__whos_turn == 1:
                selection = self.__gui_select_square(self.player1, self.__time_per_turn)
                if type(self.player1) == Human:
                    human_player = True
            else:
                selection = self.__gui_select_square(self.player2, self.__time_per_turn)
                if type(self.player2) == Human:
                    human_player = True
            if not human_player and 0 < self.__time_per_turn < time.perf_counter() - st_time:
                # raise TimeoutError("0X42 Player{} ran out of time on turn".format(self.__whos_turn))
                print("!!!!!!!!!!!!!!!!!!!!TIME OUT!!!!!!!!!!!!!!!!!!!!!!!")
                self.__gameboard.set_all_squares(-self.__whos_turn + 3)
                selection = None
            # print("player {} chose {}".format(self.__whos_turn, selection))
            if selection is not None:
                skip_count = 0
                self.__gameboard.update_board(selection, self.__whos_turn)
            else:
                skip_count += 1
            if self.__gameboard.find_winner()[0] > -1 or skip_count >= 2:
                game_over = True
            self.__whos_turn = 1 if self.__whos_turn == 2 else 2
        if self.__gui_game:
            GUIGameboard(self.__gameboard)
        else:
            print(self.__gameboard)
        print("{} with {} as p1 and {} as p2".format(self.__gameboard.find_winner(), self.player1, self.player2))

    def get_game_results(self):
        _, p1, p2 = self.__gameboard.find_winner()
        if p1 == p2:
            return 0, p1, p2
        if p1 > p2:
            return 1, p1, p2
        return 2, p1, p2


