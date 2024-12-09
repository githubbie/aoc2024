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

def file_checksum(position, file, size):
    return file*sum(range(position, position+size))

def defrag1(files, spaces):
    files = files.copy()
    spaces = spaces.copy()
    while len(spaces) > 1:
        file_pos, file_num, file_size = files[-1]
        space_pos, space_size = spaces[0]
        if space_pos > file_pos:
            break
        if space_size == file_size or space_pos+space_size == file_pos:
            files.insert(0, (space_pos, file_num, file_size))
            del spaces[0]
            del files[-1]
        elif space_size < file_size:
            files.insert(0, (space_pos, file_num, space_size))
            files[-1] = (file_pos, file_num, file_size-space_size)
            del spaces[0]
        else: # space_size > file_size
            files.insert(0, (space_pos, file_num, file_size))
            spaces[0] = (space_pos + file_size, space_size - file_size)
            del files[-1]
    return files

def defrag2(files, spaces):
    spaces = spaces.copy()
    new_files = []
    for file_pos, file_num, file_size in reversed(files):
        index, space = next(((i,s) for i,s in enumerate(spaces) if s[0] < file_pos and s[1] >= file_size), (-1, None))
        if index >= 0:
            space_pos, space_size = space
            new_files.append((space_pos, file_num, file_size))
            if space_size == file_size:
                del spaces[index]
            else: # space_size < file_size
                spaces[index] = (space_pos+file_size, space_size-file_size)
        else:
            new_files.append((file_pos, file_num, file_size))
    return new_files

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()

        num_files = int(len(line)/2)
        files, spaces = [], []
        position = 0
        for file in range(num_files):
            size = int(line[file*2])
            files.append((position, file, size))
            position += size
            size = int(line[file*2+1])
            if size > 0:
                spaces.append((position, size))
                position += size
        size = int(line[-1])
        files.append((position, num_files, size))

        print(sum(file_checksum(*f) for f in defrag1(files, spaces)))
        print(sum(file_checksum(*f) for f in defrag2(files, spaces)))

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
