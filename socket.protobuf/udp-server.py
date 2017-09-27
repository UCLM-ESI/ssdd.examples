#!/usr/bin/python3

import socket
from sensor_pb2 import Reading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 2000))
reading = Reading()

while True:
    data, address = sock.recvfrom(1024)
    print("sensor address: {}, raw-data: {}".format(address, data))

    reading.ParseFromString(data)
    print("Sensor {0.Id} ({1}) value:{0.value:.2f} {0.unit}".format(
        reading, Reading.SensorType.Name(reading.type)))
