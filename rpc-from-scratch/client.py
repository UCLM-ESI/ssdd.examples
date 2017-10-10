#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import socket
import struct


class ClientStub:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.sock.connect((host, port))

    def factorial(self, n):
        request = struct.pack("B", n)
        self.sock.sendall(request)

        reply = self.sock.recv(128)
        result = struct.unpack("Q", reply)[0]
        return result


if len(sys.argv) != 3:
    print("usage: ./client <server> <value>")
    sys.exit(1)


server = sys.argv[1]
value = int(sys.argv[2])

stub = ClientStub(server, 2000)
result = stub.factorial(value)
print("result = '{}'".format(result))
