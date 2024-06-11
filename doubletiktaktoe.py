from math import inf as infinity
from random import choice
import platform
import time
from os import system

import dearpygui.dearpygui as dpg

class DoubleTikTakToe():

    def __init__(self):
        self.MAX_ROWS = self.MAX_COL = 3

        self.board = [[[[" " for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

        self.activePlayer = "X"
        self.cache = ""
        self.otherPlayer = "O"
        self.forceFieldROW = 3
        self.forceFieldCOL = 3
        self.streak = 0
        self.diagonal = [2,1,0]
        self.isglobalwin = 0
        self.firstOpen = True

    def checkGlobalWin(self, event):
        winningPlayer = "W" + self.otherPlayer
        streak = 0
        for i in range(3):
            if self.board[i][event[1]][event[2]][event[3]] == self.winningPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[event[0]][i][event[2]][event[3]] == self.winningPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[i][i][event[2]][event[3]] == self.winningPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[i][self.diagonal[i]][event[2]][event[3]] == self.winningPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        return 0

    def win(self, event):
        for i in range(3):
            for j in range(3):
                self.winningPlayer = "W" + self.otherPlayer
                self.board[event[0]][event[1]][i][j] = self.winningPlayer

    def checkWin(self, event):
        streak = 0
        for i in range(3):
            if self.board[event[0]][event[1]][i][event[3]] == self.otherPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[event[0]][event[1]][event[2]][i] == self.otherPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[event[0]][event[1]][i][i] == self.otherPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        for i in range(3):
            if self.board[event[0]][event[1]][i][self.diagonal[i]] == self.otherPlayer:
                streak = streak + 1
        if streak == 3:
            return 1
        streak = 0
        return 0

    def checkObstructed(self):
        for i in range(3):
            for j in range(3):
                if self.board[self.forceFieldROW][self.forceFieldCOL][i][j] == " ": return False
        return True

    def place(self, event):
        error = False

        if self.forceFieldCOL != 3 and self.forceFieldROW != 3:
            forceboard = self.board[self.forceFieldCOL][self.forceFieldROW][1][1]
            if forceboard == "WX" or forceboard == "WO" or forceboard == "B":
                for i in range(3):
                    self.forceFieldCOL = 3
                    self.forceFieldROW = 3
        if self.forceFieldCOL != 3 and self.forceFieldROW != 3:
            if self.checkObstructed() == True:
                self.forceFieldCOL = 3
                self.forceFieldROW = 3
        if self.forceFieldCOL != event[0] or self.forceFieldROW != event[1]:
            error = True
            if self.forceFieldCOL == 3 and self.forceFieldROW == 3:
                error = False
            if error == True:
                return [9, self.activePlayer]

        if self.board[event[0]][event[1]][event[2]][event[3]] == " " and error == False:
            self.board[event[0]][event[1]][event[2]][event[3]] = self.activePlayer

            self.forceFieldCOL = event[3]
            self.forceFieldROW = event[2]

            self.cache = self.activePlayer
            self.activePlayer = self.otherPlayer
            self.otherPlayer = self.cache
            iswin = self.checkWin(event)
            if iswin == 1:
                self.win(event)
                self.isglobalwin = self.checkGlobalWin(event)
                iswin = 0
            if self.isglobalwin == 1:
                return [1, self.otherPlayer]
        elif error != True:
            return [8, self.activePlayer]
        error = False
        return [7, self.activePlayer]

    def pickPlace(self, a, b, c, d):
        event = [a, b, c, d]
        placeState = self.place(event)
        return [placeState, [self.forceFieldCOL, self.forceFieldROW], self.board, event]

    def rndPlace(self):
        c = choice([0, 1, 2])
        print(c)
        d = choice([0, 1, 2])
        if self.forceFieldCOL == 3 and self.forceFieldROW == 3:
            a = choice([0, 1, 2])
            b = choice([0, 1, 2])
        else:
            a = self.forceFieldCOL
            b = self.forceFieldROW
        event = [a, b, c, d]
        placeState = self.place(event)
        return [placeState, [self.forceFieldCOL, self.forceFieldROW], self.board, event]

    def settings(self):
        self.MAX_ROWS = self.MAX_COL = 3

        self.board = [[[[" " for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

        self.activePlayer = "X"
        self.cache = ""
        self.otherPlayer = "O"
        self.forceFieldROW = 3
        self.forceFieldCOL = 3
        self.streak = 0
        self.diagonal = [2,1,0]
        self.isglobalwin = 0
        self.firstOpen = True

        return self.board

    def clean(self):
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

class Render():

    def __init__(self):
        dpg.create_context()
        self.userData = [0,0,0,0]
        self.newData = False
        self.game = DoubleTikTakToe()

        self.board = self.game.settings()
        self.forceFieldCOL = 3
        self.forceFieldROW = 3

        self.state = [[1337, "1337"], [3, 3], self.board]

        self.tableObjects = [[[[0 for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

    def clb_selectable(self, sender, app_data, user_data):
        # try:
        a, b, c, d = user_data

        print(self.tableObjects[a][b][c][d])
        self.state = self.game.pickPlace(a, b, c, d)
        if self.state[0][0] == 1:
            print(f"You Won {state[0][1]}")
            exit()
        elif self.state[0][0] == 7:
            self.board = self.state[2]
            text = "#" if self.board[a][b][c][d] == " " else self.board[a][b][c][d]
            dpg.set_value(self.tableObjects[a][b][c][d], True)

            self.forceFieldCOL = self.state[1][0]
            self.forceFieldROW = self.state[1][1]
            self.state[0][0] = 0

            while self.state[0][0] != 7:
                self.state = self.game.rndPlace()
                if self.state[0][0] == 1:
                    print(f"You Won {self.state[0][1]}")
                    exit()

            a, b, c, d = self.state[3]

            self.board = self.state[2]
            text = "#" if self.board[a][b][c][d] == " " else self.board[a][b][c][d]
            dpg.set_value(self.tableObjects[a][b][c][d], True)

            self.forceFieldCOL = self.state[1][0]
            self.forceFieldROW = self.state[1][1]
            self.state[0][0] = 0
        # except:
            # pass

    def requestData(self):
        if self.newData:
            return self.userData
        else:
            return False

    def render(self):

        with dpg.theme() as table_theme:
            with dpg.theme_component(dpg.mvTable):
                # dpg.add_theme_color(dpg.mvThemeCol_HeaderHovered, (255, 0, 0, 100), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_HeaderActive, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_Header, (0, 0, 0, 0), category=dpg.mvThemeCat_Core)

        with dpg.window(tag="Selectable Tables"):
            with dpg.table(tag="SelectCells", header_row=False) as selectablecells:
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()

                for i in range(9):
                    with dpg.table_row():
                        for j in range(9):
                            if i < 3: a = 0
                            elif i <6: a = 1
                            else: a = 0
                            if j < 3: b = 0
                            elif j <6: b = 1
                            else: b = 0

                            if i == 0 or i == 3 or i == 7: c = 0
                            elif i == 1 or i == 4 or i == 8: c = 1
                            else: c = 2
                            if j == 0 or j == 3 or j == 7: d = 0
                            elif j == 1 or j == 4 or j == 8: d = 1
                            else: d = 2
                            text = "#" if self.board[a][b][c][d] == " " else self.board[a][b][c][d]

                            self.tableObjects[a][b][c][d] = uuid = dpg.generate_uuid()

                            dpg.add_selectable(label=f"{text}", callback=self.clb_selectable, user_data=(a, b, c, d), tag=self.tableObjects[a][b][c][d])
                    if i == 2 or i == 5:
                        with dpg.table_row():
                            for j in range(9):
                                dpg.add_selectable(label=f"---", callback=self.clb_selectable, user_data=(99,99))
            # dpg.bind_item_theme(item=selectablecells, theme=table_theme)

        dpg.create_viewport(width=800, height=600)
        dpg.setup_dearpygui()
        dpg.show_viewport()

        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

if __name__ == "__main__":
    render = Render()

    render.render()