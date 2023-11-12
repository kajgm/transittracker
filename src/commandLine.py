from helpers import *
from format import *


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

            if valid_status:
                resJson = res.json()[0]
                closestSchedule = resJson["Schedules"][0]

                print_status(
                    closestSchedule["ExpectedCountdown"],
                    closestSchedule["ExpectedLeaveTime"],
                    closestSchedule["ScheduleStatus"],
                    closestSchedule["LastUpdate"],
                )
            else:
                print_error(res)

            wait(WAIT_TIME)
