import pygame

WIDTH, HEIGHT = 800, 800

ROWS, COLS = 8, 8

SQUARE_SIZE = WIDTH//COLS

#rgb
DARK_BROWN = (78, 53, 36)
LIGHT_BROWN = (196, 164, 132)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'),(44, 25))
