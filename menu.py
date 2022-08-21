

import pygame_menu
from pygame_menu.examples import create_example_window
import pygame

from board import *
from constants import *
from game import Game
from typing import Tuple, Any

surface = create_example_window('Checkers', (600, 400))
file=open('geek.txt','w')
file.write('AI')
file.close()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.
    :return: None
    """
    file=open('geek.txt','w')
    file.write(selected[0][0])
    print(selected[0][0])
    file.close()
def start_the_game() -> None:
    WIN = pygame.display.set_mode((ScrWIDTH, ScrHEIGHT))
    pygame.display.set_caption('Checkers by Aadhavan, Ridham, Samarth')
    clock = pygame.time.Clock()
    game = Game(WIN)
    # Main game loop
    run=True
    while run:
        clock.tick(FPS)
        if (game.board.gameWon != NOTDONE) and (game.board.winner() != NOTDONE): #???
            print(game.board.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col) # from move of user- white

        game.update()

    pygame.quit()

menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)

menu.add.selector('Difficulty: ', [('AI', 1), ('RANDOM', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    pygame.init()

    menu.mainloop(surface)