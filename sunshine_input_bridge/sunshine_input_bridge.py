import asyncio

import evdev

from .input_pipe import InputPipe
from .output_devices import OutputDevices
from .settings import InputMapping, Settings
from .source_devices import SourceDevices
from .utils import log


class SunshineInputBridge:
    def __init__(self, settings: Settings, loop: asyncio.AbstractEventLoop):
        self.settings = settings
        self.loop = loop
        self.outputs: OutputDevices | None = None
        self.sources: SourceDevices | None = None
        self.pipes: dict[InputMapping, InputPipe] = {}

    def start(self):
        self.outputs = OutputDevices(self.settings)
        self.outputs.open()

        self.sources = SourceDevices(self.settings)
        self.sources.open(self.loop)
        self.sources.add_callback("add", self.on_device_add)
        self.sources.add_callback("remove", self.on_device_remove)

    def stop(self):
        if self.outputs is not None:
            self.outputs.close()
            self.outputs = None

        if self.sources is not None:
            self.sources.close()
            self.sources = None

        for mapping, pipe in self.pipes.items():
            asyncio.ensure_future(pipe.close())

    def on_device_add(self, key, input_device: evdev.InputDevice):
        if self.outputs is None:
            return
        for mapping in self.settings.mappings:
            if mapping in self.pipes:
                continue
            if mapping.input == key:
                output_device = self.outputs[mapping.output]
                if output_device is not None:
                    self.pipes[mapping] = InputPipe(input_device, output_device)
                    log.info(
                        f"Opened a pipe between {mapping.input} and {mapping.output}."
                    )

    def on_device_remove(self, key, input_device: evdev.InputDevice):
        for mapping in self.settings.mappings:
            if mapping.input == key and mapping in self.pipes:
                pipe = self.pipes.pop(mapping, None)
                if pipe is not None:
                    asyncio.ensure_future(pipe.close())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
