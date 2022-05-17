from copy import deepcopy
import pygame

from checkers.constants import BLACK, WHITE

def minimax(position, depth, max_player, game, color = BLACK):
    if position.winner() == WHITE:
        return float('inf'), position
    elif position.winner() == BLACK:
        return float('-inf'), position
    
    if depth == 0 or position.winner():
        return position.evaluate(), position
    
    if max_player:
        max_eval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            max_eval = max(max_eval, evaluation)
            if max_eval == evaluation:
                best_move = move
            
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            min_eval = min(min_eval, evaluation)
            if min_eval == evaluation:
                best_move = move
        
        return min_eval, best_move

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1]) 
    if skip:
        board.remove(skip)    
        
    return board
    
def get_all_moves(board, color, game):
    moves = []
    max_skip=0
    possible_best_moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)
            if len(skip) > max_skip:
                max_skip = len(skip)
                possible_best_moves = []
            if len(skip) == max_skip:
                possible_best_moves.append((piece, move, skip))
    
    for piece, move, skip in possible_best_moves:        
        if len(skip) == max_skip:
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
                
    return moves

def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(1000)