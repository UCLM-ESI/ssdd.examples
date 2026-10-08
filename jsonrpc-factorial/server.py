#!/usr/bin/env python3
# JSON-RPC 2.0 server over HTTP, with jsonrpclib (python3-jsonrpclib-pelix)

from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer


def factorial(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")

    result = 1
    for i in range(2, n + 1):
        result *= i

    return result


def log(text):
    print("log:", text, flush=True)


server = SimpleJSONRPCServer(("", 2000), logRequests=False)
server.register_function(factorial)
server.register_function(log)

try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
