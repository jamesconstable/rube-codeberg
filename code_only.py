#! /usr/bin/env python3

import random
from bs4 import BeautifulSoup

message = []

def is_wall(x, y, maze):
    return maze[y][x] != ' '

def is_end(cell, maze):
    x, y = cell
    max_x = len(maze[0])
    max_y = len(maze)
    return ((x+2 == max_x) and
            (y+2 == max_y))

def dfs(maze, visit_fn):
    max_x = len(maze[0])
    max_y = len(maze)
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
    x, y = cell
    if maze[y][x] not in ' █':
        message.append(maze[y][x])

def neighbours(cell, maze):
    x, y = cell
    if maze[y-1][x] == ' ':
        yield (x, y-2)
    if maze[y][x+1] == ' ':
        yield (x+2, y)
    if maze[y+1][x] == ' ':
        yield (x, y+2)
    if maze[y][x-1] == ' ':
        yield (x-2, y)

f = open('rube_codeberg.py', 'r')
maze = f.readlines()
f.close()

for i, line in enumerate(maze):
    maze[i] = line.split('#')[-1]
    maze[i] = list(maze[i])

dfs(maze, write_cell)
message = (''.join(message)
        .replace('.', ' ')
        .replace('"', '')
        .replace('^', '')
        .rstrip())

soup = BeautifulSoup(message,
    'html.parser')

print(soup.title.string)
