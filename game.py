import pygame
from constants import *
from board import board
from minmax import *

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def _init(self):
        self.selected = None
        self.turn=firstPlayer
        self.board = board(height,width,self.turn)
        self.valid_moves = {}

    def cmpPieceTurn(self,piece):
        if (self.turn == WHITE and piece.color==WHITE_color) or (self.turn == BLACK and piece.color==BLACK_color):
            return True
        else:
            return False

    def select(self, row, col):
        #print("select")
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and self.cmpPieceTurn(piece):
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False


    def selectBlack(self, row, col):
            
            piece = self.board.get_piece(row, col)
            if piece != 0 and self.cmpPieceTurn(piece):
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                #print("black valid moves")
                #print(self.valid_moves)
                for (row,col),val in self.valid_moves.items():
                    #print(row,col)
                    #print(val)
                    row1=row
                    col1=col
                    #if val==WHITE_color:
                        #row1 =row+1
                        #col1=col-1
                    result = self._move(row1,col1) #key_list[0])
                    self.turn=BLACK
                    if result:
                        return False

                return True

    def update(self):
        #print("update")
        self.board.draw(self.win)
        if (self.turn==WHITE):
            self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        if (self.turn == WHITE):
            for move in moves:
                row, col = move
                pygame.draw.circle(self.win, BLUE_color, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 35)

    def reset(self):
        self._init()

    '''
    def winner(self):
        return self.board.winner()
    '''

    def _move(self, row, col):
        #print("game.move")
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            '''
            moveFrom = (self.selected.row, self.selected.col)
            moveTo = (row, col)
            
            print(moveFrom)
            print(moveTo)
            print(self.board.whitelist)
            print(self.board.blacklist)
        
            if self.turn == WHITE:
                self.board.moveSilentWhite(moveFrom, moveTo, NOTDONE)
            else:
                self.board.moveSilentBlack(moveFrom, moveTo, NOTDONE)

            
            if (self.turn==WHITE):
                self.board.moveSilentWhite((self.selected.row,self.selected.col), (row,col), NOTDONE)
            else:
                self.board.moveSilentBlack((self.selected.row,self.selected.col), (row,col), NOTDONE)
            '''
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped) #???
            self.change_turn()
        else:
            return False

        return True

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    '''
    def Diff(self, li1, li2):
        return list(set(li1) - set(li2)) + list(set(li2) - set(li1))
 

            #self.board.turn=BLACK
            temp = minMax2(self.board)

            wl=self.Diff(temp[0].whitelist, self.board.whitelist)
            wb=self.Diff(temp[0].blacklist, self.board.blacklist)
            print(wl)
            print(wb)
            self.board = temp[0]

            if wl:
                self.board.removeMinmax(wl)
            if wb:
                self.board.removeMinmax(wb)

            #self.update()
            #self.change_turn()
    

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
            #self.board.turn=BLACK
            temp = minMax2(self.board)
            self.board = temp[0]
            self.change_turn()
        else:
            self.turn = WHITE
            #self.board.turn = WHITE

    '''