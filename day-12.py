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

def print_map(map):
    for line in map:
        print(line)

DIR = ((0,1), (-1,0), (0,-1), (1,0))

def find_regions(map):
    def floodfill(map, plant, x, y, region):
        if not (x,y) in region and 0 <= x < len(map[0]) and 0 <= y < len(map) and map[y][x] == plant:
            region.add((x,y))
            for dx, dy in DIR:
                floodfill(map, plant, x+dx, y+dy, region)

    regions = {}
    processed = {}
    for y,line in enumerate(map):
        for x,plant in enumerate(line):
            if not (x,y) in processed:
                region = set()
                floodfill(map, plant, x, y, region)
                regions[min(region)] = region
                processed |= region
    return regions

def fence_grid(x, y, dx, dy):
    if   (dx,dy) == (-1,0):
        return (x, y+1, x, y)
    elif (dx,dy) == ( 0,-1):
        return (x, y, x+1, y)
    elif (dx,dy) == ( 1, 0):
        return (x+1, y, x+1, y+1)
    elif (dx,dy) == ( 0, 1):
        return (x+1, y+1, x, y+1)

def flip(fence):
    return (*fence[2:], *fence[:2])

def fences(region):
    return set(fence_grid(x,y,dx,dy) for x,y in region for dx,dy in DIR if not (x+dx, y+dy) in region)

def cw_right(fence):
    x0, y0, x1, y1 = fence
    dxdy = (x1-x0, y1-y0)
    cw_dxdy = DIR[(DIR.index(dxdy)+1)%4]
    return (x1, y1, x1+cw_dxdy[0], y1+cw_dxdy[1])

def cw_left(fence):
    x0, y0, x1, y1 = fence
    dxdy = (x1-x0, y1-y0)
    cw_dxdy = DIR[(DIR.index(dxdy)-1)%4]
    return (x1, y1, x1+cw_dxdy[0], y1+cw_dxdy[1])

def next(fence):
    x0, y0, x1, y1 = fence
    return (x1, y1, x1+(x1-x0), y1+(y1-y0))

def sides(fences):
    if len(fences) == 0:
        return 0
    start = min(fences)
    fence = start
    corners = 0
    while True:
        if cw_right(fence) in fences:
            new_fence = cw_right(fence)
            corners+=1
        elif cw_left(fence) in fences:
            new_fence = cw_left(fence)
            corners+=1
        else:
            new_fence = next(fence)
            assert(new_fence in fences)
        if fence != start:
            fences.remove(fence)
        fence = new_fence
        if fence == start:
            break
    fences.remove(start)
    return corners+sides(fences)

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(line)
    
    regions = find_regions(input)

    print(sum(len(fences(region))*len(region) for region in regions.values()))
    print(sum(sides(fences(region))*len(region) for region in regions.values()))

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
