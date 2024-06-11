from tiktaktoe import TikTakToe
import time

ttt = TikTakToe(headless=True)

ttt.main()
game_board = ttt.headless_player_choice(1, True)

state = 10

while state !=0 or state !=1 or state !=-1:
    print(game_board)
    print(state)
    zahl = input("Zahl zwischen 1-9: ")
    action = int(zahl)
    state, game_board = ttt.headless_turn(action)
    # ttt.ai_turn(0,1)

print(state)
