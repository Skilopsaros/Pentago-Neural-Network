import numpy as np
import random
import copy
import board

class network:

    def __init__(self,Ms,Vs):
        self.M = Ms
        self.V = Vs
        self.rating = 0

    def hypertan(self,list):
        output = np.zeros(len(list))
        for i in range(len(list)):
            if list[i]>10:
                output[i]=1.
            elif list[i]<-10:
                output[i]=1.
            else:
                exponential = np.exp(2*list[i])
                output[i] = (exponential-1)/(exponential+1)
        return(output)

    def calculate_output(self, input):

        output = input
        for i in range(len(self.M)):
            output = (np.dot(self.M[i], output)+self.V[i])
        return(self.hypertan(output))

    def produce_child(self, weight_sigma = 0.1, bias_sigma = 0.1, chance_to_change = 0.5):
        new_Ms = copy.deepcopy(self.M)
        for i in range(len(new_Ms)):
            for j in range(len(new_Ms[i])):
                for k in range(len(new_Ms[i][j])):

                    if random.uniform(0, 1)<chance_to_change:
                        new_Ms[i][j][k] += random.gauss(0,weight_sigma*self.M[i][j][k])

        new_Vs = copy.deepcopy(self.V)
        for i in range(len(new_Vs)):
            for j in range(len(new_Vs[i])):

                if random.uniform(0, 1)<chance_to_change:
                    new_Vs[i][j] += random.gauss(0,weight_sigma*self.V[i][j])

        return(network(new_Ms,new_Vs))

    def get_weights(self):
            return(self.M,self.V)

    def calculate_move(self,board):

        pass
