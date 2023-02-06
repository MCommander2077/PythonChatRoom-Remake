import socket
import threading
import tkinter as tk
import tkinter.messagebox as tkm

import customtkinter as ctk

# 创建套接字
a = 1
# 登陆窗口
loginRoot = ctk.CTk()
loginRoot.title('聊天室')
loginRoot.geometry("400x300")
loginRoot.resizable(0, 0)  # 限制窗口大小

select_path = tk.StringVar()

IP1 = tk.StringVar()
IP1.set('154.12.35.239:5678')  # 默认显示的ip和端口
User = tk.StringVar()
User.set('')
'''Password = tk.StringVar()
Password.set('P^$$W0rd')'''

# 服务器标签
labelIP = ctk.CTkLabel(loginRoot, text='地址:端口')
labelIP.place(x=20, y=10, width=200, height=40)

entryIP = ctk.CTkEntry(loginRoot, width=80, textvariable=IP1)
entryIP.place(x=120, y=10, width=260, height=40)

# 用户名标签
labelUser = ctk.CTkLabel(loginRoot, text='昵称')
labelUser.place(x=30, y=50, width=160, height=40)

entryUser = ctk.CTkEntry(loginRoot, width=80, textvariable=User)
entryUser.place(x=120, y=50, width=260, height=40)

'''
# 密码标签
labelPassword = ctk.CTkLabel(loginRoot, text='密码')
labelPassword.place(x=30, y=90, width=160, height=40)

entryPassword = ctk.CTkEntry(loginRoot, width=80, textvariable=Password)
entryPassword.place(x=120, y=90, width=260, height=40)
'''

# 登录按钮
def login(*args):
    global IP, PORT, user#, Password
    IP, PORT = entryIP.get().split(':')  # 获取IP和端口号
    #Password = entryPassword.get()  # 获取密码
    PORT = int(PORT)                     # 端口号需要为int类型
    user = entryUser.get()
    if not user:
        tkm.showerror('温馨提示', message='请输入任意的用户名！')
    else:
        loginRoot.destroy()                  # 关闭窗口


loginRoot.bind('<Return>', login)            # 回车绑定登录功能
but = ctk.CTkButton(loginRoot, text='登录', command=login)
but.place(x=10, y=150, width=70, height=30)

loginRoot.mainloop()

socket_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 此处端口看服务端的端口，127.0.0.1要改成服务端主机的ipv4地址
print((IP , PORT))
socket_connect.connect((IP, PORT))
socket_connect.send(User.get().encode())

def receive(s, msg_text):
    socket_connect.recv(1024).decode('utf-8')
    # recv_data = socket_connect.recv(1024).decode('utf-8')
    # msg_text.insert(tk.END, recv_data)
    while 1:
        recv_data = socket_connect.recv(1024).decode('utf-8')
        msg_text.insert(tk.END, recv_data)


def send(*args):
    global a
    if a == 0:
        msg = input_text.get('0.0', tk.END)
        socket_connect.send(msg.encode('utf-8'))
        input_text.delete('0.0', tk.END)
    else:
        msg = input_text.get('0.0', tk.END)
        socket_connect.send(msg.encode('utf-8'))
        input_text.delete('0.0', tk.END)
        msg_text.delete('0.0', tk.END)
        a = 0


app = ctk.CTk()
app.title('ChatRoom')
# 显示消息框
msg_frame = ctk.CTkFrame(app, width=480, height=300)
msg_frame.grid(row=0, column=0, padx=6, pady=6)
msg_frame.grid_propagate(0)  # 固定Frame的大小
msg_text = tk.Text(msg_frame, bg='white')
msg_text.grid()
# msg_text.insert('0.0','hhh')
# 输入
input_frame = ctk.CTkFrame(app, width=480, height=100)
input_frame.grid(row=1, column=0)
input_frame.grid_propagate(0)
input_text = tk.Text(input_frame, bg='white')
input_text.grid()
# 发送按钮
btn_frame = ctk.CTkFrame(app, width=480, height=20)
btn_frame.grid(row=2, column=0, sticky='E')
button = ctk.CTkButton(btn_frame, text='发送', command=send)
app.bind('<Return>', send)
button.grid()
# 线程
receive_thread = threading.Thread(
    target=receive, args=(socket_connect, msg_text))
receive_thread.daemon = True
receive_thread.start()

app.mainloop()
socket_connect.close()
