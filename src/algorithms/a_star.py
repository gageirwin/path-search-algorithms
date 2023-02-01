import pygame
import heapq
from src.tile import *

def draw_path(path, maze, start, end, draw):
    for tile in path:
        if not tile in {start, end}:
            maze[tile[1]][tile[0]].change_type(TileType.PATH)
            draw()
            pygame.time.wait(10)
            pygame.event.pump()
            pygame.display.update()

def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

def a_star(array, start, goal, draw):
    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))
    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.reverse()
            draw_path(data, array, start, goal, draw)
            return True
        if current in close_set:
            continue
        close_set.add(current)
        for i, j in [(0,1),(0,-1),(1,0),(-1,0)]:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[1] < len(array) and 0 <= neighbor[0] < len(array[0]) and array[neighbor[1]][neighbor[0]].type != TileType.WALL:
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    if array[neighbor[1]][neighbor[0]].type == TileType.EMPTY:
                        array[neighbor[1]][neighbor[0]].change_type(TileType.SEARCHED)
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        draw()
        pygame.event.pump()
        pygame.display.update() 

    return False