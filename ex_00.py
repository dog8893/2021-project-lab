import socket 
import time 

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.25',5000))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

while True:
    data = client_socket.recv(65535)
    data = data.decode()
    print(data)

    data = data.encode()
    client_socket.send(data)