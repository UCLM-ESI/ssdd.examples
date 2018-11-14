#!/usr/bin/python3
# -*- coding: utf-8; mode: python -*-

import paho.mqtt.client as mqtt

publisher = mqtt.Client()
publisher.connect('localhost')
publisher.publish("lab-02/temp-sensor", "25 ºC")
