import pygame
from src.settings import *
from src.tile import *
from src.algorithms import a_star, Dijkstra, breadth_first_search, depth_first_search, greedy_best_first_search

class Maze:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.key_pressed = False
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]
        self.start = None
        self.end = None

    def reset(self):
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]
        self.start = None
        self.end = None

    def clear_search(self):
        for row in self.maze:
            for tile in row:
                if tile.type in {TileType.SEARCHED,TileType.PATH}:
                    tile.change_type(TileType.EMPTY)        

    def remove_start(self):
        for row in self.maze:
            for tile in row:
                if tile.type == TileType.START:
                    tile.change_type(TileType.EMPTY)
                    self.start = None

    def remove_end(self):
        for row in self.maze:
            for tile in row:
                if tile.type == TileType.END:
                    tile.change_type(TileType.EMPTY)
                    self.end = None             

    def draw(self):
        self.display_surface.fill('white')
        for row in self.maze:
            for tile in row:
                action = tile.draw(self.display_surface)
                if action:
                    self.clear_search()
                if action == 'm0':
                    tile.flip_type(TileType.WALL)
                elif action == 'm1':
                    self.remove_start()
                    tile.change_type(TileType.START)
                    self.start = tile.pos
                elif action == 'm2':
                    self.remove_end()
                    tile.change_type(TileType.END)
                    self.end = tile.pos

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    self.clear_search()
                    a_star(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_2]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    self.clear_search()
                    Dijkstra(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_3]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    self.clear_search()
                    breadth_first_search(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_4]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    self.clear_search()
                    depth_first_search(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_5]:
            if self.key_pressed == False:
                self.key_pressed = True
                if self.start and self.end:
                    self.clear_search()
                    greedy_best_first_search(self.maze, self.start, self.end, self.draw)
        elif keys[pygame.K_c]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.clear_search()
        elif keys[pygame.K_r]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.reset()
        else:
            self.key_pressed = False

    def run(self):
        self.draw()
        self.input()