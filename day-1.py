#!/usr/bin/env python3
import os
import sys
from collections import Counter

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def process(filename):
    left, right = [], []
    for line in open(filename):
        line = line.strip()
        l, r= line.split()
        left.append(int(l))
        right.append(int(r))
    left = sorted(left)
    right = sorted(right)

    # part 1
    total_distance = 0
    for l,r in zip(left, right):
        total_distance = total_distance + abs(l-r)
    print(total_distance)

    # part 2
    count_right = Counter(right)
    total_similarity = 0
    for l in left:
        total_similarity = total_similarity + l*count_right.get(l, 0)
    print(total_similarity)



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
