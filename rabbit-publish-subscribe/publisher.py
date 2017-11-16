#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-three-python.html

import sys
import pika

connection=pika.BlockingConnection(pika.ConnectionParameters(host='localhost'));
channel=connection.channel();

channel.exchange_declare(exchange='twitter', exchange_type='fanout')


message=' '.join(sys.argv[1:]) or "Hello world!"
channel.basic_publish(exchange='twitter', routing_key='', body=message);

print("[x] Sent: ", message);
connection.close();
