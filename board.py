import pygame
from constants import *
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.green_left = 12
        self.create_board()
        
    def draw_board(self, screen):
        screen.fill("black")

        for x in range(cols):
            for y in range(rows):
                pygame.draw.circle(screen,white, (margin+(x*space),margin+(y*space)),10)
                if x < cols-1:
                    pygame.draw.line(screen, white, (margin+(x*space), margin+(y*space)),(margin+((x+1)*space), margin+(y*space)))
                if y < rows-1:
                    pygame.draw.line(screen,white, (margin+(x*space), margin+(y*space)),(margin+((x)*space), margin+((y+1)*space)))
                if not (x+y)%2:
                    if x<cols-1 and y<rows-1:
                        pygame.draw.line(screen,white, (margin+(x*space), margin+(y*space)),(margin+((x+1)*space), margin+((y+1)*space)))
                    if x > 0 and y<rows-1:
                        pygame.draw.line(screen,white, (margin+(x*space), margin+(y*space)), (margin+((x-1)*space),margin+((y+1)*space)))

    def create_board(self):
        for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if row < 2:
                    self.board[row].append(Piece(row,col, green))
                elif row > 2:
                    self.board[row].append(Piece(row,col, red))
                elif row == 2 and col < 2:
                    self.board[row].append(Piece(row,col, green))
                elif row == 2 and col > 2:
                    self.board[row].append(Piece(row,col, red))
                else:
                    self.board[row].append(0)

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        print(self.board)
        piece.move_piece(row, col)

    def get_piece(self, row, col):
        return self.board[row][col]

    def draw(self, screen):
        self.draw_board(screen)
        for row in range(rows):
            for col in range(cols):
                piece = self.board[row][col]
                if piece !=0:
                    piece.draw_piece(screen)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece.color == red:
                self.red_left -= 1
            elif piece.color == green:
                self.green_left -= 1

    def get_valid_moves(self, piece):
        moves = {}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if (piece.row + piece.col) % 2 == 0:
            directions += [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for direction in directions:
            row, col = piece.row + direction[0], piece.col + direction[1]
            if 0 <= row < rows and 0 <= col < cols:
                if self.board[row][col] == 0:
                    moves[(row, col)] = []
                elif self.board[row][col].color != piece.color:
                    jump_row, jump_col = row + direction[0], col + direction[1]
                    if 0 <= jump_row < rows and 0 <= jump_col < cols and self.board[jump_row][jump_col] == 0:
                        # moves[(jump_row, jump_col)] = [(row, col)]
                        moves[(jump_row, jump_col)] = [self.board[row][col]]  # Store the actual Piece object
                        self._check_additional_jumps(piece, jump_row, jump_col, direction, moves, [self.board[row][col]])
        return moves


    def _check_additional_jumps(self, piece, row, col, direction, moves, captured):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if (row + col) % 2 == 0:
            directions += [(-1, -1), (1, 1), (-1, 1), (1, -1)]
        
        for new_direction in directions:
            new_row, new_col = row + new_direction[0], col + new_direction[1]
            if 0 <= new_row < rows and 0 <= new_col < cols:
                if self.board[new_row][new_col] != 0 and self.board[new_row][new_col].color != piece.color:
                    jump_row, jump_col = new_row + new_direction[0], new_col + new_direction[1]
                    if 0 <= jump_row < rows and 0 <= jump_col < cols and self.board[jump_row][jump_col] == 0:
                        if (jump_row, jump_col) not in moves:
                            moves[(jump_row, jump_col)] = captured + [self.board[new_row][new_col]]
                            self._check_additional_jumps(piece, jump_row, jump_col, new_direction, moves, captured + [(new_row, new_col)])