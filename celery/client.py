#!/usr/bin/python3

from celery import Celery
from tasks import add

app = Celery('tasks', backend='rpc://', broker='pyamqp://')
result = add.delay(4, 4)
value = result.get(timeout=1)
print(value)
