from __future__ import annotations

from .output import (
    VirtualDevice,
    VirtualGamepad,
    VirtualKeyboard,
    VirtualMouse,
    VirtualTouchscreen,
)
from .settings import OutputDeviceType, Settings
from .utils import log


class OutputDevices:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.outputs: dict[str, VirtualDevice] = {}

    def open(self):
        for key, output in self.settings.outputs.items():
            log.info(f"Created device '{output.name}.")
            if output.type == OutputDeviceType.keyboard:
                device = VirtualKeyboard(output)
            elif output.type == OutputDeviceType.mouse:
                device = VirtualMouse(output)
            elif output.type == OutputDeviceType.gamepad:
                device = VirtualGamepad(output)
            elif output.type == OutputDeviceType.touchscreen:
                device = VirtualTouchscreen(output)
            else:
                raise ValueError(f"Unknown output device type: {output.type}")
            device.create()
            self.outputs[key] = device

    def close(self):
        for _, device in self.outputs.items():
            log.info(f"Closed device '{device.name}.")
            device.close()
        self.outputs = {}

    def __getitem__(self, key: str):
        return self.outputs.get(key, None)
