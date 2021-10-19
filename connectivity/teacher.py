#!/usr/bin/env python3

import sys
import time
import os
from threading import Thread

from tools import TCPServer, UDPServer, TCPChecker, UDPChecker


if __name__ == '__main__':
    TCPServer(2000).start()
    UDPServer(2000).start()
    TCPChecker(2001).start()
    UDPChecker(2001).start()
