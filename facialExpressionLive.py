import json
import threading
import time
from tkinter import *
from Faccortex import Cortex
import sys
class FacialExpressionLive(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.canvas = Canvas(self, width=2085, height=1080, bg='#020A2E')
        self.canvas.pack()
        self.neutral = PhotoImage(file='images/neutral.png')
        self.canvas.create_image(685, 335, image=self.neutral)
        self.back = PhotoImage(file='images/arrow.png')
        arrow = Button(self, width=40, height=30, bg='#020A2E', image=self.back, bd=0,command=lambda: controller.show_frame('FacialExpression')).place(x=5, y=5)
        thread1 = threading.Thread(target=self.live)
        thread1.daemon=True
        thread1.start()

    def live(self):
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 10000,

        }
        self.cortex = Cortex(url, user)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        status = 'load'
        profile_name = 'shreyas'
        self.cortex.setup_profile(profile_name, status)
        stream_list = ['fac']
        self.lis = []
        self.cortex.subscribe(stream_list)
        while True:
            res = self.cortex.ws.recv()
            resp=json.loads(res)
            re=resp['fac']
            action = re[0]
            frownNsurprise = re[1]
            clenchNsmile = re[3]
            time.sleep(1)
            print(action,frownNsurprise,clenchNsmile)
            if action == "neutral":
                pass
            if clenchNsmile == "smile":
                self.smile = PhotoImage(file='images/smile.png')
                self.canvas.create_image(685, 335, image=self.smile)
            if  frownNsurprise == "frown":
                self.frown=PhotoImage(file='images/frown.png')
                self.canvas.create_image(685,335,image=self.frown)
            if clenchNsmile == "clench":
                self.clench=PhotoImage(file='images/clench.png')
                self.canvas.create_image(685,335,image=self.clench)
            if frownNsurprise == "surprise":
                self.surprise = PhotoImage(file='images/surprise.png')
                self.canvas.create_image(685,335,image=self.surprise)
            if action == "blink":
                self.blink =PhotoImage(file='images/blink.png')
                self.canvas.create_image(685,335,image=self.blink)

