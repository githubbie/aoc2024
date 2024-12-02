#!/usr/bin/env python3
import os
import sys

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def is_safe(numbers):
    deltas = [a-b for a,b in zip(numbers, numbers[1:])]
    return all([1 <= d and d <= 3 for d in deltas]) or all([-3 <= d and d <= -1 for d in deltas])

def process(filename):
    num_safe = 0
    num_safe_corr = 0
    for line in open(filename):
        line = line.strip()
        numbers = list(map(int, line.split()))

        # part I
        if is_safe(numbers):
            num_safe = num_safe + 1
        else:
            # part II
            for i in range(len(numbers)):
                new_numbers = numbers[:i]+numbers[i+1:]
                if is_safe(new_numbers):
                    num_safe_corr =+ num_safe_corr + 1
                    break


    # part I
    print(num_safe)
    # part II
    print(num_safe+num_safe_corr)


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
