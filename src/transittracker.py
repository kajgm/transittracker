import sys
import os
import argparse
import logging
from api import *
from display import *
from commandLine import *

# translink api has a limit of 1000 requests per day
# see https://www.translink.ca/about-us/doing-business-with-translink/app-developer-resources/rtti
TL_WAIT_TIME = 90  # time in seconds
DEFAULT_TL_STOP = 53656
DEFAULT_TA_STOP = "TSL:75044"
DEFAULT_TA_ROUTE = "TSL:1893"
DEFAULT_TA_NAME = "Pitt River Rd / Mary Hill Rd Westbound"
DEFAULT_TA_HEADSIGN = "Coquitlam Central Station"


def main(args):
    enable_display = args.display or args.fullscreen
    fullscreen = args.fullscreen
    TL_stop = args.stop or DEFAULT_TL_STOP

    trnstApi = transitApi(
        TL_stop, DEFAULT_TA_STOP, DEFAULT_TA_ROUTE, DEFAULT_TA_NAME, DEFAULT_TA_HEADSIGN
    )

    if enable_display:
        dsp = display(trnstApi, fullscreen, TL_WAIT_TIME)
        dsp.start()
    else:
        cmdln = commandLine(trnstApi, TL_WAIT_TIME)
        cmdln.start()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="transittracker.log", filemode="w")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--display", required=False, default=False, action="store_true"
    )
    parser.add_argument(
        "-f", "--fullscreen", required=False, default=False, action="store_true"
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
