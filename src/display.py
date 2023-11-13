from tkinter import *
from tkinter import ttk
from tkinter import font


class display:
    root = None
    trnstApi = None
    waitTime = None
    waitCounter = 0

    dispFont = None

    waitText = None
    waitLabel = None

    contextText = None
    contextLabel = None

    timeText = None
    timeFont = None
    timeLabel = None

    statusText = None
    statusLabel = None

    lastUpdateText = None
    lastUpdateLabel = None

    def __init__(self, tApi, wTime):
        self.root = Tk()
        self.waitTime = wTime

        self.waitText = StringVar()
        self.contextText = StringVar()
        self.timeText = StringVar()
        self.statusText = StringVar()
        self.lastUpdateText = StringVar()

        self.dispFont = font.Font(family="Helvetica", size=20)
        self.timeFont = font.Font(family="Helvetica", size=50, weight="bold")

        self.setLabels()

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
            self.contextText.set(
                "Next bus leaves at "
                + closestSchedule["ExpectedLeaveTime"].split(" ")[0]
                + " in"
            )
            self.timeText.set(str(closestSchedule["ExpectedCountdown"]) + "min")
            self.setStatus(closestSchedule["ScheduleStatus"])
            self.scheduleText.set("Last updated at " + closestSchedule["LastUpdate"])
        elif len(res.json()) == 0:
            self.contextText.set("")
            self.timeText.set("N/A")
            self.scheduleText.set("No busses currently available")
        elif res != None and res.status_code and res.reason:
            self.contextText.set("")
            self.timeText.set("Error: " + str(res.status_code))
            self.scheduleText.set(res.reason)
        else:
            self.timeText.set("Error")

        self.wait()

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

    def setStatus(self, status):
        color = "white"
        text = ""

        match status:
            case "*":
                color = "white"
                text = "On time"
            case "-":
                color = "orange"
                text = "Delayed"
            case "+":
                color = "red"
                text = "Ahead of Schedule"

        self.statusText.set(text)
        self.statusLabel.config(foreground=color)

    def setLabels(self):
        self.waitLabel = ttk.Label(
            self.root,
            textvariable=self.waitText,
            font=self.dispFont,
            foreground="white",
            background="black",
        )
        self.contextLabel = ttk.Label(
            self.root,
            textvariable=self.contextText,
            font=self.dispFont,
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
        self.statusLabel = ttk.Label(
            self.root,
            textvariable=self.statusText,
            font=self.dispFont,
            foreground="white",
            background="black",
        )
        self.lastUpdateLabel = ttk.Label(
            self.root,
            textvariable=self.lastUpdateText,
            font=self.dispFont,
            foreground="white",
            background="black",
        )

        self.waitLabel.place(relx=0.5, rely=0, anchor=CENTER)
        self.contextLabel.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.timeLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.statusLabel.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.lastUpdateLabel.place(relx=0.5, rely=0.9, anchor=CENTER)
