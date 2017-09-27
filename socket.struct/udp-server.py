#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import sys
import socket
import struct


def deserialize_reading(data):
    format_ = "!hBfB"
    fixed = struct.calcsize(format_)
    id_, type_, value, unit_len = struct.unpack(format_, data[:fixed])   
    unit = data[fixed:][:unit_len]
    return id_, type_, value, unit.decode()

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', int(2000)))

    while 1:
        data, client = sock.recvfrom(1024)
        print("New message {}".format(client))
        
        reading = deserialize_reading(data)
        print("Sensor {0} ({1}) value:{2:.2f} {3}".format(*reading))


try:
    main()
except KeyboardInterrupt:
    pass
