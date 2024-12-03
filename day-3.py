#!/usr/bin/env python3
import os
import sys
import collections
import re

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def execute_all(line):
    ins = re.compile('mul\(([0-9]{1,3}),([0-9]{1,3})\)')
    return sum(int(i)*int(j) for i,j in ins.findall(line))

def execute_cond(line):
    ins = re.compile("(do)\(\)|(don't)\(\)|(mul)\(([0-9]{1,3}),([0-9]{1,3})\)")
    total, conditional = 0, 1
    for do,dont,mul,i,j in ins.findall(line):
        if do != '':
            conditional = 1
        elif dont != '':
            conditional = 0
        else:
            total = total + conditional*int(i)*int(j)
    return total

def process(filename):
    input = ''
    for line in open(filename):
        line = line.strip()
        input=input+line

    # part 1
    print(execute_all(input))

    # part 2
    print(execute_cond(input))

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
