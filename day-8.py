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

def find_antinodes(nodes, max_x, max_y, c):
    anti_nodes = set()
    for n1, n2 in itertools.combinations(nodes, 2):
        dx, dy = n1[0] - n2[0], n1[1] - n2[1]
        a1 = (n1[0]+dx, n1[1]+dy)
        a2 = (n2[0]-dx, n2[1]-dy)
        if 0 <= a1[0] and a1[0] < max_x and 0 <= a1[1] and a1[1] < max_y:
            anti_nodes.add(a1)
            print("OK", c, n1, n2, (dx,dy), a1)
        else:
            print("--", c, n1, n2, (dx,dy), a1)
        if 0 <= a2[0] and a2[0] < max_x and 0 <= a2[1] and a2[1] < max_y:
            anti_nodes.add(a2)
            print("OK", c, n1, n2, (dx,dy), a2)
        else:
            print("--", c, n1, n2, (dx,dy), a2)
    return anti_nodes

def find_harmonic_antinodes(nodes, max_x, max_y, c):
    anti_nodes = set()
    N = max(max_x, max_y)
    for n1, n2 in itertools.combinations(nodes, 2):
        dx, dy = n1[0] - n2[0], n1[1] - n2[1]
        for n in range(-N,N+1):
            a = (n1[0]+dx*n, n1[1]+dy*n)
            if 0 <= a[0] and a[0] < max_x and 0 <= a[1] and a[1] < max_y:
                anti_nodes.add(a)
                print("OK", c, n1, n2, (dx,dy), a)
            else:
                print("--", c, n1, n2, (dx,dy), a)
    return anti_nodes


def process(filename):
    input = []
    nodes = {}
    y = 0
    max_x, max_y = 0, 0
    for line in open(filename):
        line = line.strip()
        for x in range(len(line)):
            if line[x] != '.':
                c = line[x]
                if not c in nodes:
                    nodes[c] = []
                nodes[c].append((x,y))
        y+=1
        max_x = len(line)
    max_y = y

    anti_nodes = set()
    for c in nodes:
        anti_nodes.update(find_antinodes(nodes[c], max_x, max_y, c))
    print(len(anti_nodes))

    anti_nodes = set()
    for c in nodes:
        anti_nodes.update(find_harmonic_antinodes(nodes[c], max_x, max_y, c))
    print(len(anti_nodes))

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
