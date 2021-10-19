import os
import socket
from threading import Thread
from socketserver import (
    StreamRequestHandler, ForkingTCPServer,
    DatagramRequestHandler, ForkingUDPServer)

ForkingTCPServer.allow_reuse_address = True

OK = 'ok'
FAIL = 'FAIL'
TIMEOUT = 3


def check_remote_tcp_server(server, port, proof='proof'):
    s = socket.socket()
    s.settimeout(TIMEOUT)
    try:
        s.connect((server, port))
        s.sendall(proof.encode())
        data = s.recv(1024)
        print("TCP server reply:", data.decode())
    except socket.timeout as e:
        print("TCP server error:", e)
        return FAIL, str(e)
    except ConnectionError as e:
        print("TCP server error:", e)
        return FAIL, str(e)
    finally:
        s.close()

    return OK, ''


def check_remote_udp_server(server, port, proof='proof'):
    s = socket.socket(type=socket.SOCK_DGRAM)
    s.settimeout(TIMEOUT)
    s.sendto(proof.encode(), (server, port))
    try:
        data, addr = s.recvfrom(1024)
        print("UDP server reply:", data.decode())
    except socket.timeout as e:
        print("UDP server error:", e)
        return FAIL, str(e)
    finally:
        s.close()

    return OK, ''


class TCPHandler(StreamRequestHandler):
    def handle(self):
        data = os.read(self.rfile.fileno(), 512)
        data = data.decode().strip()
        print(f"TCP client '{data}'")
        reply = ('ok {}'.format(data)).encode()
        self.wfile.write(reply)
        self.wfile.flush()


class TCPServer(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        print("TCP server starts")
        self.server = ForkingTCPServer(('', self.port), TCPHandler)
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class UDPHandler(DatagramRequestHandler):
    def handle(self):
        data = self.rfile.read().decode()
        print(f"UDP client '{data}'")
        reply = ('ok {}'.format(data)).encode()
        self.wfile.write(reply)


class UDPServer(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        print("UDP server starts")
        self.server = ForkingUDPServer(('', self.port), UDPHandler)
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


class TCPChecker_handler(StreamRequestHandler):
    def handle(self):
        data = os.read(self.rfile.fileno(), 512)
        data = data.decode().strip()
        print("TCP checker remote endpoint:", {data})
        ip, port = data.split(':')

        result, msg = check_remote_tcp_server(ip, int(port), 'checker')

        reply = '{}:{}'.format(result, msg).encode()
        self.wfile.write(reply)
        self.wfile.flush()


class TCPChecker(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        print("TCP checker starts")
        server = ForkingTCPServer(('', self.port), TCPChecker_handler)
        server.serve_forever()


class UDPChecker_handler(DatagramRequestHandler):
    def handle(self):
        data = self.rfile.read().decode()
        print("UDP checker remote endpoint:", {data})
        ip, port = data.split(':')

        result, msg = check_remote_udp_server(ip, int(port), 'checker')

        reply = '{}:{}'.format(result, msg).encode()
        self.wfile.write(reply)


class UDPChecker(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        print("UDP checker starts")
        server = ForkingUDPServer(('', self.port), UDPChecker_handler)
        server.serve_forever()
