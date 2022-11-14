#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-three-python.html

import time
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel();
channel.exchange_declare(exchange='twitter', exchange_type='fanout')
result = channel.queue_declare(queue='', exclusive='True')
queue_name = result.method.queue

channel.queue_bind(exchange='twitter', queue=queue_name)

print("[*] Waiting for messages. To exit press Ctrl+")

def callback(ch, method, properties, body):
	print("[x] Received %r " % (body.decode("UTF-8")))

channel.basic_consume(
	on_message_callback=callback,
	queue=queue_name,
	auto_ack=True
)

channel.start_consuming()
