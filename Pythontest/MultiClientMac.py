# import tkinter
# from distutils.command.config import config
import time
from socket import *
import threading
from tkinter import *
import os
import tkinter.messagebox
# from PyQt5.QtWidgets import QApplication,QWidget
# from PyQt5.QtGui import QIcon
# from PTL import Image,ImageTk
from tkinter import messagebox
import pyttsx3
import pyttsx3.drivers
#import pyttsx3.drivers.sapi5
#import pythoncom

from configparser import ConfigParser
import ThreadPlayWav

address='10.0.0.21'   #服务器的ip地址  UserLogin###13901888127###666666
port=19101

cf = ConfigParser()
f = open("ClientData.ini")
cf.read_file(f)
address = cf.get('Server', 'host')
port = int(cf.get('Server', 'port'))
f.close()
buffsize=1024

# print(address)
# print(port)

globalsocket=socket(AF_INET, SOCK_STREAM)
globalsocket.connect((address,port))



booleanIFFlash = 0
timer=None
Labelusernamestatus=None

def flashLogofun_timer():

    # //return
    global booleanIFFlash
    # gui.image = gui.canvaslogo.create_image(1000, 200, anchor='nw', image=gui.image_file)
    # print(booleanIFFlash)
    if booleanIFFlash == 1:
        if gui.canvaslogo.winfo_viewable():
            gui.canvaslogo.forget()
        else:
            gui.canvaslogo.pack()
    elif booleanIFFlash == 0:
        gui.canvaslogo.pack()
    # print(gui.canvaslogo)
    if booleanIFFlash == 1:
        global timer #定义变量
        timer = threading.Timer(0.5,flashLogofun_timer) #60秒调用一次函数
        #定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
        timer.start()  #启用定时器

def PlaySound_time(msg1):
    global booleanIFFlash,timer
    #import winsound
    while booleanIFFlash == 1:
        time.sleep(1) # 暂停 1 秒

    booleanIFFlash=1
    timer = threading.Timer(0.1, flashLogofun_timer)  # 首次启动
    timer.start()
    # print(msg1)

    #pythoncom.CoInitialize()
    engine = pyttsx3.init()
    # languages = engine.getProperty('languages')
    # print(languages)
    # volume = engine.getProperty('volume')
    # print(volume)
    # engine.setProperty('volume', volume + 1.25)
    # volume = engine.getProperty('volume')
    print(msg1)
    engine.say(msg1)
    engine.runAndWait()
    # winsound.PlaySound('Wav/Play.wav',winsound.SND_FILENAME)
    # winsound.PlaySound('Wav/Play.wav', winsound.SND_FILENAME)
    # winsound.PlaySound('Wav/Play.wav', winsound.SND_FILENAME)
    booleanIFFlash=0
    return



def recvServerdata():
    while True:
        print('开始检测服务方应答\n')
        recvdata = globalsocket.recv(buffsize).decode('utf-8')
        #gui.listBox.insert(END, recvdata)
        print('收到服务方应答\n' + recvdata + '\n')
        hello_str = recvdata.split("###")
        if hello_str[0] == "PlayAlert":
            t = threading.Timer(1, PlaySound_time,[hello_str[4]])  # 首次启动
            t.start()
            gui.listBox.insert(END, hello_str[5]+"["+hello_str[3] + "]"+hello_str[4])
        elif hello_str[0] == "UserLogin":
            if hello_str[1] == "LoginType":
                if hello_str[2] == "True":
                    Labelusernamestatus.config(text="成功登录")
                    gui.listBox.insert(END, gui.entryusername.get()+"成功登录")

                    mycf = ConfigParser()
                    # 先读出来
                    mycf.read("ClientData.ini", encoding="utf-8")
                    # fileOpenmycf = open("ClientData.ini")

                    mycf.set("UserAccount", "mobile", gui.entryusername.get())
                    mycf.set("UserAccount", "passwordencode", gui.entryuserPassword.get())

                    mycf.write(open("ClientData.ini",  "r+", encoding="utf-8"))  # 追加模式写入
                    # fileOpenmycf.close()

                    #messagebox.showinfo("提示", "成功登录")

                else:
                    Labelusernamestatus.config(text="登录不成功")
                    gui.listBox.insert(END, gui.entryusername.get()+"登录不成功")
                    #messagebox.showinfo("提示", "登录不成功")


class GUI:
    def __init__(self, argroot):

        self.root = argroot

        self.canvaslogo = Canvas(self.root, width=220, height=80)
        self.image_file = PhotoImage(file="60x60.png")
        self.image = self.canvaslogo.create_image(100,20, anchor='nw', image=self.image_file)
        self.canvaslogo.pack()

        #self.canvaslogo.place(x=3,y=0,anchor=NW)
        #self.canvaslogo.forget()

        # self.setWindowFlags(Qt.Qt.CustomizeWindowHint)
        self.Labelusername = Label(self.root, text='用户名:')
        self.Labelusername.place(x=60,y=110,anchor=NW)

        f = open("ClientData.ini")
        cf.read_file(f)
        mobile = cf.get('UserAccount', 'mobile')
        passwordencode = cf.get('UserAccount', 'passwordencode')
        f.close()
        self.stringmobile = StringVar()
        self.stringmobile.set(mobile)
        self.stringpasswordencode = StringVar()
        self.stringpasswordencode.set(passwordencode)

        self.entryusername = Entry(self.root,textvariable =self.stringmobile)
        self.entryusername.place(x=120, y=110, anchor=NW)

        self.LabeluserPassword = Label(self.root, text='用户名:')
        self.LabeluserPassword.place(x=60, y=140, anchor=NW)

        self.entryuserPassword = Entry(self.root, textvariable=self.stringpasswordencode, show='*')
        self.entryuserPassword.place(x=120, y=140, anchor=NW)

        global Labelusernamestatus
        Labelusernamestatus = Label(self.root, text='尚未登录')
        Labelusernamestatus.place(x=280, y=110, anchor=NW)

        self.LoginBtn = Button(self.root, text='登录', command=self.login)
        self.LoginBtn.place(x=120, y=180, anchor=NW)
        self.LoginBtn = Button(self.root, text='注销', command=self.logout)
        self.LoginBtn.place(x=180, y=180, anchor=NW)

        self.scrolly = Scrollbar(self.root)
        self.scrolly.place(x=485, y=215, width=15.9, height=160.9, anchor=NW)
        self.listBox = Listbox(self.root, yscrollcommand=self.scrolly.set)
        self.listBox.place(x=5, y=220, width=480, height=150.9, anchor=NW)
        self.scrolly.config(command=self.listBox.yview)
        #self.listBox.pack()

        # self.entry = Entry(self.root)
        # self.entry.pack()
        # self.sendBtn = Button(self.root, text='发送', command=self.send)
        # self.sendBtn.pack()
        if len(mobile)>0 and len(passwordencode):
            self.login()
        # global booleanIFFlash
        # global timer
        # booleanIFFlash = 0
        # timer = threading.Timer(0.1, flashLogofun_timer)  # 首次启动
        # timer.start()
        print(1111111111111)
        return


    def login(self):
        # t = threading.Timer(1, PlaySound_time)  # 首次启动
        # t.start()

        senddataentryusername = self.entryusername.get()
        senddataentryuserPassword = self.entryuserPassword.get()
        strwillsend="UserLogin###"+senddataentryusername+"###"+senddataentryuserPassword
        Labelusernamestatus.config(text=(senddataentryusername+"正在登录"))
        globalsocket.send(strwillsend.encode())
    def logout(self):
        self.entryusername.delete(0,END)
        self.entryuserPassword.delete(0, END)
        self.entryuserPassword.select_clear()
        Labelusernamestatus.config(text="注销登录")



# 计算窗口居中的位置
def get_window_positon(argrootWindow,width, height):
    nScreenWid, nScreenHei = argrootWindow.maxsize()
    window_x_position = (nScreenWid - width) // 2
    window_y_position = (nScreenHei - height) // 2
    return window_x_position, window_y_position

def CallbackClose():
    if tkinter.messagebox.askyesno(title='警告',message='确认关闭吗？'):
        os._exit(0)

def createGUI():
    global gui
    rootWindow = Tk()
    gui = GUI(rootWindow)
    # rootWindow.iconbitmap("Img/lvyanlogo.ico")
    print('绿雁信息科技（上海）有限公司  智慧服务提醒')
    rootWindow.title('绿雁信息科技（上海）有限公司  智慧服务提醒')
    rootWindow.protocol("WM_DELETE_WINDOW",CallbackClose)
    # rootWindow.overrideredirect(True)
    # rootWindow.setWindowFlags(Qt.Qt.CustomizeWindowHint)
    tk_width = 500  # 窗口的宽度
    tk_height = 400  # 窗口的长度
    #rootWindow.setWindowIcon(QIcon("Img/lvyanlogo.ico"))
    pos = get_window_positon(rootWindow,tk_width, tk_height)  # 调用get_window_positon()方法
    rootWindow.geometry(f'{tk_width}x{tk_height}+{pos[0]}+{pos[1]}')  # 窗口的大小与位置
    rootWindow.resizable(False, False)  # 窗口大小不可变

    rootWindow.mainloop()




if __name__ == '__main__':

    #t2 = threading.Thread(target=createGUI, args=(), name='gui')
    #rint('1111')
    t1 = threading.Thread(target=recvServerdata, args=(), name='recvServerdata')
    t1.start()

    createGUI()
    #print('222')
    #recvServerdata()


    #t2.start()


