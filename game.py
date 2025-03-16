import pygame
from board import Board
from constants import *

def evaluate(board, ai_color):
    """Evaluate the board state for the AI."""
    winner = board.winner()
    if winner == ai_color:
        return 1000
    elif winner is not None:
        return -1000
    else:
        if ai_color == green:
            return board.green_left - board.red_left
        else:
            return board.red_left - board.green_left

def minimax(board, depth, is_maximizing, ai_color):
    """Implement the minimax algorithm for AI decision-making."""
    if depth == 0 or board.winner() is not None:
        return evaluate(board, ai_color), None
    if is_maximizing:
        max_eval = -float('inf')
        best_move = None
        for move in board.get_all_moves(ai_color):
            new_board = board.copy()
            from_row, from_col = move[0]
            to_row, to_col = move[1]
            piece = new_board.get_piece(from_row, from_col)
            new_board.move(piece, to_row, to_col)
            if move[2]:
                skipped_pieces = [new_board.get_piece(pos[0], pos[1]) for pos in move[2]]
                new_board.remove(skipped_pieces)
            eval, _ = minimax(new_board, depth - 1, False, ai_color)
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        opponent_color = red if ai_color == green else green
        for move in board.get_all_moves(opponent_color):
            new_board = board.copy()
            from_row, from_col = move[0]
            to_row, to_col = move[1]
            piece = new_board.get_piece(from_row, from_col)
            new_board.move(piece, to_row, to_col)
            if move[2]:
                skipped_pieces = [new_board.get_piece(pos[0], pos[1]) for pos in move[2]]
                new_board.remove(skipped_pieces)
            eval, _ = minimax(new_board, depth - 1, True, ai_color)
            if eval < min_eval:
                min_eval = eval
        return min_eval, None

class Game:
    def __init__(self, screen):
        self._init()
        self.screen = screen
        self.ai_color = green
    
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
        """Handle piece selection and move attempts."""
        if self.selected:
            if (row, col) in self.valid_moves:
                result = self._move(row, col)
                if result:
                    return True
            else:
                if not self.jump_made_in_turn:
                    piece = self.board.get_piece(row, col)
                    if piece != 0 and piece.color == self.turn:
                        self.selected = piece
                        self.valid_moves = self.board.get_valid_moves(piece)
                        return True
                return False
        else:
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.color == self.turn:
                self.selected = piece
                self.valid_moves = self.board.get_valid_moves(piece)
                return True
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # Animate the move
            self.animate_move(self.selected, row, col)
            # Now update the board state once the animation is complete
            self.board.move(self.selected, row, col)
            skipped_pieces = self.valid_moves[(row, col)]
            if skipped_pieces:
                self.board.remove(skipped_pieces)
                self.jump_made_in_turn = True
                new_valid_moves = self.board.get_valid_moves(self.selected)
                jump_moves = {move: skips for move, skips in new_valid_moves.items() if skips}
                if jump_moves:
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
        self.jump_made_in_turn = False
        self.turn = green if self.turn == red else red
        

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
        return self.board.winner()

    def ai_move(self, depth):
        _, move = minimax(self.board, depth, True, self.ai_color)
        if move:
            from_row, from_col = move[0]
            to_row, to_col = move[1]
            piece = self.board.board[from_row][from_col]
            self.select(piece.row, piece.col)  # Select the piece
            self._move(to_row, to_col)  # Make the move

    def animate_move(self, piece, final_row, final_col):
        # Calculate starting and final pixel positions
        start_x, start_y = piece.x, piece.y
        final_x = margin + (final_col * space)
        final_y = margin + (final_row * space)
        steps = 20  # Number of frames in the animation
        for i in range(steps):
            t = (i + 1) / steps  # Normalized progress (0 to 1)
            piece.x = start_x + (final_x - start_x) * t
            piece.y = start_y + (final_y - start_y) * t
            # Redraw board and the moving piece
            self.board.draw(self.screen)
            piece.draw_piece(self.screen)
            pygame.display.update()
            pygame.time.delay(25)  # Delay in milliseconds between frames
