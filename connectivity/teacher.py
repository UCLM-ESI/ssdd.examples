#!/usr/bin/env python3

import sys
import time
import os
from threading import Thread

from tools import TCPServer, UDPServer, TCPChecker, UDPChecker


if __name__ == '__main__':
    TCPServer(4000).start()
    UDPServer(4000).start()
    TCPChecker(4001).start()
    UDPChecker(4001).start()
