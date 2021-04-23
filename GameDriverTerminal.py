from reversi.Game import Game
from reversi.Players import RandomPlayer, Human, AIAgent

wins = [0, 0, 0]
piece_counts = [0, 0]
players = [AIAgent, RandomPlayer]
time_per_turn = 1  # in seconds
for i in range(70):
    print("On game {}".format(i+1))
    if i % 2 == 0:
        g = Game(players[0](1, name="25th Night"), players[1](2, name="Rando"), time_per_turn=time_per_turn)
        g.start_game()
        winner, p1_pieces, p2_pieces = g.get_game_results()
        wins[winner] += 1
        piece_counts[0] += p1_pieces
        piece_counts[1] += p2_pieces
    else:
        g = Game(players[1](1, name="25th Night"), players[0](2, name="Rando"), time_per_turn=time_per_turn)
        g.start_game()
        winner, p1_pieces, p2_pieces = g.get_game_results()
        wins[(-winner + 3) % 3] += 1
        piece_counts[1] += p1_pieces
        piece_counts[0] += p2_pieces


print("---RESULTS---")
print("{} won {} games total pieces = {}".format(players[0](1), wins[1], piece_counts[0]))
print("{} won {} games total pieces = {}".format(players[1](1), wins[2], piece_counts[1]))
print("games tied = {}".format(wins[0]))
