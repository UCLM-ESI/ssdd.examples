# Pico-RMI

A minimal illustration of the "distributed object" middleware style used by frameworks
such as ZeroC Ice or CORBA, built with the same struct/socket approach as
[`../pico-rpc`](../pico-rpc).

Unlike plain RPC, where a client always talks to the one implementation living on the
server, here the server can host several independent objects at once. Each one is
registered under an identity, and a client reaches a specific object by combining an
endpoint (host, port) with that identity.

## Terminology

Following ZeroC Ice:

- **Servant** -- an object implementing an interface (e.g. `CounterI`), by inheriting
  from a generated base class (`Counter`) that knows how to unmarshal a request and call
  the right method on itself.
- **Identity** -- the name a servant is registered under.
- **Object adapter** -- holds servants by identity and routes each incoming request to
  the one it names; it knows nothing about any particular interface, since dispatching
  a request is the servant's own job.
- **Proxy** -- client-side handle for one specific remote object (endpoint + identity).

## Files

- `picormi.py` -- pico-rmi runtime: IDL primitives, identity encoding, the Servant base
  class and the ObjectAdapter.
- `rmigen.py` -- interface compiler: idl -> client/server stubs.
- `counter.idl.py` -- interface definition of the Counter service.
- `server.py`, `client.py` -- programmer's code: `CounterI` inherits the generated
  `Counter` server stub and implements `increment`/`get`; two independent instances
  (`c1`, `c2`) are hosted by one adapter.

## Try it

```
$ make generate
$ ./server.py &
$ ./client.py localhost c1
$ ./client.py localhost c2
```

Note how `c1` and `c2` keep independent counts: they are two different remote objects,
not two calls to the same global implementation.
