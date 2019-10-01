#_*_coding:utf-8 _*_
#auther    :LEO.TAN
#buildtime :2019/1/15 18:03
#file      :login.py
#IDE       :PyCharm

import pickle  # 存放数据的模块
import tkinter as tk
import tkinter.messagebox
import ThreadPlayWav,threading,pygame,time


window = tk.Tk()
window.iconbitmap("Img/lvyanlogo.ico")
window.title("智慧服务提醒服务")

# 计算窗口居中的位置
def get_window_positon(width, height):
    nScreenWid, nScreenHei = window.maxsize()
    window_x_position = (nScreenWid - width) // 2
    window_y_position = (nScreenHei - height) // 2
    return window_x_position, window_y_position
# 设置窗口属性
# login = tkinter.Tk()
# login.title('此处输入窗口的标题')
tk_width = 500  # 窗口的宽度
tk_height = 400 # 窗口的长度
pos = get_window_positon(tk_width, tk_height) #调用get_window_positon()方法
window.geometry(f'{tk_width}x{tk_height}+{pos[0]}+{pos[1]}') # 窗口的大小与位置
window.resizable(False, False) # 窗口大小不可变
booleanIFFlash=0#是否闪烁标志
#window.geometry("500x400")

canvaslogo = tk.Canvas(window, height=120, width=120)
image_file = tk.PhotoImage(file="Img/60x60.png")
image = canvaslogo.create_image(0, 60, anchor='nw', image=image_file)
canvaslogo.pack(side='top')


tk.Label(window, text='用户名:').place(x=50, y=200)
tk.Label(window, text='密码:').place(x=50, y=250)

var_usr_name = tk.StringVar()
var_usr_name.set('请输入用户名')

var_usr_pwd = tk.StringVar()
#var_usr_pwd.set('请输入密码')

entry_usr_name = tk.Entry(window, textvariable=var_usr_name)
entry_usr_name.place(x=160, y=200)
entry_usr_pwd = tk.Entry(window, textvariable=var_usr_pwd, show='*')
entry_usr_pwd.place(x=160, y=250)

booleanIFFlash=0

def PlaySound_time():
    # intNumber = 0
    # global booleanIFFlash
    # while 1:
    #
    #     booleanIFFlash = 1
    import winsound
    winsound.PlaySound('Wav/Play.wav',winsound.SND_FILENAME)
    winsound.PlaySound('Wav/Play.wav', winsound.SND_FILENAME)
    winsound.PlaySound('Wav/Play.wav', winsound.SND_FILENAME)
    global booleanIFFlash
    booleanIFFlash = 0
    #pygame.init()
        #pygame.display.set_mode([1, 1])
        # if pygame.mixer.music.get_busy() == False:
        #     if intNumber == 3:
        #         break
        #     else:
        #         intNumber = intNumber + 1
        #         print('is playing!' + str(intNumber))
        #         #screen = pygame.display.set_mode([640, 480])
        #         #pygame.mixer.music.load('Wav/outgoing.wav')
        #         #pygame.mixer.music.play()
        # else:
        #     flashLogofun_timer()
        #     time.sleep(0.1)
        #     print(booleanIFFlash)

    booleanIFFlash = 0
    return

    # pygame.init()
    # pygame.display.set_mode([1, 1])
    # pygame.mixer.music.load('Wav/outgoing.wav')
    # pygame.mixer.music.play()
    # time.sleep(2)
    # global booleanIFFlash
    # booleanIFFlash = 0
    # return

def flashLogofun_timer():
    #print('hello timer') #打印输出
    # window.title("智慧服务提醒服务111")
    # image_file = tk.PhotoImage(file="Img/Icon-1024.png")
    # image = canvas.create_image(0, 60, anchor='nw', image=image_file)
    # canvas.pack(side='top')
    #image = addTransparency(image, factor=0.7)
    if booleanIFFlash == 1:
        if canvaslogo.winfo_viewable():
            canvaslogo.forget()
        else:
            canvaslogo.pack()
    else:
        canvaslogo.pack()
    global timer #定义变量
    timer = threading.Timer(0.5,flashLogofun_timer) #60秒调用一次函数
    #定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer.start()  #启用定时器




def usr_Logout():

   # timer11 = threading.Timer(0.1, PlaySound_time)  # 首次启动
   # timer11.start()
   # timer11.abort()
    global booleanIFFlash
    booleanIFFlash=1
    #  t = threading.Thread(target=PlaySound_time(), name="MyThread")
    t = threading.Timer(1, PlaySound_time)  # 首次启动
    t.start()
    print("111111111111111111exit")

def usr_login():
    usr_name = var_usr_name.get()
    usr_pwd = var_usr_pwd.get()

    try:
        with open("usrs_info.pickle", "rb") as usr_file: #注意这个地方用到了pickle可以百度一下使用方法
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open("usrs_info.pickle", "wb") as usr_file:  # with open with语句可以自动关闭资源
            usrs_info = {"admin": "admin"}  # 以字典的形式保存账户和密码
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title="Welcome", message="How are you! " + usr_name)
        else:
            tk.messagebox.showerror(message="Error,your password is wrong,try again")
    else:
        is_sign_up = tk.messagebox.askyesno("Welcome", "You have not sign up yet.Sign up today?")
        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    def sign_to_Python():
        signpwd = sign_pwd.get()
        signpwdconfirm = sign_pwd_confirm.get()
        signname = sign_name.get()
        with open("usrs_info.pickle", "rb") as usr_file:
            exist_usr_info = pickle.load(usr_file)
        if signpwd != signpwdconfirm:
            tk.messagebox.showerror("Error", "Password and confirm password must be the same!")
        elif signname in exist_usr_info:
            tk.messagebox.showerror("Error", "The user has already signed up! ")
        else:
            exist_usr_info[signname] = signpwd
            with open("usrs_info.pickle", "wb") as usr_file:
                pickle.dump(exist_usr_info, usr_file)

            tk.messagebox.showinfo("Welcome", "You have successfully signed up!")
            # close window
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(window)
    window_sign_up.geometry("350x200")
    window_sign_up.title("注册页面")

    sign_name = tk.StringVar()
    sign_name.set('请输入用户名')
    tk.Label(window_sign_up, text="User name:").place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=sign_name)
    entry_new_name.place(x=150, y=10)

    sign_pwd = tk.StringVar()
    tk.Label(window_sign_up, text="Password:").place(x=10, y=50)
    entry_usr_pwd = tk.Entry(window_sign_up, textvariable=sign_pwd, show='*')
    entry_usr_pwd.place(x=150, y=50)

    sign_pwd_confirm = tk.StringVar()
    tk.Label(window_sign_up, text="Confirm password:").place(x=10, y=90)
    entry_usr_pwd_confirm = tk.Entry(window_sign_up, textvariable=sign_pwd_confirm, show='*')
    entry_usr_pwd_confirm.place(x=150, y=90)

    btn_confirm_sign_up = tk.Button(window_sign_up, text="Sign up", command=sign_to_Python)
    btn_confirm_sign_up.place(x=150, y=130)


# login and sign up
btn_login = tk.Button(window, text="播放", command=usr_Logout)
btn_login.place(x=155, y=300)

btn_sign_up = tk.Button(window, text="登陆", command=usr_sign_up)
btn_sign_up.place(x=270, y=300)

window.mainloop()