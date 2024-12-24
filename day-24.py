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

def output(op, wire1, wire2):
    if op == 'AND':
        return wire1 & wire2
    elif op == 'OR':
        return wire1 | wire2
    else: # op == 'XOR'
        return wire1 ^ wire2

def number(wires, letter):
    letter_wires = [(wire, value) for wire, value in wires.items() if wire.startswith(letter)]
    return sum(wire_value[1]*(2**i) for i, wire_value in enumerate(sorted(letter_wires)))

def solve(wires, gates):
    while gates:
        processed = set()
        for gate in gates:
            wire1, op, wire2, wire_out = gate
            if wire1 in wires and wire2 in wires:
                wires[wire_out] = output(op, wires[wire1], wires[wire2])
                processed.add(gate)
        gates -= processed
    return wires

def rename(wire, old_wire, new_wire):
    if wire == old_wire:
        return new_wire
    return wire

def rename_wire(gates, old_wire, new_wire):
    return set((rename(wire0, old_wire, new_wire),
                op,
                rename(wire1, old_wire, new_wire),
                rename(wire_out, old_wire, new_wire)) for wire0, op, wire1, wire_out in gates)

def rename_output_wire(gates, old_wire, new_wire):
    return set((wire0, op, wire1, rename(wire_out, old_wire, new_wire)) for wire0, op, wire1, wire_out in gates)

def swap_outputs(gates, wire0, wire1):
    gates = rename_output_wire(gates, wire0, 'TEMP')
    gates = rename_output_wire(gates, wire1, wire0)
    return  rename_output_wire(gates, 'TEMP', wire1)

def order_wires(gates):
    o_gates = set()
    for gate in gates:
        wire0, op, wire1, wire_out = gate
        if wire0 < wire1:
            o_gates.add(gate)
        else: # wire0 >= wire1:
            o_gates.add((wire1, op, wire0, wire_out))
    return o_gates

def check_gates(gates):
    renames = {}

    for gate in order_wires(gates):
        wire0, op, wire1, wire_out = gate
        if wire0.startswith('x') and wire1.startswith('y'):
            xn = int(wire0.replace('x',''))
            yn = int(wire1.replace('y',''))
            if xn == yn:
                if op == 'AND':
                    logical_name = f"{xn:02d}-AND"
                    gates = rename_wire(gates, wire_out, logical_name)
                    renames[logical_name] = wire_out
                elif op == 'XOR' and not wire_out.startswith('z'):
                    logical_name = f"{xn:02d}-XOR"
                    gates = rename_wire(gates, wire_out, logical_name)
                    renames[logical_name] = wire_out

    # carry gates
    gates = rename_wire(gates, '00-AND', 'CARRY-00')
    for gate in order_wires(gates):
        wire0, op, wire1, wire_out = gate
        if wire0.endswith('-XOR') and op == 'AND':
            n = int(wire0.replace('-XOR',''))
            logical_name = f"{n:02d}-CAND"
            gates = rename_wire(gates, wire_out, logical_name)
            renames[logical_name] = wire_out
        elif wire0.endswith('-AND') and op == 'OR':
            n = int(wire0.replace('-AND',''))
            logical_name = f"CARRY-{n:02d}"
            gates = rename_wire(gates, wire_out, logical_name)
            renames[logical_name] = wire_out

    gates = order_wires(gates)
    # check
    for i in range(1,45):
        i_and = f"{i:02d}-AND"
        i_xor = f"{i:02d}-XOR"
        i_cand = f"{i:02d}-CAND"
        carry_i = f"CARRY-{i:02d}"
        carry_i_min_1 = f"CARRY-{i-1:02d}"
        zi = f"z{i:02d}"
        expected = set([(i_and, 'OR', i_cand, carry_i),
                        (i_xor, 'AND', carry_i_min_1, i_cand),
                        (i_xor, 'XOR', carry_i_min_1, zi)])
        if (expected & gates) != expected:
            print(f"========= Bit {i:2d} NOT OK =========")
            print('Expected:', sorted(expected))
            print('Matched:', sorted(expected & gates))
            others = set((w0, op, w1, wo) for w0, op, w1, wo in gates if w0 in (i_and, i_xor)) - (expected & gates)
            print('Others:', sorted(others))
            print('Renames:', sorted((k,v) for k,v in renames.items() if f"{i:02d}" in k))
            print(f"=================================")
        else:
            print(f"Bit {i} OK")

def process(filename):
    input = []
    wires = {}
    gates = set()
    for line in open(filename):
        line = line.strip()
        if ':' in line:
            wire, value = line.split(':')
            wire, value = wire.strip(), int(value)
            wires[wire] = value
        elif '->' in line:
            wire0, op, wire1, _, wire_out = map(lambda s: s.strip(), line.split())
            gates.add((wire0, op, wire1, wire_out))
    
    print(number(solve(wires.copy(), gates.copy()), 'z'))

    check_gates(gates)
    SWAPS = [('mvb', 'z08'), ('rds', 'jss'), ('wss', 'z18'), ('bmn', 'z23')]
    for swap_w0, swap_w1 in SWAPS:
        gates = swap_outputs(gates, swap_w0, swap_w1)
    check_gates(gates)
    print(','.join(sorted([w for w,_ in SWAPS] + [w for _,w in SWAPS])))

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
