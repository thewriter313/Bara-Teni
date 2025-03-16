import pygame
from constants import *
from game import Game

def get_row_col_from_mouse(pos):
    """Convert mouse position to board row and column."""
    x, y = pos
    row = y // (height // 5)
    col = x // (width // 5)
    return row, col

def main():
    """Run the main game loop."""
    running = True
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    game = Game(screen)
    font = pygame.font.Font(None, 74)

    while running:
        winner = game.winner()
        if winner:
            # Display the winner message
            text = font.render(f"{color_names[winner]} wins!", True, (255, 255, 255))
            screen.blit(text, (width // 2 - text.get_width() // 2, height-50))
            pygame.display.update()
            pygame.time.wait(3000)
            # running = False
            game = Game(screen)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and game.turn != game.ai_color:
                    # Human player's move
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game.end_turn()
            if game.turn == game.ai_color:
                # AI's move
                game.ai_move(3)
            game.update()
            clock.tick(fps)
    pygame.quit()

if __name__ == '__main__':
    main()