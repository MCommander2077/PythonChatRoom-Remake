import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 8001))
sock.listen(5)

while True:
        connection,address = sock.accept()
        try:
            connection.settimeout(5)
            buf = connection.recv(1024).decode('utf-8')
            if buf == 'P^$$VV0rd':
                connection.send('welcome to server'.encode('utf-8'))
            else:
                connection.send('please go out!'.encode('utf-8'))
        except socket.timeout:
            print('connection time out')
        connection.close()