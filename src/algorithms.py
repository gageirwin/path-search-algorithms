import pygame
import heapq
from src.tile import *
from queue import PriorityQueue

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

def a_star(maze, start, goal, draw):
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
            draw_path(data, maze, start, goal, draw)
            return True
        if current in close_set:
            continue
        close_set.add(current)
        for i, j in [(0,1),(0,-1),(1,0),(-1,0)]: # (1,1),(-1,-1),(1,-1),(-1,1) can hop through wall corners
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[1] < len(maze) and 0 <= neighbor[0] < len(maze[0]) and maze[neighbor[1]][neighbor[0]].type != TileType.WALL:
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue
                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    if maze[neighbor[1]][neighbor[0]].type == TileType.EMPTY:
                        maze[neighbor[1]][neighbor[0]].change_type(TileType.SEARCHED)
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
        draw()
        pygame.event.pump()
        pygame.display.update() 

    return False

def Dijkstra(maze, start, end, draw):
    rows, cols = len(maze), len(maze[0])
    dist = [[float('inf') for _ in range(cols)] for _ in range(rows)]
    prev = [[None for _ in range(cols)] for _ in range(rows)]
    queue = PriorityQueue()
    dist[start[1]][start[0]] = 0
    queue.put((0, start))

    while not queue.empty():
        curr_dist, curr_pos = queue.get()
        if curr_dist == float('inf'):
            break

        col, row  = curr_pos
        for i, j in [(0,1),(0,-1),(1,0),(-1,0)]:
            nrow, ncol = row+i, col+j
            if 0 <= nrow < rows and 0 <= ncol < cols and maze[nrow][ncol].type != TileType.WALL:
                alt = dist[row][col] + 1
                if alt < dist[nrow][ncol]:
                    dist[nrow][ncol] = alt
                    prev[nrow][ncol] = curr_pos
                    if maze[nrow][ncol].type == TileType.EMPTY:
                        maze[nrow][ncol].change_type(TileType.SEARCHED)
                    if (ncol, nrow) == end:
                        curr_pos = end
                        path = [end]
                        while curr_pos != start:
                            curr_pos = prev[curr_pos[1]][curr_pos[0]]
                            path.append(curr_pos)
                        path.reverse()
                        draw_path(path, maze, start, end, draw)
                        return True
                    queue.put((alt, (ncol, nrow)))
        draw()
        pygame.event.pump()
        pygame.display.update() 

    return False

def breadth_first_search():
    pass

def depth_first_search():
    pass

def greedy_Best_first_search():
    pass