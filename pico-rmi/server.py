#!/usr/bin/python3

from picormi import ObjectAdapter
from counter_server_stub import Counter


class CounterI(Counter):
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1
        return self.value

    def get(self):
        return self.value


adapter = ObjectAdapter(port=2001)
adapter.add('c1', CounterI())
adapter.add('c2', CounterI())
adapter.run()
