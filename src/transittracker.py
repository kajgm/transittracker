import sys
import os
import argparse
from api import *
from helpers import *
from display import *
from commandLine import *


def main(args):
    trnstApi = transitApi()

    enable_display = True  # args.display

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
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print("\nExiting")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(1)
