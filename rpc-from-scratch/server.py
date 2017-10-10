#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-

import socket
import struct


def factorial(n):
    if n == 0:
        return 1

    return n * factorial(n - 1)


def server_stub(sock):
    request = sock.recv(128)
    value = struct.unpack("B", request)[0]

    result = factorial(value)

    reply = struct.pack("Q", result)
    sock.send(reply)


sock = socket.socket()
sock.bind(('', 2000))
sock.listen(10)

try:
    while True:
        client, address = sock.accept()
        server_stub(client)

except KeyboardInterrupt:
    sock.close()
