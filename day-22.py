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

def next(secret):
    secret = ((secret*64)   ^ secret)%16777216
    secret = ((secret//32)  ^ secret)%16777216
    secret = ((secret*2048) ^ secret)%16777216
    return secret

def secrets(secret, n):
    secrets = [secret]
    for _ in range(n):
        secrets.append(next(secrets[-1]))
    return secrets

def prices_per_group(secrets):
    prices = [secret%10 for secret in secrets]
    deltas = [(p0)-(p1) for p0,p1 in zip(prices, prices[1:])]
    groups = [(a,b,c,d) for a,b,c,d in zip(deltas, deltas[1:], deltas[2:], deltas[3:])]
    values = [prices[i+4] for i in range(len(groups))]
    result = {}
    for i, group in enumerate(groups):
        if not group in result:
            result[group] = values[i]
    return result

def process(filename):
    input = []
    for line in open(filename):
        line = line.strip()
        input.append(int(line))

    print(sum(secrets(i, 2000)[-1] for i in input))

    sum_groups = collections.defaultdict(int)
    for i in input:
        for group, price in prices_per_group(secrets(i, 2000)).items():
            sum_groups[group] += price

    print(max(sum_groups.values()))

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
