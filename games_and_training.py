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

def generate_random_network(dimensions = [39,45,43,42]):

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

def generate_child_generation(networks_to_reproduce, number_in_generation = 20):
    new_networks = []
    number_to_create = number_in_generation-len(networks_to_reproduce)
    number_of_childeren = (number_to_create//(5*len(networks_to_reproduce)))
    number_of_randoms = number_to_create - (number_of_childeren*3*len(networks_to_reproduce))
    for i in networks_to_reproduce:
        new_Ms,new_Vs = i.get_weights()
        new_networks.append(nw.network(new_Ms,new_Vs))
        for j in range(number_of_childeren):
            new_networks.append(i.produce_child())
            new_networks.append(i.produce_child(weight_sigma = 0.2, bias_sigma = 0.2, chance_to_change = 0.6))
            new_networks.append(i.produce_child(weight_sigma = 0.5, bias_sigma = 0.5, chance_to_change = 0.8))
            new_networks.append(i.produce_child(weight_sigma = 1.0, bias_sigma = 1.0, chance_to_change = 0.9))
    for i in range(number_of_randoms):
        new_networks.append(generate_random_network())
    return(new_networks)

def run_generation(networks, number_to_win = 2):

    print('Generation started')
    with Bar('Playing games', max=len(networks)*(len(networks)-1), fill='█',empty_fill = '∙') as bar:
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

    winners = []
    winners.append(networks.pop(find_best_network(networks)))
    print('first winner score:')
    print(winners[0].score)
    for i in range(number_to_win-1):
        winners.append(networks.pop(find_best_network(networks)))

    return(winners)

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

def train_networks(state = 'new', parents = [], gen = 0, number_in_generation = 20, number_of_winners = 2): #state takes 'new' to generate new ones, 'file' to read latest from file, or 'cont' and two networks to use two existing ones

    if 'new' == state:
        networks = generate_random_generation(size=number_in_generation)
    elif 'cont' == state:
        networks = generate_child_generation(parents, number_in_generation=number_in_generation)
    elif 'file' == state:
        files = os.listdir(path+'/training')
        largest_gen = 0
        for i in files:
            if int(i.split('#')[1].split('.')[0])>largest_gen:
                largest_gen = int(i.split('#')[1].split('.')[0])
        gen = largest_gen
        file = open('training/Generation #'+str(gen)+'.txt', 'r')
        one_parent_string = file.read()
        file.close()

        parent_strings = one_parent_string.split('@')
        for i in range(len(parent_strings)):
            parents.append(strings_to_networks(parent_strings[i]))

        networks = generate_child_generation(parents, number_in_generation=number_in_generation)
    elif 'comb' == state:
        files = os.listdir(path+'/training')
        parents = []
        for i in files:
            file = open('training/'+i, 'r')
            parent_strings = file.read().split('@')
            for j in range(len(parent_strings)):
                parents.append(strings_to_networks(parent_strings[j]))
            file.close()
        networks = generate_child_generation(parents, number_in_generation=number_in_generation)


    gen += 1
    for i in range(4):
        print()
        print('Generation '+str(gen))
        winners = run_generation(networks, number_to_win = number_of_winners)
        print(len(winners))
        networks = generate_child_generation(winners, number_in_generation=number_in_generation)
        gen += 1
    print()
    print('Generation '+str(gen))
    winners = run_generation(networks, number_to_win = number_of_winners)
    winner_strings = []
    for i in range(len(winners)):
        winner_strings.append(winners[i].weights_to_string())
    generation_string = '@'.join(winner_strings)
    with open('training/Generation #'+str(gen)+'.txt', 'w') as f:
        f.write(generation_string)


    train_networks(state = 'cont', parents = winners, gen = gen, number_in_generation = number_in_generation, number_of_winners = number_of_winners)

train_networks(state = 'comb', number_in_generation = 200, number_of_winners = 30)
