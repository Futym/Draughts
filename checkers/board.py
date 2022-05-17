
import pygame
from checkers.constants import BLACK, COLS, DARK_BROWN, LIGHT_BROWN, ROWS, SQUARE_SIZE, WHITE
from checkers.piece import Piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = []
        self.black_left = self.white_left = 8
        self.black_queens = self.white_queens = 0
        self.black_queen_moves = 0
        self.white_queen_moves = 0
        self.create_board()
        
    def draw_squares(self, win):
        win.fill(DARK_BROWN)
        for row in range(ROWS):
            for col in range(row%2, ROWS, 2):
                pygame.draw.rect(win,LIGHT_BROWN,(row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def evaluate(self):
        my_rating = 0
        opponents_rating = 0
        size=len(self.board)
        for i in range(size):
            for j in range((i + 1) % 2, size, 2):
                piece = self.board[i][j]
                if (piece != 0): # field is not empty
                    zone=self.check_zone(size, (piece.col, piece.row))
                    if piece.color == WHITE: # this is my piece
                        if piece.queen:
                            my_rating += zone * 5 # this is my queen
                        else:
                            my_rating += zone * 1 # this is my man
                    else:
                        if piece.queen:
                            opponents_rating += zone * 5 # this is opponent's queen
                        else:
                            opponents_rating += zone * 1  
        # print("Type your message here, you will see it in the log window\n");
        return my_rating - opponents_rating
    
    def check_zone(self, size, field):
        y, x = field
        zone = 1
        
        if y > 0 and x > 0 and y < size - 1 and x < size - 1:
            zone = 2
        
        if y > 1 and x > 1 and y < size - 2 and x < size - 2:
            zone = 3
        
        return zone
    
    def get_all_pieces(self, color):
        pieces = []
        size=len(self.board)
        for i in range(size):
            for j in range((i + 1) % 2, size, 2):
                piece = self.board[i][j]
                if piece != 0 and piece.color == color: # field is not empty
                    pieces.append(piece)
        return pieces
              
    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] =  self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)
        
        if row == ROWS - 1 or row == 0:
            if piece.color == WHITE and row == 0 and not piece.queen:
                piece.make_queen()
                self.white_queens += 1
            
            if piece.color == BLACK and row == ROWS -1 and not piece.queen:
                piece.make_queen()
                self.black_queens += 1
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1
                    
    def winner(self):
        if self.white_left == 0:
            return BLACK
        elif self.black_left == 0:
            return WHITE        
        return None
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 2:
                        self.board[row].append(Piece(row, col, BLACK)) 
                    elif row > 5:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
                    
                    
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)
                    
    def get_valid_moves(self, piece):
        moves ={}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row
        
        if piece.color == WHITE and not piece.queen:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left, piece = piece))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right, piece = piece))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left, piece = piece))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right, piece = piece))
            
        if piece.color == BLACK and not piece.queen:
            moves.update(self._traverse_left(row +1, min(row + 3, ROWS), 1, piece.color, left, piece = piece))
            moves.update(self._traverse_right(row +1, min(row + 3, ROWS), 1, piece.color, right, piece = piece))
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left, piece = piece))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right, piece = piece))
            
        if piece.queen:
            moves.update(self._traverse_left_queen(row +1, ROWS, 1, piece.color, left, piece.queen))
            moves.update(self._traverse_right_queen(row +1, ROWS, 1, piece.color, right, piece.queen))
            moves.update(self._traverse_left_queen(row - 1, -1, -1, piece.color, left, piece.queen))
            moves.update(self._traverse_right_queen(row - 1, -1, -1, piece.color, right, piece.queen))
        
        moves = self.choose_longest_jump(moves)
        return moves
        
        
    def _traverse_left(self, start, stop, step, color, left, skipped = [], piece = None):
        moves = {}
        last =[]
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == piece:
                current = 0
            
            if current == 0:
                if skipped and not last:
                    break
                elif skipped :
                    last = last + skipped
                elif not last:
                    if (step == -1 and color == WHITE) or (step == 1 and color == BLACK):
                        moves[(r,left)] = last  
                    
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                        moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped = last, piece = piece))
                        moves.update(self._traverse_left(r-step, min(r+3, ROWS), -1*step, color, left-1, skipped = last, piece = piece))
                    else:
                        row = min(r+3, ROWS)      
                        moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped = last, piece = piece))
                        moves.update(self._traverse_left(r-step, max(r-3, -1), -1*step, color, left-1, skipped = last, piece = piece))
                    if not moves:
                        moves[(r,left)] = last 
                break
                
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]
                
            
            left -= 1
            
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped = [], piece = None):
        moves = {}
        last =[]
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == piece:
                current = 0
                
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    last = last + skipped
                elif not last:
                    if (step == -1 and color == WHITE) or (step == 1 and color == BLACK):
                        moves[(r,right)] = last     
                    
                if last:
                    
                    if step == -1:
                        row = max(r-3, -1)
                        moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r-step, min(r+3, ROWS), -1*step, color, right+1, skipped = last, piece = piece))
                    else:
                        row = min(r+3, ROWS)      
                        moves.update(self._traverse_left(r+step, row, step, color,right-1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped = last, piece = piece))
                        moves.update(self._traverse_right(r-step, max(r-3, -1), -1*step, color, right+1, skipped = last, piece = piece))
                        
                    if not moves:
                        moves[(r,right)] = last   
                
                break  
            elif current.color == color:
                break
            else:
                if current in skipped:
                    break
                last = [current]
            
            right += 1
        
        return moves
                                        

    def _traverse_left_queen(self, start, stop, step, color, left, queen, skipped = []):
        moves = {}
        last =[]
        skip = skipped
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]
            
            if current == 0:
                if not last and not skip:
                    moves[(r,left)] = last
                    
                if last:
                    tmp_mvs = {}
                    if step == -1:
                        row = -1
                        tmp_mvs.update(self._traverse_left_queen(r+step, row, step, color, left-1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r+step, row, step, color, left+1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_left_queen(r-step, ROWS, -1*step, color, left-1, queen, skipped = last+skip))
                    else:
                        row = ROWS
                        tmp_mvs.update(self._traverse_left_queen(r+step, row, step, color, left-1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r+step, row, step, color, left+1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_left_queen(r-step, -1, -1*step, color, left-1, queen, skipped = last+skip))
                    
                    if not tmp_mvs:
                        moves[(r,left)] = last + skip
                    else:
                        moves.update(tmp_mvs) 
            elif current.color == color:
                break
            elif not last:
                if current in skip:
                    break
                last = [current]
            else: 
                break
            
            left -= 1
        
        return moves
    
    def _traverse_right_queen(self, start, stop, step, color, right, queen, skipped = []):
        moves = {}
        last =[]
        skip = skipped
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            
            if current == 0:
                if not last and not skip:
                    moves[(r,right)] = last
                               
                if last:
                    tmp_mvs = {}
                    if step == -1:
                        row = -1
                        tmp_mvs.update(self._traverse_left_queen(r+step, row, step, color, right-1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r+step, row, step, color, right+1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r-step, ROWS, -1*step, color, right+1, queen, skipped = last+skip))
                    else:
                        row = ROWS
                        tmp_mvs.update(self._traverse_left_queen(r+step, row, step, color, right-1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r+step, row, step, color, right+1, queen, skipped = last+skip))
                        tmp_mvs.update(self._traverse_right_queen(r-step, -1, -1*step, color, right+1, queen, skipped = last+skip))
                    
                    if not tmp_mvs:
                        moves[(r,right)] = last + skip
                    else:
                        moves.update(tmp_mvs) 
            elif current.color == color:
                break
            elif not last:
                if current in skip:
                    break
                last = [current]
            else: 
                break
            
            right += 1
        
        return moves
    
    def choose_longest_jump(self, moves):
        trimed_moves = {}
        max_jump=0
        for item in moves:
            if len(moves[item]) > max_jump:
                trimed_moves = {}
                trimed_moves[item] = moves[item]
                max_jump = len(moves[item])
            elif len(moves[item]) == max_jump:
                trimed_moves[item] = moves[item]
                
        return trimed_moves
            
            