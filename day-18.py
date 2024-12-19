#!/usr/bin/env python3
import os
import sys
import collections
import re
import itertools

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def solve_maze(init_t, walls, end):
    start = (0,0)
    positions = [ set([(0,0)]) ]
    visited = positions[0]
    while True:
        next = set()
        for x,y in positions[-1]:
            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                if (0 <= nx <= end[0]) and (0 <= ny <= end[1]) and (not (nx,ny) in visited) \
                        and (walls.get((nx, ny), sys.maxsize) >= init_t):
                    next.add((nx, ny))
        positions.append(next)
        visited.update(next)
        if (next == set()) or (end in next):
            break
    if end in next:
        return positions
    else:
        return []

def process(filename):
    walls = {}
    for t, line in enumerate(open(filename)):
        line = line.strip()
        walls[tuple(map(int, line.split(',')))] = t
    end = (max(x for x,_ in walls), max(y for _,y in walls))

    # part 1
    print(len(solve_maze(1024, walls, end))-1)

    # part 2
    t_range = (0,len(walls))
    while (t_range[1] - t_range[0]) > 1:
        mid_t = sum(t_range) // 2
        if len(solve_maze(mid_t, walls, end)) > 0:
            t_range = (mid_t, t_range[1])
        else:
            t_range = (t_range[0], mid_t)
    print([(x,y) for x,y in walls if walls[(x,y)] == t_range[0]])

test = f'input/test-{DAY}.txt'
real = f'input/day-{DAY}.txt'

if len(sys.argv) > 1:
    if sys.argv[1] == '-t':
        process(test)
    elif sys.argv[1] == '-r':
        process(real)
    else:
        process(sys.argv[1])
else:
    if os.path.exists(test):
        process(test)
    if os.path.exists(real):
        process(real)
