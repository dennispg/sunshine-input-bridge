from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Callable, Literal

import evdev
import pyudev

from .utils import log

if TYPE_CHECKING:
    from .settings import Settings


class SourceDevices:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.context: pyudev.Context | None = None
        self.monitor: pyudev.Monitor | None = None
        self.sources: dict[str, evdev.InputDevice] = {}
        self._add_callbacks: list[Callable[[str, evdev.InputDevice], None]] = []
        self._remove_callbacks: list[Callable[[str, evdev.InputDevice], None]] = []

    def add_callback(
        self,
        type: Literal["add", "remove"],
        callback: Callable[[str, evdev.InputDevice], None],
    ):
        if type == "add":
            self._add_callbacks.append(callback)
        else:
            self._remove_callbacks.append(callback)

    async def add_device(self, device_node: str):
        try:
            await asyncio.sleep(0.1)
            device = evdev.InputDevice(device_node)
        except PermissionError:
            log.critical(f"Permission denied: Could not open device {device_node}")
            return None

        for key, input in self.settings.inputs.items():
            if (
                device.uniq == input.uniq
                or device.path == input.device_node
                or (
                    (input.name is None or device.name == input.name)
                    and (input.vendor is None or device.info.vendor == input.vendor)
                    and (input.product is None or device.info.product == input.product)
                )
            ):
                self.sources[key] = device
                log.info(f"Added source device [{key}] for {device_node}.")
                for callback in self._add_callbacks:
                    callback(key, device)
                return device
        device.close()

    def remove_device(self, device_node: str):
        found_key: str = ""
        for key, device in self.sources.items():
            if device.path == device_node:
                found_key = key
                break
        device = self.sources.pop(found_key, None)
        if device is not None:
            for callback in self._remove_callbacks:
                callback(found_key, device)
            device.close()
            log.info(f"Removed source device [{found_key}] from {device_node}.")

    def open(self, loop: asyncio.AbstractEventLoop):
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context, "kernel")
        self.monitor.filter_by("input")
        self.monitor.start()
        loop.add_reader(self.monitor.fileno(), self.handle_udev_event, self.monitor)

    def close(self):
        if self.monitor is not None:
            self.monitor = None
            self.context = None

        for key, source in self.sources.items():
            log.info(f"Closing source device [{key}]...")
            source.close()
        self.sources = {}

    def handle_udev_event(self, monitor: pyudev.Monitor):
        device = monitor.poll(0)
        if device is None or device.device_node is None:
            return
        if device.device_node.startswith("/dev/input/event"):
            if device.action == "add":
                asyncio.ensure_future(self.add_device(device.device_node))
            elif device.action == "remove":
                self.remove_device(device.device_node)
