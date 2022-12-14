# Provides the minmax functionality as well as static evaluation
from copy import deepcopy
from constants import * 
import random
def is_won(board):
    """
        Returns true if the game has been won
    """
    return board.gameWon != NOTDONE
        

def minMax2(board):
    """
        Main minmax function, takes a board as input and returns the best possible move in the form
        of a board and the value of that board.
    """
    bestBoard = None
    currentDepth = board.maxDepth + 1
    #print("in maxmin")
    #print(board.maxDepth)
    while not bestBoard and currentDepth > 0:
        currentDepth -= 1
        # Get the best move and it's value from maxMinBoard (minmax handler)
        (bestBoard, bestVal) = maxMove2(board, currentDepth)
        # If we got a NUll board raise an exception
    if not bestBoard:
        raise Exception("Could only return null boards")
    # Otherwise return the board and it's value
    else:
        return (bestBoard, bestVal)

def maxMove2(maxBoard, currentDepth):
    """
        Calculates the best move for BLACK player (computer) (seeks a board with INF value)
    """
    return maxMinBoard(maxBoard, currentDepth-1, float('-inf'))
    

def minMove2(minBoard, currentDepth):
    """
        Calculates the best move from the perspective of WHITE player (seeks board with -INF value)
    """
    return maxMinBoard(minBoard, currentDepth-1, float('inf'))

def maxMinBoard(board, currentDepth, bestMove):
    """
        Does the actual work of calculating the best move
    """
    # Check if we are at an end node
    if is_won(board) or currentDepth <= 0:
        return (board, staticEval2(board))
  
    # So we are not at an end node, now we need to do minmax
    # Set up values for minmax
    #f=open('geek.txt','r')

    #playmode=f.read()
    #f.close()
    # So we are not at an end node, now we need to do minmax
    # Set up values for minmax
    '''
    if(playmode=='AI'):
        best_move = bestMove
    else:
        ran=randrange(10)
        if(ran<5):
            best_move=float('-inf')
        else:
            best_move=float('inf')
    best_board = None    
'''
    abc=float(1)
    f=open('geek.txt','r')
    pmode=f.read()
    f.close()
    ll=[1.0,-1.0]
    if(pmode=='RANDOM'):
        abc=random.choice(ll)
    best_move = bestMove
    best_board = None    
    #print(pmode)
    #print(abc)
    # MaxNode
    if bestMove == (float('-inf')*abc):
        # Create the iterator for the Moves
        moves = board.iterBlackMoves()
        for move in moves:
            row, col = move[0]
            row1,col1=move[1]
            if row >= row1:
                continue
            maxBoard = deepcopy(board)
            #piece = maxBoard.get_piece(row, col)

            maxBoard.moveSilentBlack(*move)
            '''
            print(move[0])
            print(move[1])
            print(move[2])        
            print(row1, col1)
            '''
            #maxBoard.move(piece, row1, col1) # in move we call silent move for black.white lists
            #maxBoard.gameWon=move[2]
            value = minMove2(maxBoard, currentDepth-1)[1]
            if value > best_move:
                best_move = value
                best_board = maxBoard         
  
    # MinNode
    elif bestMove ==(abc*float('inf')):
        moves = board.iterWhiteMoves()
        for move in moves:
            row, col = move[0]
            row1,col1=move[1]
            if row <= row1:
                continue
            minBoard = deepcopy(board)
            #row, col = move[0]
            #row1,col1=move[1]
            #piece = minBoard.get_piece(row, col)
            
            minBoard.moveSilentWhite(*move)
            #minBoard.move(piece,row1,col1)            
            #minBoard.gameWon=move[2]
            value = maxMove2(minBoard, currentDepth-1)[1]
            # Take the smallest value we can
            if value < best_move:
                best_move = value
                best_board = minBoard
  
    # Something is wrong with bestMove so raise an Exception
    else:
        raise Exception("bestMove is set to something other than inf or -inf")
  
    # Things appear to be fine, we should have a board with a good value to move to
    return (best_board, best_move)

def staticEval2(evalBoard):
    if evalBoard.gameWon == BLACK:
        return float('inf')  
    elif evalBoard.gameWon == WHITE:
        return float('-inf')
    
    # Some setup
    score = 0
    pieces = None   
    if evalBoard.turn == WHITE:
        pieces = evalBoard.whitelist
        scoremod = -1
    elif evalBoard.turn == BLACK:
        pieces = evalBoard.blacklist
        scoremod = 1

    # Super Gigadeath Defense Evaluator
    distance = 0
    for piece1 in pieces:
        for piece2 in pieces:
            if piece1 == piece2:
                continue
            dx = abs(piece1[0] - piece2[0])
            dy = abs(piece1[1] - piece2[1])
            distance += dx**2 + dy**2
    distance /= len(pieces)
    if (distance==0):
        distance=0.001
    score = 1.0/distance * scoremod
    
    return score
