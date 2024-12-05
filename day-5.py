#!/usr/bin/env python3
import os
import sys
import collections
import re

try:
  DAY=int(sys.argv[0].split('-')[-1].replace('.py',''))
except:
  DAY=0

def middle_page(update):
    return update[int((len(update)-1)/2)]

def violation(update, before, start_pos=0, seen=None):
    if seen == None:
        seen = set()
    if start_pos >= len(update):
        return False
    page = update[start_pos]
    for condition in before.get(page, []):
        if condition in seen:
            return True
    seen.add(page)
    return violation(update, before, start_pos+1, seen)

def fix(update, before, start_pos=0, seen=None):
    if seen == None:
        seen = set()
    if start_pos >= len(update):
        return update
    page = update[start_pos]
    for condition in before.get(page, []):
        if condition in seen:
            swap_pos = update.index(condition)
            update[swap_pos], update[start_pos] = update[start_pos], update[swap_pos]
            return fix(update, before, swap_pos, set(update[:swap_pos]))
    seen.add(page)
    return fix(update, before, start_pos+1, seen)

def process(filename):
    before = {}
    updates = []
    in_ordering = True
    for line in open(filename):
        line = line.strip()
        if line == "":
            in_ordering = False
        else:
            if in_ordering:
                a,b = line.split('|')
                a,b = int(a), int(b)
                if not a in before:
                    before[a] = []
                before[a].append(b)
            else:
                updates.append(list(map(int, line.split(','))))
    
    print(sum(middle_page(update) for update in updates if not violation(update, before)))
    print(sum(middle_page(fix(update, before)) for update in updates if violation(update, before)))

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
