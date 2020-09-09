from tkinter import *
from tkinter.ttk import Progressbar
import time
from gyroCortex import Cortex
import threading
class CursorTrainer(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.c = Canvas(self, width=2085, height=1080, bg='#020A2E')
        self.c.pack()

        self.back = PhotoImage(file='images/arrow.png')
        arrow = Button(self, width=40, height=30, bg='#020A2E', image=self.back, bd=0,command=lambda:controller.show_frame("Navigator")).place(x=5, y=5)
        label = Label(self, text="CURSOR CONTROL", bg='#020A2E', fg='white', font='Arial 30 bold').place(x=50, y=50)
        self.round_rectangle(50, 140, 420, 560, radius=10, fill='#2C3547')  # container of buttons to train
        self.c.create_text(200, 160, text="TRAIN", anchor=N, font='Arial 15 ', fill='white')
        Button(self,width=32, height=1, text='GO LIVE', bg='#222233', fg='white',
                           font='Arial 12 bold',command=lambda:controller.show_frame("CursorLive")).place(x=70, y=590)
        self.c.create_text(690, 680,
                           text="NOTE : Train all the mental commmands before you go LIVE and Train Neutral emotion first before the training of others,Each button will retain it's color after training completes for corresponding command",
                           fill='#AACCFF')
        self.neutalTrainButton()
        self.LiftTrainButton()
        self.DropTrainButton()
        self.LeftTrainButton()
        self.RightTrainButton()
        #self.PushTrainButton()
        self.neutraldelete = Button(self, width=6, height=2, bg='#5F5D6B',text='Del', bd=0,fg='white').place(x=350, y=207)
        self.liftdelete = Button(self, width=6, height=2, bg='#5F5D6B',text='Del',bd=0,fg='white').place(x=350, y=278)
        self.dropdelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0,text='Del',fg='white').place(x=350, y=348)
        self.leftdelete = Button(self, width=6, height=2, bg='#5F5D6B', bd=0, text='Del',fg='white').place(x=350, y=418)
        self.rightdelete = Button(self, width=6, height=2, bd=0, bg='#5F5D6B',text='Del',fg='white').place(x=350, y=488)
        #self.pushdelete = Button(self, width=6, height=2, bd=0, bg='#5F5D6B').place(x=350, y=560)

        self.round_rectangle(440,140,1300,640,radius=10,fill="#445b6e")
        #self.c.create_rectangle(700,150,1000,630,fill="#FFFFFF")
        #self.c.create_rectangle(450,295,1290,495,fill='#FFFFFF')
        self.c.create_rectangle(450,295,703,485,fill="#342e2e",outline="") #left
        self.c.create_text(575,390,text="LEFT",font='Arial 18 bold',fill="#FFFFFF")
        self.c.create_rectangle(1022,295,1290,485,fill="#342e2e",outline="") #right
        self.c.create_text(1157,390,text="RIGHT",fill="#FFFFFF",font="Arial 18 bold")
        self.c.create_rectangle(713,150,1012,285,fill='#342e2e',outline="") #top
        self.c.create_text(860,220,text="LIFT",fill="#FFFFFF",font="Arial 18 bold")
        self.c.create_rectangle(713,495,1012,630,fill="#342e2e",outline="")#down
        self.c.create_text(860,560,text="PULL",fill="#FFFFFF",font="Arial 18 bold")
        self.c.create_text(858,308,text="INSTRUCTIONS",font="Arial 14",fill="#FFFFFF")

        self.c.create_text(860,403,text=" 1. It is mandatory to train NEUTRAL before you train any\n    other actions.\n"
                                        " 2. Each buttons of training will take 3 cycle to improve\n    the expectancy in output,so appox it may take few\n    seconds to train each.\n"
                                        " 3. While training try to imagine the focus in which\n    direction you want it to move.\n"
                                        " 4. The more you train,more perfection you get in Live.\n"
                                        " 5. Deleting the action will delete all your trainings\n    of respective action.",fill="#FFFFFF")
        #self.c.create_rectangle(460,305,693,475,fill="#443c3c",outline="")

        #self.img=PhotoImage(file="greysolid.png")
        #self.c.create_image(576,390,image=self.img) #left
        #self.right=PhotoImage(file='right_transperant.png')
        #self.c.create_image(1156,390,image=self.right)
        #self.top=PhotoImage(file='top_transperant.png')
        #self.c.create_image(862,216,image=self.top)
        #self.drop=PhotoImage(file='top_transperant.png')
        #self.c.create_image(862,562,image=self.drop)


    def neutalTrainButton(self):
        self.neutralTrain = self.round_rectangle(70, 240, 330, 210, radius=20, fill='#5F5D6B')  # neutral train
        self.neutralText = self.c.create_text(200, 215, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralText, '<1>', self.neutralOnclick)
        self.c.tag_bind(self.neutralTrain, '<1>', self.neutralOnclick)

    def NeutralCortex(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window=200
        height_of_window=100
        screen_width=top.winfo_screenwidth()
        screen_height=top.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        top.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x_coordinate,y_coordinate))
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name='skshreyas'
        training_action='neutral'
        number_of_train=3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        #if self.profile_name not in profiles:
         #  status = 'create'
          # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)
            if num_train == 3:
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
        sys.exit() # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def neutralOnclick(self,event):
        self.neutralClicked = self.round_rectangle(70, 240, 330, 210, radius=20, fill='yellow')  # neutral train
        self.neutralTextClicked = self.c.create_text(200, 215, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralClicked,'<1>',self.neutralReleased)
        self.c.tag_bind(self.neutralTextClicked,'<1>',self.neutralReleased)
        thread1=threading.Thread(target=self.NeutralCortex)
        thread1.daemon=True
        thread1.start()

    def neutralReleased(self):
        self.neutralRetain = self.round_rectangle(70, 240, 330, 210, radius=20, fill='#5F5D6B')  # neutral train
        self.neutralTextRetain = self.c.create_text(200, 215, text="Neutral", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.neutralRetain,'<1>',self.neutralOnclick)
        self.c.tag_bind(self.neutralTextRetain,'<1>',self.neutralOnclick)

    def LiftCortex(self):
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
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'skshreyas'
        training_action = 'lift'
        number_of_train = 3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                      action=training_action,
                                      status=status)
            if num_train == 3:
                self.LiftReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="LIFT training completed", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def LiftTrainButton(self):
        self.LiftTrain = self.round_rectangle(70, 310, 330, 280, radius=20, fill='#5F5D6B')  # LIft train
        self.liftText = self.c.create_text(200, 285, text="Lift", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.LiftTrain,'<1>',self.liftOnclick)
        self.c.tag_bind(self.liftText,'<1>',self.liftOnclick)

    def liftOnclick(self, event):
        self.liftClicked = self.round_rectangle(70, 310, 330, 280, radius=20, fill='yellow')  # smile train
        self.liftTextClicked = self.c.create_text(200, 285, text="Lift", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.liftClicked, '<1>', self.LiftReleased)
        self.c.tag_bind(self.liftTextClicked, '<1>', self.LiftReleased)
        self.top=PhotoImage(file='images/top_transperant.png')
        self.c.create_image(862,216,image=self.top)
        thread2 = threading.Thread(target=self.LiftCortex)
        thread2.daemon = True
        thread2.start()

    def LiftReleased(self):
        self.liftRetain = self.round_rectangle(70, 310, 330, 280, radius=20, fill='#5F5D6B')  # smile train
        self.liftTextRetain = self.c.create_text(200, 285, text="Lift", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.liftRetain, '<1>', self.liftOnclick)
        self.c.tag_bind(self.liftTextRetain, '<1>', self.liftOnclick)
        self.c.create_rectangle(713, 150, 1012, 285, fill='#342e2e', outline="")  # top
        self.c.create_text(860, 220, text="LIFT", fill="#FFFFFF", font="Arial 18 bold")

    def DropCortex(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window=200
        height_of_window=100
        screen_width=top.winfo_screenwidth()
        screen_height=top.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        top.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x_coordinate,y_coordinate))
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name='skshreyas'
        training_action='drop'
        number_of_train=3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        #if self.profile_name not in profiles:
         #  status = 'create'
          # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)
            if num_train == 3:
                self.DropReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="DROP training completed", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit() # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed


    def DropTrainButton(self):
        self.dropTrain = self.round_rectangle(70, 380, 330, 350, radius=20, fill='#5F5D6B')  # Drop train
        self.dropText = self.c.create_text(200, 355, text="Drop", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.dropTrain,'<1>',self.DropClick)
        self.c.tag_bind(self.dropText,'<1>',self.DropClick)

    def DropClick(self,event):
        self.dropClicked =self.round_rectangle(70, 380, 330, 350, radius=20, fill='yellow')  # frown train
        self.dropTextClicked = self.c.create_text(200, 355, text="Drop", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.dropClicked,'<1>',self.DropReleased)
        self.c.tag_bind(self.dropTextClicked,'<1>',self.DropReleased)
        self.drop=PhotoImage(file='images/top_transperant.png')
        self.c.create_image(862,562,image=self.drop)
        thread3 = threading.Thread(target=self.DropCortex)
        thread3.daemon = True
        thread3.start()

    def DropReleased(self):
        self.dropRetained=self.round_rectangle(70,380,330,350,radius=20,fill= '#5F5D6B') #frown train
        self.dropTextRetain = self.c.create_text(200, 355, text="Drop", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.dropRetained,'<1>',self.DropClick)
        self.c.tag_bind(self.dropTextRetain,'<1>',self.DropClick)
        self.c.create_rectangle(713, 495, 1012, 630, fill="#342e2e", outline="")  # down
        self.c.create_text(860, 560, text="PULL", fill="#FFFFFF", font="Arial 18 bold")

    def LeftCortex(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window=200
        height_of_window=100
        screen_width=top.winfo_screenwidth()
        screen_height=top.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        top.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x_coordinate,y_coordinate))
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name='skshreyas'
        training_action='left'
        number_of_train=3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        #if self.profile_name not in profiles:
         #  status = 'create'
          # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)
            if num_train == 3:
                self.LeftReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="LEFT training completed", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit() # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed


    def LeftTrainButton(self):
        self.leftTrain = self.round_rectangle(70, 450, 330, 420, radius=20, fill='#5F5D6B')  # Left train
        self.leftText = self.c.create_text(200, 427, text="Left", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.leftTrain,'<1>',self.LeftClick)
        self.c.tag_bind(self.leftText,'<1>',self.LeftClick)


    def LeftClick(self,event):
        self.leftClicked = self.round_rectangle(70, 450, 330, 420, radius=20, fill='yellow')  # clench train
        self.leftTextclicked = self.c.create_text(200, 427, text="Left", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.leftClicked,'<1>',self.LeftReleased)
        self.c.tag_bind(self.leftTextclicked,'<1>',self.LeftReleased)
        self.img = PhotoImage(file="images/greysolid.png")
        self.c.create_image(576, 390, image=self.img)  # left
        thread4 = threading.Thread(target=self.LeftCortex)
        thread4.daemon = True
        thread4.start()

    def LeftReleased(self):
        self.leftRetain=self.round_rectangle(70, 450, 330, 420, radius=20, fill='#5F5D6B')  # clench train
        self.leftTextRetain = self.c.create_text(200, 427, text="Left", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.leftRetain,'<1>',self.LeftClick)
        self.c.tag_bind(self.leftTextRetain,'<1>',self.LeftClick)
        self.c.create_rectangle(450,295,703,485,fill="#342e2e",outline="") #left
        self.c.create_text(575,390,text="LEFT",font='Arial 18 bold',fill="#FFFFFF")

    def RightCortex(self):
        top = Toplevel(self)
        top.grab_set()
        top.title("BCOT")
        top.wm_iconbitmap('logo.ico')
        progress = Progressbar(top, orient=HORIZONTAL, length=100, mode='determinate')
        progress.pack(pady=10)
        progress['value'] = 0
        width_of_window=200
        height_of_window=100
        screen_width=top.winfo_screenwidth()
        screen_height=top.winfo_screenheight()
        x_coordinate = (screen_width/2)-(width_of_window/2)
        y_coordinate = (screen_height/2)-(height_of_window/2)
        top.geometry("%dx%d+%d+%d"%(width_of_window,height_of_window,x_coordinate,y_coordinate))
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name='skshreyas'
        training_action='pull'
        number_of_train=3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        #if self.profile_name not in profiles:
         #  status = 'create'
          # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                 action=training_action,
                                 status=status)
            if num_train == 3:
                self.RightReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="RIGHT training completed", font=("Helvetica", 10))
        w.pack()
        Button(top, text='ok', command=lambda win=top: win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit() # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed


    def RightTrainButton(self):
        self.rightTrain = self.round_rectangle(70, 520, 330, 490, radius=20, fill='#5F5D6B')  # Right train
        self.rightText = self.c.create_text(200, 497, text="Right", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.rightTrain,'<1>',self.RightClick)
        self.c.tag_bind(self.rightText,'<1>',self.RightClick)

    def RightClick(self,event):
        self.rightClicked=self.round_rectangle(70, 520, 330, 490, radius=20, fill='yellow')  # surprise train
        self.rightTextClicked=self.c.create_text(200, 497, text="Right", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.rightClicked,'<1>',self.RightReleased)
        self.c.tag_bind(self.rightTextClicked, '<1>', self.RightReleased)
        self.right=PhotoImage(file='images/right_transperant.png')
        self.c.create_image(1156,390,image=self.right)
        thread5=threading.Thread(target=self.RightCortex)
        thread5.daemon=True
        thread5.start()

    def RightReleased(self):
        self.rightRetain=self.round_rectangle(70, 520, 330, 490, radius=20, fill='#5F5D6B')  # surprise train
        self.rightTextRetain=self.c.create_text(200, 497, text="Right", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.rightRetain,'<1>',self.RightClick)
        self.c.tag_bind(self.rightTextRetain, '<1>', self.RightClick)
        self.c.create_rectangle(1022, 295, 1290, 485, fill="#342e2e", outline="")  # right
        self.c.create_text(1157, 390, text="RIGHT", fill="#FFFFFF", font="Arial 18 bold")

    """def pushCortex(self):
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
        user = {
            "license": "",
            "client_id": "",
            "client_secret": "",
            "debit": 100,
            "number_row_data": 10
        }
        self.cortex = Cortex(user, debug_mode=True)
        self.headset_id = self.cortex.query_headset()
        self.cortex.connect_headset()
        self.cortex.request_access()
        auth = self.cortex.authorize()
        self.cortex.create_session(auth, self.headset_id)
        profile_name = 'skshreyas'
        training_action = 'push'
        number_of_train = 3

        stream = ['sys']
        self.cortex.sub_request(stream)

        profiles = self.cortex.query_profile()

        # if self.profile_name not in profiles:
        #  status = 'create'
        # self.cortex.setup_profile(self.profile_name, status)

        status = 'load'
        self.cortex.setup_profile(profile_name, status)

        print('begin train -----------------------------------')
        num_train = 0

        while num_train < number_of_train:
            num_train = num_train + 1
            progress['value'] = 33.33 + progress['value']
            top.update_idletasks()
            time.sleep(1)
            print('start training {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'start'
            self.cortex.train_request(detection='mentalCommand',
                                      action=training_action,
                                      status=status)

            print('accept {0} time {1} ---------------'.format(training_action, num_train))
            print('\n')
            status = 'accept'
            self.cortex.train_request(detection='mentalCommand',
                                      action=training_action,
                                      status=status)
            if num_train == 3:
                self.PushReleased()

        print('save trained action')
        status = "save"
        self.cortex.setup_profile(profile_name, status)

        status = 'unload'
        self.cortex.setup_profile(profile_name, status)
        self.cortex.close_session()
        w = Label(top, text="push training completed", font=("Helvetica", 10))
        w.pack()
        Button(top,width=10,height=10,text='ok', command=lambda win=top:win.destroy()).pack(pady=10)
        top.grab_release()
        sys.exit()  # this helps in the binding the thread with daemon and kill the thread using dameon when the frame is closed

    def PushTrainButton(self):
        self.pushTrain = self.round_rectangle(70, 590, 330, 560, radius=20, fill='#5F5D6B')  # Right train
        self.pushText = self.c.create_text(200, 567, text="Push", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.pushTrain,'<1>',self.PushClick)
        self.c.tag_bind(self.pushText,'<1>',self.PushClick)

    def PushClick(self,event):
        self.pushClicked=self.round_rectangle(70, 590, 330, 560, radius=20, fill='yellow')  # surprise train
        self.pushTextClicked=self.c.create_text(200, 567, text="Push", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.pushClicked,'<1>',self.PushReleased)
        self.c.tag_bind(self.pushTextClicked, '<1>', self.PushReleased)
        self.push=PhotoImage(file='images/right_transperant.png')
        self.c.create_image(1156,390,image=self.push)
        thread5=threading.Thread(target=self.pushCortex)
        thread5.daemon=True
        thread5.start()

    def PushReleased(self):
        self.pushRetain=self.round_rectangle(70, 590, 330, 560, radius=20, fill='#5F5D6B')  # surprise train
        self.pushTextRetain=self.c.create_text(200, 567, text="Push", anchor=N, font='Arial 12 ', fill='white')
        self.c.tag_bind(self.pushRetain,'<1>',self.PushClick)
        self.c.tag_bind(self.pushTextRetain, '<1>', self.PushClick)
        self.c.create_rectangle(1022, 295, 1290, 485, fill="#342e2e", outline="")  # right
        self.c.create_text(1157, 390, text="Push", fill="#FFFFFF", font="Arial 18 bold")"""

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

        return self.c.create_polygon(points, **kwargs, smooth=True)

