import pygame

from checkers.board import Board
from checkers.constants import BLUE, SQUARE_SIZE, WHITE, BLACK, CROWN

class Game:
    def __init__(self, win) -> None:
        self._init()
        self.win = win
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw_selection()
        pygame.display.update()
        
    def draw_selection(self):
        if self.selected:
            pygame.draw.circle(self.win, (0,255,0), (self.selected.x, self.selected.y), 50, 5)
        
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn_number = 0
        self.turn = WHITE
        self.valid_moves = {}
        
    def winner(self):
        return(self.board.winner())
    
    def reset(self):
        self._init()
        
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
                
        
        main_piece = self.board.get_piece(row, col)
        
        
        if main_piece != 0 and main_piece.color == self.turn:
            self.selected = main_piece
            
            self.valid_moves = self.board.get_valid_moves(main_piece)
            
            if len(self.valid_moves) > 0:
                max_skip = len(list(self.valid_moves.values())[0])
                print("reduce")  
                for piece in self.board.get_all_pieces(main_piece.color):
                    if self.valid_moves == {}:
                        break
                    if (piece.row, piece.col) != (main_piece.row, main_piece.col):
                        valid_moves = self.board.get_valid_moves(piece)
                        for move, skip in valid_moves.items():
                            if len(skip) > max_skip:
                                self.valid_moves = {}
                                break
            if main_piece.queen:
                if piece.color == BLACK:
                    self.board.black_queen_moves += 1
                else:
                    self.board.white_queen_moves += 1
            return True
        
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece == self.selected:
            piece = 0
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE //2), 15)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
            
    def get_board(self):
        return self.board
      
    def ai_move(self, board):
        self.board = board  
        self.change_turn()
        
    def draw_endgame(self, color):
        pygame.font.init()
        pygame.draw.rect(self.win,WHITE,(2*SQUARE_SIZE, 3*SQUARE_SIZE, SQUARE_SIZE*4, SQUARE_SIZE*2))
        my_font = pygame.font.SysFont('Comic Sans MS', 30)
        if(color == WHITE):
            winner = "White wins"
        elif color == BLACK:
            winner == "Black wins"
        else:
            winner = "Draw"
        text_surface = my_font.render(winner, False, (0, 0, 0))
        self.win.blit(text_surface, (2*SQUARE_SIZE+SQUARE_SIZE, 3*SQUARE_SIZE+SQUARE_SIZE*3/4))
    