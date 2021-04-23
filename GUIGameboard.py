from tkinter import *
from reversi.Game import *

from reversi.GameBoard import GAMEBOARD_EDGE


class GUIGameboard():
    def __init__(self, gameboard, possible_moves=[]):
        self.__root = Tk()
        self.__root.title("Reversi - CSCI 4332 @ HSUTX")
        self.__root.resizable(False, False)
        self.__root.geometry('426x526+600+100')
        self.__window = Canvas(self.__root, width=426, height=426)
        self.__root.bind('<1>', self.click_square)
        self.draw_board(gameboard)
        self.__possible_moves = possible_moves
        self.__stored_clicks = []
        self.__root.mainloop()

    def get_clicked_squares(self):
        # print("------------{}".format(self.__stored_clicks))
        while len(self.__stored_clicks) > 0:
            temp = self.__stored_clicks.pop()
            if temp in self.__possible_moves:
                return temp
        return None

    def click_square(self, event):
        c = (event.y-13) // 50
        r = (event.x-13) // 50
        # print("clicked ({},{})".format(r, c))
        temp = (r, c)
        if temp in self.__possible_moves:
            self.__stored_clicks.append((r, c))
            self.__root.destroy()

    def draw_board(self, gameboard):
        brd = gameboard
        for r in range(GAMEBOARD_EDGE):
            for c in range(GAMEBOARD_EDGE):
                sq = brd.get_square_value((r, c))
                if sq == 1:
                    color = "white"
                elif sq == 2:
                    color = "black"
                else:
                    color = "green"
                x_0 = 13 + (r * 50)
                y_0 = 13 + (c * 50)
                x_1 = x_0 + 50
                y_1 = y_0 + 50
                self.__window.create_rectangle(x_0, y_0, x_1, y_1, fill="green", outline="black")
                self.__window.create_oval(x_0 + 4, y_0 + 4, x_1 - 4, y_1 - 4, fill=color, outline=color)

        self.__window.pack()
