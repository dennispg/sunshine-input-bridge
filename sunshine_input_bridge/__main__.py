import argparse
import asyncio
import signal

import yaml
from pidfile import PIDFile

from .settings import Settings
from .sunshine_input_bridge import SunshineInputBridge
from .utils import log


async def shutdown(
    signal, bridge: SunshineInputBridge, loop: asyncio.AbstractEventLoop
):
    log.info(f"Received exit signal {signal.name}...")
    bridge.stop()
    loop.stop()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        "-c",
        help="config file path",
        dest="configfile",
        default="config.yaml",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "--pidfile",
        "-pd",
        dest="pidfile",
        default="/tmp/sunshine_input_bridge.pid",
        help="pid file path",
    )
    args = parser.parse_args()
    settings = Settings.parse_obj(yaml.safe_load(args.configfile))

    loop = asyncio.get_event_loop()

    with PIDFile(args.pidfile):
        with SunshineInputBridge(settings, loop) as bridge:
            signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
            for s in signals:
                loop.add_signal_handler(
                    s, lambda s=s: asyncio.create_task(shutdown(s, bridge, loop))
                )
            try:
                bridge.start()
                loop.run_forever()
            finally:
                loop.stop()


if __name__ == "__main__":
    main()
