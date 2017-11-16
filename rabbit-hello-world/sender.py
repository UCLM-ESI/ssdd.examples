#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'));
channel = connection.channel();

channel.queue_declare(queue="hello");

message="Hello world!"
channel.basic_publish(exchange='', routing_key='hello', body=message)

print("[x] Sent: ", message);
connection.close();
