#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-one-python.html

import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'));
channel = connection.channel();
channel.queue_declare(queue='hello');


def callback(ch, method, properties, body):
	print("[x] Received: %r" % body.decode("UTF-8"));


channel.basic_consume(callback, queue='hello', no_ack=True);


print("[*] Waiting for messages. To exit press Ctrl+");
channel.start_consuming();
