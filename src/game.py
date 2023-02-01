import pygame
from src.settings import *
import heapq
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

class Maze:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.key_pressed = False
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]
        self.start = None
        self.end = None

    def reset(self):
        self.maze = [[ Tile((col, row), TileType.EMPTY) for col in range(MAZE_WIDTH) ] for row in range(MAZE_HEIGHT)]

    def search(self):
        path = self.a_star(self.maze, self.start, self.end)
        for tile in path:
            if not tile in {self.start, self.end}:
                self.maze[tile[1]][tile[0]].change_type(TileType.PATH)
                self.draw()
                pygame.time.wait(10)
                pygame.event.pump()
                pygame.display.update()

    def a_star(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])
        heap = [(0, start)]
        visited = set()
        parents = {}
        while heap:
            (cost, curr) = heapq.heappop(heap)
            if curr == end:
                path = [end]
                while path[-1] != start:
                    path.append(parents[path[-1]])
                path.reverse()
                return path
            if curr in visited:
                continue
            visited.add(curr)
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                x, y = curr
                nx, ny = x + dx, y + dy
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx].type != TileType.WALL:
                    if (nx, ny) not in visited:
                        if grid[ny][nx].type == TileType.EMPTY:
                            grid[ny][nx].change_type(TileType.SEARCHED)
                        heapq.heappush(heap, (cost + 1, (nx, ny)))
                        parents[(nx, ny)] = curr
            self.draw()
            pygame.event.pump()
            pygame.display.update() 
        return None

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.search()
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
