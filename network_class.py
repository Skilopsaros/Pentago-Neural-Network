import numpy as np
import random
import copy
import board

class network:

    def __init__(self,Ms,Vs):
        '''Ms and Vs are two lists.
        Ms is a list of 2-D arrays, that will work as the weights of the network.
        Vs is a list of 1-D arrays that will work as the biases.'''
        self.M = Ms
        self.V = Vs
        self.score = 0

    def hypertan(self,list):
        ''' A hyperbolic tangent function that accepts a list and returns a list of the hyperbolic tangent of each element
        the hypertan is used to normalise resaults (any number will be maped to a number between -1 and 1) '''
        output = np.zeros(len(list))
        for i in range(len(list)):
            # for valuses greater than 10 or lower than -10, the output would be so close to 1 that the function outputs exactly 1 anyway
            # we don't want to have to calculate e^20 or anything higher than that, so we just say that it's 1
            if list[i]>10:
                output[i]=1.
            elif list[i]<-10:
                output[i]=1.
            else:
                exponential = np.exp(2*list[i]) # This just uses the hyperbolic tan function for every element in the list
                output[i] = (exponential-1)/(exponential+1)
        return(output)

    def calculate_output(self, input):
        '''this is the function that the network will use to calculate what move to do given the state of the board
        it doesn't take directly the board and output directly the move, instead it's meant to be used inside another function
        that will look at the board, encode it into what this function will understand, and then take what this function outputs and make a move from that

        its input is an array which needs to be as long as self.M[0][i], and its output a normalised array'''

        output = input # the output will be calculated from the input
        for i in range(len(self.M)): #each repetition of this is going from one layer to the next
            # The maths here is done like matrix addition and multiplication. This is because this is faster than doing it linearly
            output = (np.dot(self.M[i], output)+self.V[i]) # To go from each layer to the next, multiply by the weights matrix and add the biases vector.
        return(self.hypertan(output)) #retern a normalised output

    def produce_child(self, weight_sigma = 0.1, bias_sigma = 0.1, chance_to_change = 0.4):
        ''' This function will return another network object, slightly mutated from the one that run the function'''
        new_Ms = copy.deepcopy(self.M) #the new network's weights are the same as the old one's, but some will change later
        for i in range(len(new_Ms)):
            for j in range(len(new_Ms[i])):
                for k in range(len(new_Ms[i][j])):

                    if random.uniform(0, 1)<chance_to_change:#for each value in the weights, there is a chance it will change
                        new_Ms[i][j][k] += random.gauss(0,weight_sigma*self.M[i][j][k])#if a value is to change, change it by some random ammount
                        #the random ammount is decided with a normal distribution, who's standard deviation is equal to a small fraction of the original weight

        new_Vs = copy.deepcopy(self.V) #same thing we did for the weights we do for the biases
        for i in range(len(new_Vs)):
            for j in range(len(new_Vs[i])):

                if random.uniform(0, 1)<chance_to_change:
                    new_Vs[i][j] += random.gauss(0,weight_sigma*self.V[i][j])

        return(network(new_Ms,new_Vs))#and done, we just changed some weights, and make a new network. this is a child network, slighlty mutated

    def get_weights(self):
        '''returns the weights of the network'''
        return(self.M,self.V)

    def calculate_move(self,game):
        ''' this function will take the game object from board.py, translate it into a valid input for calculate_output,
         then make the move on the board based on the output'''
        input = np.zeros(39)# the network will take 39 inputs
        input[0] = float(game.board.turn)/36 # the first will be a normalised turn number, how many turns have been played
         # for the second, we will look at the centre of each board, count the free ones, normalise it and use it as the second input
        for i in range(2):
             for j in range(2):
                 if 0 == game.board.subs[i][j].contents[1][1]:
                     input[1] += 0.25
        input[2] = -2*(game.board.turn%2)+1 # this will be 1 if the network is player 1 or -1 if it's player 2
        for i in range(36): # now add the contents of the board into the next 36 inputs
            number = game.board.subs[(i//18)%2][(i//3)%2].contents[(i//6)%3][(i%3)]
            if input[2] == number: # 1 if it is a stone that belongs to the network
                input[i] = 1
            elif 0 == number: # 0 of it is empty
                input[i] = 0
            else: # -1 if it is a stone that belongs to the enemy
                input[i] =-1

        # Now that the input is ready, it's time to calculate the outputs
        outputs = self.calculate_output(input)
        # Now to convert the outputs into a valid move
        #print(outputs)
        best_move_output = -2
        move_to_play = 0
        outputs_range = [*range(36)]
        for i in outputs_range:
            if outputs[i] > best_move_output:
                best_move_output = outputs[i]
                move_to_play = i
        del outputs_range[move_to_play]
        move_x = (move_to_play%6)+1
        move_y = (move_to_play//6)+1

        best_rotation_output = -2
        rotation_to_play = 0
        for i in range(4):
            if outputs[i+36] > best_rotation_output:
                rotation_to_play = i
        move_rx = rotation_to_play%2
        move_ry = rotation_to_play//2

        move_r = 'C'
        if outputs[40]>outputs[41]:
            move_r = 'A'

        # Now to atempt to make a move
        #first we try the stone placement. if the move is invalid, then place randomly
        failed = 0
        while 0 == game.first_half_round(move_x,move_y): # Each time the code will atempt to change the board. if the move is valid, it will skip the loop.
            failed += -1 # recording that it failed at least once
            best_move_output = -2
            move_to_play = 0
            for i in outputs_range:
                if outputs[i] > best_move_output:
                    best_move_output = outputs[i]
                    move_to_play = i
            outputs_range.remove(move_to_play)
            move_x = (move_to_play%6)+1
            move_y = (move_to_play//6)+1

        self.score += failed #punishing the netwoork for bad play
        #print(self.score)
        # thankfully, there are no invalid possible moves for the second move.
        return(game.second_half_round(move_rx,move_ry,move_r)) #returns the win state of the game

    def weights_to_string(self):
        M_string_list_1 = []
        for i in range(len(self.M)):
            M_string_list_2 = []
            for j in range(len(self.M[i])):
                M_string_list_3 = []
                for k in range(len(self.M[i][j])):
                    M_string_list_3.append(str(self.M[i][j][k]))
                M_string_list_2.append(",".join(M_string_list_3))
            M_string_list_1.append(";".join(M_string_list_2))
        M_string = ":".join(M_string_list_1)

        V_string_list_1 = []
        for i in range(len(self.V)):
            V_string_list_2 = []
            for j in range(len(self.V[i])):
                V_string_list_2.append(str(self.V[i][j]))
            V_string_list_1.append(",".join(V_string_list_2))
        V_string = ";".join(V_string_list_1)

        output_string = '#'.join([M_string, V_string])
        return(output_string)
