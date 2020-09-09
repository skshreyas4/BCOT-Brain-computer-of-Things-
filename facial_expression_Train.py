from tkinter import *
from tkinter.ttk import Progressbar
import time
from Faccortex import Cortex
import threading
class FacialExpression(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller

        # self.delete=PhotoImage(file='images/delete.png')
        self.c = Canvas(self, width=2085, height=1080, bg='#020A2E')
        self.c.pack()
        self.back = PhotoImage(file='images/arrow.png')
        arrow = Button(self, width=40, height=30, bg='#020A2E', image=self.back, bd=0,command=lambda: controller.show_frame('Navigator')).place(x=5, y=5)
        label = Label(self, text="FACIAL EXPRESSIONS", bg='#020A2E', fg='white', font='Arial 30 bold').place(x=50, y=40)
        self.round_rectangle(50, 120, 390, 620, radius=10, fill='#2C3547')  # container of buttons to train
        self.c.create_text(185, 140, text="TRAIN", anchor=N, font='Arial 14 ', fill='white')
        self.neutral = PhotoImage(file='images/neutral.png')
        self.c.create_image(685, 335, image=self.neutral)
        self.Valence_Arousal_Map()
        self.live = Button(self,width=20, height=1, text='GO LIVE', bd=0, bg='#222233', fg='white',
                           font='Arial 12 bold',command=lambda: controller.show_frame('FacialExpressionLive')).place(x=570, y=620)
        self.c.create_text(685, 690,
                           text="NOTE : Train all the emotions before you go LIVE and Train Neutral emotion first before the training of others,Each button will retain it's color after training completes for corresponding emotion,Valence says about awareness(+ve/-veness) &\n"
                                "             Arousal says how much calming and exciting a person is and Deleting a command will erase all the data trained before.\n",
                           fill='#AACCFF')
        self.neutalTrainButton()
        self.smileTrainButton()
        self.frownTrainButton()
        self.clenchTrainButton()
        self.surpriseTrainButton()
        self.blinkTrainButton()
        self.neutraldelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0,text='Del',fg='white',font='Arial 10').place(x=323, y=188)
        self.smiledelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0,text='Del',fg='white',font='Arial 10',command=self.delete_command).place(x=323, y=258)

    def delete_command(self):
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'skshreyas'
        profiles = self.cortex.queryProfile()
        status = 'load'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.delete(detection='facialExpression', action='smile', status='erase')
        status = "save"
        self.cortex.setup_profile(profile_name, status)
        status = 'unload'
        self.cortex.setup_profile(profile_name, status)

    def Valence_Arousal_Map(self):
        self.c.create_rectangle(970, 120, 1300, 620, fill='#040F40', width=2, outline='#707070')
        self.c.create_line(1135, 120, 1135, 620, fill='#707070', width=5)
        self.c.create_line(970, 380, 1300, 380, fill='#707070', width=5)
        self.c.create_text(1220, 395, text='Valence', fill='#5A76B9', font='Arial 15 ')
        self.c.create_text(1120, 250, text='Arousal', fill='#5A76B9', font='Arial 15', angle=90)
        self.c.create_polygon(980, 250, 987, 235, 995, 250, fill='#FFA60D')
        self.c.create_text(990, 258, text='Angry', font='Arial 10', fill='white')
        self.c.create_polygon(1000, 500, 1007, 485, 1015, 500, fill='#FFA60D')
        self.c.create_text(1010, 508, text="Frown", font='Arial 10', fill='white')
        self.c.create_polygon(1180, 550, 1187, 535, 1195, 550, fill='green')
        self.c.create_text(1190, 558, text='Neutral', font='Arial 10', fill='white')
        self.c.create_polygon(1260, 500, 1267, 485, 1274, 500, fill='#FFA60D')
        self.c.create_text(1270, 508, text='Smile', font='Arial 10', fill='white')
        self.c.create_polygon(1240, 300, 1247, 285, 1255, 300, fill='#FFA60D')
        self.c.create_text(1250, 308, text='Blink', font='Arial 10', fill='white')
        self.c.create_polygon(1210, 200, 1217, 185, 1225, 200, fill='#FFA60D')
        self.c.create_text(1220, 208, text='Surprise', font='Arial 10', fill='white')

    def neutalTrainButton(self):
        self.neutralTrain = self.round_rectangle(70, 220, 300, 190, radius=20, fill='#5F5D6B')  # neutral train
        self.neutralText = self.c.create_text(185, 197, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralText, '<1>', self.neutralOnclick)
        self.c.tag_bind(self.neutralTrain, '<1>', self.neutralOnclick)

    def smileTrainButton(self):
        self.smileTrain = self.round_rectangle(70, 290, 300, 260, radius=20, fill='#5F5D6B')  # smile train
        self.smileText = self.c.create_text(185, 267, text="Smile", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.smileText, '<1>', self.smileOnclick)
        self.c.tag_bind(self.smileTrain, '<1>', self.smileOnclick)

    def frownTrainButton(self):
        self.frownTrain = self.round_rectangle(70, 360, 300, 330, radius=20, fill='#5F5D6B')  # frown train
        self.frownText = self.c.create_text(185, 337, text="Frown", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.frownTrain, '<1>', self.frownClick)
        self.c.tag_bind(self.frownText, '<1>', self.frownClick)
        self.frowndelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0,text='Del',fg='white',font='Arial 10').place(x=323, y=328)

    def clenchTrainButton(self):
        self.clenchTrain = self.round_rectangle(70, 430, 300, 400, radius=20, fill='#5F5D6B')  # clench train
        self.clenchText = self.c.create_text(185, 407, text="Clench", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.clenchTrain, '<1>', self.clenchClick)
        self.c.tag_bind(self.clenchText, '<1>', self.clenchClick)
        self.clenchdelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0,text='Del',fg='white',font='Arial 10').place(x=323, y=398)

    def surpriseTrainButton(self):
        self.surpriseTrain = self.round_rectangle(70, 500, 300, 470, radius=20, fill='#5F5D6B')  # surprise train
        self.surpriseText = self.c.create_text(185, 477, text="Surprise", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.surpriseTrain, '<1>', self.surpriseClick)
        self.c.tag_bind(self.surpriseText, '<1>', self.surpriseClick)
        self.surprisedelete = Button(self, width=6, height=2, bd=0, bg='#5F5D6B',text='Del',fg='white',font='Arial 10').place(x=325, y=468)

    def blinkTrainButton(self):
        self.blinkTrain = self.round_rectangle(70, 570, 300, 540, radius=20, fill='#5F5D6B')  # blink train
        self.blinkText = self.c.create_text(185, 547, text="Blink", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.blinkText, '<1>', self.blinkClick)
        self.c.tag_bind(self.blinkTrain, '<1>', self.blinkClick)
        self.deleteBlink = Button(self, width=6, height=2, bd=0, bg='#5F5D6B',text='Del',fg='white',font='Arial 10').place(x=325, y=538)

    def Neutralcortexfile(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window = 200
        height_of_window = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        top.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'shreyas'
        training_action = 'neutral'
        number_of_train = 5

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.queryProfile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 20 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)
            if num_train == 5:
                self.neutralReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="NEUTRAL training completed", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def neutralOnclick(self, event):
        self.neutralClicked = self.round_rectangle(70, 220, 300, 190, radius=20, fill='yellow')  # neutral train
        self.neutralTextClicked = self.c.create_text(185, 197, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralClicked, '<1>', self.neutralReleased)
        self.c.tag_bind(self.neutralTextClicked, '<1>', self.neutralReleased)
        thred1 = threading.Thread(target=self.Neutralcortexfile)
        thred1.daemon = True
        thred1.start()

    def neutralReleased(self):
        self.neutralRetain = self.round_rectangle(70, 220, 300, 190, radius=20, fill='#5F5D6B')  # neutral train
        self.neutralTextRetain = self.c.create_text(185, 197, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralRetain, '<1>', self.neutralOnclick)
        self.c.tag_bind(self.neutralTextRetain, '<1>', self.neutralOnclick)

    def Smilecortexfile(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window = 250
        height_of_window = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        top.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'shreyas'
        training_action = 'smile'
        number_of_train = 5

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.queryProfile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 20 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)
            if num_train == 5:
                self.smileReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="NEUTRAL TRAINING COMPLETED", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def smileOnclick(self, event):
        self.smileClicked = self.round_rectangle(70, 290, 300, 260, radius=20, fill='yellow')  # smile train
        self.smileTextClicked = self.c.create_text(185, 267, text="Smile", anchor=N, font='Arial 12 ', fill='white')
        self.expr = PhotoImage(file="images/smile.png")
        self.c.create_image(685, 335, image=self.expr)
        self.c.tag_bind(self.smileClicked, '<1>', self.smileReleased)
        self.c.tag_bind(self.smileTextClicked, '<1>', self.smileReleased)
        thread2 = threading.Thread(target=self.Smilecortexfile)
        thread2.daemon = True
        thread2.start()

    def smileReleased(self):
        self.smileRetain = self.round_rectangle(70, 290, 300, 260, radius=20, fill='#5F5D6B')  # smile train
        self.smileTextRetain = self.c.create_text(185, 267, text="Smile", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.smileRetain, '<1>', self.smileOnclick)
        self.c.tag_bind(self.smileTextRetain, '<1>', self.smileOnclick)

    def Frowncortexfile(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window = 250
        height_of_window = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        top.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'shreyas'
        training_action = 'frown'
        number_of_train = 5

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.queryProfile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 20 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)
            if num_train == 5:
                self.frownReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="FROWN TRAINING COMPLETED", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def frownClick(self, event):
        self.frownClicked = self.round_rectangle(70, 360, 300, 330, radius=20, fill='yellow')  # frown train
        self.frownTextClicked = self.c.create_text(185, 337, text="Frown", anchor=N, font='Arial 12 ', fill='white')
        self.frownImg = PhotoImage(file='images/frown.png')
        self.c.create_image(685, 335, image=self.frownImg)
        self.c.tag_bind(self.frownClicked, '<1>', self.frownReleased)
        self.c.tag_bind(self.frownTextClicked, '<1>', self.frownReleased)
        thread3 = threading.Thread(target=self.Frowncortexfile)
        thread3.daemon = True
        thread3.start()

    def frownReleased(self):
        self.frownRetained = self.round_rectangle(70, 360, 300, 330, radius=20, fill='#5F5D6B')  # frown train
        self.frownTextRetain = self.c.create_text(185, 337, text="Frown", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.frownRetained, '<1>', self.frownClick)
        self.c.tag_bind(self.frownTextRetain, '<1>', self.frownClick)

    def Clenchcortexfile(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window = 250
        height_of_window = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        top.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'shreyas'
        training_action = 'clench'
        number_of_train = 5

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.queryProfile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 20 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)
            if num_train == 5:
                self.clenchReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="CLENCH TRAINING COMPLETED", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def clenchClick(self, event):
        self.clenchClicked = self.round_rectangle(70, 430, 300, 400, radius=20, fill='yellow')  # clench train
        self.clenchTextclicked = self.c.create_text(185, 407, text="Clench", anchor=N, font='Arial 12 ', fill='white')
        self.clenchImg = PhotoImage(file="images/clench.png")
        self.c.create_image(685, 335, image=self.clenchImg)
        self.c.tag_bind(self.clenchClicked, '<1>', self.clenchReleased)
        self.c.tag_bind(self.clenchTextclicked, '<1>', self.clenchReleased)
        thread4 = threading.Thread(target=self.Clenchcortexfile)
        thread4.daemon = True
        thread4.start()

    def clenchReleased(self):
        self.clenchRetain = self.round_rectangle(70, 430, 300, 400, radius=20, fill='#5F5D6B')  # clench train
        self.clenchTextRetain = self.c.create_text(185, 407, text="Clench", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.clenchRetain, '<1>', self.clenchClick)
        self.c.tag_bind(self.clenchTextRetain, '<1>', self.clenchClick)

    def Surprisecortexfile(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window = 250
        height_of_window = 100
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        x_coordinate = (screen_width / 2) - (width_of_window / 2)
        y_coordinate = (screen_height / 2) - (height_of_window / 2)
        top.geometry("%dx%d+%d+%d" % (width_of_window, height_of_window, x_coordinate, y_coordinate))
        url = "wss://localhost:6868"
        user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(url, user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'shreyas'
        training_action = 'surprise'
        number_of_train = 5

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.queryProfile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 20 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='facialExpression',
                                      action=training_action,
                                      status=status)
            if num_train == 5:
                self.surpriseReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="SURPRISE TRAINING COMPLETED", font=("Helvetica", 10))
        w.pack()
        Button(top, width=10, height=2, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def surpriseClick(self, event):
        self.surpriseClicked = self.round_rectangle(70, 500, 300, 470, radius=20, fill='yellow')  # surprise train
        self.surpriseTextClicked = self.c.create_text(185, 477, text="Surprise", anchor=N, font='Arial 12 ',
                                                      fill='white')
        self.surpriseImg = PhotoImage(file='images/surprise.png')
        self.c.create_image(685, 335, image=self.surpriseImg)
        self.c.tag_bind(self.surpriseClicked, '<1>', self.surpriseReleased)
        self.c.tag_bind(self.surpriseTextClicked, '<1>', self.surpriseReleased)
        thread5 = threading.Thread(target=self.Surprisecortexfile)
        thread5.daemon = True
        thread5.start()

    def surpriseReleased(self):
        self.surpriseRetain = self.round_rectangle(70, 500, 300, 470, radius=20, fill='#5F5D6B')  # surprise train
        self.surpriseTextRetain = self.c.create_text(185, 477, text="Surprise", anchor=N, font='Arial 12 ',
                                                     fill='white')
        self.c.tag_bind(self.surpriseRetain, '<1>', self.surpriseClick)
        self.c.tag_bind(self.surpriseTextRetain, '<1>', self.surpriseClick)

    def blinkClick(self, event):
        self.blinkClicked = self.round_rectangle(70, 570, 300, 540, radius=20, fill='yellow')  # blink train
        self.blinkTextClicked = self.c.create_text(185, 547, text="Blink", anchor=N, font='Arial 12 ', fill='white')
        self.blinkImg = PhotoImage(file='images/blink.png')
        self.c.create_image(685, 335, image=self.blinkImg)
        self.c.tag_bind(self.blinkTextClicked, '<1>', self.blinkReleased)
        self.c.tag_bind(self.blinkClicked, '<1>', self.blinkReleased)

    def blinkReleased(self, event):
        self.blinkRetain = self.round_rectangle(70, 570, 300, 540, radius=20, fill='#5F5D6B')  # blink train
        self.blinkTextRetain = self.c.create_text(185, 547, text="Blink", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.blinkRetain, '<1>', self.blinkClick)
        self.c.tag_bind(self.blinkTextRetain, '<1>', self.blinkClick)

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
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

        return self.c.create_polygon(points, **kwargs, smooth=True)
