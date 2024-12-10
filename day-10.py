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

def update(input, endings, ratings, height):
    steps = [(1,0), (0,1), (-1,0), (0,-1)]

    sx, sy = len(input), len(input[0])
    for x in range(sx):
        for y in range(sy):
            if input[x][y] == height:
                if height == 9:
                    endings[x][y] = {(x,y)}
                    ratings[x][y] = 1
                else:
                    endings[x][y] = set()
                    ratings[x][y] = 0
                    for dx, dy in steps:
                        nx, ny = x+dx, y+dy
                        if 0 <= nx < sx and 0 <= ny < sy:
                            if input[nx][ny] == height+1:
                                endings[x][y] |= endings[nx][ny]
                                ratings[x][y] += ratings[nx][ny]

def print_map(input):
    for line in input:
        print(" ".join(map(str,line)))

def trailheads(input, height=0):
    return [(y,x) for y,line in enumerate(input) for x,h in enumerate(line) if h == height]

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(line)

    input = [[int(c) for c in line] for line in input]

    endings = [[set()]*len(input[0]) for _ in input]
    ratings = [[-1]*len(input[0]) for _ in input]
    for height in range(9, -1, -1):
        update(input, endings, ratings, height)

    print(sum(len(endings[x][y]) for x,y in trailheads(input)))
    print(sum(ratings[x][y] for x,y in trailheads(input)))

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
