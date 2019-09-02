#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import json
import time
import random
import paho.mqtt.client as mqtt


def take_reading():
    return {
        'identifier': 'X002',
        'value': random.randint(20, 40),
        'unit': 'Celsius',
        'timestamp': time.time(),
    }


publisher = mqtt.Client()
publisher.connect('127.0.0.1')

while 1:
    publisher.publish('temperature/X002', json.dumps(take_reading()))
    time.sleep(1)
