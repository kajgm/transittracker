from tkinter import *
from tkinter import ttk
from tkinter import font
from helpers import *


class display:
    root = None
    trnstApi = None
    waitTime = None

    contextText = None
    contextFont = None
    contextLabel = None

    timeText = None
    timeFont = None
    timeLabel = None

    scheduleText = None
    scheduleFont = None
    scheduleLabel = None

    def __init__(self, tApi, wtime):
        self.root = Tk()

        self.contextText = StringVar()
        self.timeText = StringVar()
        self.scheduleText = StringVar()

        self.contextFont = font.Font(family="Helvetica", size=20)
        self.timeFont = font.Font(family="Helvetica", size=50, weight="bold")
        self.scheduleFont = font.Font(family="Helvetica", size=20)

        self.contextLabel = ttk.Label(
            self.root,
            textvariable=self.contextText,
            font=self.contextFont,
            foreground="white",
            background="black",
        )
        self.timeLabel = ttk.Label(
            self.root,
            textvariable=self.timeText,
            font=self.timeFont,
            foreground="white",
            background="black",
        )
        self.scheduleLabel = ttk.Label(
            self.root,
            textvariable=self.scheduleText,
            font=self.scheduleFont,
            foreground="white",
            background="black",
        )

        self.contextLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.timeLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.scheduleLabel.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.trnstApi = tApi
        self.waitTime = wtime

    def quit(self, *args):
        self.root.destroy()

    def show_time(self):
        res = self.trnstApi.get_stop_info()
        valid_status = check_response_status(res, False)

        if valid_status:
            resJson = res.json()[0]
            closestSchedule = resJson["Schedules"][0]

            self.setColors(closestSchedule["ScheduleStatus"])

            self.contextText.set(
                "The next bus leaves in "
                + str(closestSchedule["ExpectedCountdown"])
                + "min at"
            )
            self.timeText.set(closestSchedule["ExpectedLeaveTime"].split(" ")[0])
            self.scheduleText.set(
                "["
                + getScheduleLabel(closestSchedule["ScheduleStatus"])
                + "] - Last updated at "
                + closestSchedule["LastUpdate"]
            )
        elif res != None and res.status_code and res.reason:
            self.contextText.set("")
            self.timeText.set("Error: " + str(res.status_code))
            self.scheduleText.set(res.reason)

        self.root.after(self.waitTime * 1000, self.show_time)

    def setColors(self, status):
        color = "white"

        match status:
            case "*":
                color = "white"
            case "-":
                color = "orange"
            case "+":
                color = "red"

        self.timeLabel.config(fg=color)

    def start(self):
        self.root.attributes("-fullscreen", True)
        self.root.config(background="black", cursor="none")
        self.root.bind("x", quit)
        self.root.after(1000, self.show_time)

        self.root.mainloop()
