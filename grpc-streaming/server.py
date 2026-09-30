#!/usr/bin/env python3

import math
import time
from concurrent import futures

import grpc
import math_pb2
import math_pb2_grpc


class Math(math_pb2_grpc.MathServicer):
    def factorials(self, request, context):
        for n in range(1, request.value + 1):
            time.sleep(0.5)
            yield math_pb2.Number(value=math.factorial(n))

    def sum(self, request_iterator, context):
        total = 0
        for number in request_iterator:
            total += number.value

        return math_pb2.Number(value=total)

    def factorial_each(self, request_iterator, context):
        for number in request_iterator:
            yield math_pb2.Number(value=math.factorial(number.value))


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
math_pb2_grpc.add_MathServicer_to_server(Math(), server)
server.add_insecure_port('[::]:2000')
server.start()

try:
    server.wait_for_termination()

except KeyboardInterrupt:
    server.stop(0)
