# Packet Chai

Multi-client TCP chat: one server process broadcasts each line to every other connected client. Plain sockets, no encryption (lab tool, not a product).

## Run

```bash
# terminal 1
python3 server.py --port 5050

# terminal 2 / 3
python3 client.py --host 127.0.0.1 --port 5050
```

Type messages and press enter. `/quit` disconnects.

## Notes

- Default port `5050`
- Server is multithreaded (one thread per client)
- No auth, no TLS — keep it on localhost

## License

MIT
