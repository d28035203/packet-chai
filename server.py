#!/usr/bin/env python3
"""packet-chai server — multi-client TCP chat broadcaster."""
from __future__ import annotations

import argparse
import socket
import threading
from typing import List, Tuple

clients: List[Tuple[socket.socket, str]] = []
lock = threading.Lock()


def broadcast(msg: str, skip: socket.socket | None = None) -> None:
    data = (msg + "\n").encode("utf-8", errors="replace")
    with lock:
        dead = []
        for conn, name in clients:
            if conn is skip:
                continue
            try:
                conn.sendall(data)
            except OSError:
                dead.append((conn, name))
        for item in dead:
            clients.remove(item)
            try:
                item[0].close()
            except OSError:
                pass


def handle(conn: socket.socket, addr) -> None:
    name = f"{addr[0]}:{addr[1]}"
    with lock:
        clients.append((conn, name))
    broadcast(f"* {name} joined")
    try:
        f = conn.makefile("r", encoding="utf-8", errors="replace")
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            if line == "/quit":
                break
            broadcast(f"{name}: {line}", skip=conn)
    finally:
        with lock:
            clients[:] = [(c, n) for c, n in clients if c is not conn]
        try:
            conn.close()
        except OSError:
            pass
        broadcast(f"* {name} left")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=5050)
    args = p.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((args.host, args.port))
    sock.listen(16)
    print(f"packet-chai listening on {args.host}:{args.port}")
    try:
        while True:
            conn, addr = sock.accept()
            threading.Thread(target=handle, args=(conn, addr), daemon=True).start()
    except KeyboardInterrupt:
        print("\nshutting down")
    finally:
        sock.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
