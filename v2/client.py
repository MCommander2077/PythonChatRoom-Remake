import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8001))
time.sleep(2)
sock.send('P^$$VV0rd'.encode())
print(sock.recv(1024).decode('utf-8'))
sock.close()
input()
