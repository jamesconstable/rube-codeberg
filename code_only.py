#! /usr/bin/env python3

#from bs4 import BeautifulSoup

def is_wall(x, y, maze):
    return maze[y][x] != ' '

def dfs(x, y, maze):
    fringe = [(0, 0)]
    seen = set()
    while len(fringe) > 0:
        curr = fringe.pop()
        seen.add(curr)
        ns = get_neighbours(curr)
        for n in ns:
            if n in seen:
                continue
            fringe.append(curr)

f = open('rube_codeberg.py', 'r')
maze = f.readlines()
f.close()

for i, line in enumerate(maze):
    maze[i] = line.split('#')[-1]
    maze[i] = list(maze[i])

print(maze)

