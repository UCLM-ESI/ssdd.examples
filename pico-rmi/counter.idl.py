# Interface definition of the Counter service. Run `rmigen.py` to generate
# the proxy and server stubs.

from picormi import Interface, uint64


class Counter(Interface):
    def increment() -> uint64: ...
    def get() -> uint64: ...
