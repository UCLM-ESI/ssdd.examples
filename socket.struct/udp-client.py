#!/usr/bin/python3 -u
"Usage: {0} <host>"

import sys
import socket
import struct

UNKNOWN  = 0
HUMIDITY = 1
PRESSURE = 2
ACCELERATION = 3


def serialize_reading(id_, type_, value, unit):
    unit = unit.encode()
    unit_len = len(unit)
    return struct.pack('!hBfB{}s'.format(unit_len), id_, type_, value, unit_len, unit)


if len(sys.argv) != 2:
    print(__doc__.format(__file__))
    sys.exit(1)


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
data = serialize_reading(id_=8, type_=PRESSURE, value=16.3, unit='bar')  
sock.sendto(data, (sys.argv[1], 2000))
sock.close()
