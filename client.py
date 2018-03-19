#!/usr/bin/env python3
"""socket-chai-chat client."""

from __future__ import print_function
import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 5050


def recv_loop(sock):
 while True:
 data = sock.recv(1024)
 if not data:
 print("\n[disconnected]")
 os_exit()
 break
 sys.stdout.write(data.decode("utf-8", "replace"))
 sys.stdout.flush()


def os_exit():
 try:
 sys.exit(0)
 except SystemExit:
 pass


def main():
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 sock.connect((HOST, PORT))
 threading.Thread(target=recv_loop, args=(sock,), daemon=True).start()
 try:
 while True:
 line = sys.stdin.readline()
 if not line:
 break
 sock.sendall(line.encode("utf-8"))
 except KeyboardInterrupt:
 pass
 finally:
 sock.close()


if __name__ == "__main__":
 main()
