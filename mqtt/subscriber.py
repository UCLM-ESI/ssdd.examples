#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import json
import paho.mqtt.client as mqtt


def callback(client, userdata, message):
    decoded = json.loads(message.payload.decode())
    print("topic: {}, msg: {}".format(
        message.topic, decoded))

    print(decoded["value"])


subscriber = mqtt.Client()
subscriber.on_message = callback
subscriber.connect('localhost')
subscriber.subscribe('temperature/+')

try:
    subscriber.loop_forever()
except KeyboardInterrupt:
    pass
