import socket,threading #导入文件
def receive(new_s,socket_list):#创建一个收的函数
    try:
        nikename = new_s.recv(1024).decode('utf-8').strip()#为当前客户端执行一次‘收'来获取
    except:
        new_s.close()#关闭当前客户端的套接字
        socket_list.remove(new_s)#去除套接字列表里的nes_s
        for i in socket_list:
            i.send('\n公告:一个未知的人离开了聊天室'.encode('utf-8'))#广播
        return None
    for i in socket_list:
        i.send(f'\n公告:欢迎{nikename}进入了聊天室\n'.encode('utf-8'))#广播
    while 1:
        try:
            recv_data = new_s.recv(1024).decode('utf-8')#如果接受到了客户端发来的信息
            print(recv_data)#仅作提醒用
            for i in socket_list:
                i.send(f'{nikename}:{recv_data}'.encode('utf-8'))#广播
        except:
            new_s.close()#关闭当前客户端的套接字
            socket_list.remove(new_s)#去除套接字列表里的nes_s
            for i in socket_list:
                i.send(f'公告:{nikename}离开了聊天室'.encode('utf-8'))#广播
            break#跳出循环
def send(new_s):
    while 1:
        msg = input('')#发出
        new_s.send(msg.encode('utf-8'))
#创建套接字
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cip = input('ip')
cport = input('port')
#绑定
s.bind((str(cip),int(cport)))#端口
#监听
s.listen(5)
print('listening on' + cip + cport)
socket_list = []
while 1:
    #接入
    new_s,addr = s.accept()
    socket_list.append(new_s)
    #new_s.send('请输入昵称:'.encode('utf-8'))
    t1 = threading.Thread(target=receive,args=(new_s,socket_list))
    t2 = threading.Thread(target=send,args=(new_s,))
    t1.start()
    t2.start()
# new_s.close()
# s.close()

