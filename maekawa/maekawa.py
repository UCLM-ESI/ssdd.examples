#!/usr/bin/env python3

import sys

def maekawa_voting_sets(n):
    k = n // 2 + 1
    voting_sets = []
    for i in range(n):
        vs = [(i + j) % n for j in range(k)]
        voting_sets.append(vs)
    return voting_sets


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <n_proc>")
    sys.exit(1)

if __name__ == '__main__':
    n = int(sys.argv[1])

    for i, vs in enumerate(maekawa_voting_sets(n)):
        print(f"Process {i:>2} voting set {vs}")
