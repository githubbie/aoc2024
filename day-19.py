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

def arrange(pattern, towels, o):
    if pattern == '':
        return True
    return any(arrange(pattern[len(towel):], towels, o) for towel in towels if pattern.startswith(towel))

def count_arrange(pattern, towels):
    counts = [1] + [0]*len(pattern)
    for i in range(len(pattern)):
        for towel in towels:
            if pattern[i:].startswith(towel):
                counts[i+len(towel)] += counts[i]
    return counts[-1]

def reverse_s(s):
    return ''.join(reversed(s))

def process(filename):
    towels = {}
    patterns = None
    for line in open(filename):
        line = line.strip()
        if patterns != None:
            patterns.append(line)
        elif line == '':
            patterns = []
        else:
            towels = set(map(lambda s: s.strip(), line.split(',')))

    # part 1
    reversed_towels = [reverse_s(towel) for towel in towels]
    print(sum(1 for pattern in patterns if arrange(reverse_s(pattern), reversed_towels, reverse_s(pattern))))

    # part 1 - revisited after part 2
    print(sum(1 for pattern in patterns if count_arrange(pattern, towels) > 0))

    # part 2
    print(sum(count_arrange(pattern, towels) for pattern in patterns))


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
