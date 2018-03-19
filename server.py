#!/usr/bin/env python3
"""socket-chai-chat server — broadcast TCP chat (CN lab 2018)."""

from __future__ import print_function
import socket
import threading
import sys

HOST = "0.0.0.0"
PORT = 5050
clients = []
lock = threading.Lock()


def broadcast(msg, skip=None):
 with lock:
 dead = []
 for c in clients:
 if c is skip:
 continue
 try:
 c.sendall(msg)
 except Exception:
 dead.append(c)
 for c in dead:
 clients.remove(c)


def handle(conn, addr):
 print("joined:", addr)
 try:
 conn.sendall(b"welcome to socket-chai-chat. type something.\n")
 while True:
 data = conn.recv(1024)
 if not data:
 break
 line = b"[%s:%d] %s" % (addr[0].encode(), addr[1], data)
 sys.stdout.write(line.decode("utf-8", "replace"))
 sys.stdout.flush()
 broadcast(line, skip=conn)
 finally:
 with lock:
 if conn in clients:
 clients.remove(conn)
 conn.close()
 print("left:", addr)


def main():
 s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 s.bind((HOST, PORT))
 s.listen(5)
 print("chai chat listening on %d" % PORT)
 try:
 while True:
 conn, addr = s.accept()
 with lock:
 clients.append(conn)
 threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
 except KeyboardInterrupt:
 print("\nserver stopping")
 finally:
 s.close()


if __name__ == "__main__":
 main()
