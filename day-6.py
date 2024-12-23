#!/usr/bin/env python3
import os
import sys
import collections
import re
import copy

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def print_maze(maze):
    for y in range(len(maze)):
        print("".join(maze[y]))

def next_pos(maze, guard):
    x,y,o = guard
    if o == '<':
        if x <= 0:
            return (x-1, y, '@')
        if maze[y][x-1] == '#':
            return next_pos(maze, (x, y, '^'))
        return (x-1, y, o)
    if o == '^':
        if y <= 0:
            return (x, y-1, '@')
        if maze[y-1][x] == '#':
            return next_pos(maze, (x, y, '>'))
        return (x, y-1, o)
    if o == '>':
        if x >= len(maze[0])-1:
            return (x+1, y, '@')
        if maze[y][x+1] == '#':
            return next_pos(maze, (x, y, 'v'))
        return (x+1, y, o)
    if o == 'v':
        if y >= len(maze)-1:
            return (x, y+1, '@')
        if maze[y+1][x] == '#':
            return next_pos(maze, (x, y, '<'))
        return (x, y+1, o)
    return (x,y,'@')

def fill_maze1(maze, guard):
    x,y,o = guard
    maze[y][x] = 'X'
    while guard[2] != '@':
        guard = next_pos(maze, guard)
        x,y,o = guard
        if o != '@':
            maze[y][x] = 'X'

def o_code(o):
    return 2**('^>v<'.index(o))

def o_code_rotate(o):
    return 2**('>v<^'.index(o))

def mark(maze, guard):
    x,y,o = guard
    if maze[y][x] == '#':
        return '#'
    elif maze[y][x] in '01234567890abcdef':
        current = int(maze[y][x],16)
    else:
        current = 0
    return hex(current|o_code(o))[-1]

def fill_maze2(maze, guard):
    x,y,o = guard
    maze[y][x] = mark(maze, guard)
    while guard[2] != '@':
        guard = next_pos(maze, guard)
        x,y,o = guard
        if o != '@':
            if maze[y][x] == mark(maze, guard):
                return True
            else:
                maze[y][x] = mark(maze, guard)
        #print_maze(maze)
        #print(guard)
    return False

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(list(line))

    guard = None
    for x in range(len(input[0])):
        for y in range(len(input)):
            if input[y][x] in ['<', '>', '^', 'v']:
                guard = (x, y, input[y][x])
                input[y][x] = '.'
                break
        if guard != None:
            break

    for o in '^>v<':
        print(o_code(o), o_code_rotate(o))

    maze = copy.deepcopy(input)
    fill_maze1(maze, guard)
    print(sum(maze[y].count('X') for y in range(len(maze))))

    g_x, g_y, _ = guard
    obstacles = 0
    for y in range(len(input)):
        for x in range(len(input[0])):
            maze = copy.deepcopy(input)
            if maze[y][x] != '#' and (g_x != x or g_y != y):
                maze[y][x] = '#'
                if fill_maze2(maze, guard):
                    obstacles += 1
                    print("obstacle", x, y)
                    print_maze(maze)
                else:
                    print("ok      ", x, y)
    print(obstacles)


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
