import pygame
from board import Board
from constants import *

class Game:
    def __init__(self, screen):
        self._init()
        self.screen = screen
    
    def update(self):
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = red
        self.valid_moves = {}
        self.jump_made_in_turn = False

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            if (row, col) in self.valid_moves:
                result = self._move(row, col)
                if result:
                    return True
            else:
                # Allow selecting another piece only if no jump has been made yet
                if not self.jump_made_in_turn:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.turn:
                        self.selected = piece
                        self.valid_moves = self.board.get_valid_moves(piece)
                        return True
                return False
        else:
            # No piece selected yet, select the clicked piece
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped_pieces = self.valid_moves[(row, col)]
            if skipped_pieces:
                self.board.remove(skipped_pieces)
                self.jump_made_in_turn = True  # Record that a jump was made
                # After a jump, check for additional jump moves only
                new_valid_moves = self.board.get_valid_moves(self.selected)
                # Filter to only include jump moves (i.e., have skipped pieces)
                jump_moves = {move: skips for move, skips in new_valid_moves.items() if skips}
                if jump_moves:
                    # There are additional jump moves available
                    self.valid_moves = jump_moves  # Only jump moves allowed
                    return True
                else:
                    self.change_turn()  # No more jumps, end turn
            else:
                self.change_turn()  # Non-jump move, end turn
        else:
            return False
        
        return True
    
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, orange, (margin+(col*space), margin+(row*space)), 15)

    
    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        self.turn = green if self.turn == red else red
        self.jump_made_in_turn = False

    def has_valid_moves(self):
        for row in range(rows):
            for col in range(cols):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn:
                    moves = self.board.get_valid_moves(piece)
                    if moves:
                        return True
        return False
    
    def end_turn(self):
        if self.jump_made_in_turn:
            self.change_turn()

    def winner(self):
        if self.board.red_left == 0:
            return "Green"  # Green wins if all red pieces are captured
        elif self.board.green_left == 0:
            return "Red"  # Red wins if all green pieces are captured
        return None

