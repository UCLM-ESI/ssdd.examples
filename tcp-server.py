#!/usr/bin/python3
# Copyright: See AUTHORS and COPYING
"Usage: {0} <port>"

import sys
import time
import os
from socketserver import StreamRequestHandler, ForkingTCPServer

ForkingTCPServer.allow_reuse_address = True


class Handler(StreamRequestHandler):
    def handle(self):
        data = os.read(self.rfile.fileno(), 512)
        request = data.decode().strip()
        print(request)
        reply = ('ok {}'.format(request)).encode()
        self.wfile.write(reply)


if len(sys.argv) != 2:
    print(__doc__.format(sys.argv[0]))
    sys.exit(1)

server = ForkingTCPServer(('', int(sys.argv[1])), Handler)
server.serve_forever()
