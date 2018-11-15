#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import paho.mqtt.client as mqtt


def callback(client, userdata, message):
    print("topic: {}, value: {}".format(
        message.topic, message.payload.decode()))


subscriber = mqtt.Client()
subscriber.on_message = callback
subscriber.connect('localhost')
subscriber.subscribe("lab-02/temp-sensor")

try:
    subscriber.loop_forever()
except KeyboardInterrupt:
    pass
