#!/usr/bin/env python3
"""packet-chai client — connect and chat."""
from __future__ import annotations

import argparse
import select
import socket
import sys


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=5050)
    args = p.parse_args()

    sock = socket.create_connection((args.host, args.port))
    sock.setblocking(False)
    print(f"connected to {args.host}:{args.port}  (type /quit to leave)")
    try:
        while True:
            r, _, _ = select.select([sock, sys.stdin], [], [])
            if sock in r:
                data = sock.recv(4096)
                if not data:
                    print("server closed")
                    break
                sys.stdout.write(data.decode("utf-8", errors="replace"))
                sys.stdout.flush()
            if sys.stdin in r:
                line = sys.stdin.readline()
                if not line:
                    break
                sock.sendall(line.encode("utf-8"))
                if line.strip() == "/quit":
                    break
    finally:
        sock.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
