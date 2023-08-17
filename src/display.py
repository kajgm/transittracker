from tkinter import *
from tkinter import ttk
from tkinter import font
from helpers import *


class display:
    root = None
    txt = None
    fnt = None
    lbl = None
    tApi = None

    def __init__(self, api):
        self.root = Tk()
        self.txt = StringVar()
        self.fnt = font.Font(family="Helvetica", size=35, weight="bold")
        self.lbl = ttk.Label(
            self.root,
            textvariable=self.txt,
            font=self.fnt,
            foreground="white",
            background="black",
        )
        self.lbl.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.tApi = api

    def quit(self, *args):
        self.root.destroy()

    def show_time(self):
        res = self.tApi.get_stop_info()
        resJson = res.json()[0]
        closestSchedule = resJson["Schedules"][0]
        self.txt.set(closestSchedule["ExpectedLeaveTime"])
        self.root.after(40 * 1000, self.show_time)

    def show_display(self):
        self.root.attributes("-fullscreen", True)
        self.root.config(background="black", cursor="none")
        self.root.bind("x", quit)
        self.root.after(1000, self.show_time)

        self.root.mainloop()
