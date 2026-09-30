#!/usr/bin/env python3

import sys

import grpc
import math_pb2
import math_pb2_grpc


if len(sys.argv) != 3:
    print("usage: ./client <server> <value>")
    sys.exit(1)

server = sys.argv[1]
limit = int(sys.argv[2])

channel = grpc.insecure_channel('{}:2000'.format(server))
stub = math_pb2_grpc.MathStub(channel)


def numbers(values):
    for value in values:
        yield math_pb2.Number(value=value)


print("server streaming:")
for reply in stub.factorials(math_pb2.Limit(value=limit)):
    print("  ", reply.value)

print("client streaming:")
reply = stub.sum(numbers(range(1, limit + 1)))
print("  ", reply.value)

print("bidirectional streaming:")
for reply in stub.factorial_each(numbers(range(1, limit + 1))):
    print("  ", reply.value)
