import socket
from ctypes import memmove
import time
import cv2

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.45',8888))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

number_0 = 0
number_1 = 0
count = 0

while True:
    if count == 0:
        number_0 = input("number_0 : ")
        temp_0 = number_0.encode("utf-8")

        number_1 = input("number_1 : ")
        temp_1 = number_1.encode("utf-8")

        if not temp_0:
            print("ERROR")

        if not temp_1:
            print("ERROR")

        else:
            client_socket.send(temp_0)
            client_socket.send(temp_1)
            data_0 = temp_0.decode("utf-8")
            print(data_0)
            data_1 = temp_1.decode("utf-8")
            print(data_1)

            count = 1
    
    if count != 0:
        count = count + 1

    if count == 20:
        temp_0 = bytes()
        temp_1 = bytes()
        count = 0

    print(count)