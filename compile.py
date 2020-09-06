#! /usr/bin/env python3

CODE_WIDTH = 35

with open('code_only.py', 'r') as source_file:
    raw_source = source_file.readlines()

with open('maze.txt', 'r') as maze_file:
    maze = maze_file.readlines()

raw_source += [''] * (len(maze) - len(raw_source))
for s, m in zip(raw_source, maze):
    print(s.rstrip().ljust(CODE_WIDTH) + ' #' + m, end='')
