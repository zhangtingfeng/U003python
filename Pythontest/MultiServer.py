import hashlib
import threading
import time
import traceback
from configparser import ConfigParser
from socket import *
from tkinter import *

import pymssql
# 创建SqlServer连接
import _mssql
import uuid
import decimal

address = '0.0.0.0'
port = 19101

cf = ConfigParser()
f = open('Data.ini')
cf.read_file(f)
address = cf.get('Server', 'host')
port = int(cf.get('Server', 'port'))
DBhost = cf.get('DB', 'host')
DBuser = cf.get('DB', 'user')
DBpassword = cf.get('DB', 'password')
DBdatabase = cf.get('DB', 'database')
f.close()

buffsize = 1024
s = socket(AF_INET, SOCK_STREAM)
s.bind((address, port))
s.listen(50)  # 最大连接数
conn_list = []
conn_dt = {}
conn_dt_MobilePhone = {}


def tcplink(sock, addr):
    while True:
        try:
            recvdata = sock.recv(buffsize).decode('utf-8')
            print(recvdata, addr)
            hello_str = recvdata.split("###")
            # if 1==1:
            if hello_str[0] == "UserLogin":
                print(hello_str)
                print(conn_dt_MobilePhone)

                m2 = hashlib.md5()
                m2.update((hello_str[2] + "LY_BPM_2019_1_3").encode('utf-8'))
                passwordMD5 = m2.hexdigest()

                # 创建SqlServer连接
                # import pymssql
                conn = pymssql.connect(host=DBhost, user=DBuser, password=DBpassword, database=DBdatabase)
                # 如果和本机数据库交互，只需修改链接字符串
                # conn=pymssql.connect(host='.',database='FamilyDoctor')
                # 创建游标
                strSQL = "select count(1) as RecordCount FROM CM_IDUsers where Mobile='" + hello_str[1] + "' and Password='" + passwordMD5 + "'"
                # print(strSQL)
                cur = conn.cursor()
                cur.execute(strSQL)
                # 如果update/delete/insert记得要conn.commit()
                # 否则数据库事务无法提交
                # print(cur.fetchall())
                row = cur.fetchone()
                print(row[0])
                intCanLogin = int(row[0])
                # 关闭游标
                cur.close()
                # 关闭连接
                conn.close()
                if intCanLogin >= 1:
                    conn_dt_MobilePhone[addr] = hello_str[1]
                    strwillsend = "UserLogin###LoginType###True###" + time.strftime("%Y-%m-%d %X")
                    conn_dt[addr].sendall(strwillsend.encode('utf-8'))
                    recvdata+=strwillsend
                else:
                    strwillsend = "UserLogin###LoginType###False###" + time.strftime("%Y-%m-%d %X")
                    conn_dt[addr].sendall(strwillsend.encode('utf-8'))
                    recvdata += strwillsend
                    if addr in conn_dt_MobilePhone.keys():
                        conn_dt_MobilePhone.pop(addr)

            gui.infoList.config(state=NORMAL)
            gui.infoList.insert(END, addr, 'name')
            gui.infoList.insert(END, '：\t')
            gui.infoList.insert(END, recvdata, 'conment')
            gui.infoList.insert(END, '\n\n')
            gui.infoList.config(state=DISABLED)
            if not recvdata:
                break
        except Exception as e:
            sock.close()
            print(addr, 'offline')
            _index = conn_list.index(addr)
            gui.listBox.delete(_index)
            conn_dt.pop(addr)
            conn_list.pop(_index)
            conn_dt_MobilePhone.pop(addr)

            # print('str(Exception):\t', str(Exception))
            # print('str(e):\t\t', str(e))
            # print('repr(e):\t', repr(e))
            # print('e.message:\t', e.message)
            # print('traceback.print_exc():';traceback.print_exc())
            # print('traceback.format_exc():\n%s' % traceback.format_exc())
            traceback.print_exc()
            break


def CheckSQLSERVER():
    strMoblie = ""
    for value in conn_dt_MobilePhone.values():
        # print(value)
        strMoblie += ("'" + value + "',")
    if strMoblie == "":
        return

    strMoblie += "''"

    strSQL = "SELECT top 1 CM_IDUsers.Mobile, Z04_CSMessage.CSMessageID,Z04_CSMessage.TaskType, Z04_CSMessage.TaskMess,Z04_CSMessage.TaskInsertTime"
    strSQL += "    FROM      CM_Employees LEFT OUTER JOIN"
    strSQL += "    CM_IDUsers ON CM_Employees.Tab_UserID = CM_IDUsers.UserID AND"
    strSQL += "    CM_Employees.TenantID = CM_IDUsers.DefaultTenant RIGHT OUTER JOIN"
    strSQL += "    Z04_CSMessage ON CM_Employees.TenantID = Z04_CSMessage.TenantID AND"
    strSQL += "   CM_Employees.UserID = Z04_CSMessage.UserID"
    strSQL += " where  Z04_CSMessage.Finished=0 and CM_IDUsers.Mobile in (" + strMoblie + ")"
    strSQL += " order by Z04_CSMessage.CreatedTime desc"
    print(strSQL)
    # conn = pymssql.connect(host='123.57.163.87', user='jin', password='p@ssw0rd', database='BPM_LY')
    conn = pymssql.connect(host=DBhost, user=DBuser, password=DBpassword, database=DBdatabase)
    # 如果和本机数据库交互，只需修改链接字符串
    # conn=pymssql.connect(host='.',database='FamilyDoctor')
    # 创建游标
    # print(strSQL)
    cur = conn.cursor()
    rowcount = cur.execute(strSQL)
    # 如果update/delete/insert记得要conn.commit()
    # 否则数据库事务无法提交

    # print(cur.fetchall())
    row = cur.fetchone()
    # rowcount = cur.rowcount

    # intCanLogin = int(row[0])
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    # print("rowcount="+str(rowcount))
    if row is not None:
        databaseMobile = row[0]
        databaseCSMessageID = row[1]
        TaskType = row[2]
        TaskMess = row[3]
        TaskInsertTime = row[4]

        print(databaseMobile)
        print(databaseCSMessageID)
        for key in conn_dt_MobilePhone:
            if conn_dt_MobilePhone[key] == databaseMobile:
                print(key)
                conn_dt[key].sendall(("PlayAlert###Alert1###3###" + TaskType + "###" + TaskMess + "###" + TaskInsertTime.strftime("%Y-%m-%d %X")).encode('utf-8'))
                strupdateSQL = "update Z04_CSMessage set Finished=1,FinishedTime=getdate(),ModifiedTime=getdate(),ModifiedBy='提取服务警告' where CSMessageID='" + databaseCSMessageID + "'"
                conndb = pymssql.connect(host=DBhost, user=DBuser, password=DBpassword, database=DBdatabase)
                curdb = conndb.cursor()
                curdb.execute(strupdateSQL)
                effectrow = curdb.rowcount  # 是否可以获取返回操作数据库影响的行数？
                print("effectRow是否可以获取返回操作数据库影响的行数=" + str(effectrow) + strupdateSQL)
                # 关闭游标
                curdb.close()
                # 关闭连接
                conndb.commit()
                conndb.close()
        time.sleep(0.2)
        CheckSQLSERVER()  # 重新连接检查数据库   有数据才继续检查


def conn_dt_MobilePhoneTask():
    while True:
        time.sleep(3)
        intneedrecord = len(conn_dt_MobilePhone)
        if intneedrecord > 0:
            CheckSQLSERVER()


def recs():
    while True:
        clientsock, clientaddress = s.accept()
        if clientaddress not in conn_list:
            conn_list.append(clientaddress)
            conn_dt[clientaddress] = clientsock
            gui.listBox.insert(END, clientaddress)
            # conn_dt_MobilePhone[clientaddress] = "13901888127"
        print('connect from:', clientaddress)
        # 在这里创建线程，就可以每次都将socket进行保持
        t = threading.Thread(target=tcplink, args=(clientsock, clientaddress))
        t.start()


class GUI:
    def __init__(self, root):
        self.root = root
        self.leftFrame = Frame(self.root, width=20, height=30)
        self.leftFrame.grid(row=0, column=0)
        self.rightFrame = Frame(self.root, width=20, height=30)
        self.rightFrame.grid(row=0, column=1)
        Label(self.leftFrame, text='在线IP地址列表').grid(row=0, column=0)

        self.listBox = Listbox(self.leftFrame, width=15, height=10)
        self.listBox.grid(row=1, column=0)
        self.entry = Entry(self.rightFrame, font=('Serief', 18), width=30)
        self.entry.grid(row=0, column=0)
        self.sendBtn = Button(self.rightFrame, text='发送', command=self.send, width=10)
        self.sendBtn.grid(row=0, column=1)

        Label(self.rightFrame, text='聊天信息').grid(row=1, columnspan=2)
        self.infoList = Text(self.rightFrame, width=40, height=12)
        self.infoList.grid(row=2, columnspan=2)
        self.infoList.tag_config('name', background='yellow', foreground='red')
        self.infoList.tag_config('conment', background='black', foreground='white')

    def send(self):
        _index = self.listBox.curselection()
        conn_dt[self.listBox.get(_index)].sendall(self.entry.get().encode('utf-8'))
        # self.entry.delete(0, END)


def createGUI():
    global gui
    root = Tk()
    gui = GUI(root)
    root.title('服务提醒服务器端')
    root.mainloop()


if __name__ == '__main__':
    t1 = threading.Thread(target=recs, args=(), name='rec')
    t2 = threading.Thread(target=createGUI, args=(), name='GUI')
    t3CheckSQLSERVER = threading.Thread(target=conn_dt_MobilePhoneTask, args=(), name='conn_dt_MobilePhoneTask')

    t1.start()
    t2.start()
    t3CheckSQLSERVER.start()
