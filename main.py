import pygame

from board import *
from constants import *
from game import Game
from piece import Piece

WIN = pygame.display.set_mode((ScrWIDTH, ScrHEIGHT))
pygame.display.set_caption('Checkers by Aadhavan, Ridham, Samarth')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

### MAIN PROGRAM ###


def main():
    clock = pygame.time.Clock()
    game = Game(WIN)

    # Main game loop
    run=True
    while run:
        clock.tick(FPS)
        if game.board.winner() != NOTDONE and game.board.gameWon != NOTDONE: #???
            if (game.board.gameWon==WHITE):
                print("white wins!!")
            elif (game.board.gameWon==BLACK):
                print("Black wins!!")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            val=None
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                #print("white now")
                game.turn=WHITE
                piece = game.board.get_piece(row, col)
                #print("#white pieces")
                #print(game.board.white_left)
                #print("#black pieces")
                #print(game.board.black_left)

                if (piece !=0 and piece.color == BLACK_color) == False:
                    val=game.select(row, col) # from move of user- white
                    game.update()
                #print(game.turn)
                #print(val)
                if (val==False and game.turn == BLACK): #white moved
                    #print("black now")
                    #copy board to lists
                    game.board.synch_board2lists()
                    val=None
                    temp = minMax2(game.board)
                    diffHere=game.board.Diff(game.board.blacklist,temp[0].blacklist)
                    game.board=temp[0]
                    game.board.synch_lists2board()
                    game.turn=game.board.turn
                        
                    ok=True
                    i=-1
                    while ok==True:
                        i = i+1
                        if i < len(game.board.blacklist) and diffHere == []: # no change in blacklist
                            #print("in main: no change in blacklist")
                            game.turn=BLACK
                            row2,col2=game.board.blacklist[i]
                            #print(row2,col2)
                            ok=game.selectBlack(row2, col2) 

                            game.board.synch_board2lists()
                        else:
                            ok=False
                        diffHere=game.board.Diff(game.board.blacklist,temp[0].blacklist)
                    
                    game.update()
            game.update()

    pygame.quit()

main()

'''

def get_User_Move(b):
    while True: # Loop until proper input
        statement1 = "Select one of your tokens to move in format row col with space"
        print(statement1)
        move = []
        move = input().split()
        moveFromTup = (int(move[0]), int(move[1]))
        statement1 = "Select one of the locations to move to format row col with space"
        print(statement1)
        move = input().split()
        moveToTup = (int(move[0]), int(move[1]))
        #print(move)
        #if not(len(move) == 2):
            #print ("That is not a valid move, try again.", statement1)
            #continue
        #print(b.whitelist)
        # Is the piece we want to move one we own?
        if not (moveFromTup in b.whitelist):
            print ("You do not own", moveFromTup, "please select one of.", b.whitelist)
            continue
        break
    move = (moveFromTup, moveToTup, b.NOTDONE)
    return move



    # First it is the users turn
    userMove = get_User_Move(b)
    print("User move ",userMove)
    try:
        b.moveWhite(*userMove)
        print("movewhite complete")
    except Exception:
        print ("Invalid move")
        continue
        
    # Then it is the computers turn
    temp = minMax2(b)
    print("minmax complete")
    b = temp[0]
    print ("**********COMPUTER MOVE**********")
    b.printBoard()

    if b.gameWon == b.WHITE:
        print( "White Wins Game Over")
        break
    elif b.gameWon == b.BLACK:
        print ("Black Wins Game Over")
        break

'''
