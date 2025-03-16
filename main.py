import pygame
from constants import *
from game import Game

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // (height // 5)
    col = x // (width // 5)
    return row, col

def main():
    running = True

    pygame.init()

    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()

    game = Game(screen)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row,col)
            
            if event.type == pygame.KEYDOWN:
                # Press space to end the turn manually if you’re done with jumping.
                if event.key == pygame.K_SPACE:
                    game.end_turn()


        game.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == '__main__':
    main()