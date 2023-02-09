import customtkinter as ctk
import tkinter as tk
import socket
import threading
import time
import sys

Bool_Is_Connect = False
Str_Send_Message = ""
Str_Data_Receive = ""

sock_ip = "127.0.0.1"
sock_port = 50583

verification_KEY = '''ex|ZhXd8;$X}oNqTo4{$Clq;hy6ums&'cye"q^9TGI3U/=e@pwLMB&c#p/B(34jZDffrkiOwNa3dCf2ZWnoBF7$\=N&zmoeum8#'''
USERNAME = socket.gethostname()
# 密码功能正在火速研发中()
# PASSWORD = ""


class Client:
    def __init__(self):
        # ipv4  TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, server_ip, server_port):
        self.client.connect((server_ip, server_port))
        # 验证
        self.client.send(verification_KEY.encode())
        if self.client.recv(1024).decode('utf-8') == 'False':
            self.client.close()
            sys.exit("KEY VERIFICATION FAILED")
        Bool_Is_Connect = True

    def send(self):
        while Bool_Is_Connect:
            message = input("message:")
            self.client.send(f'{USERNAME}:{message}'.encode())

    def receive(self):
        while Bool_Is_Connect:
            response = self.client.recv(1024).decode('utf-8')
            print(response)

    def disconnect(self):
        self.client.close()
        Bool_Is_Connect = False


def main():
    client = Client()
    client.connect('127.0.0.1', 50583)

    thread_send = threading.Thread(target=client.send)
    thread_receive = threading.Thread(target=client.receive)

    thread_send.start()
    thread_receive.start()

    client.disconnect()

if __name__ == '__main__':
    main()

root = ctk.CTk()
root.title("TCP Client")
root.geometry("300x300")
root.resizable(False, False)
root.config(bg="pink")
root.columnconfigure(0, weight=1)
root.mainloop()

