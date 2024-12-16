#!/usr/bin/env python3
import os
import sys
import collections
import re
import itertools
import heapq

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

DIRS = '>v<^'

def cw_right(px, py, dir):
    return (px, py, DIRS[(DIRS.index(dir)+1)%4])

def cw_left(px, py, dir):
    return (px, py, DIRS[(DIRS.index(dir)-1)%4])

def flip(px, py, dir):
    return (px, py, DIRS[(DIRS.index(dir)+2)%4])

def move(px, py, dir):
   if dir == '>':
       return (px+1, py, dir)
   elif dir == 'v':
       return (px, py+1, dir)
   elif dir == '<':
       return (px-1, py, dir)
   else: # dir == '^':
       return (px, py-1, dir)

def move_back(px, py, dir):
   if dir == '>':
       return (px-1, py, dir)
   elif dir == 'v':
       return (px, py-1, dir)
   elif dir == '<':
       return (px+1, py, dir)
   else: # dir == '^':
       return (px, py+1, dir)

def print_maze(maze, marks):
    for r, line in enumerate(maze):
        for c, char in enumerate(line):
            print(marks.get((c,r), char), end='')
        print()

def solve_maze_detailed(maze, start, end):
    cost = {}
    start = (*start, '>')
    min_cost = { start: 0 }
    process = [(0,start)] # maintained using heapq
    end_cost = sys.maxsize
    while True:
        here_cost, here = heapq.heappop(process)
        if here_cost > min_cost[here]:
            continue
        if here_cost > end_cost:
            break
        options = { move(*here): 1, cw_right(*here): 1000, cw_left(*here): 1000, flip(*here): 2000 }
        for next, cost in options.items():
            nx, ny, _ = next
            cost += here_cost
            if (maze[ny][nx] != '#') and (cost <= min_cost.get(next, sys.maxsize)):
                min_cost[next] = cost
                heapq.heappush(process, (cost, next))
        end_cost = min(min_cost.get((*end, dir), sys.maxsize) for dir in DIRS)
    return min_cost, end_cost

def solve_maze(maze, start, end):
    _, end_cost = solve_maze_detailed(maze, start, end)
    return end_cost

def backtrack(maze, start, end, min_cost):
    to_visit = set([(*end,dir) for dir in DIRS if (*end, dir) in min_cost])
    visited = set([(*end,dir)])
    while to_visit:
        here = to_visit.pop()
        options = { move_back(*here): 1, cw_left(*here): 1000, cw_right(*here): 1000, flip(*here): 2000 }
        for next, cost in options.items():
            if min_cost.get(next, sys.maxsize) == min_cost[here]-cost:
                to_visit.add(next)
                visited.add(next)
    spaces = set((x,y) for x,y,d in visited)

    marks = {}
    for c,r,d in visited:
        if (c,r) in marks:
            marks[(c,r)] = 'x'
        else:
            marks[(c,r)] = d
    marks[start] = 'S'
    marks[end] = 'E'
    print_maze(maze, marks)

    return len(spaces)

def solve_maze2(maze, start, end):
    min_cost, _ = solve_maze_detailed(maze, start, end)
    return backtrack(maze, start, end, min_cost)

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(line)

    for r, line in enumerate(input):
        for c, char in enumerate(line):
            if char == 'S':
                start = (c,r)
            elif char == 'E':
                end = (c,r)

    print_maze(input, { start: 'S', end: 'E' })

    print(solve_maze(input, start, end))
    print(solve_maze2(input, start, end))

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
