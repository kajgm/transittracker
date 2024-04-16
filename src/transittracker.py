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


def transittracker(args):
    enable_display = args.display or args.window
    windowed = args.window
    TL_stop = args.stop or DEFAULT_TL_STOP

    trnstApi = transitApi(
        TL_stop, DEFAULT_TA_STOP, DEFAULT_TA_ROUTE, DEFAULT_TA_NAME, DEFAULT_TA_HEADSIGN
    )

    if enable_display:
        dsp = display(trnstApi, windowed, TL_WAIT_TIME)
        dsp.start()
    else:
        cmdln = commandLine(trnstApi, TL_WAIT_TIME)
        cmdln.start()
