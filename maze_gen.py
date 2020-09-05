#! /usr/bin/env python3

from enum import Flag, auto
import random

class Direction(Flag):
    N = auto()
    E = auto()
    S = auto()
    W = auto()

ALL_WALLS = Direction.N | Direction.E | Direction.S | Direction.W
NO_WALLS = Direction.N & Direction.S

def opposite_direction(d):
    if d is Direction.N:
        return Direction.S
    if d is Direction.S:
        return Direction.N
    if d is Direction.E:
        return Direction.W
    return Direction.E

def random_suit():
    return random.choice((' ', ' ', ' ', ' ', '♣️', '♠️', '♥️', '♦️'))

def dfs_maze(grid, x, y):
    grid[y][x] = (True, grid[y][x][1], grid[y][x][2])
    neighbours = [
        (x, y-1, Direction.N),
        (x+1, y, Direction.E),
        (x, y+1, Direction.S),
        (x-1, y, Direction.W)]
    random.shuffle(neighbours)
    for i, j, d in neighbours:
        if 0 <= i < maze_x and 0 <= j < maze_y and not grid[j][i][0]:
            grid[y][x] = (True, grid[y][x][1] & ~d, grid[y][x][2])
            grid[j][i] = (True, grid[j][i][1] & ~opposite_direction(d),
                    grid[j][i][2])
            dfs_maze(grid, i, j)

def maze_box_char(top_left, top_right=NO_WALLS, bottom_left=NO_WALLS):
    if top_left & Direction.E:
        if top_left & Direction.S:
            if bottom_left & Direction.E:
                return '┼' if top_right & Direction.S else '┤'
            return '┴' if top_right & Direction.S else '┘'
        if bottom_left & Direction.E:
            return '├' if top_right & Direction.S else '│'
        return '└' if top_right & Direction.S else '╵'
    else:
        if bottom_left & Direction.E:
            if top_left & Direction.S:
                return '┬' if top_right & Direction.S else '┐'
            return '┌' if top_right & Direction.S else '╷'
        if top_left & Direction.S:
            return '─' if top_right & Direction.S else '╴'
        return '╶' if top_right & Direction.S else ' '

maze_x = 20
maze_y = 20

maze = []
for i in range(maze_y):
    row = []
    for j in range(maze_x):
        row.append((False, ALL_WALLS, ' '))
    maze.append(row)

# Add exit point
maze[maze_y-1][maze_x-1] = (False, ALL_WALLS & ~Direction.E, ' ')

# Generate the maze
dfs_maze(maze, 0, 0)

# Print the first row
print(maze_box_char(NO_WALLS, Direction.S, NO_WALLS), end='')
for x in range(maze_x):
    print(maze_box_char(Direction.S, Direction.S, NO_WALLS), end='')
    print(maze_box_char(Direction.S, NO_WALLS if x+1 == maze_x else Direction.S,
            maze[0][x][1]), end='')
print()

# Print the rest of the maze. Sorry this is utterly unreadable but I'm on a
# tight deadline here.
for y in range(maze_y):
    start_wall = NO_WALLS if y == 0 else Direction.E
    print(maze_box_char(start_wall, NO_WALLS, start_wall), end='')
    for x in range(maze_x):
        print(maze[y][x][2], end='')
        right_wall = maze[y][x][1] & Direction.E
        print(maze_box_char(right_wall, NO_WALLS, right_wall), end='')
    print()
    print(maze_box_char(start_wall, maze[y][0][1],
            NO_WALLS if y+1 == maze_y else Direction.E), end='')
    for x in range(maze_x):
        bottom_wall = maze[y][x][1] & Direction.S
        print(maze_box_char(bottom_wall, bottom_wall), end='')
        print(maze_box_char(maze[y][x][1],
                maze[y][x+1][1] if x+1 < maze_x else NO_WALLS,
                maze[y+1][x][1] if y+1 < maze_y else Direction.N),
                end='')
    print()
