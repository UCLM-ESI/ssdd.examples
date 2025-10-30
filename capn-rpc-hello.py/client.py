#!/usr/bin/env -S python3 -u

import asyncio
import sys
import socket
import time

import capnp
import upper_capnp


async def main(host, port):
    connection = await capnp.AsyncIoStream.create_connection(
        host=host, port=port)

    client = capnp.TwoPartyClient(connection)
    text_processor = client.bootstrap().cast_as(upper_capnp.TextProcessor)

    reply = await text_processor.upper(message="hello, world!")
    print("Server reply:", reply.result)


def wait_server_ready(host, port):
    while socket.socket().connect_ex((host, port)) != 0:
        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(f"Usage: {sys.argv[0]} <host> <port>")

    host, port = (sys.argv[1], int(sys.argv[2]))
    wait_server_ready(host, port)
    print(f"- Client connecting to {host}:{port}")
    asyncio.run(capnp.run(main(host, port)))
