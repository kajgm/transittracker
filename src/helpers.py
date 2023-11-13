import sys
import time

WAIT_TIME = 45  # time in seconds


def check_response_status(res, printflag):
    if res == None or res.status_code != 200:
        if printflag:
            print("Error: Response Returned " + str(res.status_code))
        return False
    else:
        if printflag:
            print("Request returned " + str(res.status_code))
        return True


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
