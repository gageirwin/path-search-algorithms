import pygame
from src.settings import *
from enum import Enum, auto

class TileType(Enum):

    EMPTY = auto()
    WALL = auto()
    START = auto()
    END = auto()
    SEARCHED = auto()
    PATH = auto()

class Tile:
    def __init__(self, pos, type:TileType):
        self.pos = pos
        self.rect = pygame.Rect((pos[0]*TILE_SIZE, pos[1]*TILE_SIZE), (TILE_SIZE, TILE_SIZE))
        self.type = None
        self.color = 'white'
        self.change_type(type)    
        self.mouse_0_click = False
        self.mouse_1_click = False
        self.mouse_2_click = False

    def change_type(self, type:TileType):
        self.type = type
        if type == TileType.EMPTY:
            self.color = 'white'
        elif type == TileType.WALL:
            self.color = 'black'
        elif type == TileType.START:
            self.color = 'red'
        elif type == TileType.END:
            self.color = 'green'
        elif type == TileType.SEARCHED:
            self.color = 'blue'
        elif type == TileType.PATH:
            self.color = 'red'  

    def draw(self, surface):
        action = None
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):

            if pygame.mouse.get_pressed()[0] and self.mouse_0_click == False:
                self.mouse_0_click = True
                action = 'm0'
            elif not pygame.mouse.get_pressed()[0]:
                self.mouse_0_click = False

            if pygame.mouse.get_pressed()[1] and self.mouse_1_click == False:
                self.mouse_1_click = True
                action = 'm1'
            elif not pygame.mouse.get_pressed()[1]:
                self.mouse_1_click = False

            if pygame.mouse.get_pressed()[2] and self.mouse_2_click == False:
                self.mouse_2_click = True
                action = 'm2'
            elif not pygame.mouse.get_pressed()[2]:
                self.mouse_2_click = False

        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, 'black', self.rect, 1)

        return action