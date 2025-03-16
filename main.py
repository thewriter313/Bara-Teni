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
    font = pygame.font.Font(None, 74)  # Initialize font for winner message

    while running:

        winner = game.winner()
        if winner:
            text = font.render(f"{winner} wins!", True, (255,255,255))  # White text
            # Center the text on the screen
            screen.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(3000) 
            running = False  

        if not game.has_valid_moves():
            game.change_turn()

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