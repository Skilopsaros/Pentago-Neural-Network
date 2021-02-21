import board
import network_class as nw
import numpy as np
import random
import copy
import os

# detect the current working directory
path = os.getcwd()

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

def generate_random_generation(size=20):
    networks = []
    for i in range(size):
        networks.append(generate_random_network())
    return(networks)

def generate_child_generation(networks_to_reproduce):
    new_networks = []
    for i in networks_to_reproduce:
        new_networks.append(nw.network(i.get_weights()))
        for j in range(2):
            new_networks.append(i.produce_child())
            new_networks.append(i.produce_child(weight_sigma = 0.2, bias_sigma = 0.2, chance_to_change = 0.6))
            new_networks.append(i.produce_child(weight_sigma = 0.3, bias_sigma = 0.3, chance_to_change = 0.8))
    for i in range(6):
        new_networks.append(generate_random_network())
    return(new_networks)

def run_generation(networks):

    for i in range(len(networks)):
        for j in range(len(networks)):
            if i != j:
                network_game(networks[i],networks[j])

    def find_best_network(networks):
        best = networks[0]
        best_index = 0
        for i in range(len(networks)):
            if networks[i].score > best.score:
                best = networks[i]
                best_index = i
        return(best_index)

    first_winner  = networks.pop(find_best_network(networks))
    print('first winner score:')
    print(first_winner.score)
    second_winner = networks.pop(find_best_network(networks))
    print('second winner score:')
    print(second_winner.score)


run_generation(generate_random_generation())
