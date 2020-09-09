from cortex import Cortex
import json
import threading
from tkinter import *
from ACTcortex import Cortex

class CursorLive(Frame):
    def __init__(self, parent,controller):
        Frame.__init__(self, parent)
        self.controller=controller
        self.image1 = PhotoImage(file=r'images/iot.png')
        self.image2 = PhotoImage(file=r'images/facialExp.png')
        self.image3 = PhotoImage(file=r'images/cursor.png')
        self.image4 = PhotoImage(file=r'images/mindR.png')
        self.imgg = PhotoImage(file=r'images/arrow.png')
        self.canvas = Canvas(self, width=2085, height=1080, bg='#020A2E')
        self.canvas.pack()

        label = Label(self, text="FEATURES", bg='#020A2E', fg='white', font='Arial 50 bold').place(x=80, y=20)
        self.back = PhotoImage(file='images/arrow.png')
        arrow = Button(self, width=40, height=30, bg='#020A2E', image=self.back, bd=0,
                       command=lambda: controller.show_frame("Navigator")).place(x=5, y=5)

        button1 = Button(self, width=200, height=215, bg="#3A3535", bd=0, image=self.image1,
                         command=lambda: controller.show_frame("eyeblink")).place(x=380, y=150)
        self.canvas.create_rectangle(75, 150, 380, 365, fill='#615A5A')
        self.canvas.create_text(220, 160, text="BLINK FOR ON/OFF", anchor=N, font='Arial 14 bold', fill='white')
        self.canvas.create_text(223, 230, text="  Feature contains IOT Devices-\n"
                                               "  Focus over the icon and blink twice\n"
                                               "  to turn on/off.", font='Arial 12 bold', fill='white')
        self.canvas.create_text(220, 270, text="      This feature will be active for 7 seconds and the\n"
                                               "      frame  will  automatically  closes by  itself, after \n"
                                               "      the frame is opened wait for 3  seconds to, then \n"
                                               "      start to blink.", anchor=N, font='Arial 9 bold', fill='white')

        button2 = Button(self, width=200, height=215, bg="#3A3535", bd=0, image=self.image2,
                         command=lambda: controller.show_frame("FacialExpression")).place(x=1100, y=150)
        self.canvas.create_rectangle(795, 150, 1101, 368, fill='#615A5A')
        self.canvas.create_text(950, 160, text="FACIAL EXPRESSION", anchor=N, font='Arial 14 bold', fill='white')
        # canvas.create_rectangle(770, 130,1325,390, fill='#FFFFFF')
        self.canvas.create_text(948, 230, text="This feature has Training Frame and\n"
                                               " Live Frame-The more you train more\n"
                                               " accuracy obtained.", font='Arial 12 bold', fill='white')
        self.canvas.create_text(945, 302, text="  The  training  frame  has 5 facial  commands  that\n"
                                               "  needs to be trained,if the live feed is not accurate\n"
                                               "  then train  neutral more. The live feed takes 3 sec\n"
                                               "  to initiate connection."
                                , font='Arial 9 bold', fill='white')

        button3 = Button(self, width=200, height=215, bg="#3A3535", bd=0, image=self.image3,
                         command=lambda: controller.show_frame("CursorTrainer")).place(x=380, y=450)
        self.canvas.create_rectangle(75, 450, 380, 667, fill='#615A5A')
        self.canvas.create_text(220, 460, text="CURSOR CONTROL", anchor=N, font='Arial 14 bold', fill='white')
        # canvas.create_rectangle(50,430,607,690,fill='#FFFFFF')
        self.canvas.create_text(223, 530, text="  The feature has 4 mental commands\n"
                                               "   to train  and  live mode frame allows\n"
                                               "   to control the whole application.", font='Arial 12 bold',
                                fill='white')
        self.canvas.create_text(223, 600, text="  The  training  frame  has  4  mental  commands\n"
                                               "  that  needs  to  be trained, if the live  feed is not\n"
                                               "  accurate then train  neutral more. The live feed \n"
                                               "  takes 3 sec to initiate connection.", font='Arial 9 bold',
                                fill='white')

        button4 = Button(self, width=200, height=215, bg="#3A3535", bd=0, image=self.image4,
                         command=lambda: controller.show_frame("Act2Speak")).place(x=1100, y=450)
        self.canvas.create_rectangle(795, 450, 1100, 669, fill='#615A5A')
        self.canvas.create_text(950, 460, text="ACT TO SPEECH", anchor=N, font='Arial 14 bold', fill='white')
        # canvas.create_rectangle(770,430,1325,688,fill='#FFFFFF')
        self.canvas.create_text(948, 530, text="This feature  has an  Artificial voice -\n"
                                               " speaks when muscular movement is\n"
                                               " made or thought about something.", font='Arial 12 bold', fill='white')
        self.canvas.create_text(948, 600, text="This allows person to make 8 different speechs\n"
                                               "the number can be increased but it takes more\n"
                                               "cognitive ability.", font='Arial 9 bold', fill='white')

        self.my_img = PhotoImage(file="images/sky.png")
        self.my_rectangle = self.canvas.create_image(330, 255, image=self.my_img, tags='close_tag')
        # my_rectangle=canvas.create_rectangle(50,130,610,390,fill="#FFFFFF", stipple="gray12")
        parent.master.bind("<Left>", self.left)
        parent.master.bind("<Right>", self.right)
        parent.master.bind("<Up>", self.up)
        parent.master.bind("<Down>", self.down)
        parent.master.bind("<Return>", self.enter)
        thread = threading.Thread(target=self.func)
        thread.daemon = True
        thread.start()

    def enter(self,event):
        pos = self.canvas.coords('close_tag')
        if pos == [330.0, 255.0]:
            self.controller.show_frame("eyeblink")
        if pos == [1050.0,255.0]:
            self.controller.show_frame("FacialExpressionLive")
        if pos == [330.0, 555.0]:
            self.controller.show_frame("Navigator")
        if pos == [1050.0, 555.0]:
            self.controller.show_frame("Act2Speak")

    def func(self):
         url = "wss://localhost:6868"
         user = {
             "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
             "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
             "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
             "debit": 100,
             "number_row_data": 10
         }
         self.count=0
         self.cortex = Cortex(url, user)
         self.headset_id = self.cortex.query_headset()
         self.cortex.connect_headset()
         self.cortex.request_access()
         auth = self.cortex.authorize()
         self.cortex.create_session(auth, self.headset_id)
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
             #print(action)
             self.FocusChanger(action)

    def FocusChanger(self, action):
        if action == 'left':
            pos = self.canvas.coords('close_tag')
            self.left('<Left>')
            self.lis.append(action)
            if len(self.lis) == 3:
                del self.lis[0]
                print(self.lis)
                if self.lis[0] == self.lis[1]:
                    self.count = self.count + 1
                    if self.count > 15:
                        if pos == [330.0, 255.0]:
                            self.controller.show_frame('eyeblink')
                        if pos == [330.0, 555.0]:
                            self.controller.show_frame('Navigator')
                    print(self.count)
                else:
                    self.count = 0

        if action == 'right':
             pos = self.canvas.coords('close_tag')
             self.right('<Right>')
             self.lis.append(action)
             if len(self.lis) == 3:
                 del self.lis[0]
                 print(self.lis)
                 if self.lis[0] == self.lis[1]:
                     self.count = self.count + 1
                     if self.count > 15:
                         if pos == [1050.0, 255.0]:
                             self.controller.show_frame('FacialExpressionLive')
                         if pos == [1050.0, 555.0]:
                             self.controller.show_frame('Act2Speak')
                     print(self.count)
                 else:
                     self.count = 0

        if action == 'lift':
            pos = self.canvas.coords('close_tag')
            self.up('<Up>')
            self.lis.append(action)
            if len(self.lis) == 3:
                del self.lis[0]
                print(self.lis)
                if self.lis[0] == self.lis[1]:
                    self.count = self.count + 1
                    if self.count > 10:
                        if pos == [330.0, 255.0]:
                            self.controller.show_frame('eyeblink')
                        if pos == [1050.0, 255.0]:
                            self.controller.show_frame('FacialExpressionLive')
                    print(self.count)
                else:
                    self.count = 0

        if action == 'drop':
            pos = self.canvas.coords('close_tag')
            self.down('<down>')
            self.lis.append(action)
            if len(self.lis) == 3:
                del self.lis[0]
                print(self.lis)
                if self.lis[0] == self.lis[1]:
                    self.count = self.count + 1
                    if self.count > 15:
                        if pos == [330.0, 555.0]:
                            self.controller.show_frame('Navigator')
                        if pos == [1050.0, 555.0]:
                            self.controller.show_frame('Act2Speak')
                    print(self.count)
                else:
                    self.count = 0

    def left(self, event):
         x = -720
         y = 0
         pos = self.canvas.coords('close_tag')
         print(pos)
         if pos == [1050.0, 255.0] or pos == [1050.0, 555.0]:
             # print('left', pos)
             self.canvas.move(self.my_rectangle, x, y)

    def right(self, event):
         x = 720
         y = 0
         pos = self.canvas.coords('close_tag')
         print(pos)
         if pos == [330.0, 255.0] or pos == [330.0, 555.0]:
             # print('right', pos)
             self.canvas.move(self.my_rectangle, x, y)

    def up(self, event):
         x = 0
         y = -300
         pos = self.canvas.coords('close_tag')
         print(pos)
         if pos == [330.0, 555.0] or pos == [1050.0, 555.0]:
             # print('up', pos)
             self.canvas.move(self.my_rectangle, x, y)

    def down(self, event):
         x = 0
         y = 300
         pos = self.canvas.coords('close_tag')
         print(pos)
         if pos == [330.0, 255.0] or pos == [1050.0, 255.0]:
             # print('down', pos)
             self.canvas.move(self.my_rectangle, x, y)
