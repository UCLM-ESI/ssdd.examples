#!/usr/bin/python3

import sys

from counter_client_stub import CounterProxy


if len(sys.argv) != 3:
    print("usage: ./client <server> <identity>")
    exit(1)

server = sys.argv[1]
identity = sys.argv[2]

counter = CounterProxy(identity, server, 2001)
print("get() = '{}'".format(counter.get()))
print("increment() = '{}'".format(counter.increment()))
print("increment() = '{}'".format(counter.increment()))
print("get() = '{}'".format(counter.get()))
