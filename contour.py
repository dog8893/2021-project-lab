import cv2
import numpy as np
from realsense_camera import *

def empty(a):
    pass

cv2.namedWindow('Parameters')
cv2.resizeWindow('Parameters', 640, 240)
cv2.createTrackbar('Threshold1', 'Parameters', 60, 255, empty)
cv2.createTrackbar('Threshold2', 'Parameters', 60, 255, empty)

rs = RealsenseCamera()

def stackImages(scale,imgArray): # 사이즈가 다른 이미지 & 흑백 컬러 이미지 & resize 할때 사용하는 함수
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else: imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def differential(bgr_frame):
    gray = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)
    roberts_x = np.array([[-1, 0, 0], [0, 1, 0], [0, 0, 0]])
    roberts_y = np.array([[0, 0, -1], [0, 1, 0], [0, 0, 0]])
    prewitt_x = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
    prewitt_y = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]])
    sobel_x = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    sobel_y = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    roberts_x = cv2.convertScaleAbs(cv2.filter2D(gray, -1, roberts_x))
    roberts_y = cv2.convertScaleAbs(cv2.filter2D(gray, -1, roberts_y))
    prewitt_x = cv2.convertScaleAbs(cv2.filter2D(gray, -1, prewitt_x))
    prewitt_y = cv2.convertScaleAbs(cv2.filter2D(gray, -1, prewitt_y))
    sobel_x = cv2.convertScaleAbs(cv2.filter2D(gray, -1, sobel_x))
    sobel_y = cv2.convertScaleAbs(cv2.filter2D(gray, -1, sobel_y))
    prewitt = cv2.addWeighted(prewitt_x, 1, prewitt_y, 1, 0)
    roberts = cv2.addWeighted(roberts_x, 1, roberts_y, 1, 0)
    sobel = cv2.addWeighted(sobel_x, 1, sobel_y, 1, 0)
    return prewitt, roberts, sobel

while(True):
    ret, bgr_frame, depth_frame = rs.get_frame_stream()
    img_size = cv2.resize(bgr_frame, (960, 480))

    bgr_prewitt, bgr_roberts, bgr_sobel = differential(bgr_frame)
    bgr_laplacian = cv2.Laplacian(bgr_frame,cv2.CV_8U,ksize=5)

    img_contour = img_size.copy()

    img_Blur = cv2.GaussianBlur(img_size, (7, 7), 1)
    img_Gray = cv2.cvtColor(img_Blur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos('Threshold1', 'Parameters')
    threshold2 = cv2.getTrackbarPos('Threshold2', 'Parameters')
    img_Canny = cv2.Canny(img_Gray, threshold1, threshold2)
    kernel = np.ones((16, 16))
    img_Dil = cv2.dilate(img_Canny, kernel, iterations = 1)

    contours, hierarchy = cv2.findContours(img_Dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 100 > area > 100000:
            cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 2)

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.3 * peri, True)
            print(len(approx))
            x, y, w, h = cv2.boundingRect(approx)
            #cv2.rectangle(img_contour, (x, y), (x + w, y + h), (0, 255, 0), 5)

            cv2.putText(img_contour, 'points: ' + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_contour, 'Area: ' + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_contour, 'BOX', (x + w + 20, y + 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_contour, 'height : ' + str(int(h)), (20, 40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img_contour, 'width : ' + str(int(w)), (20, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            #cv2.putText(img_contour, 'length : ' + str(int(peri)), (20, 60), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0), 2)

    imgStack = stackImages(0.4, ([bgr_frame, bgr_prewitt], [bgr_roberts, bgr_laplacian]))

    cv2.imshow('result', imgStack)

    if cv2.waitKey(100) & 0XFF == 27:
        break

cv2.destroyAllWindows()