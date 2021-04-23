from random import randint
from copy import deepcopy
import time
from reversi.GameBoard import *


class RandomPlayer:
    def __init__(self, player_number, name="Random"):
        self.__player_number = player_number
        self.__name = name

    def __str__(self):
        return self.__name

    def select_square(self, gameboard, time_left=-1):
        possible_moves = gameboard.get_current_moves(self.__player_number)
        # print("Random player's possible moves are {}".format(possible_moves))
        if len(possible_moves) == 0:
            return None
        r = randint(0, len(possible_moves)-1)
        # print("---and selected {}".format(possible_moves[r]))
        return possible_moves[r]


class Human:
    def __init__(self, player_number, name="Human"):
        self.__player_number = player_number
        self.__name = name

    def select_square(self, gameboard, time_limit=-1):
        print(gameboard)
        possible_moves = gameboard.get_current_moves(self.__player_number)
        for i, v in enumerate(possible_moves):
            print("{}) {}".format(i, v))
        x = int(input("Enter selection: "))
        return possible_moves[x]

    def __str__(self):
        return self.__name


class AIAgent:
    def __init__(self, player_number, name="25th Night"):
        self.__player_number = player_number
        self.__name = name

    def __str__(self):
        return self.__name

    def select_square(self, gameboard, time_limit=300):
        start_time = time.perf_counter()
        i = 3
        move, _ = self.__minmax(gameboard, time_limit, start_time, depth=i)
        while time.perf_counter() - start_time <= time_limit:
            i += 1
            if time.perf_counter() - start_time >= time_limit/65:
                return move
            move, _ = self.__minmax(gameboard, time_limit, start_time, depth=i)
        return move

    def __eval_fn(self, gameboard, move):
        _, p1, p2 = gameboard.count_pieces()
        weight = 1
        edges = [(0,0), (0,7), (7,0), (7,7), (0,4), (0,5), (0,6), (0,3), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0),
                 (0,1), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (0,2), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7)]
        neg = [(1,1), (1,6), (6,6), (6,1)]
        if move in neg and p1+p2 <= 40:
            weight -= 18
        elif move in edges:
            weight += 13
            if move in edges[0:4]:
                weight += 35

        if p1 == p2:
            weight -= 60

        if self.__player_number == 1:
            if p1 > p2:
                weight += 38
            weight -= 38
            return weight * (p1 - p2)
        else:
            if p2 > p1:
                weight += 38
            weight -= 38
            return weight * (p2 - p1)

    def __utility(self, gameboard, move):
        if gameboard.find_winner()[0] == self.__player_number:
            return float("inf")
        if gameboard.find_winner()[0] != 0 and gameboard.find_winner()[0] != -1 and gameboard.find_winner()[0] != self.__player_number:
            return float("-inf")
        if gameboard.find_winner()[0] == 0:
            return 0
        else:
            return self.__eval_fn(gameboard, move)

    def __minmax(self, gameboard, time_limit, start_time, depth=float("inf"), maximizing_player=True):
        new_board = deepcopy(gameboard)
        if depth == 0:
            return None, 0

        if maximizing_player:
            possible_moves = gameboard.get_current_moves(self.__player_number)
            if len(possible_moves) == 0:
                return None, 0
            max_eval = float("-inf")
            max_node = possible_moves[0]
            for move in possible_moves:
                eval = self.__utility(gameboard, move)
                if eval == float("inf") or eval == float("-inf") or eval == 0:
                    return None, eval
                if time.perf_counter() - start_time >= time_limit/65:
                    return move, 0
                new_board.update_board(move, self.__player_number)
                _, curr_eval = self.__minmax(new_board, time_limit, start_time, depth-1, not maximizing_player)
                if curr_eval > max_eval:
                    max_eval = curr_eval
                    max_node = move
            return max_node, max_eval

        else:
            if self.__player_number == 1:
                player_two = 2
            else:
                player_two = 1

            possible_moves = gameboard.get_current_moves(player_two)
            if len(possible_moves) == 0:
                return None, 0
            min_eval = float("inf")
            min_node = possible_moves[0]
            for move in possible_moves:
                eval = self.__utility(gameboard, move)
                if eval == float("inf") or eval == float("-inf") or eval == 0:
                    return None, eval
                if time.perf_counter() - start_time >= time_limit/65:
                    return move, 0
                new_board.update_board(move, player_two)
                _, curr_eval = self.__minmax(new_board, time_limit, start_time, depth-1, not maximizing_player)
                if curr_eval < min_eval:
                    min_eval = curr_eval
                    min_node = move
            return min_node, min_eval

    def __alphabeta(self, gameboard, time_limit, start_time, depth=float("inf"), maximizing_player=True, alpha=float("-inf"), beta=float("inf")):
        new_board = deepcopy(gameboard)
        if depth == 0:
            return None, 0

        if maximizing_player:
            possible_moves = gameboard.get_current_moves(self.__player_number)
            if len(possible_moves) == 0:
                return None, 0
            max_eval = float("-inf")
            max_node = possible_moves[0]
            for move in possible_moves:
                eval = self.__utility(gameboard, move)
                if eval == float("inf") or eval == float("-inf") or eval == 0:
                    return None, eval
                if time.perf_counter() - start_time >= time_limit/65:
                    return move, 0
                max_eval = eval
                new_board.update_board(move, self.__player_number)
                _, curr_eval = self.__alphabeta(new_board, time_limit, start_time, depth - 1, not maximizing_player)
                if curr_eval > max_eval:
                    max_eval = curr_eval
                    max_node = move
                alpha = max(alpha, curr_eval)
                if alpha >= beta:
                    break
            return max_node, max_eval

        else:
            if self.__player_number == 1:
                player_two = 2
            else:
                player_two = 1

            possible_moves = gameboard.get_current_moves(player_two)
            if len(possible_moves) == 0:
                return None, 0
            min_eval = float("inf")
            min_node = possible_moves[0]
            for move in possible_moves:
                eval = self.__utility(gameboard, move)
                if depth == 0 or eval == float("inf") or eval == float("-inf") or eval == 0:
                    return None, eval
                if time.perf_counter() - start_time >= time_limit/65:
                    return move, 0
                min_eval = eval
                new_board.update_board(move, player_two)
                _, curr_eval = self.__alphabeta(new_board, time_limit, start_time, depth - 1, not maximizing_player)
                if curr_eval < min_eval:
                    min_eval = curr_eval
                    min_node = move
                if alpha >= beta:
                    break
            return min_node, min_eval


if __name__ == "__main__":
    ai = AIAgent(1)
    ai.select_square(gameboard=GameBoard())