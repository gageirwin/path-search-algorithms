import pygame
from src.settings import *
from src.tile import *
from src.algorithms.a_star import a_star

class Maze:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.key_pressed = False
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]
        self.start = None
        self.end = None

    def reset(self):
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    a_star(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_r]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.reset()
        else:
            self.key_pressed = False

    def clear_type(self, type):
        for row in self.maze:
            for col in row:
                if col.type == type:
                    col.change_type(TileType.EMPTY)

    def draw(self):
        self.display_surface.fill('white')
        for row in self.maze:
            for col in row:
                action = col.draw(self.display_surface)
                if action == 'm0':
                    if col.type == TileType.WALL:
                        col.change_type(TileType.EMPTY)
                    else:
                        col.change_type(TileType.WALL)
                elif action == 'm1':
                    if col.type == TileType.START:
                        col.change_type(TileType.EMPTY)
                        self.start = None
                    else:
                        self.clear_type(TileType.START)
                        col.change_type(TileType.START)
                        self.start = col.pos
                elif action == 'm2':
                    if col.type == TileType.END:
                        col.change_type(TileType.EMPTY)
                        self.end = None
                    else:
                        self.clear_type(TileType.END)
                        col.change_type(TileType.END)
                        self.end = col.pos
        
    def run(self):
        self.draw()
        self.input()