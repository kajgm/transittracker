import sys
import time
from format import *


def getScheduleLabel(scheduleSymbol):
    label = "On time"

    match scheduleSymbol:
        case "*":
            label = "On time"
        case "-":
            label = "Late"
        case "+":
            label = "Ahead of schedule"

    return label


def wait(sec):
    # output the . -> .. -> ... waiting loop animation
    for j in range(sec):
        print(".", end="")
        sys.stdout.flush()
        time.sleep(1)
    # clear the terminal line
    print("\r", end="")
    print("                                                   ", end="\r")
    time.sleep(1)


class commandLine:
    trnstApi = None
    waitTime = None

    def __init__(self, tApi, wTime):
        self.trnstApi = tApi
        self.waitTime = wTime

    def start(self):
        while 1:
            res = self.trnstApi.get_stop_info()

            if len(res.json()) > 0 and res.status_code == 200:
                resJson = res.json()[0]
                closestSchedule = resJson["Schedules"][0]

                print_status(
                    closestSchedule["ExpectedCountdown"],
                    closestSchedule["ExpectedLeaveTime"],
                    closestSchedule["ScheduleStatus"],
                    closestSchedule["LastUpdate"],
                )
            elif len(res.json()) == 0:
                self.contextText.set("")
                self.timeText.set("No busses currently available")
                self.scheduleText.set("")
            elif res != None and res.status_code and res.reason:
                print_error(res)
            else:
                print("Error\n")

            wait(self.waitTime)
