from __future__ import annotations

from typing import TYPE_CHECKING
from urllib.parse import quote

from . import requests_unixsocket

if TYPE_CHECKING:
    from .settings import Settings


class CommandClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.session = requests_unixsocket.Session()

    def _get(self, path: str):
        request_path = (
            f"http+unix://{quote(self.settings.health_socket, safe='')}{path}"
        )
        return self.session.get(request_path)

    def is_healthy(self):
        try:
            response = self._get("/health")
            status = response.status_code == 200
            return status
        except requests_unixsocket.requests.exceptions.ConnectionError:
            return False
