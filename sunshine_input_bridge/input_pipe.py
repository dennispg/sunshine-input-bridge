import asyncio

import evdev

from .output import VirtualDevice
from .utils import ecodes


class InputPipe:
    def __init__(self, input_device: evdev.InputDevice, output_device: VirtualDevice):
        self.input_device = input_device
        self.output_device = output_device
        self.task = asyncio.ensure_future(self.process_events())

    async def process_events(self):
        with self.input_device.grab_context():
            async for event in self.input_device.async_read_loop():
                self.process_event(event)

    def process_event(self, event: evdev.InputEvent):
        if event.type == ecodes.EV_SYN:
            self.output_device.syn()
        else:
            self.output_device.write(event.type, event.code, event.value)

    async def close(self):
        if self.task.cancel():
            await self.task
