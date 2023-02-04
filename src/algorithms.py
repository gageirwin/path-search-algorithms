import pygame
import heapq
from src.tile import *
from queue import PriorityQueue
from collections import deque

def draw_path(path, maze, start, end, draw):
    for tile in path:
        if not tile in {start, end}:
            maze[tile[1]][tile[0]].change_type(TileType.PATH)
            draw()
            pygame.time.wait(10)
            pygame.event.pump()
            pygame.display.update()

# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
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
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))
                    if maze[neighbor[1]][neighbor[0]].type == TileType.EMPTY:
                        maze[neighbor[1]][neighbor[0]].change_type(TileType.SEARCHED)
        draw()
        pygame.event.pump()
        pygame.display.update() 

    return False

# Manhattan distance
def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Pseudocode
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
                    if maze[nrow][ncol].type == TileType.EMPTY:
                        maze[nrow][ncol].change_type(TileType.SEARCHED)
        draw()
        pygame.event.pump()
        pygame.display.update() 

    return False

# https://en.wikipedia.org/wiki/Breadth-first_search#Pseudocode
def breadth_first_search(maze, start, end, draw):
    Q = deque([(start, None)])
    explored = set([start])
    while Q:
        v, parent = Q.popleft()
        if v == end:
            path = []
            while parent:
                path.append(v)
                v, parent = parent
            path.append(v)
            path.reverse()
            draw_path(path, maze, start, end, draw)
            return True
        x, y = v
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2, y2 = x + dx, y + dy
            if 0 <= y2 < len(maze) and 0 <= x2 < len(maze[0]) and (x2, y2) not in explored and maze[y2][x2].type != TileType.WALL:
                w = (x2, y2)
                explored.add(w)
                Q.append((w, (v, parent)))
                if maze[y2][x2].type == TileType.EMPTY:
                    maze[y2][x2].change_type(TileType.SEARCHED)
        draw()
        pygame.event.pump()
        pygame.display.update()
        
    return False

# https://en.wikipedia.org/wiki/Depth-first_search#Pseudocode
# non-recursive implementation of DFS
def depth_first_search(maze, start, end, draw):
    S = [(start, None)]
    discovered = set([start])
    while S:
        v, parent = S.pop()
        if v == end:
            path = []
            while parent:
                path.append(v)
                v, parent = parent
            path.append(v)
            path.reverse()
            draw_path(path, maze, start, end, draw)
            return True
        x, y = v
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2, y2 = x + dx, y + dy
            if 0 <= y2 < len(maze) and 0 <= x2 < len(maze[0]) and (x2, y2) not in discovered and maze[y2][x2].type != TileType.WALL:
                w = (x2, y2)
                discovered.add(w)
                S.append((w, (v, parent)))
                if maze[y2][x2].type == TileType.EMPTY:
                    maze[y2][x2].change_type(TileType.SEARCHED)
        draw()
        pygame.event.pump()
        pygame.display.update()
    return False

# https://en.wikipedia.org/wiki/Best-first_search#Greedy_BFS
def greedy_best_first_search(maze, start, end, draw):
    visited = set([start])
    queue = PriorityQueue()
    queue.put((0, start))
    parent = {start: None}
    while not queue.empty():
        (dist, current_node) = queue.get()
        if current_node == end:
            path = []
            while current_node is not None:
                path.append(current_node)
                current_node = parent[current_node]
            path.reverse()
            draw_path(path, maze, start, end, draw)
            return True
        x, y = current_node
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            x2, y2 = x + dx, y + dy
            if 0 <= y2 < len(maze) and 0 <= x2 < len(maze[0]) and (x2, y2) not in visited and maze[y2][x2].type != TileType.WALL:
                n = (x2, y2)
                visited.add(n)
                parent[n] = current_node
                queue.put((dist + abs(x2 - end[0]) + abs(y2 - end[1]), n))
                if maze[y2][x2].type == TileType.EMPTY:
                    maze[y2][x2].change_type(TileType.SEARCHED)
        draw()
        pygame.event.pump()
        pygame.display.update()
    return False
