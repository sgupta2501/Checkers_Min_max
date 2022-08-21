from constants import * 
from piece import Piece
from minmax import *

class board(object):

    def __init__(self, height, width, firstPlayer):
        # Set the height and width of the game board
        self.board = []

        self.width = width
        self.height = height
        # Create two lists which will contain the pieces each player posesses
        self.blacklist = []
        self.whitelist = []
        self.gameWon = NOTDONE
        self.turn = firstPlayer
        self.maxDepth = MAX_SEARCH_DEPTH
        self.white_left = self.black_left = 12
        self.white_kings = self.black_kings = 0
        self.create_board()
    
    def create_board(self):
        for row in range(height):
            # Set default piece positions
            #self.blacklist.append((row, (row+1)%2)) # row,col format same as board[row=0,1,2]
            #self.whitelist.append((row, height - (row%2) - 1)) #same as board[row=0,1,2]
            self.board.append([])
            for col in range(width):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK_color))
                        self.blacklist.append((row, col)) # row,col format same as board[row=0,1,2]
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE_color))
                        self.whitelist.append((row, col)) #same as board[row=0,1,2]
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def synch_board2lists(self):
        self.whitelist.clear()
        self.blacklist.clear()
        for row in range(height):
            for col in range(width):
                if self.board[row][col] != 0 and self.board[row][col].color==BLACK_color:
                    self.blacklist.append((row, col)) 
                elif self.board[row][col] != 0 and self.board[row][col].color==WHITE_color:
                    self.whitelist.append((row, col)) 

    def Diff(self, li1, li2):
        return list(set(li1) - set(li2)) # + list(set(li2) - set(li1))

    def synch_lists2board(self):
        #self.board.clear()
        #self.white_left = self.black_left = 0
        w = []
        b = []

        for row in range(height):
            for col in range(width):
                if self.get_piece(row,col) != 0 and self.board[row][col].color==BLACK_color:
                    b.append((row, col)) 
                elif self.get_piece(row,col) != 0 and self.board[row][col].color==WHITE_color:
                    w.append((row, col)) 
        #print(self.whitelist)
        #print(w)
        #print(self.blacklist)
        #print(b)

        wdiff=self.Diff(w,self.whitelist) #extra on board
        for (row,col) in wdiff:
            self.board[row][col]=0
            self.white_left = self.white_left -1
        #print (wdiff)
        wdiff=self.Diff(self.whitelist, w) #extra on list
        for (row,col) in wdiff:
            self.board[row][col]= Piece(row, col, WHITE_color) #.append(Piece(row, col, WHITE_color))
            self.white_left = self.white_left +1
        #print (wdiff)
        bdiff=self.Diff(b,self.blacklist) #extra on board
        for (row,col) in bdiff:
            self.board[row][col]=0
            self.black_left = self.black_left -1
        #print(bdiff)
        bdiff1=self.Diff(self.blacklist, b) #extra on list
        for (row,col) in bdiff1:
            self.board[row][col] = Piece(row, col, BLACK_color) #.append(Piece(row, col, BLACK_color))
            self.black_left = self.black_left +1
            if row == height - 1:
                self.board[row][col].make_king()
                self.black_kings += 1

        #print(bdiff)
        #if (bdiff or bdiff1) == False: # no change in blacklist
            #print("changing depth")
            #self.maxDepth = 4
        '''
        bdiff=self.Diff(b,self.blacklist)
        print(wdiff)
        print(bdiff)
        for (row,col) in wdiff:
            if self.get_piece(row, col)==0:
                self.board[row].append(Piece(row, col, WHITE_color))
                self.white_left = self.white_left +1
            else:
                self.board[row][col]=0
                self.white_left = self.white_left -1
        for (row,col) in bdiff:
            if self.get_piece(row, col)==0:
                self.board[row].append(Piece(row, col, BLACK_color))
                self.black_left = self.black_left +1
            else:
                self.board[row][col]=0
                self.black_left = self.black_left -1

        
        for row in range(height):
            self.board.append([])
            for col in range(width):
                if (row,col) in self.blacklist:
                    self.board[row].append(Piece(row, col, BLACK_color))
                    self.black_left = self.black_left + 1

                elif (row,col) in self.whitelist:
                    self.board[row].append(Piece(row, col, WHITE_color))
                    self.white_left = self.white_left + 1
                else:
                    self.board[row].append(0)
        '''

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        
        if piece.color == WHITE_color or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == BLACK_color or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, height), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, height), 1, piece.color, right))
        
        return moves

    def draw_squares(self, win):
        win.fill(GREEN_color)
        for row in range(height):
            for col in range(row % 2, width, 2):
                pygame.draw.rect(win, GREY_color, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(height):
            for col in range(width):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def winner(self):
        nb=0
        nw=0
        for row in range(height):
            for col in range(width):
                piece = self.board[row][col]
                if piece!=0 and piece.color==BLACK_color:
                    nb=nb+1
                elif piece!=0 and piece.color==WHITE_color:
                    nw=nw+1
        self.white_left = nw                    
        self.black_left = nb                    

        if self.white_left <= 0:
            self.gameWon = BLACK
        elif self.black_left <= 0:
            self.gameWon = WHITE
        else:
            self.gameWon = NOTDONE
        
        return self.gameWon 

    def move(self, piece, row, col):

        '''        
        moveFrom = (piece.row, piece.col)
        moveTo = (row, col)

        if self.turn == WHITE:
            self.moveSilentWhite(moveFrom, moveTo, NOTDONE)
        else:
            self.moveSilentBlack(moveFrom, moveTo, NOTDONE)
        '''
        
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == 0 and piece.color == WHITE_color:
            piece.make_king()
            self.white_kings += 1

        if row == height - 1 and piece.color == BLACK_color:
            piece.make_king()
            self.black_kings += 1
        
    def remove(self, pieces):
        #to remove from both board and white/black lists
        for piece in pieces:
            if piece != 0:
                self.board[piece.row][piece.col] = 0
                if self.turn==BLACK:    
                    if (piece.row, piece.col) in self.blacklist:
                        self.blacklist.remove((piece.row, piece.col)) # row,col format same as board[row=0,1,2]
                    self.black_left -= 1
                else:
                    if (piece.row, piece.col) in self.whitelist:
                        self.whitelist.remove((piece.row, piece.col)) #same as board[row=0,1,2]
                    self.white_left -= 1
                    

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, height)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= width:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, height)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves


    # Generate an iterator for all of the moves
    def iterWhiteMoves(self):
        """
            Main generator for white moves
        """
        for piece in self.whitelist:
            for move in self.iterWhitePiece(piece):
                yield move
                
    def iterBlackMoves(self):
        """
            Main Generator for black moves
        """
        for piece in self.blacklist:
            for move in self.iterBlackPiece(piece):
                yield move
                
    def iterWhitePiece(self, piece):
        """
            Generates possible moves for a white piece
        """            
        return self.iterBoth(piece, ((-1,-1),(1,-1)))
    
    def iterBlackPiece(self, piece):
        """
            Generates possible moves for a black piece
        """
        return self.iterBoth(piece, ((-1,1),(1,1)))

    def iterBoth(self, piece, moves):
        """
            Handles the actual generation of moves for either black or white pieces
        """
        for move in moves:
            # Regular Move
            targetx = piece[0] + move[0]
            targety = piece[1] + move[1]
            # If the move is out of bounds don't move
            if targetx < 0 or targetx >= self.width or targety < 0 or targety >= self.height:
                continue
            target = (targetx, targety)
            # Check that there is nothing in the way of moving to the target
            black = target in self.blacklist
            white = target in self.whitelist
            if not black and not white:
                yield (piece, target, NOTDONE)
            # There was something in the way, can we jump it?
            else:
                # It has to be of the opposing color to jump
                if self.turn == BLACK and black:
                    continue
                elif self.turn == WHITE and white:
                    continue
                # Jump proceeds by adding the same movement in order to jump over the opposing 
                # piece on the checkerboard
                jumpx = target[0] + move[0]
                jumpy = target[1] + move[1]
                # If the jump is going to be out of bounds don't do it.
                if jumpx < 0 or jumpx >= self.width or jumpy < 0 or jumpy >= self.height:
                    continue
                jump = (jumpx, jumpy)
                # Check that there is nothing in the jumpzone
                black1 = jump in self.blacklist
                white1 = jump in self.whitelist
                if not black1 and not white1:
                    #remove target
                    if white:
                        self.whitelist.remove(target)
                    #else:
                        #self.blacklist.remove(target)
                    yield (piece, jump, self.turn)                   

    # Movement of pieces
    def moveSilentBlack(self, moveFrom, moveTo, winLoss): 
        """
            Move black piece without printing
        """
        if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
            raise Exception("That would move black piece", moveFrom, "out of bounds")
        black = moveTo in self.blacklist
        white = moveTo in self.whitelist
        if not (black or white):
            self.blacklist[self.blacklist.index(moveFrom)] = moveTo
            self.turn = WHITE
            self.gameWon = winLoss
        else:
            raise Exception
        
    def moveSilentWhite(self, moveFrom, moveTo, winLoss):

        if moveTo[0] < 0 or moveTo[0] >= self.width or moveTo[1] < 0 or moveTo[1] >= self.height:
            raise Exception("That would move white piece", moveFrom, "out of bounds")
        black = moveTo in self.blacklist
        white = moveTo in self.whitelist
        if not (black or white):
            self.whitelist[self.whitelist.index(moveFrom)] = moveTo
            self.turn = BLACK
            self.gameWon = winLoss
        else:
            raise Exception
    
