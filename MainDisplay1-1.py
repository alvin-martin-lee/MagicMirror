# -*- coding: utf-8 -*-

from tkinter import *
from datetime import date, datetime
from pytz import *
import time
import WeatherModule
import CalendarModule
import feedparser

defaultPad = 10

class MagicMirror(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(self, background='black')
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomeScreen, WeatherPage, NewsPage, WorldTimePage, SettingsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomeScreen")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class HomeScreen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='black')
        self.controller = controller

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.clockLabel = Label(self, text='', font=('Helvetica', 80), fg = 'white', bg = 'black')
        self.clockLabel.bind('<Button-1>', lambda x: self.controller.show_frame("WorldTimePage"))
        self.clockLabel.bind('<Button-3>', lambda x: self.controller.show_frame('SettingsPage'))
        self.clockLabel.grid(row=0, sticky=W, padx=5, pady=(defaultPad, 0))

        self.dateLabel = Label(self, text='', font=('Helvetica', 20), fg = 'white', bg = 'black')
        self.dateLabel.grid(row=1, sticky=NW, padx=(defaultPad+5, 0))

        self.weatIconImg = PhotoImage(file='WeatherIcons/unknown.pgm').subsample(15)
        self.weatIconLabel = Label(self, bg='black')
        self.weatIconLabel.image = self.weatIconImg
        self.weatIconLabel.bind('<Button-1>', lambda x: self.controller.show_frame("WeatherPage"))
        self.weatIconLabel.grid(row=0, column=1, sticky=E, padx=(0, defaultPad), pady=(defaultPad, 0))

        self.weatStatusLabel = Label(self, text='', font=('Helvetica', 20), fg = 'white', bg = 'black', wraplength=200)
        self.weatStatusLabel.bind('<Button-1>', lambda x: self.controller.show_frame("WeatherPage"))
        self.weatStatusLabel.grid(row=1, column=1, sticky=E, padx=(0, defaultPad))

        self.weatTempLabel = Label(self, text='', font=('Helvetica', 20), fg = 'white', bg = 'black', wraplength=200)
        self.weatTempLabel.bind('<Button-1>', lambda x: self.controller.show_frame("WeatherPage"))
        self.weatTempLabel.grid(row=2, column=1, sticky=NE, padx=(0, defaultPad))

        self.calLabel = Label(self, text='Calendar:', font=('Helvetica', 18, 'bold'), fg = 'white', bg = 'black')
        self.calLabel.grid(row=3, sticky=SW, padx=(defaultPad, 0))
        self.calEventList = Listbox(self, font=('Helvetica', 18), fg = 'white', bg = 'black', width=20, activestyle='none', borderwidth=0, highlightbackground='black', highlightcolor='white', highlightthickness=0, selectbackground='black', selectborderwidth=0, selectforeground='white')
        self.calEventList.grid(row=4, sticky=NW, padx=(defaultPad+10, 0))
        self.rowconfigure(4, minsize = 420)

        self.count = 0
        self.newsLabel = Label(self, text='', font=('Helvetica', 15), fg = 'white', bg = 'black', wraplength=400)
        self.newsLabel.bind('<Button-1>', lambda x: self.controller.show_frame("NewsPage"))
        self.newsLabel.grid(row=5, columnspan=2, sticky=S, padx=(defaultPad+10, 0))
        self.rssFeedCon = []

        self.updateClockDate()
        self.updateWeather()
        self.updateCalendar()
        self.updateFeed()
        self.displayNews()


    def updateClockDate(self):
        curTime = time.strftime('%H:%M')
        self.clockLabel.configure(text=curTime)
        curDate = date.today().strftime('%d %B %Y')
        self.dateLabel.configure(text=curDate)
        MagicMirror.after(self, 1000, lambda: self.updateClockDate())

    def updateWeather(self):
        curWeatStat, curTemp = WeatherModule.getCurWeatInfo()
        curIconPath = WeatherModule.getIcon(curWeatStat)
        self.weatStatusLabel.configure(text=curWeatStat)
        self.weatTempLabel.configure(text=curTemp)

        weatIconImg = PhotoImage(file=curIconPath).subsample(15)
        self.weatIconLabel.configure(image=weatIconImg)
        self.weatIconLabel.image = weatIconImg

        MagicMirror.after(self, 3600000, lambda: self.updateWeather())

    def updateCalendar(self):
        self.calEventList.delete(0,END)
        events = CalendarModule.getCalEvents()
        if not events:
            self.calEventList.insert(1,'No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            self.calEventList.insert(END, '%s/%s/%s'%(start[8:10], start[5:7], start[:4]))
            self.calEventList.insert(END, '- ' + event['summary'])
        MagicMirror.after(self, 3600000, lambda: self.updateWeather())

    def updateFeed(self):
        self.count = 0
        rss = 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'
        feed = feedparser.parse(rss)
        self.rssFeedCon = feed
        MagicMirror.after(self, 3600000, lambda: self.updateFeed())


    def displayNews(self):
        self.newsLabel.configure(text=self.rssFeedCon['entries'][self.count]['title'])
        if self.count < len(self.rssFeedCon['entries']):
            self.count += 1
        else:
            self.count = 0
        MagicMirror.after(self, 5000, lambda: self.displayNews())

class WeatherPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='black')
        self.controller = controller

        for i in range(4):
            self.columnconfigure(i, weight=1)

        self.backLabel = Label(self, text='X', font=('Helvetica', 50), fg = 'white', bg = 'black')
        self.backLabel.bind('<Button-1>', lambda x: self.controller.show_frame('HomeScreen'))
        self.backLabel.grid(row=0, sticky=W, padx=defaultPad, pady=defaultPad*2)

        self.titleLabel = Label(self, text='10 Day Forecast ', font=('Helvetica', 35), fg = 'white', bg = 'black')
        self.titleLabel.grid(row=0, column=1, sticky=W, columnspan=3, padx=defaultPad, pady=defaultPad)

        forecast = WeatherModule.getForecast()
        secRowStart = [1, 1, 4, 4, 7, 7, 10, 10, 13, 13]
        secColumnStart = [0, 2]

        for i in range(10):
            conImage = PhotoImage(file=WeatherModule.getIcon(forecast[i]['conditions'])).subsample(21)
            conImageLabel = Label(self, bg='black', image=conImage)
            conImageLabel.image = conImage
            conImageLabel.grid(row=secRowStart[i], column=secColumnStart[i%2], sticky=W, rowspan=3, padx=(5, 0), pady=defaultPad)

            day = Label(self, text='%s (%s/%s)'%(forecast[i]['date']['weekday_short'], forecast[i]['date']['day'], forecast[i]['date']['month']), font=('Helvetica', 12, 'bold'), fg = 'white', bg = 'black')
            day.grid(row=secRowStart[i], column=secColumnStart[i%2]+1, sticky=W)

            condition = Label(self, text=forecast[i]['conditions'], font=('Helvetica', 12), fg = 'white', bg = 'black')
            condition.grid(row=secRowStart[i]+1, column=secColumnStart[i%2]+1, sticky=W)

            highTemp = Label(self, text='H:%s°C L:%s°C'%(forecast[i]['high']['celsius'], forecast[i]['low']['celsius']), font=('Helvetica', 12), fg = 'white', bg = 'black')
            highTemp.grid(row=secRowStart[i]+2, column=secColumnStart[i%2]+1, sticky=W, pady=(0, defaultPad))

class NewsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='black')
        self.controller = controller

        self.backLabel = Label(self, text='X Headlines', font=('Helvetica', 50), fg = 'white', bg = 'black')
        self.backLabel.bind('<Button-1>', lambda x: self.controller.show_frame('HomeScreen'))
        self.backLabel.grid(row=0, sticky=W, padx=defaultPad, pady=defaultPad)

        rss = 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'
        feed = feedparser.parse(rss)

        for i in range(4):
            self.columnconfigure(i, weight=1)
            title = Label(self, text=feed['entries'][i]['title'], font=('Helvetica', 15, 'bold'), justify=LEFT, fg = 'white', bg = 'black', wraplength=460)
            title.grid(row=2*i+1, sticky=W, padx=defaultPad)
            description = Label(self, text=feed['entries'][i]['description'], font=('Helvetica', 15), justify=LEFT, fg = 'white', bg = 'black', wraplength=460)
            description.grid(row=2*i+2, sticky=W, padx=defaultPad, pady=(0, defaultPad))

class WorldTimePage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='black')
        self.controller = controller

        self.columnconfigure(0, weight=1)

        self.backLabel = Label(self, text='X World Clock', font=('Helvetica', 50), fg = 'white', bg = 'black')
        self.backLabel.bind('<Button-1>', lambda x: self.controller.show_frame('HomeScreen'))
        self.backLabel.grid(row=0, sticky=W, padx=defaultPad, pady=defaultPad)

        clockLocations = ['London', 'Kuala Lumpur', 'New York']
        for i in range(len(clockLocations)):
            clockInfo = Label(self, text='Time in '+clockLocations[i], font=('Helvetica', 30), fg = 'white', bg = 'black')
            clockInfo.grid(row=i*2+1)

        self.clockLabelLon = Label(self, text='', font=('Helvetica', 90), fg = 'white', bg = 'black')
        self.clockLabelLon.grid(row=2, pady=(0, defaultPad))

        self.clockLabelKL = Label(self, text='', font=('Helvetica', 90), fg = 'white', bg = 'black')
        self.clockLabelKL.grid(row=4, pady=(0, defaultPad))

        self.clockLabelNY = Label(self, text='', font=('Helvetica', 90), fg = 'white', bg = 'black')
        self.clockLabelNY.grid(row=6, pady=(0, defaultPad))

        self.updateClocks()

    def updateClocks(self):

        self.clockLabelLon.configure(text=time.strftime('%H:%M'))
        self.clockLabelKL.configure(text=datetime.now(timezone('Asia/Kuala_Lumpur')).strftime('%H:%M'))
        self.clockLabelNY.configure(text=datetime.now(timezone('America/New_York')).strftime('%H:%M'))

        MagicMirror.after(self, 1000, lambda: self.updateClocks())

class SettingsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, background='black')
        self.controller = controller

        self.backLabel = Label(self, text='X Settings', font=('Helvetica', 50), fg = 'white', bg = 'black')
        self.backLabel.bind('<Button-1>', lambda x: self.controller.show_frame('HomeScreen'))
        self.backLabel.grid(row=0, sticky=W, padx=defaultPad, pady=defaultPad)

        self.backLabel = Label(self, text='Quit', font=('Helvetica', 50), fg = 'white', bg = 'black')
        self.backLabel.bind('<Button-1>', lambda x: root.destroy())
        self.backLabel.grid(row=1, sticky=W, padx=defaultPad, pady=defaultPad)

root = MagicMirror()
root.geometry("480x800")
root.attributes('-fullscreen', True)
root.mainloop()
