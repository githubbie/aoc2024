#!/usr/bin/env python3
import os
import sys
import collections

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(map(int, line.split()))
    left,right = map(sorted, zip(*input))

    # part 1
    print(sum(abs(l-r) for l,r in zip(left, right)))

    # part 2
    count = collections.Counter(right)
    print(sum(l*count[l] for l in left))

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
