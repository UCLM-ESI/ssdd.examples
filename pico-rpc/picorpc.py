#!/usr/bin/python3

# pico-rpc runtime: IDL primitives to describe a remote interface, plus
# the Dispatcher used by generated server stubs to route incoming calls.

import functools
import inspect
import socket
from collections import namedtuple

# uint8/uint64 double as struct format characters and as the parameter/return
# annotations read by _procedure() below to build the wire format of a call.
uint8 = 'B'
uint64 = 'Q'

Param = namedtuple('Param', ['name', 'type'])

MAX_MESSAGE_SIZE = 128  # fixed-size recv() buffer for both requests and replies


class Procedure(namedtuple('Procedure', ['name', 'params', 'result'])):
    @property
    def params_fmt(self):
        return ''.join(p.type for p in self.params)

    @property
    def result_fmt(self):
        return self.result


def _procedure(name, function):
    sig = inspect.signature(function)
    params = [Param(pname, p.annotation) for pname, p in sig.parameters.items()
              if p.annotation is not inspect.Parameter.empty]
    return Procedure(name, params, sig.return_annotation)


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
    def __init__(self, port):
        self.port = port
        self.stubs = {}

    def register(self, stub_module, implementation):
        for id_, stub in stub_module.STUBS.items():
            self.stubs[id_] = functools.partial(stub, implementation=implementation)

    def dispatch(self, sock):
        request = sock.recv(MAX_MESSAGE_SIZE)
        function_id, args = request[0], request[1:]
        stub = self.stubs[function_id]
        result = stub(args)
        sock.sendall(result)

    def run(self, backlog=10):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(backlog)
        print("Server ready: {}".format(sock.getsockname()))

        try:
            while True:
                client, address = sock.accept()
                self.dispatch(client)

        except KeyboardInterrupt:
            sock.close()
