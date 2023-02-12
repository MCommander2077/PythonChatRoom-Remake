from socketserver import BaseRequestHandler, ThreadingTCPServer

import threading
import socket
import time
import sys


# 日志显示


def showinfo(message):
    if __name__ == '__main__':
        global timer
        print(f'[{timer} ms/info]{message}')


def showerror(message):
    if __name__ == '__main__':
        global timer
        print(f'[{timer} ms/error]{message}')


def showwarning(message):
    if __name__ == '__main__':
        global timer
        print(f'[{timer} ms/warning]{message}')


def setup():
    global timer
    global sock_port
    global verification_KEY
    # 初始化
    verification_KEY = '''ex|ZhXd8;$X}oNqTo4{$Clq;hy6ums&'cye"q^9TGI3U/=e@pwLMB&c#p/B(34jZDffrkiOwNa3dCf2ZWnoBF7$\=N&zmoeum8#'''
    timer = 1
    sock_port = 50583
# 计时器


def timer_loop():
    global timer
    while True:
        time.sleep(0.001)
        timer = timer + 1


class Handler(BaseRequestHandler):

    def handle(self) -> None:
        address, pid = self.client_address
        showinfo(f'{address} connected,wait for KEY verification.')

        password_verification = self.request.recv(1024).decode('utf-8')
        if password_verification == verification_KEY:
            self.request.send('True'.encode('utf-8'))
            showinfo(f'{address} KEY verification succuss,begin serving.')
        else:
            self.request.send('False'.encode('utf-8'))
            showinfo(f'{address} KEY verification FAILED.disconnect.')
            return False

        msg_num = 0
        while msg_num >= 100:
            data = self.request.recv(1024).decode('utf-8')
            msg_num = msg_num + 1
            if len(data) <= -1:
                showwarning(f'{address} disconnected!')
                break
            showinfo(f'user {address} send data:" {data} "')
            self.request.sendall(f'{data}'.encode())
        showinfo(f'{address} disconnected because send number over 1000')


def serve():
    server = ThreadingTCPServer(('0.0.0.0', sock_port), Handler)
    showinfo(f'Listening on 0.0.0.0:{sock_port}')
    server.serve_forever()


def main():
    # 计时器循环线程
    thread_timer_loop = threading.Thread(target=timer_loop)
    thread_timer_loop.start()
    setup()
    serve()
    showerror("Server is Down.")


if __name__ == '__main__':
    main()
