#!/usr/bin/python3

# pico-rpc runtime: IDL primitives to describe a remote interface, plus
# the Dispatcher used by generated server stubs to route incoming calls.

import inspect
import socket
from collections import namedtuple
from typing import Annotated, get_args

WireFormat = namedtuple('WireFormat', ['name', 'fmt'])  # fmt: struct format char

uint8 = Annotated[int, WireFormat('uint8', 'B')]
uint64 = Annotated[int, WireFormat('uint64', 'Q')]

Param = namedtuple('Param', ['name', 'type'])


class Procedure(namedtuple('Procedure', ['name', 'params', 'result'])):
    @property
    def params_fmt(self):
        return ''.join(p.type.fmt for p in self.params)

    @property
    def result_fmt(self):
        return self.result.fmt


def _wire_format(annotation):
    return next(meta for meta in get_args(annotation) if isinstance(meta, WireFormat))


def _procedure(name, function):
    sig = inspect.signature(function)
    params = [Param(pname, _wire_format(p.annotation)) for pname, p in sig.parameters.items()
              if p.annotation is not inspect.Parameter.empty]
    return Procedure(name, params, _wire_format(sig.return_annotation))


class Interface:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.procedures = [_procedure(name, member)
                           for name, member in vars(cls).items()
                           if inspect.isfunction(member)]

    @classmethod
    def procedure_id(cls, name):
        for index, procedure in enumerate(cls.procedures):
            if procedure.name == name:
                return index
        raise KeyError(name)


class Dispatcher:
    def __init__(self):
        self.stubs = {}

    def register(self, stub_module, implementation):
        for id_, stub in stub_module.STUBS.items():
            self.stubs[id_] = lambda args, stub=stub: stub(args, implementation)

    def dispatch(self, sock):
        request = sock.recv(128)
        function_id, args = request[0], request[1:]
        stub = self.stubs[function_id]
        result = stub(args)
        sock.sendall(result)

    def run(self, port, backlog=10):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', port))
        sock.listen(backlog)
        print("Server ready: {}".format(sock.getsockname()))

        try:
            while True:
                client, address = sock.accept()
                self.dispatch(client)

        except KeyboardInterrupt:
            sock.close()
