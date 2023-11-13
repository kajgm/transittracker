from tkinter import *
from tkinter import ttk
from tkinter import font
from helpers import *


class display:
    root = None
    trnstApi = None
    waitTime = None
    waitCounter = 0

    waitText = None
    waitFont = None
    waitLable = None

    contextText = None
    contextFont = None
    contextLabel = None

    timeText = None
    timeFont = None
    timeLabel = None

    scheduleText = None
    scheduleFont = None
    scheduleLabel = None

    def __init__(self, tApi, wTime):
        self.root = Tk()
        self.waitTime = wTime

        self.waitText = StringVar()
        self.contextText = StringVar()
        self.timeText = StringVar()
        self.scheduleText = StringVar()

        self.waitFont = font.Font(family="Helvetica", size=20)
        self.contextFont = font.Font(family="Helvetica", size=20)
        self.timeFont = font.Font(family="Helvetica", size=50, weight="bold")
        self.scheduleFont = font.Font(family="Helvetica", size=20)

        self.waitLabel = ttk.Label(
            self.root,
            textvariable=self.waitText,
            font=self.waitFont,
            foreground="white",
            background="black",
        )
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

        self.waitLabel.place(relx=0.5, rely=0, anchor=CENTER)
        self.contextLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.timeLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.scheduleLabel.place(relx=0.5, rely=0.8, anchor=CENTER)

        self.trnstApi = tApi

    def start(self):
        self.root.attributes("-fullscreen", True)
        self.root.config(background="black", cursor="none")
        self.root.bind("x", quit)
        self.root.after(1000, self.show_time)

        self.root.mainloop()

    def quit(self, *args):
        self.root.destroy()

    def show_time(self):
        res = self.trnstApi.get_stop_info()

        if res.status_code == 200 and len(res.json()) > 0:
            resJson = res.json()[0]
            closestSchedule = resJson["Schedules"][0]

            self.setColors(closestSchedule["ScheduleStatus"])

            self.contextText.set(
                "Next bus leaves at "
                + closestSchedule["ExpectedLeaveTime"].split(" ")[0]
                + "in"
            )
            self.timeText.set(str(closestSchedule["ExpectedCountdown"]) + "min")
            self.scheduleText.set("Last updated at " + closestSchedule["LastUpdate"])
        elif len(res.json()) == 0:
            self.contextText.set("")
            self.timeText.set("N/A")
            self.scheduleText.set("No busses currently available")
        elif res != None and res.status_code and res.reason:
            self.contextText.set("")
            self.timeText.set("Error: " + str(res.status_code))
            self.scheduleText.set(res.reason)

        self.wait()

    def setColors(self, status):
        color = "white"

        match status:
            case "*":
                color = "white"
            case "-":
                color = "orange"
            case "+":
                color = "red"

        self.timeLabel.config(foreground=color)

    def wait(self):
        if self.waitCounter < self.waitTime:
            self.waitCounter += 1
            dotString = ""

            for i in range(self.waitCounter):
                dotString += "."

            self.waitText.set(dotString)
            self.root.after(1000, self.wait)
        else:
            self.waitCounter = 0
            self.show_time()
