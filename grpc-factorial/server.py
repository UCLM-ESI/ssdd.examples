#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# This example is based on https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld

from concurrent import futures
import time

import grpc
import math_pb2
import math_pb2_grpc

DAY_SECONDS = 24 * 60 * 60


class Math(math_pb2_grpc.MathServicer):
    def factorial(self, request, context):
        result = 1
        n = request.value

        while n:
            result *= n
            n -= 1

        return math_pb2.FactorialReply(result=result)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
math_pb2_grpc.add_MathServicer_to_server(Math(), server)
server.add_insecure_port('[::]:2000')
server.start()

try:
    while True:
        time.sleep(DAY_SECONDS)

except KeyboardInterrupt:
    server.stop(0)
