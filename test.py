
from checkers.constants import WHITE
from checkers.piece import Piece


piece = Piece(1, 1, WHITE)
piece2 = Piece(1, 1, WHITE)
print ((piece.col, piece.row) == (piece2.col, piece2.row))