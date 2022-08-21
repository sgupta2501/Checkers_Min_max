import pygame

MAX_SEARCH_DEPTH = 6 #taken for fast running
FPS = 60

BLACK = 1
WHITE = 0
NOTDONE = -1

# Setup variables
width = 8
height = 8
firstPlayer = WHITE #0, human

ScrWIDTH, ScrHEIGHT = 800, 800
SQUARE_SIZE = ScrWIDTH//width


# rgb
RED_color = (255, 0, 0)
WHITE_color = (255, 255, 255)
BLACK_color = (0, 0, 0)
BLUE_color = (0, 0, 255)
GREY_color = (170,170,170)
GREEN_color = (0,255,0)
YELLOW_color = (250, 250, 50)

CROWN = pygame.transform.scale(pygame.image.load('d:/SNU/assignment2/Python-Checkers-master/checkers/assets/crown.png'), (44, 25))