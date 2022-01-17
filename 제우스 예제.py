import socket 
import time 
from ctypes import memmove
import pyzbar.pyzbar as pyzbar
import cv2

sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever_socket.bind(('192.168.0.24',8888))
sever_socket.listen(0)
client_socket, addr = sever_socket.accept()

cap = cv2.VideoCapture(0)

count = 0
temp_1 = bytes()

while(cap.isOpened()):

    ret, img = cap.read()
    img1 = cv2.resize(img, (1080, 800), cv2.INTER_LINEAR)

    if not ret:
        continue

    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    decoded = pyzbar.decode(gray)
    if count == 0: ## count 0?? ??
        for d in decoded: 
            x, y, w, h = d.rect
            barcode_data = d.data.decode("utf-8")
            barcode_type = d.type

            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 0, 255), 2)
            text = '%s (%s)' % (barcode_data, barcode_type)         
            cv2.putText(img1, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            temp = barcode_data ## QR?? ?? ??? ??
            temp_1=temp.encode("utf-8") ## 8??? ???? ?? 

        if not temp_1:
            print("NO QR") ## QR ??? ?????

        else:
            client_socket.send(temp_1) ## zeus? temp_1 ? ??? ??? ??
            data = client_socket.recv(65535)
            data = d.data.decode("utf-8")
            print(data)
            print("QR DATA =",temp_1.decode())
            count = 1 ## data ??? count ?? 1? ??

    if count != 0:
        count = count + 1

    if count == 20:
        temp_1= bytes()  ## ????? count? 15?? ?? -> 30??? temp_1 ?? ??? 
        count = 0

    print(count)
    cv2.imshow('img1', img1)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cap.release()
cv2.destroyAllWindows()

# 1122334455 제우스와이파이 비밀번호, iptim 설정에서 확인가능

# ifconfig ip주소확인