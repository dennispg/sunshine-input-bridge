from .output import VirtualDevice, VirtualGamepad, VirtualKeyboard, VirtualMouse
from .settings import Settings
from .utils import log


class OutputDevices:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.outputs: dict[str, VirtualDevice] = {}

    def open(self):
        for key, output in self.settings.outputs.items():
            log.info(f"Created device '{output.name}.")
            if output.type == "keyboard":
                device = VirtualKeyboard(output)
            elif output.type == "mouse":
                device = VirtualMouse(output)
            elif output.type == "gamepad":
                device = VirtualGamepad(output)
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
