#!/usr/bin/env python3
# JSON-RPC 2.0 client over HTTP, with jsonrpclib (python3-jsonrpclib-pelix)

import sys

import jsonrpclib


if len(sys.argv) != 3:
    print("usage: ./client.py <server> <value>")
    sys.exit(1)

server = jsonrpclib.ServerProxy("http://{}:2000".format(sys.argv[1]))
value = int(sys.argv[2])

print("factorial({}) = {}".format(value, server.factorial(value)))

# A notification: no "id", and no response
server._notify.log("computed factorial({})".format(value))

# A batch: several requests in a single message
batch = jsonrpclib.MultiCall(server)
batch.factorial(value + 1)
batch.factorial(value + 2)
print("batch:", list(batch()))
