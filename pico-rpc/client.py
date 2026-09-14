#!/usr/bin/python3

import sys

from math_client_stub import MathStub


if len(sys.argv) != 3:
    print("usage: ./client <server> <arg>")
    exit(1)

server = sys.argv[1]
arg = int(sys.argv[2])

stub = MathStub(server, 2000)
print("factorial({}) = '{}'".format(arg, stub.factorial(arg)))
print("power({}, {}) = '{}'".format(arg, arg-1, stub.power(arg, arg-1)))
