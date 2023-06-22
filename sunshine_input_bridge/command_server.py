from __future__ import annotations

import socketserver
import threading
from functools import partial
from http.server import BaseHTTPRequestHandler
from typing import TYPE_CHECKING, Any
from .utils import log

if TYPE_CHECKING:
    from .sunshine_input_bridge import SunshineInputBridge


class CommandServerHandler(BaseHTTPRequestHandler):
    def __init__(self, bridge: SunshineInputBridge, request, client_address, server):
        self.bridge = bridge
        super().__init__(request, client_address, server)

    def log_message(self, format: str, *args: Any) -> None:
        log.debug(format % args)

    def do_GET(self):
        if self.path == "/health":
            self.healthcheck()
        else:
            self.not_found()

    def healthcheck(self):
        if self.bridge.is_open:
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write("true".encode("utf8"))
        else:
            self.send_response(503)
            self.send_header("Content-type", "plain/text")
            self.end_headers()
            self.wfile.write("Service Unavailable".encode("utf8"))

    def not_found(self):
        self.send_response(404)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write("".encode("utf8"))


class UnixSocketHttpServer(socketserver.UnixStreamServer):
    def get_request(self):
        request, client_address = super(UnixSocketHttpServer, self).get_request()
        return (request, ["local", 0])


class CommandServer:
    def __init__(self, sock, bridge):
        self.bridge = bridge
        self.sock = sock
        self.server_thread = None
        self.server = None

    def _run(self):
        handler = partial(CommandServerHandler, self.bridge)
        self.server = UnixSocketHttpServer((self.sock), handler)
        self.server.serve_forever()

    def start(self):
        if self.server_thread is not None or self.server is not None:
            self.stop()

        self.server_thread = threading.Thread(target=self._run, name="CommandServer")
        self.server_thread.daemon = False
        self.server_thread.start()

    def stop(self):
        if self.server is not None:
            self.server.shutdown()
            self.server = None

        if self.server_thread is not None:
            self.server_thread.join(timeout=10)
            self.server_thread = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
