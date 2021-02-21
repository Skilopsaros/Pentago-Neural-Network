import board
import network_class as nw
import numpy as np
import random

def network_game(player_1,player_2):
    game_board = board.game()
    game_won = 0
    players = [player_1, player_2]
    while 0 == game_won:
        #print('player '+str(game_board.board.turn%2+1))
        game_won = players[game_board.board.turn%2].calculate_move(game_board)
        #print()
        #game_board.board.show()
        #print()
    if game_won == 3:
        for i in players:
            i.score += 37
    else:
        #print('I am here')
        players[game_won-1].score += (72-game_board.board.turn)
        players[2-game_won].score += (game_board.board.turn)
    #print(game_won)
    #print(game_board.board.turn)
    #print(player_1.score)
    #print(player_2.score)

def generate_random_network(dimensions = [39,31,31,5]):

    Ms=[0,0,0]
    for i in range(3):
        Ms[i]=np.zeros((dimensions[i+1],dimensions[i]))
        for j in range(dimensions[i+1]):
            for k in range(dimensions[i]):
                Ms[i][j][k] = random.gauss(0,0.15)

    Vs=[0,0,0]
    for i in range(3):
        Vs[i]=np.zeros(dimensions[i+1])
        for j in range(dimensions[i+1]):
            Vs[i][j] = random.gauss(0,0.15)

    return(nw.network(Ms,Vs))
