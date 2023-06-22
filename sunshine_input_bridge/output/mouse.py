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
            ecodes.EV_REL: (
                ecodes.REL_X,
                ecodes.REL_Y,
                ecodes.REL_HWHEEL,
                ecodes.REL_WHEEL,
                ecodes.REL_WHEEL_HI_RES,
                ecodes.REL_HWHEEL_HI_RES,
            ),
            ecodes.EV_KEY: (
                ecodes.BTN_LEFT,
                ecodes.BTN_MIDDLE,
                ecodes.BTN_RIGHT,
                ecodes.BTN_SIDE,
                ecodes.BTN_EXTRA,
                ecodes.BTN_FORWARD,
                ecodes.BTN_BACK,
                ecodes.BTN_TASK,
                *range(280, 288),
            ),
            ecodes.EV_MSC: (ecodes.MSC_SCAN,),
        }

    def close(self):
        VirtualDevice.close(self)
        VirtualMouse._init_cnt -= 1
