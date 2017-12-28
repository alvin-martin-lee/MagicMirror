# import tkinter as tk   # python3
# #import Tkinter as tk   # python
#
# TITLE_FONT = ("Helvetica", 18, "bold")
#
# class SampleApp(tk.Tk):
#
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)
#
#         # the container is where we'll stack a bunch of frames
#         # on top of each other, then the one we want visible
#         # will be raised above the others
#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
#
#         self.frames = {}
#         for F in (StartPage, PageOne, PageTwo):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#
#             # put all of the pages in the same location;
#             # the one on the top of the stacking order
#             # will be the one that is visible.
#             frame.grid(row=0, column=0, sticky="nsew")
#
#         self.show_frame("StartPage")
#
#     def show_frame(self, page_name):
#         '''Show a frame for the given page name'''
#         frame = self.frames[page_name]
#         frame.tkraise()
#
#
# class StartPage(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is the start page", font=TITLE_FONT)
#         label.pack(side="top", fill="x", pady=10)
#
#         button1 = tk.Button(self, text="Go to Page One",
#                             command=lambda: controller.show_frame("PageOne"))
#         button2 = tk.Button(self, text="Go to Page Two",
#                             command=lambda: controller.show_frame("PageTwo"))
#         button1.pack()
#         button2.pack()
#
#
# class PageOne(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is page 1", font=TITLE_FONT)
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()
#
#
# class PageTwo(tk.Frame):
#
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()
#
#
# if __name__ == "__main__":
#     app = SampleApp()
#     app.mainloop()

#from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E
#
# class Calculator:
#
#     def __init__(self, master):
#         self.master = master
#         master.title("Calculator")
#
#         self.total = 0
#         self.entered_number = 0
#
#         self.total_label_text = IntVar()
#         self.total_label_text.set(self.total)
#         self.total_label = Label(master, textvariable=self.total_label_text)
#
#         self.label = Label(master, text="Total:")
#
#         vcmd = master.register(self.validate) # we have to wrap the command
#         self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))
#
#         self.add_button = Button(master, text="+", command=lambda: self.update("add"))
#         self.subtract_button = Button(master, text="-", command=lambda: self.update("subtract"))
#         self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))
#
#         # LAYOUT
#
#         self.label.grid(row=0, column=0, sticky=W)
#         self.total_label.grid(row=0, column=1, columnspan=2, sticky=E)
#
#         self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)
#
#         self.add_button.grid(row=2, column=0)
#         self.subtract_button.grid(row=2, column=1)
#         self.reset_button.grid(row=2, column=2, sticky=W+E)
#
#     def validate(self, new_text):
#         if not new_text: # the field is being cleared
#             self.entered_number = 0
#             return True
#
#         try:
#             self.entered_number = int(new_text)
#             return True
#         except ValueError:
#             return False
#
#     def update(self, method):
#         if method == "add":
#             self.total += self.entered_number
#         elif method == "subtract":
#             self.total -= self.entered_number
#         else: # reset
#             self.total = 0
#
#         self.total_label_text.set(self.total)
#         self.entry.delete(0, END)
#
# root = Tk()
# my_gui = Calculator(root)
# root.mainloop()

import tkinter as tk
import time

# def update_timeText():
#     # Get the current time, note you can change the format as you wish
#     current = time.strftime("%H:%M")
#     # Update the timeText Label box with the current time
#     timeText.configure(text=current)
#     # Call the update_timeText() function after 1 second
#     root.after(1000, update_timeText)
#
# root = tk.Tk()
# root.wm_title("Simple Clock Example")
#
# # Create a timeText Label (a text box)
# timeText = tk.Label(root, text="", font=("Helvetica", 150))
# timeText.pack()
# update_timeText()
# root.mainloop()

# import feedparser
#
# rss = 'http://feeds.bbci.co.uk/news/rss.xml?edition=uk'
# feed = feedparser.parse(rss)
# print(feed['entries'][0]['title'])

import urllib.request
import json
key = '7047852fabf9ea82'
url = 'http://api.wunderground.com/api/' + key + '/geolookup/forecast10day/q/UK/London.json'
f = urllib.request.urlopen(url)
json_string = f.read()
parsed_json = json.loads(json_string.decode())
for day in parsed_json['forecast']['simpleforecast']['forecastday']:
	print( day['date']['weekday'] + ' (' + day['date']['pretty'] + '):')
	print ('  Conditions: ' + day['conditions'])
	print ('  High:' + day['high']['fahrenheit'] + 'F')
	print ('  Low: ' + day['low']['fahrenheit'] + 'F')
f.close()

import Tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        <other code here...>

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.frame = None
        refreshButton = tk.Button(self.root, text="refresh", command=self.refresh)
        self.refresh()

    def refresh(self):
        if self.frame is not None:
            self.frame.destroy()
        self.frame = Example(self.root)
        self.frame.grid(...)