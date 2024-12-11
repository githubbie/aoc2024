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

def blink(stones):
    new = collections.defaultdict(int)
    for stone, count in stones.items():
        if stone == 0:
            new[1] += count
        else:
            str_stone = str(stone)
            num_digits = len(str_stone)
            if num_digits%2 == 0:
                new[int(str_stone[:int(len(str_stone)/2)])] += count
                new[int(str_stone[int(len(str_stone)/2):])] += count
            else:
                new[stone*2024] += count
    return new
      
def process(filename):
    input = []
    for line in open(filename):
        line = list(map(int, line.strip().split()))

        stones = collections.Counter(line)
        for i in range(25):
            #print(i, sum(count for count in stones.values()), stones)
            stones = blink(stones)
        print(sum(count for count in stones.values()))

        for i in range(50):
            #print(i, sum(count for count in stones.values()), stones)
            stones = blink(stones)
        print(sum(count for count in stones.values()))

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
