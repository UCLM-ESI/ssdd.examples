#!/usr/bin/python3

from celery import Celery
app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def add(x, y):
    print("invocado")
    return x + y
