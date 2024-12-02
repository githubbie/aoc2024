#!/usr/bin/env python3
import os
import sys
import collections

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

# part I
def is_safe(numbers):
    deltas = [a-b for a,b in zip(numbers, numbers[1:])]
    return all([1 <= d and d <= 3 for d in deltas]) or all([-3 <= d and d <= -1 for d in deltas])

# part II
def is_damper_safe(numbers):
    return is_safe(numbers) or any(is_safe(numbers[:i]+numbers[i+1:]) for i in range(len(numbers)))

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(list(map(int, line.split())))

    # part I
    print(sum(1 for numbers in input if is_safe(numbers)))

    # part II
    print(sum(1 for numbers in input if is_damper_safe(numbers)))


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
