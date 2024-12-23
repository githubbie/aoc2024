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

def process(filename):
    input = collections.defaultdict(set)
    for line in open(filename):
        line = line.strip()
        a,b = line.split('-')
        input[a].add(b)
        input[b].add(a)

    three_icc = set()
    for a in input:
        for b in input[a]:
            for c in input[b]:
                if a != c and c in input[a]:
                    three_icc.add(frozenset([a,b,c]))
    print(len([icc for icc in three_icc if any(node.startswith('t') for node in icc)]))

    iccs = [three_icc]
    while len(iccs[-1]) > 0:
        next_icc = set()
        for icc in iccs[-1]:
            connected = set.intersection(*(input[node] for node in icc))
            for node in connected:
                next_icc.add(frozenset(list(icc) + [node]))
        iccs.append(next_icc)
    assert(len(iccs[-2]) == 1)
    print(','.join(sorted(iccs[-2].pop())))


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
