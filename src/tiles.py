import pygame
from src.settings import *

class Tile:

    def __init__(self, pos):
        self.rect = pygame.Rect(pos, (TILE_SIZE,TILE_SIZE))
        self.color = 'black'

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)   

class Wall(Tile):

    def __init__(self, pos):
        super().__init__(pos)

class Empty(Tile):

    def __init__(self, pos):
        super().__init__(pos)
        self.width = 1

    def checked(self):
        self.color = 'blue'
        self.width = 0

    def path(self):
        self.color = 'red'
        self.width = 0

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, self.width) 

class Player(Tile):

    def __init__(self, pos):
        super().__init__(pos)
        self.color = 'red'

class Goal(Tile):

    def __init__(self, pos):
        super().__init__(pos)
        self.color = 'green'