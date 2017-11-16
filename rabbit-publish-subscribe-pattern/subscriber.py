#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-five-python.html

import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'));
channel = connection.channel();
channel.exchange_declare(exchange='twitter-pattern', exchange_type='topic');
result = channel.queue_declare(exclusive='True')
queue_name = result.method.queue

binding_keys=sys.argv[1:]
if not binding_keys:
	sys.stderr.write("Usage: %s [binding key]...\n", sys.argv[0])
	sys.exit(1)

for binding_key in binding_keys:
	channel.queue_bind(exchange='twitter-pattern', queue=queue_name, routing_key=binding_key);

print("[*] Waiting for messages. To exit press Ctrl+");

def callback(ch, method, properties, body):
	print("[x] Received %r: %r " % (method.routing_key, body.decode("UTF-8")));

channel.basic_consume(callback, queue=queue_name, no_ack=True);

channel.start_consuming();
