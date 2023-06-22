from evdev import AbsInfo

from ..settings import OutputSetting
from ..utils import ecodes
from .base import VirtualDevice


class VirtualTouchscreen(VirtualDevice):
    _init_cnt = 0

    def __init__(self, settings: OutputSetting):
        VirtualDevice.__init__(self)
        self.name = settings.name or "virtual-touchscreen"
        self.vendor = settings.vendor or 0x46D
        self.product = settings.product or 0x4038
        self.version = settings.version or 0x111
        self.phys = settings.phys or (
            "joydrv/virttouch" + VirtualTouchscreen._init_cnt.__str__()
        )
        self.bustype = settings.bustype or "BUS_USB"
        self.input_props = [1]

        VirtualTouchscreen._init_cnt += 1

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
            ecodes.EV_KEY: (
                ecodes.BTN_TOOL_PEN,
                ecodes.BTN_TOOL_FINGER,
                ecodes.BTN_TOUCH,
            ),
        }

    def close(self):
        VirtualDevice.close(self)
        VirtualTouchscreen._init_cnt -= 1
