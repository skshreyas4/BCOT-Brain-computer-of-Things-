import json
from itertools import cycle
from tkinter import *
from math import sin, cos
# from connector import Cortex
from connector import Cortex
import threading
from multiprocessing import Process

class eyeblink(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.packet_count = 0
        self.count = 0
        self.id_sequence = 0
        self.switch_on_off = None
        self.controller = controller
        self.c = Canvas(self, width=2085, height=1080, bg="#020A2E")
        self.c.pack()
        self.create_good_rectangle(self.c, 400, 200, 950, 500, 20, 5, '#2C3547')
        label = Label(self, text="BLINK", bg='#020A2E', fg='white', font='Arial 50 bold').place(x=80, y=20)
        self.light = self.create_good_rectangle(self.c, 450, 250, 650, 450, 10, 5, '#5A5D50')  # light
        self.fan = self.create_good_rectangle(self.c, 700, 250, 900, 450, 10, 5, '#5A5D50')  # fan
        self.c.tag_bind(self.fan, '<1>', self.fan_function)
        self.c.tag_bind(self.light, '<1>', self.light_function)
        self.bulb = PhotoImage(file='images/bulb1.png')
        self.lighter = self.c.create_image(500, 265, image=self.bulb, anchor=NW)
        self.c.tag_bind(self.lighter, '<1>', self.light_function)
        self.fann = PhotoImage(file='images/fan1.png')
        self.cooler = self.c.create_image(720, 265, image=self.fann, anchor=NW)
        self.c.tag_bind(self.cooler, '<1>', self.fan_function)
        thread1=threading.Thread(target=self.con)
        thread1.daemon=True
        thread1.start()

    def con(self):

        self.fan = PhotoImage(file='images/fan1.png')

        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url,user)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        stream_list=['fac']
        self.cortex.subscribe(stream_list)
        while True:
            resp = self.cortex.ws.recv()
            res = json.loads(resp)
            val = res['fac']
            eyeact = val[0]
            alternator = cycle(("on", "off"))
            if eyeact == 'blink':
                self.cortex.count += 1
                if self.cortex.count == 14:
                    self.cortex.switch_on_off=next(alternator)
                    self.fan = self.create_good_rectangle(self.c, 700, 250, 900, 450, 10, 5, '#FFCE09')
                    self.fan = PhotoImage(file='images/fan1.png')
                    self.cooler = self.c.create_image(720, 265, image=self.fan, anchor=NW)
                    print(self.cortex.switch_on_off)
                    #time.sleep(0.5)
                if self.cortex.count == 24:
                    self.cortex.switch_on_off="off"
                    self.fan = self.create_good_rectangle(self.c, 700, 250, 900, 450, 10, 5, '#5A5D50')  # fan
                    self.fa = PhotoImage(file='images/fan1.png')
                    self.cooler = self.c.create_image(720, 265, image=self.fa, anchor=NW)
                    print(self.switch_on_off)
                    self.cortex.count = 0
                    #time.sleep(0.5)
            self.cortex.packet_count += 1


    def fan_function(self, event):
            self.fan = self.create_good_rectangle(self.c, 700, 250, 900, 450, 10, 5, '#FFCE09')  # fan
            self.fan = PhotoImage(file='images/fan1.png')
            self.cooler = self.c.create_image(720, 265, image=self.fan, anchor=NW)
            print("you clicked fan")

    def light_function(self, event):
        self.light = self.create_good_rectangle(self.c, 450, 250, 650, 450, 10, 5, '#FFCE09')  # light
        self.bulb = PhotoImage(file='images/bulb1.png')
        self.lighter = self.c.create_image(500, 265, image=self.bulb, anchor=NW)
        print("you clicked light")

    def create_good_rectangle(self, c, x1, y1, x2, y2, feather, res, color):  # feather says blunting scale
        points = []
        # top side
        points += [x1 + feather, y1,
                   x2 - feather, y1]
        # top right corner
        for i in range(res):
            points += [x2 - feather + sin(i / res * 2) * feather,
                       y1 + feather - cos(i / res * 2) * feather]
        # right side
        points += [x2, y1 + feather,
                   x2, y2 - feather]
        # bottom right corner
        for i in range(res):
            points += [x2 - feather + cos(i / res * 2) * feather,
                       y2 - feather + sin(i / res * 2) * feather]
        # bottom side
        points += [x2 - feather, y2,
                   x1 + feather, y2]
        # bottom left corner
        for i in range(res):
            points += [x1 + feather - sin(i / res * 2) * feather,
                       y2 - feather + cos(i / res * 2) * feather]
        # left side
        points += [x1, y2 - feather,
                   x1, y1 + feather]
        # top left corner
        for i in range(res):
            points += [x1 + feather - cos(i / res * 2) * feather,
                       y1 + feather - sin(i / res * 2) * feather]

        return c.create_polygon(points, fill=color)  # ?

