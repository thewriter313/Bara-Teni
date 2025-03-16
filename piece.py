import pygame
from constants import *

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x=0
        self.y=0
        self.calc_pos(row,col)

    def calc_pos(self,row,col):
        self.x = margin+(self.col*space)
        self.y = margin+(self.row*space)

    def move_piece(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos(row,col)

    def draw_piece(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 50)

    def __repr__(self):
        return str(self.color)
