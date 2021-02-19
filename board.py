import copy
import numpy as np

# defining the sub board class
class sub_board:

    def __init__(self):
        #each sub board has 9 positions, arranged in a 3X3
        self.contents = np.zeros([3, 3], dtype=int)

    def rotate(self,direction):
        '''Rotates the sub-board. direction "C" rotates it clockwise, and "A" rotates it anticlockwise'''
        temp=copy.deepcopy(self.contents)
        if direction == 'C':
            #rotate clockwise
            self.contents = np.array([[temp[2][0],temp[1][0],temp[0][0]],[temp[2][1],temp[1][1],temp[0][1]],[temp[2][2],temp[1][2],temp[0][2]]])
        elif direction == 'A':
            #rotate anticlockwise
            self.contents = np.array([[temp[0][2],temp[1][2],temp[2][2]],[temp[0][1],temp[1][1],temp[2][1]],[temp[0][0],temp[1][0],temp[2][0]]])

    def show(self):
        for i in range(3):
            print(self.contents[i])


###########################################################################################################
# defining the board class
class board:

    def __init__(self):
        self.subs = [[sub_board(),sub_board()],[sub_board(),sub_board()]]
        self.contents = np.zeros([6, 6], dtype=int)
        self.turn = 0

    def calculate_contents(self):
        for i in range(6):
            for j in range(6):
                self.contents[i][j] = self.subs[(i)//3][(j)//3].contents[i-3*((i)//3)][j-3*((j)//3)]

    def show(self):
        for i in range(3):
            print(str(self.subs[0][0].contents[i])+str(self.subs[0][1].contents[i]))
        print("--------------")
        for i in range(3):
            print(str(self.subs[1][0].contents[i])+str(self.subs[1][1].contents[i]))

    def change_board(self,x,y,value):
        self.subs[(y-1)//3][(x-1)//3].contents[y-1-3*((y-1)//3)][x-1-3*((x-1)//3)] = value

    def rotate_sub(self,x,y,direction):
        '''rotates one of the sub boards. x=0 y=0 is top left, x=0 y=1 is top right, etc. direction "C" for clockwise and "A" for anticlockwise'''
        self.subs[y][x].rotate(direction)

    def check_for_win(self):
        '''checks the board for a win state. Returns 1 if player 1 won, 2 if player 2 won, 3 if it is a tie, and 0 otherwise'''
        def check_vertical(x,y,n):
            if (self.contents[y][x] == self.contents[y+1][x]):
                if n<3:
                    return(check_vertical(x,y+1,n+1))
                else:
                    return(self.contents[y][x])
            else:
                return(0)

        def check_horizontal(x,y,n):
            if (self.contents[y][x] == self.contents[y][x+1]):
                if n<3:
                    return(check_horizontal(x+1,y,n+1))
                else:
                    return(self.contents[y][x])
            else:
                return(0)

        def check_diagonal(x,y,n):
            if (self.contents[y][x] == self.contents[y+1][x+1]):
                if n<3:
                    return(check_diagonal(x+1,y+1,n+1))
                else:
                    return(self.contents[y][x])
            else:
                return(0)

        def check_reverse_diagonal(x,y,n):
            if (self.contents[y][x] == self.contents[y-1][x+1]):
                if n<3:
                    return(check_reverse_diagonal(x+1,y-1,n+1))
                else:
                    return(self.contents[y][x])
            else:
                return(0)

        self.calculate_contents()
        wins_player_1 = 0
        wins_player_2 = 0
        for i in range(2):
            for j in range(6):
                if self.contents[j][i] != 0:
                    win = check_horizontal(i,j,0)
                    if 1 == win:
                        wins_player_1 += 1
                    elif 2 == win:
                        wins_player_2 += 1
                if self.contents[i][j] !=0:
                    win = (check_vertical(j,i,0))
                    if 1 == win:
                        wins_player_1 += 1
                    elif 2 == win:
                        wins_player_2 += 1
            for j in range(2):
                if self.contents[j][i] != 0:
                    win = (check_diagonal(i,j,0))
                    if 1 == win:
                        wins_player_1 += 1
                    elif 2 == win:
                        wins_player_2 += 1
                    win = (check_reverse_diagonal(i,5-j,0))
                    if 1 == win:
                        wins_player_1 += 1
                    elif 2 == win:
                        wins_player_2 += 1
        if wins_player_1 > wins_player_2:
            return(1)
        elif wins_player_2 > wins_player_1:
            return(2)
        elif wins_player_2 == wins_player_1 and wins_player_1 != 0:
            return(3)
        else:
            return(0)

class game:

    def __init__(self):
        self.board = board()

    def first_half_round(self,x,y):
        if 0 == self.board.subs[(y-1)//3][(x-1)//3].contents[y-1-3*((y-1)//3)][x-1-3*((x-1)//3)]:
            self.board.change_board(x,y,(board.turn%2+1))
            return(1)
        else:
            return(0)

    def second_half_round(self,rx,ry,direction):
        self.board.rotate_sub(rx,ry,direction)
        self.board.turn += 1
        return(self.board.check_for_win())

#something New
