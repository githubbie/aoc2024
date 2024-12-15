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

# gx = ax*A + bx*B
# gy = ay*A + by*B
# 
# A = (gx-bx*B) / ax
# 
# gy = ay*(gx-bx*B)/ax + by*B
# gy*ax = ay*gx-ay*bx*B + ax*by*B
# gy*ax-ay*gx = (ax*by-ay*bx)*B
# (gy*ax-gx*ay)/(ax*by-ay*bx) = B

def fast_solve(puzzle):
    buttons, goal = puzzle
    ac, ax, ay = buttons['A']
    bc, bx, by = buttons['B']
    gx, gy = goal

    if (gy*ax-gx*ay) % (ax*by-ay*bx) == 0:
        b = (gy*ax-gx*ay) // (ax*by-ay*bx)
        if (gx-bx*b) % ax == 0:
            a = (gx-bx*b) // ax
            c = a*ac + b*bc
            return c
    return 0

def fix(puzzle):
    buttons, goal = puzzle
    return (buttons, (10000000000000+goal[0], 10000000000000+goal[1]))
    
COST = { 'A': 3, 'B': 1 }
def process(filename):
    input = []
    buttons = {}
    goal = None
    for line in open(filename):
        line = line.strip()
        if line != "":
            part, data = line.split(':')
            parts = part.split()
            if len(parts) == 1:
                assert(part=='Prize')
                data = data.replace(',','').replace('=',' ').split()
                goal = (int(data[1]), int(data[3]))
                input.append((buttons, goal))
                buttons = {}
                goal = None
            else:
                assert(parts[0] == 'Button')
                button = parts[1]
                data = data.replace(',','').replace('+',' ').split()
                steps = (COST[button], int(data[1]), int(data[3]))
                buttons[button] = steps

    print(sum(fast_solve(puzzle) for puzzle in input))
    print(sum(fast_solve(fix(puzzle)) for puzzle in input))

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
