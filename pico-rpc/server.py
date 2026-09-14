#!/usr/bin/python3

from picorpc import Dispatcher
import math_server_stub


class MathI:
    def factorial(self, n):
        if n == 0:
            return 1

        return n * self.factorial(n - 1)

    def power(self, base, exp):
        return base ** exp


dispatcher = Dispatcher(port=2000)
dispatcher.register(math_server_stub, MathI())
dispatcher.run()
