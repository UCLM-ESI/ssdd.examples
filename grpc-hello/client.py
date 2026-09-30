#!/usr/bin/env python3
# This example is based on https://github.com/grpc/grpc/tree/v1.6.x/examples/python/helloworld

import sys
import grpc
import hello_pb2
import hello_pb2_grpc


if len(sys.argv) != 3:
    print("usage: ./client.py <host> <port>")
    sys.exit(1)

server = sys.argv[1]
port = sys.argv[2]
channel = grpc.insecure_channel(f'{server}:{port}')
stub = hello_pb2_grpc.HelloStub(channel)
message = hello_pb2.PrintRequest(message='hello')
stub.write(message)
