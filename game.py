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

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)

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
                # After a jump, check for additional jump moves only.
                new_valid_moves = self.board.get_valid_moves(self.selected)
                # Filter to only include moves that are jump moves (i.e., have skipped pieces)
                jump_moves = {move: skips for move, skips in new_valid_moves.items() if skips}
                if jump_moves:
                    # There are additional jump moves available.
                    # Update valid moves so that only jump moves remain.
                    self.valid_moves = jump_moves
                    return True
                else:
                    self.change_turn()
            else:
                self.change_turn()
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

