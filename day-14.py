#!/usr/bin/env python3
import os
import sys
import collections
import re
import itertools
import math

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def robot_position(gx,gy, px,py, vx,vy, steps):
    x, y = ((px+steps*vx) % gx, (py+steps*vy)%gy)
    return (x,y)

def quadrant(gx,gy, x,y):
    mx, my = (gx-1)//2, (gy-1)//2
    if x == mx or y == my:
        return 0
    return 1 + (x > mx) + (y > my)*2

def map_char(count):
    if count == 0:
        return '.'
    elif count > 9:
        return 'X'
    return str(count)

def print_map(grid, all_p):
    p_count = collections.Counter(all_p)
    for y in range(grid[1]):
        print("".join([map_char(p_count[(x,y)]) for x in range(grid[0])]))

def has_more_robots(pv, threshold):
    x_count = collections.Counter(p[0] for p,_ in pv)
    y_count = collections.Counter(p[1] for p,_ in pv)
    return max(x_count.values()) > threshold and max(y_count.values()) > threshold

def process(filename):
    input = []
    if 'test' in filename:
        grid = (11,7)
    else:
        grid = (101,103)
    for line in open(filename):
        line = line.strip()
        data = list(map(int, line.replace('p=','').replace('v=','').replace(',',' ').split()))
        p,v = tuple(data[:2]), tuple(data[2:])
        input.append((p,v))

    qsum = [0]*5
    for p,v in input:
        qsum[quadrant(*grid, *robot_position(*grid, *p, *v, 100))] += 1
    print(math.prod(qsum[1:]))

    for i in range(grid[0]*grid[1]+1):
        if has_more_robots(input, 20):
            print("="*10, i, "="*10)
            print_map(grid, [p for p,_ in input])
        input = [(robot_position(*grid, *p, *v, 1),v) for p,v in input]

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
