import numpy as np
from GameExceptions import *

from reversi.GameExceptions import InvalidSelection

GAMEBOARD_EDGE = 8
GAME_DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class GameBoard:
    def __init__(self):
        self.__squares = np.zeros((GAMEBOARD_EDGE, GAMEBOARD_EDGE), dtype=np.int8)
        self.__squares[3, 3] = self.__squares[4, 4] = 1
        self.__squares[4, 3] = self.__squares[3, 4] = 2

    def get_current_moves(self, whos_turn):
        """
        Get a list of possible squares to select on a turn
        :param whos_turn: a value from set {1,2} with 1=player1 and 2=player2
        :return: a list of tuples which serve as the possible squares to select
        """
        potential_moves = []
        opp_val = 1 if whos_turn == 2 else 2
        for r in range(GAMEBOARD_EDGE):
            for c in range(GAMEBOARD_EDGE):
                if self.__squares[r, c] == opp_val:
                    potential_moves += self.__possible_moves((r, c), whos_turn)
        potential_moves = list(set(potential_moves))
        return potential_moves

    def __possible_moves(self, square, whos_turn):
        """
        Given square this gives possible moves from that square
        :param square: a tuple value of (row, col)
        :param whos_turn: a value from set {1,2} with 1=player1 and 2=player2
        :return: a list of possible square values
        """
        results = []
        for direction in GAME_DIRECTIONS:
            potential_sq = tuple(np.add(direction, square))
            if self.__is_valid_sq(potential_sq) and self.__squares[potential_sq] == 0:
                temp_direction = tuple(np.product((direction, (-1, -1)), axis=0))
                temp_sq = tuple(np.add(square, temp_direction))
                keep_searching = True
                while self.__is_valid_sq(temp_sq) and keep_searching:
                    temp_sq_val = self.__squares[temp_sq]
                    if temp_sq_val == whos_turn:
                        results.append(potential_sq)
                        keep_searching = False
                    elif temp_sq_val == 0:
                        keep_searching = False
                    temp_sq = tuple(np.add(temp_sq, temp_direction))
        return results

    def update_board(self, square, whos_turn):
        """
        Update the board given the square and who's turn
        :param square: a tuple value of (row, col)
        :param whos_turn: a value from set {1,2} with 1=player1 and 2=player2
        :return: None
        """
        # print("player {} is updating the board at position {}.".format(whos_turn, square))
        opp_val = -whos_turn + 3
        # print("square = {} and whos_turn = {} on board\n{}".format(square, whos_turn, self.__squares))
        if not self.__is_valid_sq(square) or self.__squares[square] != 0:
            raise InvalidSelection(selection_value=square)
        for direction in GAME_DIRECTIONS:
            temp_sq_list = [square]
            temp_sq = tuple(np.add(direction, square))
            keep_searching = True
            while self.__is_valid_sq(temp_sq) and keep_searching:
                temp_sq_val = self.__squares[temp_sq]
                if temp_sq_val == whos_turn:
                    for val in temp_sq_list:
                        self.__squares[val] = whos_turn
                    keep_searching = False
                elif temp_sq_val == opp_val:
                    temp_sq_list.append(temp_sq)
                else:
                    keep_searching = False
                temp_sq = tuple(np.add(temp_sq, direction))

    def find_winner(self):
        """
        :return: a tuple with three elements. The first is the winner (-1=no winner yet, 0=tie, 1=player1, 2=player2)
        """
        counts = self.count_pieces()
        if counts[0] > 0 and counts[1] != 0 and counts[2] != 0:
            return -1, counts[1], counts[2]
        if counts[1] > counts[2]:
            return 1, counts[1], counts[2]
        elif counts[2] > counts[1]:
            return 2, counts[1], counts[2]
        else:
            return 0, counts[1], counts[2]

    def count_pieces(self):
        """
        :return: a tuple of the count of (open squares, player1 squares, player2 squares)
        """
        count_pieces = [0, 0, 0]
        for r in range(GAMEBOARD_EDGE):
            for c in range(GAMEBOARD_EDGE):
                val = self.__squares[r, c]
                count_pieces[val] += 1
        return count_pieces

    @staticmethod
    def __is_valid_sq(sq):
        """
        :param sq: a tuple value of (row, col)
        :return: if the value of sq is within the bounds of the board
        """
        if sq is None:
            return False
        if not 0 <= sq[0] < GAMEBOARD_EDGE:
            return False
        if not 0 <= sq[1] < GAMEBOARD_EDGE:
            return False
        return True

    def get_square_value(self, sq):
        """
        :param sq: a tuple value of (row, col)
        :return: value from {0,1,2} as to the value of the piece on the board
        """
        if self.__is_valid_sq(sq):
            return self.__squares[sq]
        return None

    def set_all_squares(self, player):
        """
        Used for if a time out occurs to set all board pieces to a specific player
        :param player:
        :return:
        """
        for r in range(GAMEBOARD_EDGE):
            for c in range(GAMEBOARD_EDGE):
                self.__squares[r,c] = player

    def __str__(self):
        """
        returns the numpy matrix str method
        :return: string of the numpy matrix
        """
        return str(self.__squares)
