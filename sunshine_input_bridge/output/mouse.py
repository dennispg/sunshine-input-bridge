# type: ignore

from evdev import AbsInfo

from ..settings import OutputSetting
from ..utils import ecodes
from .base import VirtualDevice


class VirtualMouse(VirtualDevice):
    _init_cnt = 0

    def __init__(self, settings: OutputSetting):
        VirtualDevice.__init__(self)
        self.name = settings.name or "virtual-mouse"
        self.vendor = settings.vendor or 0xBEEF
        self.product = settings.product or 0xDEAD
        self.version = settings.version or 273
        self.phys = settings.phys or (
            "joydrv/virtmouse" + VirtualMouse._init_cnt.__str__()
        )
        self.bustype = settings.bustype or "BUS_USB"
        self.input_props = [1]

        VirtualMouse._init_cnt += 1

        self.capabilities = {
            ecodes.EV_ABS: [
                (
                    ecodes.ABS_X,
                    AbsInfo(value=0, min=0, max=19200, fuzz=1, flat=0, resolution=28),
                ),
                (
                    ecodes.ABS_Y,
                    AbsInfo(value=0, min=0, max=12000, fuzz=1, flat=0, resolution=28),
                ),
            ],
            ecodes.EV_REL: (ecodes.REL_X, ecodes.REL_Y),
            ecodes.EV_KEY: (
                ecodes.BTN_LEFT,
                ecodes.BTN_MIDDLE,
                ecodes.BTN_RIGHT,
                ecodes.BTN_TOOL_PEN,
                ecodes.BTN_TOOL_FINGER,
                ecodes.BTN_TOUCH,
            ),
        }

    def close(self):
        VirtualDevice.close(self)
        VirtualMouse._init_cnt -= 1
