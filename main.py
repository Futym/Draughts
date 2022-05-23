
import pygame
import time

from checkers.constants import BLACK, SQUARE_SIZE, WHITE, WIDTH, HEIGHT
from checkers.game import Game
from minimax.algorithm import minimax

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    whitetime=0
    blacktime=0
    run = True
    clock = pygame.time.Clock()
    
    game = Game(WIN)
    
    while run:
        clock.tick(FPS)
        # for event in pygame.event.get():
                
            # if  event.type == pygame.MOUSEBUTTONDOWN:
                            
        if game.turn == WHITE and game.board.white_left!=0:
            begin_time = round(time.time() * 1000)
            _, new_board = minimax(game.get_board(), 3, True, game, alpha = float('-inf'), beta = float('inf'))
            end_time = round(time.time() * 1000)
            whitetime+=end_time-begin_time
            game.ai_move(new_board)
            
        elif game.turn == BLACK and game.board.white_left!=0:
            begin_time = round(time.time() * 1000)
            _, new_board = minimax(game.get_board(), 3, False, game, alpha = float('-inf'), beta = float('inf'))
            end_time = round(time.time() * 1000)
            blacktime+=end_time-begin_time
            game.ai_move(new_board)
            game.turn_number += 1

        if game.winner() != None or game.board.black_queen_moves == 15 or game.board.white_queen_moves == 15:
            color = game.winner()
            if color == WHITE:
                print("White win")
                game.draw_endgame(WHITE)
                pygame.display.update()
            elif color == BLACK:
                print("Black win")
                game.draw_endgame(BLACK)
                pygame.display.update()
            else:
                print("Draw")
                game.draw_endgame(None)
                pygame.display.update()
            while run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                            
                    
                
            # if event.type == pygame.QUIT:
            #     run = False
                
                
        # for event in pygame.event.get():
                
        #     if  event.type == pygame.MOUSEBUTTONDOWN:
        #         pos = pygame.mouse.get_pos()
        #         row, col = get_row_col_from_mouse(pos)
        #         game.select(row, col)
        
        # game.update()
        # pygame.display.update()
        
    pygame.quit()
    print(whitetime, blacktime, game.turn_number)
    
main()
            
    