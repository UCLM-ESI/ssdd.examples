# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-three-python.html
#!/usr/bin/env python3
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'));
channel = connection.channel();
channel.exchange_declare(exchange='twitter', exchange_type='fanout');	
result = channel.queue_declare(exclusive='True')
queue_name = result.method.queue

channel.queue_bind(exchange='twitter', queue=queue_name);

print("[*] Waiting for messages. To exit press Ctrl+");

def callback(ch, method, properties, body):
	print("[x] Received %r " % (body.decode("UTF-8")));

channel.basic_consume(callback, queue=queue_name, no_ack=True);

channel.start_consuming();

 
