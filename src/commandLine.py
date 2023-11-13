from helpers import *
from format import *


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

    def __init__(self, tApi, wtime):
        self.trnstApi = tApi
        self.waitTime = wtime

    def start(self):
        while 1:
            res = self.trnstApi.get_stop_info()
            valid_status = check_response_status(res, False)

            if valid_status and len(res.json()) > 0:
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

            wait(WAIT_TIME)
