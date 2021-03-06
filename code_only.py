#! /usr/bin/env python3

import random
from bs4 import BeautifulSoup

# Hi judges!
#
# If you're just looking to skim
# read, the basic idea here is
# that the comments in this file
# encode a maze that contains an
# HTML document with the
# competition output in the title.
# The program loads its own source
# code, solves the maze using a
# DFS and stores any non-maze
# characters it encounters in a
# buffer. The buffer is then
# parsed with Beautiful Soup, and
# the title extracted and printed.
#
# Thanks for a great PyConline!

message = []

def is_wall(x, y, maze):
    return maze[y][x] != ' '

def is_end(cell, maze):
    # Checks if cell is bottom-
    # right-most cell (i.e. the
    # end!)
    x, y = cell
    max_x = len(maze[0])
    max_y = len(maze)
    return ((x+2 == max_x) and
            (y+2 == max_y))

def dfs(maze, visit_fn):
    # Run a DFS over the maze,
    # starting in the top-left
    # cell.
    fringe = [(1, 1)]
    seen = set()
    while len(fringe) > 0:
        c = fringe.pop()
        x, y = c
        if c in seen:
            continue
        seen.add(c)
        visit_fn(c, maze)
        if is_end(c, maze):
            return
        ns = neighbours(c, maze)
        for n in ns:
            fringe.append(n)

def write_cell(cell, maze):
    # Add the cell to the buffer
    # if it's not blank.
    x, y = cell
    if maze[y][x] not in ' █':
        message.append(maze[y][x])

def neighbours(cell, maze):
    # Neighbours are expanded in a
    # clockwise fashion. We don't
    # need to worry about range-
    # checking the indices as the
    # maze already contains a one
    # character safety border on
    # all sides.
    x, y = cell
    if maze[y-1][x] == ' ':
        yield (x, y-2)
    if maze[y][x+1] == ' ':
        yield (x+2, y)
    if maze[y+1][x] == ' ':
        yield (x, y+2)
    if maze[y][x-1] == ' ':
        yield (x-2, y)

# Read in program source code
f = open('rube_codeberg.py', 'r')
maze = f.readlines()
f.close()

# Extract maze
for i, line in enumerate(maze):
    maze[i] = line.split('#')[-1]
    maze[i] = list(maze[i])

# Solve maze
dfs(maze, write_cell)

# Filter out decorative characters
# and parse resulting HTML.
message = (''.join(message)
        .replace('.', ' ')
        .replace('"', '')
        .replace('^', '')
        .rstrip())

soup = BeautifulSoup(message,
    'html.parser')

print(soup.title.string)
