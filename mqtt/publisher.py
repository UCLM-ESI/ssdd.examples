#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import json
import time
import random
import paho.mqtt.client as mqtt

publisher = mqtt.Client()
publisher.connect('localhost')


def take_reading():
    return {
        'identifier': 'X002',
        'value': random.randint(20, 40),
        'unit': 'Celsius',
        'timestamp': time.time(),
    }


while 1:
    publisher.publish('temperature/X002', json.dumps(take_reading()))
    time.sleep(1)
