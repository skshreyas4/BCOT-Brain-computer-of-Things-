import json
import threading
import time
from tkinter import *
from cortex import Cortex
import pyttsx3

class Act2Speak(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = Canvas(self, width=2085, height=1080, bg='#020A2E')
        self.canvas.pack()
        self.back = PhotoImage(file='images/arrow.png')
        arrow = Button(self, width=40, height=30, bg='#020A2E', image=self.back, bd=0,command=lambda: controller.show_frame('Navigator')).place(x=5, y=5)
        label = Label(self, text="ACT TO SPEECH", bg='#020A2E', fg='white', font='Arial 50 bold').place(x=80, y=20)
        self.voicegen = pyttsx3.init()
        self.round_rectangle(440, 140, 1300, 640, radius=10, fill="#505050")

        #self.round_rectangle(0,0, 50, 30, radius=10, fill='#132639')

        #text = Text(self,width=110,height=30,bg='#505050',fg='#FFFFFF',font='Arial 10',padx=50,pady=10)
        #textContainer='the texts will be shown in here'
        #text.insert(INSERT, textContainer)
        #text.config(state=DISABLED)
        #text.place(x=440,y=140)

        self.round_rectangle(50,400,400,690,radius=10,fill='#132639')
        self.canvas.create_text(225, 420, text="SPEAKABLE SENTENCES", fill="#FFFFFF", font="Arial 18 bold")
        self.one="Hi it is glad to meet you"
        self.canvas.create_rectangle(60,450,230,475,fill='#0f4d92')
        self.canvas.create_text(145,463,text=self.one,font='Arial 9 bold',fill='white')
        self.two = 'please bring my things'
        self.canvas.create_rectangle(60,490,230,515,fill='#0f4d92')
        self.canvas.create_text(145,503,text=self.two,font='Arial 9 bold',fill='white')
        self.three ='I would like to go out'
        self.canvas.create_rectangle(60,530,230,555,fill='#0f4d92')
        self.canvas.create_text(145, 543, text=self.three, font='Arial 9 bold', fill='white')
        self.four ='I am hungry'
        self.canvas.create_rectangle(60, 570, 230, 595, fill='#0f4d92')
        self.canvas.create_text(145, 583, text=self.four, font='Arial 9 bold', fill='white')
        self.five ='I am not feeling well'
        self.canvas.create_rectangle(60, 610, 230, 635, fill='#0f4d92')
        self.canvas.create_text(145, 623, text=self.five, font='Arial 9 bold', fill='white')
        self.six = 'take me to the washroom'
        self.canvas.create_rectangle(60, 650, 230, 675, fill='#0f4d92')
        self.canvas.create_text(145, 663, text=self.six, font='Arial 9 bold', fill='white')
        self.seven ='I am excited'
        self.canvas.create_rectangle(240, 450, 390, 475, fill='#0f4d92')
        self.canvas.create_text(310, 463, text=self.seven, font='Arial 9 bold', fill='white')
        self.eight ='I am happy'
        self.canvas.create_rectangle(240, 490, 390,515, fill='#0f4d92')
        self.canvas.create_text(310, 503, text=self.eight, font='Arial 9 bold', fill='white')

        self.round_rectangle(460, 150, 690, 200, radius=10, fill='#132639')
        self.canvas.create_text(570, 175, text=self.one, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(1050,150,1280,200,radius=10,fill='#132639')
        self.canvas.create_text(1160, 175, text=self.two, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(460, 375, 690, 425, radius=10, fill='#132639')
        self.canvas.create_text(570, 400, text=self.three, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(750, 262, 980, 312, radius=10, fill='#132639')
        self.canvas.create_text(860, 287, text=self.four, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(460, 580, 690, 630, radius=10, fill='#132639')
        self.canvas.create_text(570, 605, text=self.five, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(1050, 375, 1280, 425, radius=10, fill='#132639')
        self.canvas.create_text(1160, 400, text=self.six, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(750, 478, 980, 528, radius=10, fill='#132639')
        self.canvas.create_text(860, 503, text=self.seven, fill="#FFFFFF", font="Arial 12 bold")

        self.round_rectangle(1050, 580, 1280, 630, radius=10, fill='#132639')
        self.canvas.create_text(1160, 605 , text=self.eight, fill="#FFFFFF", font="Arial 12 bold")
        thread = threading.Thread(target=self.mentalComm)
        thread.daemon=True
        thread.start()

    def mentalComm(self):
        self.url = "wss://localhost:6868"
        self.user = {
         "license": "",
         "client_id": "",
         "client_secret": "",
         "debit": 100,
         "number_row_data": 10
        }
        self.count=0
        self.cortex = Cortex(self.url, self.user)
        headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, headset_id)
        status='load'
        profile_name='skshreyas'
        self.cortex.setup_profile(profile_name,status)
        stream_list = ['com']
        self.lis = []
        self.cortex.subscribe(stream_list)
        while True:
             resp = self.cortex.ws.recv()
             res = json.loads(resp)
             mentalCommandList = res['com']
             action = mentalCommandList[0]
             print(action)
             if action == 'neutral':
                 self.count = 0
             if action == 'right':
                 self.lis.append(action)
                 if len(self.lis) == 3:
                     del self.lis[0]
                     print(self.lis)
                     if self.lis[0] == self.lis[1]:
                         self.count = self.count + 1
                         if self.count > 6:
                             self.voicegen.say("please bring my things")
                             self.voicegen.runAndWait()
                             self.count = 0
                         print(self.count)
                     else:
                         self.count = 0

             if action == 'lift':
                 self.lis.append(action)
                 if len(self.lis) == 3:
                     del self.lis[0]
                     print(self.lis)
                     if self.lis[0] == self.lis[1]:
                         self.count = self.count + 1
                         if self.count > 6:
                             self.voicegen.say("I would like to go out")
                             self.voicegen.runAndWait()
                             self.count=0
                         print(self.count)
                     else:
                         self.count = 0

             if action == 'drop':
                 self.lis.append(action)
                 if len(self.lis) == 3:
                     del self.lis[0]
                     print(self.lis)
                     if self.lis[0] == self.lis[1]:
                         self.count = self.count + 1
                         if self.count > 6:
                             self.voicegen.say("hi it is glad to meet you")
                             self.voicegen.runAndWait()
                             self.count=0
                         print(self.count)
                     else:
                         self.count = 0

             if action == 'left':
                 self.lis.append(action)
                 if len(self.lis) == 3:
                     del self.lis[0]
                     print(self.lis)
                     if self.lis[0] == self.lis[1]:
                         self.count = self.count + 1
                         if self.count > 6:
                             break
                         print(self.count)
                     else:
                         self.count = 0
        self.muscular_detectors()

    def muscular_detectors(self):
        status = 'unload'
        profile_name = 'shreyas'
        self.cortex.setup_profile(profile_name, status)
        cortex = Cortex(self.url, self.user)
        headset_id = cortex.query_headset()
        cortex.connect_headset()
        cortex.request_access()
        auth = cortex.authorize()
        cortex.create_session(auth, headset_id)
        cortex.setup_profile(profile_name, status)
        status = 'load'
        profile_name = 'shreyas'
        cortex.setup_profile(profile_name, status)
        stream_list = ['fac']
        lis = []
        cortex.subscribe(stream_list)
        while True:
            resp = self.cortex.ws.recv()
            res = json.loads(resp)
            facCommandList = res['fac']
            print(facCommandList)
            blink = facCommandList[0]
            frownNsurprise = facCommandList[1]
            clenchNsmile = facCommandList[3]
            if frownNsurprise == 'frown':
                self.lis.append(frownNsurprise)
                if len(self.lis) == 3:
                    del self.lis[0]
                    print(self.lis)
                    if self.lis[0] == self.lis[1]:
                        self.count = self.count + 1
                        if self.count > 6:
                            self.voicegen.say("I would like to go out")
                            self.voicegen.runAndWait()
                            self.count=0
                        print(self.count)
                    else:
                        self.count = 0
            if frownNsurprise == 'surprise':
                self.lis.append(frownNsurprise)
                if len(self.lis) == 3:
                    del self.lis[0]
                    print(self.lis)
                    if self.lis[0] == self.lis[1]:
                        self.count = self.count + 1
                        if self.count > 6:
                            self.voicegen.say("I am excited")
                            self.voicegen.runAndWait()
                            self.count = 0
                        print(self.count)
                    else:
                        self.count = 0
            if clenchNsmile == 'clench':
                self.lis.append(clenchNsmile)
                if len(self.lis) == 3:
                    del self.lis[0]
                    print(self.lis)
                    if self.lis[0] == self.lis[1]:
                        self.count = self.count + 1
                        if self.count > 6:
                            self.voicegen.say("take me to the washroom")
                            self.voicegen.runAndWait()
                        print(self.count)
                    else:
                        self.count = 0
            if clenchNsmile == 'smile':
                self.lis.append(clenchNsmile)
                if len(self.lis) == 3:
                    del self.lis[0]
                    print(self.lis)
                    if self.lis[0] == self.lis[1]:
                        self.count = self.count + 1
                        if self.count > 6:
                            self.voicegen.say("I am happy")
                            self.voicegen.runAndWait()
                            self.count = 0
                        print(self.count)
                    else:
                        self.count = 0

            if blink == 'blink':
                self.lis.append(clenchNsmile)
                if len(self.lis) == 3:
                    del self.lis[0]
                    print(self.lis)
                    if self.lis[0] == self.lis[1]:
                        self.count = self.count + 1
                        if self.count > 10:
                            break
                        print(self.count)
                    else:
                        self.count = 0
        self.mentalComm()

    def round_rectangle(self,x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        return self.canvas.create_polygon(points, **kwargs, smooth=True)

