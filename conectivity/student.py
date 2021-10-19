#!/usr/bin/python3
"Usage: {0} <server> <proof>"


import sys
import socket

from tools import (
    OK, FAIL, TCPServer, UDPServer,
    check_remote_tcp_server, check_remote_udp_server)


REMOTE_TCP_PORT = 2000
REMOTE_UDP_PORT = 2000
CHECKER_TCP_PORT = 2001
CHECKER_UDP_PORT = 2001
LOCAL_TCP_PORT = 3000
LOCAL_UDP_PORT = 3000
TIMEOUT = 3


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def check_local_tcp_server(server):
    s = socket.socket()
    s.settimeout(TIMEOUT)
    try:
        s.connect((server, CHECKER_TCP_PORT))
        endpoint = "{}:{}".format(get_local_ip(), LOCAL_TCP_PORT)
        s.sendall(endpoint.encode())
        data = s.recv(1024).decode()
        print(f"TCP checker reply: '{data}'")
        result, msg = data.split(':')
        if result == OK:
            return OK, ''
    except ConnectionError as e:
        print("TCP server error:", e)
        return FAIL, str(e)
    finally:
        s.close()

    return FAIL, msg


def check_local_udp_server(server):
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.settimeout(TIMEOUT)
    endpoint = "{}:{}".format(get_local_ip(), LOCAL_UDP_PORT)
    s.sendto(endpoint.encode(), (server, CHECKER_UDP_PORT))
    try:
        data, client = s.recvfrom(1024)
        data = data.decode()
        print(f"UDP checker reply: '{data}'")
        result, msg = data.split(':')
        if result == OK:
            return OK, ''
    except socket.timeout as e:
        print("UDP server timeout")
        return FAIL, str(e)
    finally:
        s.close()

    return FAIL, msg


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.format(sys.argv[0]))
        sys.exit(1)

    server = sys.argv[1]
    proof = sys.argv[2]

    servers = [TCPServer(LOCAL_TCP_PORT), UDPServer(LOCAL_UDP_PORT)]

    for s in servers:
        s.start()

    results = {
        "TCP remote server": check_remote_tcp_server(server, REMOTE_TCP_PORT, proof),
        "UDP remote server": check_remote_udp_server(server, REMOTE_UDP_PORT, proof),
        "TCP local server ": check_local_tcp_server(server),
        "UDP local server ": check_local_udp_server(server)
    }

    print()
    for test, value in results.items():
        print("- {}: {}".format(test, value[0]))

    for s in servers:
        s.shutdown()
