from tkinter import *
from tkinter import messagebox
import PIL.Image
from PIL import ImageTk
from connector import *
from IOT import eyeblink
from facial_expression_Train import FacialExpression
from Cursor_Train import CursorTrainer
from facialExpressionLive import FacialExpressionLive
from ActSpeak import Act2Speak
from Cursor_live_mode import CursorLive
class SampleApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_iconbitmap('logo.ico')
        self.title('BCOT')
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.frames = {
            "StartPage": StartPage,
            "Navigator":Navigator,
            "eyeblink":eyeblink,
            "FacialExpression":FacialExpression,
            "CursorTrainer":CursorTrainer,
            "FacialExpressionLive":FacialExpressionLive,
            "Act2Speak":Act2Speak,
            "CursorLive":CursorLive
        }

        self.show_frame("FacialExpression")

    def show_frame(self, page_name):
        # destroy the old frame
        for child in self.container.winfo_children():
            child.destroy()
        if page_name == 'eyeblink':
            #frame_class = self.frames[page_name]
            self.after(7000,self.show_frame,"Navigator")
        # create the new frame
        frame_class = self.frames[page_name]
        frame = frame_class(parent=self.container, controller=self)
        frame.pack(fill="both", expand=True)

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller=controller
        canvas = Canvas(self,width=2085, height=1080, bg='#020A2E')
        canvas.pack()
        self.img = PIL.Image.open("images/b100.png")
        self.my_img = ImageTk.PhotoImage(self.img)
        canvas.create_image(200, 310, image=self.my_img, tags='close_tag')
        self.imgg = PIL.Image.open("images/c100.png")
        self.myimg = ImageTk.PhotoImage(self.imgg)
        canvas.create_image(470, 310, image=self.myimg)
        self.oimage = PIL.Image.open("images/o100.png")
        self.omg = ImageTk.PhotoImage(self.oimage)
        canvas.create_image(820, 310, image=self.omg)
        self.timg = PIL.Image.open("images/t100.png")
        self.tmg = ImageTk.PhotoImage(self.timg)
        canvas.create_image(1150, 310, image=self.tmg)
        canvas.create_text(665, 540, text="connect to headset", anchor=S, font='Arial 8 ', fill='white')
        self.url = "wss://localhost:6868"
        self.user = {
            "license": "1d10f0b4-65e4-4424-ae8a-a56ae2fa6950",
            "client_id": "uNU5UMKd9eFLYp8JtHr6ZXXaLHg1p6rf1BReVn4N",
            "client_secret": "9wcDtQn2Wubjg7zzlO2tnkx8Hzk1GkLpqZsqgOiuaWsaI0VRkxcxeQ9ZOPrHrNvJ1tlgOAV1XEZ6ooxJ06sRwobXDApRsol08w9YsJWU0fVAieWYp6kHexOlM9OWqXWk",
            "debit": 100
            # "number_row_data" : 10
        }
        connect = Button(self,width=15, height=1, bd=0, bg='#2C3547', text="CONNECT", relief=RAISED,
                            font='Arial 10 bold ', fg='white', command=self.connection).place(x=600, y=500)
        self.next = PIL.Image.open("images/next.png")
        self.img_nxt = ImageTk.PhotoImage(self.next)

        Button(width=35, height=30, bg='#020A2E', image=self.img_nxt, bd=0, command=lambda: controller.show_frame('Navigator')).place(x=1320, y=10)

    def connection(self):
        c = Cortex(self.url, self.user)
        headset_id = c.query_headset()
        c.connect_headset()
        c.request_access()
        auth = c.authorize()
        val=c.create_session(auth, headset_id)
        if val == "error":
            messagebox.showinfo("BCOT","headset is not connected")
        else:
            messagebox.showinfo("BCOT","headset is connected")

class Navigator(Frame):
    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller=controller
        self.image1 = PhotoImage(file=r'images/iot.png')
        self.image2 = PhotoImage(file=r'images/facialExp.png')
        self.image3 = PhotoImage(file=r'images/cursor.png')
        self.image4 = PhotoImage(file=r'images/mindR.png')
        self.imgg = PhotoImage(file=r'images/arrow.png')
        self.controller = controller
        self.canvas = Canvas(self,width=2085, height=1080, bg='#020A2E')
        self.canvas.pack()
        label = Label(self,text="FEATURES", bg='#020A2E', fg='white', font='Arial 50 bold').place(x=80, y=20)
        arrow = Button(self,width=40, height=30, bg='#020A2E', image=self.imgg, bd=0,
                       command=lambda:controller.show_frame("StartPage")).place(x=10, y=10)

        button1 =Button(self,width=200, height=215, bg="#3A3535", bd=0, image=self.image1,command=lambda:controller.show_frame("eyeblink")).place(x=380, y=150)
        self.canvas.create_rectangle(75, 150, 380, 365, fill='#615A5A')
        self.canvas.create_text(220, 160, text="BLINK FOR ON/OFF", anchor=N, font='Arial 14 bold', fill='white')
        self.canvas.create_text(223,230,text="  Feature contains IOT Devices-\n"
                                             "  Focus over the icon and blink twice\n"
                                             "  to turn on/off.",font='Arial 12 bold',fill='white')
        self.canvas.create_text(220, 270, text="      This feature will be active for 7 seconds and the\n"
                                               "      frame  will  automatically  closes by  itself, after \n"
                                               "      the frame is opened wait for 3  seconds to, then \n"
                                               "      start to blink.", anchor=N, font='Arial 9 bold', fill='white')


        button2 = Button(self,width=200, height=215, bg="#3A3535", bd=0, image=self.image2,command=lambda:controller.show_frame("FacialExpression")).place(x=1100, y=150)
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

        button3 = Button(self,width=200, height=215, bg="#3A3535", bd=0, image=self.image3,command=lambda:controller.show_frame("CursorTrainer")).place(x=380, y=450)
        self.canvas.create_rectangle(75, 450, 380, 667, fill='#615A5A')
        self.canvas.create_text(220, 460, text="CURSOR CONTROL", anchor=N, font='Arial 14 bold', fill='white')
        # canvas.create_rectangle(50,430,607,690,fill='#FFFFFF')
        self.canvas.create_text(223, 530, text="  The feature has 4 mental commands\n"
                                               "   to train  and  live mode frame allows\n"
                                               "   to control the whole application.", font='Arial 12 bold', fill='white')
        self.canvas.create_text(223, 600, text="  The  training  frame  has  4  mental  commands\n"
                                               "  that  needs  to  be trained, if the live  feed is not\n"
                                               "  accurate then train  neutral more. The live feed \n"
                                               "  takes 3 sec to initiate connection.", font='Arial 9 bold',fill='white')


        button4 = Button(self,width=200, height=215, bg="#3A3535", bd=0, image=self.image4,command=lambda:controller.show_frame("Act2Speak")).place(x=1100, y=450)
        self.canvas.create_rectangle(795, 450, 1100, 669, fill='#615A5A')
        self.canvas.create_text(950, 460, text="ACT TO SPEECH", anchor=N, font='Arial 14 bold', fill='white')
        # canvas.create_rectangle(770,430,1325,688,fill='#FFFFFF')
        self.canvas.create_text(948, 530, text="This feature  has an  Artificial voice -\n"
                                               " speaks when muscular movement is\n"
                                               " made or thought about something.", font='Arial 12 bold', fill='white')
        self.canvas.create_text(948, 600, text="This allows person to make 8 different speechs\n"
                                               "the number can be increased but it takes more\n"
                                               "cognitive ability.",font='Arial 9 bold',fill='white')

        self.my_img = PhotoImage(file="images/sky.png")
        self.my_rectangle = self.canvas.create_image(330, 255, image=self.my_img, tags='close_tag')
        # my_rectangle=canvas.create_rectangle(50,130,610,390,fill="#FFFFFF", stipple="gray12")
        parent.master.bind("<Left>", self.left)
        parent.master.bind("<Right>", self.right)
        parent.master.bind("<Up>", self.up)
        parent.master.bind("<Down>", self.down)

    def left(self, event):
        x = -720
        y = 0
        # xx=event.xx
        # yy=event.yy
        pos = self.canvas.coords('close_tag')
        if pos == [1050.0, 255.0] or pos == [1050.0, 555.0]:
            print('left', pos)
            self.canvas.move(self.my_rectangle, x, y)

    def right(self, event):
        x = 720
        y = 0
        pos = self.canvas.coords('close_tag')
        if pos == [330.0, 255.0] or pos == [330.0, 555.0]:
            print('right', pos)
            self.canvas.move(self.my_rectangle, x, y)

    def up(self, event):
        x = 0
        y = -300
        pos = self.canvas.coords('close_tag')
        if pos == [330.0, 555.0] or pos == [1050.0, 555.0]:
            print('up', pos)
            self.canvas.move(self.my_rectangle, x, y)

    def down(self, event):
        x = 0
        y = 300
        pos = self.canvas.coords('close_tag')
        if pos == [330.0, 255.0] or pos == [1050.0, 255.0]:
            print('down', pos)
            self.canvas.move(self.my_rectangle, x, y)



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()