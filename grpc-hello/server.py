#!/usr/bin/env python3
# -*- coding:utf-8; mode:python -*-
# This example is based on https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld

from concurrent import futures

import grpc
import hello_pb2
import hello_pb2_grpc


class Hello(hello_pb2_grpc.HelloServicer):
    def write(self, request, context):
        print("Client sent: '{}'".format(request.message))
        return hello_pb2.PrintReply()


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
hello_pb2_grpc.add_HelloServicer_to_server(Hello(), server)
server.add_insecure_port('0.0.0.0:2000')
server.start()

try:
    server.wait_for_termination()

except KeyboardInterrupt:
    server.stop(0)
