import pygame
from checkers.constants import SQUARE_SIZE, WHITE, CROWN


class Piece:
    PADDING = 10
    OUTLINE = 2
    
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.queen = False
            
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def make_queen(self):
        self.queen = True
        
    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.color == WHITE:
            pygame.draw.circle(win, (0,0,0), (self.x, self.y), 25, 1)
        else:
            pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 25, 1)
        if self.queen:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2,self.y - SQUARE_SIZE // 2))
    
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()
        
    def __repr__(self):
        return str(self.color)