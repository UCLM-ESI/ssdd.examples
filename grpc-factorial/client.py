#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# This example is based on https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld

import sys

import grpc
import math_pb2
import math_pb2_grpc


if len(sys.argv) != 3:
    print("usage: ./client <host> <value>")
    sys.exit(1)

server = sys.argv[1]
value = int(sys.argv[2])

channel = grpc.insecure_channel('{}:2000'.format(server))
stub = math_pb2_grpc.MathStub(channel)
response = stub.factorial(math_pb2.FactorialRequest(value=value))
print("result = '{}'".format(response.result))
