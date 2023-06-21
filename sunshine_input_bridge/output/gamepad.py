# type: ignore

from evdev import AbsInfo

from ..settings import OutputSetting
from ..utils import ecodes
from .base import VirtualDevice


class VirtualGamepad(VirtualDevice):
    _init_cnt = 0

    def __init__(self, settings: OutputSetting):
        VirtualDevice.__init__(self)
        self.name = settings.name or "virtual-gamepad"
        self.vendor = settings.vendor or 0x45E
        self.product = settings.product or 0x28E
        self.version = settings.version or 272
        self.phys = settings.phys or (
            "joydrv/virtpad" + VirtualGamepad._init_cnt.__str__()
        )
        self.bustype = settings.bustype or "BUS_USB"

        VirtualGamepad._init_cnt += 1

        self.capabilities = {
            ecodes.EV_KEY: [
                ecodes.BTN_A,
                ecodes.BTN_B,
                ecodes.BTN_X,
                ecodes.BTN_Y,
                ecodes.BTN_TL,
                ecodes.BTN_TR,
                ecodes.BTN_TL2,
                ecodes.BTN_TR2,
                ecodes.BTN_SELECT,
                ecodes.BTN_START,
                ecodes.BTN_THUMBL,
                ecodes.BTN_THUMBR,
                ecodes.BTN_DPAD_UP,
                ecodes.BTN_DPAD_DOWN,
                ecodes.BTN_DPAD_LEFT,
                ecodes.BTN_DPAD_RIGHT,
                ecodes.BTN_MODE,
                ecodes.BTN_SOUTH,
                ecodes.BTN_EAST,
                ecodes.BTN_NORTH,
                ecodes.BTN_WEST,
            ],
            ecodes.EV_ABS: [
                (
                    ecodes.ABS_HAT0X,
                    AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0),
                ),
                (
                    ecodes.ABS_HAT0Y,
                    AbsInfo(value=0, min=-1, max=1, fuzz=0, flat=0, resolution=0),
                ),
                (
                    ecodes.ABS_X,
                    AbsInfo(
                        value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0
                    ),
                ),
                (
                    ecodes.ABS_Y,
                    AbsInfo(
                        value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0
                    ),
                ),
                (
                    ecodes.ABS_Z,
                    AbsInfo(value=0, min=0, max=0, fuzz=0, flat=0, resolution=0),
                ),
                (
                    ecodes.ABS_RX,
                    AbsInfo(
                        value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0
                    ),
                ),
                (
                    ecodes.ABS_RY,
                    AbsInfo(
                        value=0, min=-32768, max=32767, fuzz=16, flat=128, resolution=0
                    ),
                ),
            ],
            ecodes.EV_FF: [
                ecodes.FF_RUMBLE,
                ecodes.FF_PERIODIC,
                ecodes.FF_CONSTANT,
                ecodes.FF_RAMP,
                ecodes.FF_SINE,
                ecodes.FF_GAIN,
            ],
        }

    def close(self):
        VirtualDevice.close(self)
        VirtualGamepad._init_cnt -= 1
