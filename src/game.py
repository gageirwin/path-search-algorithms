import pygame
from src.settings import *
from src.tiles import Wall, Empty, Player, Goal
import heapq

class Maze:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.create_maze()
        self.key_pressed = False

    def reset(self):
        self.create_maze()

    def create_maze(self):
        self.maze = []
        for row_index, row in enumerate(MAZE):
            maze_row = []
            for col_index, col in enumerate(row):
                pos = (col_index*TILE_SIZE, row_index*TILE_SIZE)
                if col == 'W':
                    maze_row.append(Wall(pos))
                elif col == 'P':
                    self.player_pos = (col_index, row_index)
                    maze_row.append(Player(pos))
                elif col == 'G':
                    self.goal_pos = (col_index, row_index)
                    maze_row.append(Goal(pos))
                else:
                    maze_row.append(Empty(pos))
            self.maze.append(maze_row)

    def search(self):
        path = self.a_star(self.maze, self.player_pos, self.goal_pos)
        for tile in path:
            if not tile in {self.player_pos,self.goal_pos}:
                self.maze[tile[1]][tile[0]].path()
                self.draw()
                pygame.time.wait(10)
                pygame.event.pump()
                pygame.display.update()

    def a_star(self,  grid, start, end):
        cols, rows = len(grid), len(grid[0])
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
                if 0 <= nx < rows and 0 <= ny < cols and not isinstance(grid[ny][nx], Wall):
                    if (nx, ny) not in visited:
                        if isinstance(grid[ny][nx], Empty):
                            grid[ny][nx].checked()
                        heapq.heappush(heap, (cost + 1, (nx, ny)))
                        parents[(nx, ny)] = curr
                        self.draw()
                        pygame.time.wait(100)
                        pygame.event.pump()
                        pygame.display.update() 
        return None

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.reset()
                self.search()
        elif keys[pygame.K_r]:
            if self.key_pressed == False:
                self.key_pressed = True
                self.reset()
        else:
            self.key_pressed = False

    def draw(self):
        self.display_surface.fill('white')
        for row in self.maze:
            for col in row:
                col.draw(self.display_surface)
        
    def run(self):
        self.draw()
        self.input()
