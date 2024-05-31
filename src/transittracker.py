import sys
import os
import argparse
import logging
import json
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

dirname = os.path.dirname(__file__)
logpath = os.path.join(dirname, "../transittracker.log")


def main(args):
    enable_display = args.display or args.fullscreen
    fullscreen = args.fullscreen
    TL_stop = args.stop or DEFAULT_TL_STOP

    api_keys = get_credentials()
    if not api_keys:
        return

    trnstApi = transitApi(
        api_keys[0],
        api_keys[1],
        TL_stop,
        DEFAULT_TA_STOP,
        DEFAULT_TA_ROUTE,
        DEFAULT_TA_NAME,
        DEFAULT_TA_HEADSIGN,
    )

    if enable_display:
        dsp = display(trnstApi, fullscreen, TL_WAIT_TIME)
        dsp.start()
    else:
        cmdln = commandLine(trnstApi, TL_WAIT_TIME)
        cmdln.start()


def get_credentials():
    translink_api_key = ""
    transit_app_api_key = ""
    try:
        with open(credentialpath, "r") as json_file:
            api_json = json.load(json_file)
        translink_api_key = api_json["translink_api_key"]
        transit_app_api_key = api_json["transit_app_api_key"]
    except:
        print(
            "ERROR: credentials.json not found, please enter your translink api key followed by your transit app api key"
        )
        print("(leave blank if not applicable)")
        try:
            translink_api_key = input()
            transit_app_api_key = input()
        except:
            print("ERROR: credentials not provided as arguments")
            return None

    return [translink_api_key, transit_app_api_key]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename=logpath, filemode="w")

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
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(1)
