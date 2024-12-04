#!/usr/bin/env python3
import os
import sys
import collections
import re

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def count_xmas_at_pos(m, i, j):
    if m[i][j] != 'X':
        return 0
    else:
        count = 0
        if                  j >= 3          \
                and m[i][j-1] == 'M'   and m[i][j-2] == 'A'   and m[i][j-3] == 'S':
            count += 1
        if                  j < len(m[i])-3 \
                and m[i][j+1] == 'M'   and m[i][j+2] == 'A'   and m[i][j+3] == 'S':
            count += 1
        if i >= 3                           \
                and m[i-1][j] == 'M'   and m[i-2][j] == 'A'   and m[i-3][j] == 'S':
            count += 1
        if i < len(m)-3                     \
                and m[i+1][j] == 'M'   and m[i+2][j] == 'A'   and m[i+3][j] == 'S':
            count += 1
        if i >= 3       and j >= 3          \
                and m[i-1][j-1] == 'M' and m[i-2][j-2] == 'A' and m[i-3][j-3] == 'S':
            count += 1
        if i >= 3       and j < len(m[i])-3 \
                and m[i-1][j+1] == 'M' and m[i-2][j+2] == 'A' and m[i-3][j+3] == 'S':
            count += 1
        if i < len(m)-3 and j >= 3          \
                and m[i+1][j-1] == 'M' and m[i+2][j-2] == 'A' and m[i+3][j-3] == 'S':
            count += 1
        if i < len(m)-3 and j < len(m[i])-3 \
                and m[i+1][j+1] == 'M' and m[i+2][j+2] == 'A' and m[i+3][j+3] == 'S':
            count += 1
    return count

def count_xmas(m):
    return sum(count_xmas_at_pos(m, i, j) for i in range(len(m)) for j in range(len(m[i])))

def count_cross_mas_at_pos(m, i, j):
    if m[i][j] != 'A':
        return 0
    elif i == 0 or i == len(m)-1 or j == 0 or j == len(m[0])-1:
        return 0
    elif sorted([m[i-1][j-1], m[i+1][j-1], m[i-1][j+1], m[i+1][j+1]]) != ['M', 'M', 'S', 'S']:
        return 0
    elif m[i-1][j-1] == m[i+1][j+1]:
        return 0
    else:
        return 1

def count_cross_mas(m):
    return sum(count_cross_mas_at_pos(m, i, j) for i in range(len(m)) for j in range(len(m[i])))

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(line)
    print(count_xmas(input))
    print(count_cross_mas(input))

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
