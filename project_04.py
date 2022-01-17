from typing import Container
import cv2
import numpy as np
from realsense_camera import *
import math
import socket
from ctypes import memmove
import time

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0

xx = 0
yy = 0
#w = 300
h = 480
dis_all = 0.85
tt = 3.2
speed = 10

def nothing(x):
    pass

def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold1, threshold2, xx, yy

    # 마우스 왼쪽 버튼 누를시 실행
    if event == cv2.EVENT_LBUTTONDOWN:
        print("왼클릭 마우스 이벤트 발생")
        #print(img_bgr[y, x])
        color = img_bgr[y, x]

        one_pixel = np.uint8([[color]])
        hsv = cv2.cvtColor(one_pixel, cv2.COLOR_BGR2HSV)
        hsv = hsv[0][0]
        print(hsv)
        threshold1 = cv2.getTrackbarPos('threshold1', 'img_bgr')
        threshold2 = cv2.getTrackbarPos('threshold2', 'img_bgr')
        
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

        print(hsv[0])
        print("@1", lower_blue1, "~", upper_blue1)
        print("@2", lower_blue2, "~", upper_blue2)
        print("@3", lower_blue3, "~", upper_blue3)
    
    if event == cv2.EVENT_RBUTTONDOWN:
        print("우클릭 마우스 이벤트 발생, x:", x ," y:", y)
        #xx = x
        #yy = y

def findMaxArea(contours):
    max_contour = None
    max_area = -1
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        x,y,w,h = cv2.boundingRect(contour)
        
        if (w*h)*0.4 > area:
            continue
        
        if w > h:
            continue
        
        if area > max_area:
            max_area = area
            max_contour = contour
            
    if max_area < 10000:
        max_area = -1
        
    return max_area, max_contour    

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

cv2.namedWindow('img_bgr')
cv2.setMouseCallback('img_bgr', mouse_callback)

cv2.namedWindow('img_bgr')
cv2.createTrackbar('threshold1', 'img_bgr', 0, 255, nothing)
cv2.setTrackbarPos('threshold1', 'img_bgr', 65)
cv2.createTrackbar('threshold2', 'img_bgr', 0, 255, nothing)
cv2.setTrackbarPos('threshold2', 'img_bgr', 87)
cv2.createTrackbar('threshold3', 'img_bgr', 0, 640, nothing)
cv2.setTrackbarPos('threshold3', 'img_bgr', 329)
cv2.createTrackbar('threshold4', 'img_bgr', 0, 640, nothing)
cv2.setTrackbarPos('threshold4', 'img_bgr', 191)

rs = RealsenseCamera()

print("Ready")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.0.45',8888))
server_socket.listen(0)
client_socket, addr = server_socket.accept()

print("socket ready")

def process(img_bgr, img_depth, debug):
    global dis, tt, speed
    threshold3 = cv2.getTrackbarPos('threshold3', 'img_bgr')
    threshold4 = cv2.getTrackbarPos('threshold4', 'img_bgr')
    w = threshold3
    xx = threshold4
    
    roi = img_bgr[yy:yy+h, xx:xx+w]
    img_result = roi.copy()
    
    cv2.rectangle(img_bgr, (xx,yy), (xx+w, yy+h), (0,255,0))

    #img_result = img_bgr.copy()

    img_hsv = cv2.cvtColor(img_result, cv2.COLOR_BGR2HSV)

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
    

    for cnt_0 in contours:
        peri = cv2.arcLength(cnt_0, True)
        approx = cv2.approxPolyDP(cnt_0, 0.05 * peri, True)
        cv2.drawContours(img_result, [approx], 0, (255, 0, 0), 3)

        xx0, yy0, xx1, yy1, xx2, yy2, xx3, yy3 = box_contect(cnt_0)
        '''cv2.circle(img_result, (xx0, yy0), 5, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_0', (xx0 + 20, yy0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx1, yy1), 5, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_1', (xx1 + 20, yy1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx2, yy2), 5, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_2', (xx2 + 20, yy2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx3, yy3), 5, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_3', (xx3 + 20, yy3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.line(img_result, (xx0, yy0), (xx1, yy1), (255, 255, 0), 3)'''
        xx_dis = abs(xx0 - xx1)
        yy_dis = abs(yy0 - yy1)    
        radian = math.atan2(yy_dis, xx_dis)
        degree = radian * 180 / math.pi
        cv2.putText(img_result, "degree : {}".format(int(degree)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        xx_center = int((xx0 + xx2) / 2)
        yy_center = int((yy0 + yy2) / 2)
        xx_center_send = int(xx_center / 329 * 300)
        yy_center_send = int(yy_center / 480 * 300)
        distance = img_depth[yy_center, xx_center]
        cv2.circle(img_result, (int(xx_center), int(yy_center)), 3, (255, 255, 0), 5)
        cv2.putText(img_result, "x : {}".format(xx_center_send), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, "y : {}".format(yy_center_send), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, "Depth : {}mm".format(distance), (20, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        
        if yy0 > 10 and yy0 < 25:
            y_time0 = (yy0 / 480 * 420)
            start = time.time()

        if yy0 > 100 and yy0 < 115:
            end = time.time()
            y_time1 = (yy0 / 480 * 420)

            time_11 = (end - start)
            print("time_11 : ", time_11)

            dis = y_time1 - y_time0
            print("dis : ", dis)
            speed  = dis/time_11
            speed_1 = round(speed, 2)
            print("speed : ", speed_1)
            tt = round(dis_all/speed_1, 2)
            print("tt : ", tt)

        if yy_center_send >= 200 and yy_center_send < 250:
            time.sleep(tt)

            temp_0 = str(xx_center_send).encode("utf-8")
            temp_1 = str(yy_center_send).encode("utf-8")

            client_socket.send(temp_0)
            client_socket.send(temp_1)
            data_0 = temp_0.decode("utf-8")
            data_1 = temp_1.decode("utf-8")
            print(data_0, data_1)

            temp_0 = bytes()
            temp_1 = bytes()

        else:
            continue

        return img_result
    
    '''if max_area != -1:
        xx0, yy0, xx1, yy1, xx2, yy2, xx3, yy3 = box_contect(max_contour)
        cv2.circle(img_result, (xx0, yy0), 10, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_0', (xx0 + 20, yy0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx1, yy1), 10, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_1', (xx1 + 20, yy1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx2, yy2), 10, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_2', (xx2 + 20, yy2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.circle(img_result, (xx3, yy3), 10, (0, 255, 0), 5)
        cv2.putText(img_result, 'box_3', (xx3 + 20, yy3), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.line(img_result, (xx0, yy0), (xx1, yy1), (255, 255, 0), 5)
        xx_dis = abs(xx0 - xx1)
        yy_dis = abs(yy0 - yy1)
        radian = math.atan2(yy_dis, xx_dis)
        degree = radian * 180 / math.pi
        cv2.putText(img_result, str(int(degree)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        xx_center = str(int((xx0 + xx2) / 2))
        yy_center = str(int((yy0 + yy2) / 2))
        cv2.putText(img_result, xx_center, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, yy_center, (120, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, "{}mm".format(distance), (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.drawContours(img_result, [max_contour], 0, (0, 0, 255), 3)
    '''
    return img_result

while(True):
    
    ret, img_bgr, img_depth = rs.get_frame_stream()

    if ret == False:
        break


    result = process(img_bgr, img_depth, debug=True)
    
    cv2.imshow("img_bgr", img_bgr)
    cv2.imshow("Result", result)

    # ESC 키누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()