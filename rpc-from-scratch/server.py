#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import socket
import struct

FACTORIAL = 0
POWER = 1


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


def factorial_stub(args):
    arg = struct.unpack('B', args)[0]
    result = factorial(arg)
    return struct.pack("Q", result)


def power(base, exp):
    return base ** exp


def power_stub(args):
    base, exp = struct.unpack('BB', args)
    result = power(base, exp)
    return struct.pack("Q", result)


class Dispatcher:
    def __init__(self):
        self.stubs = {}

    def register(self, id_, function):
        self.stubs[id_] = function

    def dispatch(self, sock):
        request = sock.recv(128)
        function_id, args = request[0], request[1:]
        stub = self.stubs[function_id]
        result = stub(args)
        sock.sendall(result)


dispatcher = Dispatcher()
dispatcher.register(FACTORIAL, factorial_stub)
dispatcher.register(POWER, power_stub)


sock = socket.socket()
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', 2000))
sock.listen(10)
print("Server ready: {}".format(sock.getsockname()))

try:
    while True:
        client, address = sock.accept()
        dispatcher.dispatch(client)

except KeyboardInterrupt:
    sock.close()
