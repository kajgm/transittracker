import sys
import os
import argparse
from api import *
from display import *
from commandLine import *

WAIT_TIME = 45  # time in seconds
DEFAULT_STOP = 53656


def main(args):
    enable_display = args.display
    set_stop = args.stop or DEFAULT_STOP

    trnstApi = transitApi(set_stop)

    if enable_display:
        dsp = display(trnstApi, WAIT_TIME)
        dsp.start()
    else:
        cmdln = commandLine(trnstApi, WAIT_TIME)
        cmdln.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--display", required=False, default=False, action="store_true"
    )
    parser.add_argument("-s", "--stop", required=False)
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\nExiting")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(1)
