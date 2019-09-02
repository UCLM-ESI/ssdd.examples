#!/usr/bin/python3
# -*- coding:utf-8; mode:python -*-
# This example is based on https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld

import sys
import grpc
import hello_pb2
import hello_pb2_grpc


if len(sys.argv) != 2:
    print("usage: ./client.py <host>")
    sys.exit(1)

server = sys.argv[1]
channel = grpc.insecure_channel('{}:2000'.format(server))
stub = hello_pb2_grpc.HelloStub(channel)
message = hello_pb2.PrintRequest(message='felix')
stub.write(message)
