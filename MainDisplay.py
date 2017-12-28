# -*- coding: utf-8 -*-

from tkinter import *
from datetime import date
import time
import WeatherModule
import CalendarModule
import feedparser


class HomeScreen:

    def __init__(self, master):
        self.master = master
        master.title("HomeScreen")

        self.clockLabel = Label(master, text='', font=('Helvetica', 70), fg = 'white', bg = 'black')
        self.clockLabel.grid(row=0, sticky=W)

        self.dateLabel = Label(master, text='', font=('Helvetica', 20), fg = 'white', bg = 'black')
        self.dateLabel.grid(row=1, sticky=W)

        self.weatIconImg = PhotoImage(file='WeatherIcons/unknown.pgm').subsample(15)
        self.weatIconLabel = Label(master, bg='black')
        self.weatIconLabel.image = self.weatIconImg
        self.weatIconLabel.grid(row=0, column=1, sticky=E)

        self.weatStatusLabel = Label(master, text='', font=('Helvetica', 20), fg = 'white', bg = 'black')
        self.weatStatusLabel.grid(row=1, column=1, sticky=E)

        self.calEventList = Listbox(master, font=('Helvetica', 10), fg = 'white', bg = 'black', activestyle='none', borderwidth=0, highlightbackground='black', highlightcolor='white', highlightthickness=0, selectbackground='black', selectborderwidth=0, selectforeground='white', width=30)
        self.calEventList.grid(row=2, sticky=W)

        self.count = 0
        self.newsLabel = Label(master, text='', font=('Helvetica', 10), fg = 'white', bg = 'black')
        self.newsLabel.grid(row=3, columnspan=2, sticky=S)

        self.updateClockDate()
        self.updateWeather()
        self.updateCalendar()
        self.updateNews()

    def updateClockDate(self):
        curTime = time.strftime('%H:%M')
        self.clockLabel.configure(text=curTime)
        curDate = date.today().strftime('%d %B %Y')
        self.dateLabel.configure(text=curDate)
        root.after(1000, lambda: self.updateClockDate())

    def updateWeather(self):
        # curWeatStat, curTemp = WeatherModule.getCurWeatInfo()
        curWeatStat, curTemp= 'Thunderstorm', '26°C'
        curIconPath = WeatherModule.getIcon(curWeatStat)
        self.weatStatusLabel.configure(text=curWeatStat + ' ' + curTemp)

        weatIconImg = PhotoImage(file=curIconPath).subsample(15)
        self.weatIconLabel.configure(image=weatIconImg)
        self.weatIconLabel.image = weatIconImg

        root.after(3600000, lambda: self.updateWeather())

    def updateCalendar(self):
        self.calEventList.delete(0,END)
        events = CalendarModule.getCalEvents()
        if not events:
            self.calEventList.insert(1,'No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            self.calEventList.insert(END, '%s/%s/%s'%(start[8:10], start[5:7], start[:4]))
            self.calEventList.insert(END, '- ' + event['summary'])
        root.after(3600000, lambda: self.updateWeather())

    def updateNews(self):
        rss = 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'
        feed = feedparser.parse(rss)
        self.newsLabel.configure(text=feed['entries'][self.count]['title'])
        if self.count < 10:
            self.count += 1
        else:
            self.count = 0
        root.after(5000, lambda: self.updateNews())

root = Tk()
root.geometry("480x800")
root.configure(background='black')
magicMirror = HomeScreen(root)
root.mainloop()