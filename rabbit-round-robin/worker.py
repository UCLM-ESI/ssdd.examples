# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html
#!/usr/bin/env python3
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'));
channel = connection.channel();
channel.queue_declare(queue='task_queue', durable=True);	

print("[*] Waiting for messages. To exit press Ctrl+");

def callback(ch, method, properties, body):
	print("[x] Received %r " % (body.decode("UTF-8")));
	dots=body.count(b'.');
	time.sleep(dots);
	print("[x] Done");
	ch.basic_ack(delivery_tag=method.delivery_tag);

channel.basic_qos(prefetch_count=1);
channel.basic_consume(callback, queue='task_queue');

channel.start_consuming();

 
