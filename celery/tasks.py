#!/usr/bin/python

from celery import Celery
app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def add(x, y):
    return x + y
