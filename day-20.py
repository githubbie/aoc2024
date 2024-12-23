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

d1 = { (-1,0), (+1,0), (0,-1), (0,+1) }
d2  = { (dx,dy) for dx in range( -2, 3) for dy in range( -2, 3) if 2 <= abs(dx)+abs(dy) <= 2 }
d20 = { (dx,dy) for dx in range(-20,21) for dy in range(-20,21) if 2 <= abs(dx)+abs(dy) <= 20 }

def process(filename):
    track = {}
    for r, line in enumerate(open(filename)):
        for c, char in enumerate(line.strip()):
            if char == '.':
                track[(r,c)] = -1
            elif char == 'S':
                start = (r,c)
                track[start] = 0
            elif char == 'E':
                end = (r,c)
                track[end] = -1

    # distances from S
    pos = start
    while pos != end:
        for d in d1:
            next = (pos[0]+d[0],pos[1]+d[1])
            if track.get(next, -2) == -1:
                track[next] = track[pos]+1
                pos = next

    for ds in [d2, d20]:
        cheats = collections.defaultdict(lambda: set())
        for pos in track:
            for d in ds:
                jump = (pos[0]+d[0],pos[1]+d[1])
                gain = track.get(jump, -1) - (track[pos]+abs(d[0])+abs(d[1]))
                # Erratum, this was not supposed to be in the challenge text!
                #if abs(d[0]) == 20 and abs(pos[0]-end[0]) < 20 and pos[1] == end[1]:
                #    continue
                #if abs(d[1]) == 20 and pos[0] == end[0] and abs(pos[1]-end[1]) < 20:
                #    continue
                if (gain > 0):
                    cheats[gain].add((pos, d))
        print(sum(len(cheats[gain]) for gain in cheats if gain >= 100))

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
