#!/usr/bin/env python3
import os
import sys
import collections
import re

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def concat(a,b):
    return int(str(a) + str(b))

def matches(answer, elements, current):
    if elements == []:
        return current == answer
    next = elements[0]
    return matches(answer, elements[1:], current+next) or \
           matches(answer, elements[1:], current*next)

def matches2(answer, elements, current):
    if elements == []:
        return current == answer
    next = elements[0]
    return matches2(answer, elements[1:], current+next) or \
           matches2(answer, elements[1:], current*next) or \
           matches2(answer, elements[1:], concat(current,next))

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        answer, *elements = map(int, line.replace(':',' ').split())
        input.append((answer, elements))

    print(sum(answer for answer, elements in input if matches(answer, elements[1:], elements[0])))
    print(sum(answer for answer, elements in input if matches2(answer, elements[1:], elements[0])))


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
