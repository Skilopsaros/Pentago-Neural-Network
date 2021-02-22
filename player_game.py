import board
import games_and_training as gat
import os




def sane_int_input(lower_bound,upper_bound,text):
    try:
        output = int(input(text))
    except ValueError:
        print('Please provide a correct input, an integer between '+ str(lower_bound)+' and '+str(upper_bound)+' inclusive.')
        return(sane_int_input(upper_bound,lower_bound,text))
    if (output>=lower_bound) and (output<=upper_bound):
        return(output)
    else:
        print('Please provide a correct input, an integer between '+ str(lower_bound)+' and '+str(upper_bound)+' inclusive.')
        return(sane_int_input(lower_bound,upper_bound,text))

def sane_rotational_input(text):
    try:
        output = input(text)
    except ValueError:
        print('Please provide a correct input, either C for clockwise or A for anticlockwise. Leters must be capital.')
        return(sane_rotational_input(text))
    if (output=='C') or (output=='A'):
        return(output)
    else:
        print('Please provide a correct input, either C for clockwise or A for anticlockwise. Leters must be capital.')
        return(sane_rotational_input(text))

def play_game():
    game = board.game()
    game_over = False
    print('Coordinates are counted from the top left corner, which is always x=1, y=1.')
    print('y increases going downwards, and x increases going to the right')
    game.board.show()
    print()

    while not game_over:
        print()
        print('turn '+str(game.board.turn+1))
        print('Player '+str(game.board.turn%2+1))
        print('Enter the coordinates of the spot to drop a stone')
        valid_move = 0
        while valid_move == 0:
            x = sane_int_input(1,6,'Enter x coordinate: ')
            y = sane_int_input(1,6,'Enter y coordinate: ')
            valid_move = game.first_half_round(x,y)
            if 0 == valid_move:
                print('Invalid move')
        game.board.show()
        print('Enter the coordinatesa and direction of the tile to rotate')
        rx = sane_int_input(1,2,'Enter x coordinate: ')
        ry = sane_int_input(1,2,'Enter y coordinate: ')
        direction = sane_rotational_input('Enter direction, C for clockwise, A for anticlockwise: ')
        win_state = game.second_half_round(rx-1,ry-1,direction)
        game.board.show()
        print()

        if (win_state == 0) and (game.board.turn >= 36):
            win_state = 3

        if win_state != 0:
            game_over = True
            if win_state == 3:
                print("It's a tie!")
            else:
                print('Player '+str(win_state)+' wins!')

def game_against_network():

    files = os.listdir(os.getcwd()+'/training')
    largest_gen = 0
    for i in files:
        if int(i.split('#')[1].split('.')[0])>largest_gen:
            largest_gen = int(i.split('#')[1].split('.')[0])
    gen = largest_gen
    file = open('training/Generation #'+str(gen)+'.txt', 'r')
    one_parent_string = file.read()
    file.close()

    player_number = sane_int_input(1,2,'Enter 1 to be player 1, or 2 to be player 2 ')

    parent_strings = one_parent_string.split('@')
    enemy = gat.strings_to_networks(parent_strings[0])

    game = board.game()
    game_over = False
    print('Coordinates are counted from the top left corner, which is always x=1, y=1.')
    print('y increases going downwards, and x increases going to the right')
    print('playing against gen '+str(gen))
    game.board.show()
    print()


    while not game_over:
        print()
        print('turn '+str(game.board.turn+1))
        if game.board.turn%2+1 == player_number:
            print('Player '+str(game.board.turn%2+1))
            print('Enter the coordinates of the spot to drop a stone')
            valid_move = 0
            while valid_move == 0:
                x = sane_int_input(1,6,'Enter x coordinate: ')
                y = sane_int_input(1,6,'Enter y coordinate: ')
                valid_move = game.first_half_round(x,y)
                if 0 == valid_move:
                    print('Invalid move')
            game.board.show()
            print('Enter the coordinatesa and direction of the tile to rotate')
            rx = sane_int_input(1,2,'Enter x coordinate: ')
            ry = sane_int_input(1,2,'Enter y coordinate: ')
            direction = sane_rotational_input('Enter direction, C for clockwise, A for anticlockwise: ')
            win_state = game.second_half_round(rx-1,ry-1,direction)
            game.board.show()
            print()
        else:
            print()
            print('Network Turn')
            win_state = enemy.calculate_move(game)
            game.board.show()
            print()


        if (win_state == 0) and (game.board.turn >= 36):
            win_state = 3

        if win_state != 0:
            game_over = True
            if win_state == 3:
                print("It's a tie!")
            else:
                print('Player '+str(win_state)+' wins!')


def network_v_network():

    files = os.listdir(os.getcwd()+'/training')
    largest_gen = 0
    for i in files:
        if int(i.split('#')[1].split('.')[0])>largest_gen:
            largest_gen = int(i.split('#')[1].split('.')[0])
    gen = largest_gen
    file = open('training/Generation #'+str(gen)+'.txt', 'r')
    one_parent_string = file.read()
    file.close()

    parent_strings = one_parent_string.split('@')
    players = [gat.strings_to_networks(parent_strings[0]), gat.strings_to_networks(parent_strings[1])]

    game = board.game()
    print('Generation '+str(gen))
    game.board.show()
    print()

    while 0 == players[game.board.turn%2].calculate_move(game):
        print('Player '+str((game.board.turn+1)%2+1))
        game.board.show()
        print()
    print('Player '+str((game.board.turn+1)%2+1))
    game.board.show()
    print()
network_v_network()
