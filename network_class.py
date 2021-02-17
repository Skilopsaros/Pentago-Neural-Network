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
        self.rating = 0

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

    def produce_child(self, weight_sigma = 0.1, bias_sigma = 0.1, chance_to_change = 0.5):
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

    def calculate_move(self,board):

        pass
