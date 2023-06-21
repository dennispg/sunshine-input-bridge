from abc import ABC, abstractmethod
from evdev import UInput


class VirtualDevice(ABC):
    @abstractmethod
    def __init__(self):
        self.input_dev: UInput | None = None
        self.capabilities = None

        self.name: str
        self.vendor: int
        self.product: int
        self.version: int
        self.phys: str
        self.bustype: str
        self.input_props: list[int] | None = None

    def create(self):
        if not self.is_open():
            self.input_dev = UInput(
                self.capabilities,
                self.name,
                vendor=self.vendor,
                product=self.product,
                version=self.version,
                phys=self.phys,
                input_props=self.input_props,
            )
        return self

    def write(self, e_type=None, e_sub_type=0, value=None):
        if self.input_dev is None:
            raise RuntimeError("Device has not been created yet.")
        self.input_dev.write(e_type, int(e_sub_type), value)

    def syn(self):
        if self.input_dev is None:
            raise RuntimeError("Device has not been created yet.")
        self.input_dev.syn()
        return self

    def is_open(self) -> bool:
        return self.input_dev is not None

    def close(self):
        if self.input_dev is not None:
            self.input_dev.close()
            self.input_dev = None
