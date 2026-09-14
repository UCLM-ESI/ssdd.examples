#!/usr/bin/python3

# pico-rmi runtime: IDL primitives to describe a remote interface, an
# identity encoding used to address individual remote objects, the Servant
# base class that generated server stubs attach marshaling to, and the
# ObjectAdapter used to route incoming requests to the right servant.
#
# Unlike plain RPC (see ../pico-rpc), where every request goes to a single,
# stateless implementation, here a server can host any number of independent
# servant instances. Each one is registered under an identity, and a proxy
# addresses one specific remote object by combining an endpoint (host, port)
# with that identity

import inspect
import socket
from collections import namedtuple
from typing import Annotated, get_args

WireFormat = namedtuple('WireFormat', ['name', 'fmt'])  # fmt: struct format char

uint8 = Annotated[int, WireFormat('uint8', 'B')]
uint64 = Annotated[int, WireFormat('uint64', 'Q')]

Param = namedtuple('Param', ['name', 'type'])

IDENTITY_SIZE = 16

def encode_identity(identity):
    raw = identity.encode('utf-8')
    if len(raw) > IDENTITY_SIZE:
        raise ValueError('identity {!r} does not fit in {} bytes'.format(identity, IDENTITY_SIZE))
    return raw.ljust(IDENTITY_SIZE, b'\0')


def decode_identity(raw):
    return raw.split(b'\0', 1)[0].decode('utf-8')


class Method(namedtuple('Method', ['name', 'params', 'result'])):
    @property
    def params_fmt(self):
        return ''.join(p.type.fmt for p in self.params)

    @property
    def result_fmt(self):
        return self.result.fmt


def _wire_format(annotation):
    return next(meta for meta in get_args(annotation) if isinstance(meta, WireFormat))


def _method(name, function):
    sig = inspect.signature(function)
    params = [Param(pname, _wire_format(p.annotation)) for pname, p in sig.parameters.items()
              if p.annotation is not inspect.Parameter.empty]
    return Method(name, params, _wire_format(sig.return_annotation))


class Interface:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.methods = [
            _method(name, member) for name, member in vars(cls).items()
            if inspect.isfunction(member)]

    @classmethod
    def method_id(cls, name):
        for index, method in enumerate(cls.methods):
            if method.name == name:
                return index
        raise KeyError(name)


class Servant:
    STUBS = {}  # set by the generated subclass: function_id -> unbound stub method

    def dispatch(self, function_id, args):
        return self.STUBS[function_id](self, args)


class ObjectAdapter:
    def __init__(self, port):
        self.port = port
        self.servants = {}

    def add(self, identity, servant):
        self.servants[identity] = servant

    def dispatch(self, sock):
        request = sock.recv(128)
        identity = decode_identity(request[:IDENTITY_SIZE])
        function_id, args = request[IDENTITY_SIZE], request[IDENTITY_SIZE + 1:]

        servant = self.servants[identity]
        result = servant.dispatch(function_id, args)
        sock.sendall(result)

    def run(self, backlog=10):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(backlog)
        print("Object adapter ready: {}".format(sock.getsockname()))

        try:
            while True:
                client, address = sock.accept()
                self.dispatch(client)

        except KeyboardInterrupt:
            sock.close()
