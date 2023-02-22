import sys
import os
import argparse
from api import *

SOUND_FLAG = True


def main(args):
    '''
    tApi = transitApi()
    sound_flag = args.sound
    if args.sound == None:
        sound_flag = SOUND_FLAG
    '''

    tApi = transitApi()

    res = tApi.get_stop_info()
    resJson = res.json()[0]

    for schedule in resJson['Schedules']:
        print(schedule['ExpectedLeaveTime'])
        print(schedule['ExpectedCountdown'])
        print(schedule['ScheduleStatus'])
        print(schedule['LastUpdate'])
        print('')


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sound", required=False)
    args = parser.parse_args()

    try:
        main(args)
    except KeyboardInterrupt:
        print('\nExiting')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(1)
