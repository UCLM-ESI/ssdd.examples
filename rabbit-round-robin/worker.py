#!/usr/bin/env python3
# Extracted from: https://www.rabbitmq.com/tutorials/tutorial-two-python.html

import time
import pika

STRICT_ROUND_ROBIN = False


def callback(ch, method, properties, body):
    print("[x] Received %r " % (body.decode("UTF-8")))
    time.sleep(body.count(b'.'))
    print("[x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

if STRICT_ROUND_ROBIN:
    channel.basic_qos()
else:
    channel.basic_qos(prefetch_count=1)

channel.basic_consume(on_message_callback=callback, queue='task_queue')
print("[*] Waiting for messages. Press Ctrl+C to exit")
channel.start_consuming()
