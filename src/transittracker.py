import sys
import os
import argparse
from api import *
from helpers import *
from format import *

# Flag for terminal only (False) or with display on Linux only (True)
DISPLAY_FLAG = False


def main(args):

    tApi = transitApi()

    while (1):

        res = tApi.get_stop_info()
        resJson = res.json()[0]
        closestSchedule = resJson['Schedules'][0]

        print_status(closestSchedule['ExpectedCountdown'],
                     closestSchedule['ExpectedLeaveTime'],
                     closestSchedule['ScheduleStatus'],
                     closestSchedule['LastUpdate'])

        wait(WAIT_TIME)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--display", required=False)
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print('\nExiting')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(1)
