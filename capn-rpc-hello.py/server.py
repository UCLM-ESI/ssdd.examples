#!/usr/bin/env -S python3 -u

import asyncio
import sys

import capnp
import upper_capnp


class TextProcessorI(upper_capnp.TextProcessor.Server):
    async def upper(self, message, _context):
        print("Client sent:", message)
        return message.upper()


async def new_connection(stream):
    await capnp.TwoPartyServer(stream, bootstrap=TextProcessorI()).on_disconnect()


async def main(port):
    server = await capnp.AsyncIoStream.create_server(
        new_connection, '0.0.0.0', port)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} [port]")

    port = int(sys.argv[1])
    print(f"- Server listening on port {port}")
    asyncio.run(capnp.run(main(port)))
