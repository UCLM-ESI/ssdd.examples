#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika
import time

localhost = pika.ConnectionParameters(host='localhost')
connection = pika.BlockingConnection(localhost)

channel = connection.channel()
channel.queue_declare(queue="hello")

message = "Hello world! {}".format(time.time())
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=message)

print("[x] Sent: ", message)
connection.close()
