import socket
import time
from ctypes import memmove
import pyzbar.pyzbar as pyzbar
import cv2
import numpy as np
import math
#import winsound #비프음 모듈
from realsense_camera import *

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0
key = 0
#so1 = {'do':261}

def nothing(x):
    pass

def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold1, threshold2
    # 마우스 왼쪽 버튼 누를시 실행
    if event == cv2.EVENT_LBUTTONDOWN:
        #print(img_color[y, x])
        color = img[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        print(hsv[0])
        hsv = hsv[0][0]

        threshold1 = cv2.getTrackbarPos('threshold1', 'img1')
        threshold2 = cv2.getTrackbarPos('threshold2', 'img1')
        
        # HSV 색공간에서 얻은 픽셀값과 유사한 필셀값의 범위 지정
        if hsv[0] < 10:
            print("case1")
            lower_blue1 = np.array([hsv[0]-10+180, threshold1, threshold2])
            upper_blue1 = np.array([180, 255, 255])

            lower_blue2 = np.array([0, threshold1, threshold2])
            upper_blue2 = np.array([hsv[0], 255, 255])

            lower_blue3 = np.array([hsv[0], threshold1, threshold2])
            upper_blue3 = np.array([hsv[0]+10, 255, 255])
            
        elif hsv[0] > 170:
            print("case2")
            lower_blue1 = np.array([hsv[0], threshold1, threshold2])
            upper_blue1 = np.array([180, 255, 255])

            lower_blue2 = np.array([0, threshold1, threshold2])
            upper_blue2 = np.array([hsv[0]+10-180, 255, 255])

            lower_blue3 = np.array([hsv[0]-10, threshold1, threshold2])
            upper_blue3 = np.array([hsv[0], 255, 255])

        else:
            print("case3")
            lower_blue1 = np.array([hsv[0], threshold1, threshold2])
            upper_blue1 = np.array([hsv[0]+10, 255, 255])

            lower_blue2 = np.array([hsv[0]-10, threshold1, threshold2])
            upper_blue2 = np.array([hsv[0], 255, 255])
            
            lower_blue3 = np.array([hsv[0]-10, threshold1, threshold2])
            upper_blue3 = np.array([hsv[0], 255, 255])

        #print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)

def box_contect(contours):
    rect = cv2.minAreaRect(contours)
    box = cv2.boxPoints(rect)

    box_x0 = np.int0(box[0][0])
    box_y0 = np.int0(box[0][1])
    box_x1 = np.int0(box[1][0])
    box_y1 = np.int0(box[1][1])
    box_x2 = np.int0(box[2][0])
    box_y2 = np.int0(box[2][1])
    box_x3 = np.int0(box[3][0])
    box_y3 = np.int0(box[3][1])

    return box_x0, box_y0, box_x1, box_y1, box_x2, box_y2, box_x3, box_y3

cv2.namedWindow('img1')
cv2.setMouseCallback('img1', mouse_callback)

cv2.namedWindow('img1')
cv2.createTrackbar('threshold1', 'img1', 0, 255, nothing)
cv2.setTrackbarPos('threshold1', 'img1', 65)
cv2.createTrackbar('threshold2', 'img1', 0, 255, nothing)
cv2.setTrackbarPos('threshold2', 'img1', 87)

rs = RealsenseCamera()

#소켓통신
sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sever_socket.bind(('192.168.0.45',8888))
sever_socket.listen(0)
client_socket, addr = sever_socket.accept()
print("socket ready")

#카메라 open
#cap = cv2.VideoCapture(0)

temp_1 = bytes()

while(True):
    ret, img,__  = rs.get_frame_stream()

    if ret == False:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3

    kernel = np.ones((11,11), np.uint8)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("img_mask", img_mask)

    contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #max_area, max_contour = findMaxArea(contours)

    #print(max_area)
    key = cv2.waitKey(1)
    if key == 113:
        for cnt_0 in contours:
            peri = cv2.arcLength(cnt_0, True)
            approx = cv2.approxPolyDP(cnt_0, 0.05 * peri, True)
            cv2.drawContours(img, [approx], 0, (255, 0, 0), 3)

            xx0, yy0, xx1, yy1, xx2, yy2, xx3, yy3 = box_contect(cnt_0)
            xx_dis = abs(xx0 - xx1)
            yy_dis = abs(yy0 - yy1)    
            radian = math.atan2(yy_dis, xx_dis)
            degree = radian * 180 / math.pi
            xx_center = int((xx0 + xx2) / 2)
            yy_center = int((yy0 + yy2) / 2)
            #cv2.putText(img1, "각도 : {}".format(int(degree)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            #cv2.putText(img1, "가로 : {}".format(xx_center), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            #cv2.putText(img1, "세로 : {}".format(yy_center), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
            if xx_center > 310 and xx_center < 330:
                if yy_center > 230 and yy_center < 250:
                    print("center perfact!!")
                    if degree > 85 or degree < 5:
                        print("degree pergact!!")

                        decoded = pyzbar.decode(gray)

                        for d in decoded: 
                            x, y, w, h = d.rect
                            barcode_data = d.data.decode("utf-8")
                            barcode_type = d.type
                            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

                            text = '%s (%s)' % (barcode_data, barcode_type)
                            cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
                            temp = barcode_data ## QR?? ?? ??? ??
                            temp_1=temp.encode("utf-8") ## 8??? ???? ?? 

                        if not temp_1:
                            print("NO QR") ## QR ??? ?????

                        client_socket.send(temp_1) ## zeus? temp_1 ? ??? ??? ??
                        data = client_socket.recv(65535)
                        data = d.data.decode("utf-8")
                        print(data)
                        print("QR DATA =",temp_1.decode())

                        temp_1= bytes()  ## ????? count? 15?? ?? -> 30??? temp_1 ?? ??? 

                    else:
                        print("각도 재조정 필요! 현재각도 : {}".format(int(degree)))
                else:
                    print("세로 좌표 재조정 필요! 현재 세로좌표값 : {}".format(yy_center))
            else:
                print("가로 좌표 재조정 필요! 현재 가로좌표값 : {}".format(xx_center))

    cv2.imshow('img1', img)

    if cv2.waitKey(1) & 0xFF == 27:  
        break

cv2.destroyAllWindows()

# 1122334455 제우스와이파이 비밀번호, iptim 설정에서 확인가능
# ifconfig ip주소확인