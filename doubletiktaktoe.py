from math import inf as infinity
from random import choice
import platform
import time
from os import system

# import dearpygui.dearpygui as dpg

class DoubleTikTakToe():

    def __init__(self): # Initialisiere alle wichtigen Variablen
        self.MAX_ROWS = self.MAX_COL = 3

        self.board = [[[[0 for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

        self.activePlayer = 1
        self.cache = 0
        self.otherPlayer = 2
        self.forceFieldROW = 3
        self.forceFieldCOL = 3
        self.streak = 0
        self.diagonal = [2,1,0]
        self.isglobalwin = 0
        self.firstOpen = True

    def checkGlobalWin(self, event): # Prüfe ob ein Spieler das Spiel gewonnen hat
        winningPlayer = 2 + self.otherPlayer
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

    def win(self, event): # Markiere das ein Spieler ein Feld gewonnen hat
        for i in range(3):
            for j in range(3):
                self.winningPlayer = 2 + self.otherPlayer
                self.board[event[0]][event[1]][i][j] = self.winningPlayer

    def checkWin(self, event): # Prüft ob ein Spieler das Feld gewonnen hat
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

    def checkObstructed(self): # Prüft ob ein Feld besetzt ist
        for i in range(3):
            for j in range(3):
                if self.board[self.forceFieldROW][self.forceFieldCOL][i][j] == 0: return False
        return True

    def place(self, event): # Prüft ob der Gewünschte Move valid ist und führt diesen aus
        error = False

        if self.forceFieldCOL != 3 and self.forceFieldROW != 3: # Prüfen ob der Spieler freie Feld wahl hat, wenn nicht prüfen ob das Feld zugelasen ist
            forceboard = self.board[self.forceFieldCOL][self.forceFieldROW][1][1]
            if forceboard == 3 or forceboard == 4 or forceboard == 5:
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

        if self.board[event[0]][event[1]][event[2]][event[3]] == 0 and error == False: # Prüft ob ein Move möglich ist
            self.board[event[0]][event[1]][event[2]][event[3]] = self.activePlayer # Ausführung des Moves

            self.forceFieldCOL = event[2]
            self.forceFieldROW = event[3] # Legt nächstes Feld Fest

            self.cache = self.activePlayer # Wechsele Aktiven Spieler
            self.activePlayer = self.otherPlayer
            self.otherPlayer = self.cache
            iswin = self.checkWin(event) # Prüfe ob ein Spieler ein Feld gewonnen hat
            if iswin == 1: # Wenn ja makiere das Feld als gewonnen
                self.win(event)
                self.isglobalwin = self.checkGlobalWin(event) # Prüfe ob der Spieler das Spiel gewonnen hat
            if self.isglobalwin == 1:
                return [1, self.otherPlayer]
            if iswin == 1:
                return [10, self.otherPlayer]
            iswin = 0
        elif error != True:
            return [8, self.activePlayer]
        error = False
        return [7, self.activePlayer]

    def pickPlace(self, a, b, c, d): # Versucht einen Move für bestimmte Koordinaten auszuführen
        event = [a, b, c, d]
        placeState = self.place(event)
        return [placeState, [self.forceFieldCOL, self.forceFieldROW], self.board, event]

    def rndPlace(self): # Führt einen Move für zufällige Koordinaten aus
        c = choice([0, 1, 2])
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

    def settings(self): # Setzt das Spiel zurück
        self.MAX_ROWS = self.MAX_COL = 3

        self.board = [[[[0 for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

        self.activePlayer = 1
        self.cache = 0
        self.otherPlayer = 2
        self.forceFieldROW = 3
        self.forceFieldCOL = 3
        self.streak = 0
        self.diagonal = [2,1,0]
        self.isglobalwin = 0
        self.firstOpen = True

        return self.board

    def clean(self): # Leert console (Nicht wirklich benötigt)
        """
        Clears the console
        """
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

'''
class Render(): # Rendert das Spiel
# TODO: : in eigene Datei Refactorn um damit auch die KI nutzen zu können sollte kein Problem sein
    def __init__(self): # Initsialisiere Dearpygui
        dpg.create_context()
        self.userData = [0,0,0,0]
        self.newData = False
        self.game = DoubleTikTakToe()

        self.board = self.game.settings()
        self.forceFieldCOL = 3
        self.forceFieldROW = 3

        self.state = [[1337, "1337"], [3, 3], self.board]

        self.tableObjects = [[[[0 for l in range(3)] for k in range(3)] for j in range(3)] for i in range(9)]

    def clb_selectable(self, sender, app_data, user_data): # Reaktion auf Input und Game Loop
        try:
            a, b, c, d = user_data

            self.state = self.game.pickPlace(a, b, c, d)
            if self.state[0][0] == 1:
                print(f"You Won {state[0][1]}")
                exit()
            elif self.state[0][0] == 7:
                self.board = self.state[2]
                if self.board[a][b][c][d] == 0:
                    text = " "
                elif self.board[a][b][c][d] == 1:
                    text = "X"
                elif self.board[a][b][c][d] == 2:
                    text = "O"
                elif self.board[a][b][c][d] == 3:
                    text = "WX"
                elif self.board[a][b][c][d] == 4:
                    text = "WO"
                elif self.board[a][b][c][d] == 5:
                    text = "B"
                dpg.set_item_label(self.tableObjects[a][b][c][d], f'{text}')

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
                if self.board[a][b][c][d] == 0:
                    text = " "
                elif self.board[a][b][c][d] == 1:
                    text = "X"
                elif self.board[a][b][c][d] == 2:
                    text = "O"
                elif self.board[a][b][c][d] == 3:
                    text = "WX"
                elif self.board[a][b][c][d] == 4:
                    text = "WO"
                elif self.board[a][b][c][d] == 5:
                    text = "B"
                dpg.set_item_label(self.tableObjects[a][b][c][d], f'{text}')

                self.forceFieldCOL = self.state[1][0]
                self.forceFieldROW = self.state[1][1]
                self.state[0][0] = 0
        except:
            pass

    def requestData(self): # Wird nicht verwendet
        if self.newData:
            return self.userData
        else:
            return False

    def render(self): # Erstversion des UI erstellens

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
                            else: a = 2
                            if j < 3: b = 0
                            elif j <6: b = 1
                            else: b = 2

                            if i == 0 or i == 3 or i == 6: c = 0
                            elif i == 1 or i == 4 or i == 7: c = 1
                            else: c = 2
                            if j == 0 or j == 3 or j == 6: d = 0
                            elif j == 1 or j == 4 or j == 7: d = 1
                            else: d = 2
                            if self.board[a][b][c][d] == 0:
                                text = " "
                            else:
                                text = self.board[a][b][c][d]

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

        while dpg.is_dearpygui_running(): # Render Loop
            dpg.render_dearpygui_frame()

        dpg.destroy_context()

if __name__ == "__main__": # Rendering aufrufen
    render = Render()

    render.render()
'''
