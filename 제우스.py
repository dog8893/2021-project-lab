import socket 
import time 
from ctypes import memmove

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever_socket.bind(('192.168.0.45',8888))
sever_socket.listen(0)
client_socket, addr = sever_socket.accept()

number = 0
count = 0

while(True):        

    if count == 0: ## count 0?? ??
        number = input("number : ")
        temp = number.decode("utf-8")
        temp_1 = temp.encode("utf-8")

        if not temp_1:
            print("ERROR") ## QR ??? ?????

        else:
            client_socket.send(temp_1) ## zeus? temp_1 ? ??? ??? ??
            data = client_socket.recv(65535)
            data = data.decode("utf-8")
            print(data)
            print("NUMBER =",temp_1.decode())
            count = 1 ## data ??? count ?? 1? ??

    if count != 0:
        count = count + 1

    if count == 20:
        temp_1 = bytes()  ## ????? count? 15?? ?? -> 30??? temp_1 ?? ??? 
        count = 0

    print(count)

# 1122334455 제우스와이파이 비밀번호, iptim 설정에서 확인가능

# ifconfig ip주소확인