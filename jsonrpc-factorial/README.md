# JSON-RPC 2.0 factorial

A JSON-RPC 2.0 server and client over HTTP: no IDL, no interface compiler, no
stubs. The specification is at https://www.jsonrpc.org/specification

Both use jsonrpclib, whose API follows `xmlrpc.server` and `xmlrpc.client`
from the standard library. Each message goes in the body of an HTTP POST
request, always to the same URL: HTTP is only the transport, as in gRPC.


Depends
-------

Debian package:

- python3-jsonrpclib-pelix


Run server
----------

    $ ./server.py

It offers two methods, `factorial` and `log`, which prints a text on the
server's console.


Run client
----------

    $ ./client.py localhost 5
    factorial(5) = 120
    batch: [720, 5040]

The server prints `log: computed factorial(5)`: that call was a notification,
and the client got no response for it. The batch sends two requests in a
single message.


Run with curl
-------------

Messages are plain text, so any HTTP client can make the calls:

    $ curl localhost:2000 \
      -d '{"jsonrpc": "2.0", "method": "factorial", "params": [5], "id": 1}'
    {"result": 120, "id": 1, "jsonrpc": "2.0"}
    $ curl localhost:2000 \
      -d '{"jsonrpc": "2.0", "method": "factorial", "params": {"n": 20}, "id": 2}'
    {"result": 2432902008176640000, "id": 2, "jsonrpc": "2.0"}
    $ curl localhost:2000 \
      -d '{"jsonrpc": "2.0", "method": "log", "params": ["hello"]}'
    $ curl localhost:2000 -d '[
      {"jsonrpc": "2.0", "method": "factorial", "params": [3], "id": 3},
      {"jsonrpc": "2.0", "method": "power", "params": [2, 8], "id": 4}]'
    [{"result": 6, "id": 3, "jsonrpc": "2.0"},
     {"id": 4, "jsonrpc": "2.0",
      "error": {"code": -32601, "message": "Method power not supported."}}]

- named parameters (`{"n": 20}`) as well as positional ones (`[5]`);
- a request without `id` is a notification: the server runs it and does not
  reply, not even with an error;
- an array is a batch: one response array, without the notifications.


Demo
----

    $ ./demo.sh    # requires tmux
