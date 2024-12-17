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

def combo(operand, a,b,c):
    if operand <= 3:
        return operand
    elif operand == 4:
        return a
    elif operand == 5:
        return b
    elif operand == 6:
        return c
    return None

def combo_decode(operand):
    if operand <= 3:
        return operand
    elif operand == 4:
        return 'a'
    elif operand == 5:
        return 'b'
    elif operand == 6:
        return 'c'
    return None

def literal(operand):
    return operand

def execute(a,b,c, program):
    output=[]
    ip = 0
    while ip < len(program):
        if program[ip] == 0: # adv
            a = a // (2**combo(program[ip+1], a,b,c))
            ip += 2
        elif program[ip] == 1: # bxl
            b = b ^ literal(program[ip+1])
            ip += 2
        elif program[ip] == 2: # bst
            b = combo(program[ip+1], a,b,c) % 8
            ip += 2
        elif program[ip] == 3: # jnz
            if a == 0:
                ip += 2
            else:
                ip = literal(program[ip+1])
        elif program[ip] == 4: # bxc
            b = b ^ c
            ip += 2
        elif program[ip] == 5: # out
            value = combo(program[ip+1], a,b,c) % 8
            output.append(value)
            ip += 2
        elif program[ip] == 6: # bdv
            b = a // (2**combo(program[ip+1], a,b,c))
            ip += 2
        elif program[ip] == 7: # cdv
            c = a // (2**combo(program[ip+1], a,b,c))
            ip += 2
        #print(ip, a,b,c, program, output)
    return output

b_str = { 0: '0b000', 
          1: '0b001',
          2: '0b010',
          3: '0b011',
          4: '0b100',
          5: '0b101',
          6: '0b110',
          7: '0b111',
         'a': 'a',
         'b': 'b',
         'c': 'c',
         None: '-' }

def decode(program):
    for ip in (0,):
        while ip+1 < len(program):
            if program[ip] == 0: # adv
                print(ip, ': a = a >>', combo_decode(program[ip+1]))
            elif program[ip] == 1: # bxl
                print(ip, ': b = b ^', b_str[literal(program[ip+1])])
            elif program[ip] == 2: # bst
                print(ip, ': b =', b_str[combo_decode(program[ip+1])], '& 0b111')
            elif program[ip] == 3: # jnz
                print(ip, ': jnz a,', literal(program[ip+1]))
            elif program[ip] == 4: # bxc
                print(ip, ': b = b ^ c')
            elif program[ip] == 5: # out
                print(ip, ': out', combo_decode(program[ip+1]), '& 0b111')
            elif program[ip] == 6: # bdv
                print(ip, ': b = a >>', combo_decode(program[ip+1]))
            elif program[ip] == 7: # cdv
                print(ip, ': c = a >>', combo_decode(program[ip+1]))
            ip += 2
        if ip != len(program):
            print(ip, ': hlt')
        else:
            print(ip, ': crash')

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        if line == "":
            continue
        type, values = line.split(':')
        if type == 'Register A':
            a = int(values)
        elif type == 'Register B':
            b = int(values)
        elif type == 'Register C':
            c = int(values)
        else: # type == 'Program'
            program = list(map(int, values.split(',')))

    # part 1
    print(','.join(map(str, execute(a,b,c, program))))

    # part 2
    decode(program)

    # brute force first 2 output digits
    new_options = set(a >> 3 for a in range(0, 2**6) if execute(a,b,c, program) == program[-2:])

    # loop over next output digits
    for digit in range(3,len(program)):
        options, new_options = new_options, set()
        new_options = set(a >> 3 for option in options \
                                 for a in range(option << 6, (option << 6)+2**6) \
                                 if execute(a,b,c, program) == program[-digit:])

    # get minimum A value by checking the final digit
    min_A = min((a for option in new_options \
                   for a in range(option << 6, (option << 6)+2**6) \
                   if execute(a,b,c, program) == program), default=sys.maxsize)
    print(min_A)

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
