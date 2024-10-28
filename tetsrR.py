import numpy as np
from collections import deque

def pathplanning(S, G, n, O):
    # Create a grid representing the environment
    grid = np.zeros((16, 16), dtype=int)

    # Mark obstacles on the grid
    for i in range(n):
        for x in range(O[i][0], O[i][2] + 1):
            for y in range(O[i][1], O[i][3] + 1):
                grid[x][y] = 1

    # Initialize the wavefront from the end point
    grid[G[0], G[1]] = 2

    # Directions for moving to adjacent cells (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    queue = deque([(G, 0)])  # (position, distance)

    # BFS propagation
    while queue:
        (x, y), dist = queue.popleft()

        # Increase surrounding cells by 1 as we move outward
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            # Check if the new cell is obstacle
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
                continue
            # Check if the new cell is within bounds
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0:
                grid[nx][ny] = dist + 3  # Increment based on distance from the start
                queue.append(((nx, ny), dist + 1))
    
    print(f"{grid}\n")

    return queue

# Test Script:
start = (0, 0)
goal = (5, 5)
obstacles = [[2,3,3,4],[9,9,12,12]]

yourpath = pathplanning(start, goal, len(obstacles), obstacles)
print("Shortest path:", yourpath)