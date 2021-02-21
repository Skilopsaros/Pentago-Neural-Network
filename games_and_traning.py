import board
import network_class as nw
import numpy as np
import random
import copy
import os
from progress.bar import Bar

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
        new_Ms,new_Vs = i.get_weights()
        new_networks.append(nw.network(new_Ms,new_Vs))
        for j in range(2):
            new_networks.append(i.produce_child())
            new_networks.append(i.produce_child(weight_sigma = 0.2, bias_sigma = 0.2, chance_to_change = 0.6))
            new_networks.append(i.produce_child(weight_sigma = 0.3, bias_sigma = 0.3, chance_to_change = 0.8))
    for i in range(6):
        new_networks.append(generate_random_network())
    return(new_networks)

def run_generation(networks):

    print('Generation started')
    with Bar('Playing games', max=380, fill='█',empty_fill = '∙') as bar:
        for i in range(len(networks)):
            for j in range(len(networks)):
                if i != j:
                    network_game(networks[i],networks[j])
                    bar.next()

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

    return(first_winner,second_winner)

def strings_to_networks(one_string):
    two_strings = one_string.split('#')
    Ms = []
    Ms_lists = []
    Ms_split_strings_1 = two_strings[0].split(":")
    Ms_split_strings_2 = []
    Ms_split_strings_3 = []
    for i in range(len(Ms_split_strings_1)):
        Ms_split_strings_2.append(Ms_split_strings_1[i].split(';'))
        Ms_split_strings_3.append([])
        Ms_lists.append([])
    for i in range(len(Ms_split_strings_2)):
        for j in range(len(Ms_split_strings_2[i])):
            Ms_split_strings_3[i].append(Ms_split_strings_2[i][j].split(','))
            Ms_lists[i].append([])

    for i in range(len(Ms_split_strings_3)):
        for j in range(len(Ms_split_strings_3[i])):
            for k in range(len(Ms_split_strings_3[i][j])):
                Ms_lists[i][j].append(float(Ms_split_strings_3[i][j][k]))
        Ms.append(np.array(Ms_lists[i]))

    Vs = []
    Vs_lists = []
    Vs_split_strings_1 = two_strings[1].split(';')
    Vs_split_strings_2 = []
    for i in range(len(Vs_split_strings_1)):
        Vs_split_strings_2.append(Vs_split_strings_1[i].split(','))
        Vs_lists.append([])

    for i in range(len(Vs_split_strings_2)):
        for j in range(len(Vs_split_strings_2[i])):
            Vs_lists[i].append(float(Vs_split_strings_2[i][j]))
        Vs.append(np.array(Vs_lists[i]))

    return(nw.network(Ms,Vs))

def train_networks(state = 'new', first_parrent = 0, second_parrent = 0, gen = 0): #state takes 'new' to generate new ones, 'file' to read latest from file, or 'cont' and two networks to use two existing ones

    if 'new' == state:
        networks = generate_random_generation()
    elif 'cont' == state:
        networks = generate_child_generation([first_parrent, second_parrent])
    elif 'file' == state:
        files = os.listdir(path+'/training')
        largest_gen = 0
        for i in files:
            if int(i.split('#')[1].split('.')[0])>largest_gen:
                largest_gen = int(i.split('#')[1].split('.')[0])
        gen = largest_gen
        file = open('training/child_1_gen #'+str(gen)+'.txt', 'r')
        first_network_string = file.read()
        file.close()
        file = open('training/child_2_gen #'+str(gen)+'.txt', 'r')
        second_network_string = file.read()
        file.close()

        networks = generate_child_generation([strings_to_networks(first_network_string), strings_to_networks(second_network_string)])

    gen += 1
    for i in range(99):
        print()
        print('Generation '+str(gen))
        first_winner, second_winner = run_generation(networks)
        networks = generate_child_generation([first_winner, second_winner])
        gen += 1
    first_winner, second_winner = run_generation(networks)

    with open('training/child_1_gen #'+str(gen)+'.txt', 'w') as f:
        f.write(first_winner.weights_to_string())
    with open('training/child_2_gen #'+str(gen)+'.txt', 'w') as f:
        f.write(second_winner.weights_to_string())

    train_networks(state = 'cont', first_parrent = first_winner, second_parrent = second_winner, gen = gen)

train_networks(state = 'file')
