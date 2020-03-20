import numpy as np
import random

MAX_SEARCH_DEPTH = 4
MAX=1000000
MIN=-1000000


def is_col_empty(board, col):
    if (board[0][col] == 0):
        return True


def empty_locations(board):
    empty_locations = []
    for col in range(7):
        if is_col_empty(board, col):
            empty_locations.append(col)
    return empty_locations

def find_open_row(board, col):
	for r in range(6):
		if board[5-r][col] == 0:
			return (5-r)

def is_terminal(self,board):
    #if Player won return true
    if (AIPlayer.evaluation_function(self,board)>=MAX*2):
        return 1
    #if Adversary won return true
    elif (AIPlayer.evaluation_function(self,board)<=MIN*2):
        return 2
    #if no more spaces left 
    elif (len(empty_locations(board)) == 0):
        return 3
    else:
        return 0


def max_val(self, board, depth, alpha, beta):
    #if winning move was from either player return utility
    if (is_terminal(self,board)==1):
        return (None, MAX*2)
    elif (is_terminal(self,board)==2):
        return (None, MIN*2)
    #if it is a draw return 0
    elif (is_terminal(self,board)==3):
        return (None, 0)
    if (depth==0):
        return (None, AIPlayer.evaluation_function(self, board))
        
    locations=empty_locations(board)
    value=MIN
    #set a random column to return in case no better choice is available
    column=random.choice(locations)
    for col in locations:
        row=find_open_row(board, col)
        temp_board=board.copy()
        #dropping player's piece to calculate a new utility
        temp_board[row][col] = self.player_number
        #recusively go through min value
        new_value=min_val(self,temp_board, depth-1, alpha, beta)[1]
        if new_value>value:
            value=new_value
            column=col
        alpha=max(alpha, value)
        #prune if alpha is bigger than beta
        if alpha >=beta:
            break
    return column, value

def min_val(self, board, depth, alpha, beta):
    #if winning move was from either player return utility
    if (is_terminal(self,board)==1):
        return (None, MAX*2)
    elif (is_terminal(self,board)==2):
        return (None, MIN*2)
    #if it is a draw return 0
    elif (is_terminal(self,board)==3):
        return (None, 0)
    if (depth==0):
        return (None, AIPlayer.evaluation_function(self, board))

    locations=empty_locations(board)
    value=MAX
    #set a random column to return in case no better choice is available
    column=random.choice(locations)
    if (self.player_number==1):
        adversary=2
    else:
        adversary=1

    for col in locations:
        row=find_open_row(board, col)
        temp_board=board.copy()
        #dropping opponent's piece to calculate a new utility
        temp_board[row][col] = adversary
        #recusively go through min value
        new_value=max_val(self,temp_board, depth-1, alpha, beta)[1]
        if new_value<value:
            value=new_value
            column=col
        beta=min(beta, value)
        #prune if alpha is bigger than beta
        if alpha >=beta:
            break
    return column, value

class AIPlayer:
    """
    INPUTS:
    board - a numpy array containing the state of the board using the
                following encoding:
            - the board maintains its same two dimensions
            - row 0 is the top of the board and so is
                      the last row filled
            - spaces that are unoccupied are marked as 0
            - spaces that are occupied by player 1 have a 1 in them
            - spaces that are occupied by player 2 have a 2 in them
    """
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    def get_alpha_beta_move(self, board):

        
        col, utility =max_val(self,board,MAX_SEARCH_DEPTH,MIN,MAX)
        #print("Player", self.player_number, " Score: ", utility)
        return col


    def get_expectimax_move(self, board):

        col=self.value(board, MAX_SEARCH_DEPTH, True)[0]
        return col

    def value(self, board, depth, max):

        if (depth==0 or is_terminal(self,board)>0):
            if (max):
                return (None, self.evaluation_function(board))
            else:
                return (None, self.evaluation_function(board))
        
        if (max):
            return self.max_value(board,depth)

        else:
            return self.exp_value(board,depth)

    def max_value(self, board, depth):

        locations=empty_locations(board)
        value=MIN
        #set a random column to return in case no better choice is available
        column=random.choice(locations)
        for col in locations:
            row=find_open_row(board, col)
            temp_board=board.copy()
            #dropping player's piece to calculate a new utility
            temp_board[row][col] = self.player_number
            #recusively go through min value
            new_value=self.value(temp_board, depth-1, False)[1]
            if (new_value>value):
                value=new_value
                column=col
        return (column, value)


    def exp_value(self, board, depth):
        locations=empty_locations(board)
        value=0
        column=random.choice(locations)
        p=1/(len(locations))
        for col in locations:
            row=find_open_row(board, col)
            temp_board=board.copy()
            #dropping player's piece to calculate a new utility
            temp_board[row][col] = self.player_number
            #recusively go through min value
            new_value=self.value(temp_board, depth-1, True)[1]
            value+=p*new_value
        return (None, value)

    def evaluation_function(self, board):
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player

        RETURNS:
        The utility value for the current board
        """

        if (self.player_number==1):
            adversary=2
        else:
            adversary=1
            
        utility1=AIPlayer.checkStones(board, self.player_number)
        utility2=AIPlayer.checkStones(board, adversary)
        #print (utility1-utility2)
        return (utility1-utility2)
        
    #checks the number of connecting stones on the board for both the player and opponent
    #calculates the total utility score of the board
    def checkStones(board, playernum):

        col=row=i=0
        num_stones = two = three = four=0
        score=utility=0

        #reward for center area 
        center_array = [int(x) for x in list(board[:, 3])]
        center_count = center_array.count(playernum)
        score += center_count*3

        for i in np.nditer(board):
            if (col+1)%8==0:
                row+=1
                col=0

            #check for player stones
            if board[row][col]==playernum:
                temp_row=row
                temp_col=col
                #check vertical stones
                while temp_row!=6 and board[temp_row][temp_col]==playernum:
                    num_stones+=1 #increment any time we find a new stone
                    temp_row+=1
                if num_stones==2:
                    two+=1
                elif num_stones==3:
                    three+=1
                elif num_stones==4:
                    four+=1
                num_stones=0
                temp_row=row
                temp_col=col
                #check horizontal stones
                while temp_col!=7 and board[temp_row][temp_col]==playernum:
                    num_stones+=1 #increment any time we find a new stone
                    temp_col+=1
                if num_stones==2:
                    two+=1
                elif num_stones==3:
                    three+=1
                elif num_stones==4:
                    four+=1
                num_stones=0
                temp_row=row
                temp_col=col
                #check diagonal (SE direction) stones
                while temp_row!=6 and temp_col!=7 and board[temp_row][temp_col]==playernum:
                    num_stones+=1 #increment any time we find a new stone
                    temp_col+=1
                    temp_row+=1
                if num_stones==2:
                    two+=1
                elif num_stones==3:
                    three+=1
                elif num_stones==4:
                    four+=1
                num_stones=0
                temp_row=row
                temp_col=col
                #check diagonal (SW direction) stones
                while temp_row!=6 and temp_col+1!=0 and board[temp_row][temp_col]==playernum:
                    num_stones+=1 #increment any time we find a new stone
                    temp_col-=1
                    temp_row+=1
                if num_stones==2:
                    two+=1
                elif num_stones==3:
                    three+=1
                elif num_stones==4:
                    four+=1
                num_stones=0
            col+=1
        utility=(2*MAX*four)+(100*three)+two+score
        
        return utility

class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)
    
    #Given the current board state select a random column from the available valid moves.
    def get_move(self, board):

        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    #Given the current board state returns the human input for next move
    def get_move(self, board):


        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

