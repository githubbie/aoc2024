#!/usr/bin/env python3
import os
import sys
import collections
import re
import itertools
import copy

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=15

DIR = { '<': (-1,0) , 'v': (0,1), '>': (1,0), '^': (0,-1) }

def print_warehouse(walls, boxes, robot, title='', size=1):
    print(robot, title)
    grid = max(walls)
    for y in range(grid[1]+1):
        for x in range(grid[0]+1):
            if (x,y) in walls:
                print('#', end='')
            elif (x,y) in boxes:
                if size == 1:
                    print('O', end='')
                else: 
                    print('[', end='')
            elif size == 2 and (x-1,y) in boxes:
                print(']', end='')
            elif (x,y) == robot:
                print('@', end='')
            else:
                print('.', end='')
        print()

def moved_boxes(walls, boxes, box, direction, size=1):
    if direction[0] == 0:
        next_walls = set((box[0]+d, box[1]+direction[1]) for d in range(0,size)) & walls
    elif direction[0] == -1:
        next_walls = set((box[0]+direction[0], box[1]+d) for d in range(0,1)) & walls
    else: # direction[0] == 1
        next_walls = set((box[0]+size*direction[0], box[1]+d) for d in range(0,1)) & walls
    if next_walls:
        return set([None])

    if direction[0] == 0:
        next_boxes = set((box[0]+d, box[1]+direction[1]) for d in range(-size+1,size)) & boxes
    else:
        next_boxes = set((box[0]+size*direction[0], box[1]+d) for d in range(0,1)) & boxes
    return set([box]).union(*[moved_boxes(walls, boxes, pushed_box, direction, size) for pushed_box in next_boxes])

def move_boxes(boxes, moved_boxes, direction):
    return (boxes - moved_boxes) | set((x+direction[0],y+direction[1]) for x,y in moved_boxes)

def move(walls, boxes, robot, direction, size=1):
    dx, dy = direction
    new_robot = (robot[0]+dx, robot[1]+dy)
    if new_robot in walls:
        new_robot = robot
    else:
        pushing = set([new_robot, (new_robot[0]+1-size, new_robot[1])]) & boxes
        if pushing:
            moved = moved_boxes(walls, boxes, pushing.pop(), direction, size)
            if None in moved:
                new_robot = robot
            else:
                boxes = move_boxes(boxes, moved, direction)
    return new_robot, boxes

def gps(boxes):
    return sum(100*y+x for x,y in boxes)

def process(filename):
    y = -1
    moves = None
    walls = set()
    boxes = set()
    robot = (0,0)
    for line in open(filename):
        line = line.strip()
        y=y+1
        if line == "":
            moves = []
        elif moves == None:
            for x, c in enumerate(line):
                if c == '#':
                    walls.add((x,y))
                elif c == 'O':
                    boxes.add((x,y))
                elif c == '@':
                    robot = (x,y)
        else:
            moves.extend(DIR[c] for c in line)

    initial_boxes = boxes
    initial_robot = robot
                
    for i, direction in enumerate(moves):
        robot, boxes = move(walls, boxes, robot, direction, 1)
    print(gps(boxes))

    boxes = set((2*x,y) for (x,y) in initial_boxes)
    robot = (2*initial_robot[0], initial_robot[1])
    walls = set((2*x,y) for (x,y) in walls) | set((2*x+1,y) for (x,y) in walls)

    for i, direction in enumerate(moves):
        robot, boxes = move(walls, boxes, robot, direction, 2)
    print(gps(boxes))

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
