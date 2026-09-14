# Interface definition of the Math service. Run `rpcgen.py` to generate stubs.

from picorpc import Interface, uint8, uint64


class Math(Interface):
    def factorial(n: uint8) -> uint64: ...
    def power(base: uint8, exp: uint8) -> uint64: ...
