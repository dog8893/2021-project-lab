from typing import Container
import cv2
import numpy as np
from realsense_camera import *
import math

hsv = 0
lower_blue1 = 0
upper_blue1 = 0
lower_blue2 = 0
upper_blue2 = 0
lower_blue3 = 0
upper_blue3 = 0

def nothing(x):
    pass

def mouse_callback(event, x, y, flags, param):
    global hsv, lower_blue1, upper_blue1, lower_blue2, upper_blue2, lower_blue3, upper_blue3, threshold1, threshold2

    # 마우스 왼쪽 버튼 누를시 실행
    if event == cv2.EVENT_LBUTTONDOWN:
        print(img_bgr[y, x])
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
  
  if max_area < 150000:
    max_area = -1

  return max_area, max_contour

def distanceBetweenTwoPoints(start, end):

  x1,y1 = start
  x2,y2 = end
 
  return int(np.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2)))

def calculateAngle(A, B):

  A_norm = np.linalg.norm(A)
  B_norm = np.linalg.norm(B)
  C = np.dot(A,B)

  angle = np.arccos(C/(A_norm*B_norm))*180/np.pi
  return angle

def getFingerPosition(max_contour, img_result, debug):
  points1 = []

  # STEP 6-1
  M = cv2.moments(max_contour)

  cx = int(M['m10']/M['m00'])
  cy = int(M['m01']/M['m00'])

  max_contour = cv2.approxPolyDP(max_contour,0.02*cv2.arcLength(max_contour,True),True)
  hull = cv2.convexHull(max_contour)

  for point in hull:
    if cy > point[0][1]:
      points1.append(tuple(point[0])) 

  if debug:
    cv2.drawContours(img_result, [hull], 0, (0,255,0), 2)
    for point in points1:
      cv2.circle(img_result, tuple(point), 15, [ 0, 0, 0], -1)

  # STEP 6-2
  hull = cv2.convexHull(max_contour, returnPoints=False)
  defects = cv2.convexityDefects(max_contour, hull)

  if defects is None:
    return -1,None

  points2=[]
  for i in range(defects.shape[0]):
    s,e,f,d = defects[i, 0]
    start = tuple(max_contour[s][0])
    end = tuple(max_contour[e][0])
    far = tuple(max_contour[f][0])

    angle = calculateAngle( np.array(start) - np.array(far), np.array(end) - np.array(far))

    if angle < 90:
      if start[1] < cy:
        points2.append(start)
      
      if end[1] < cy:
        points2.append(end)

  if debug:
    cv2.drawContours(img_result, [max_contour], 0, (255, 0, 255), 2)
    for point in points2:
      cv2.circle(img_result, tuple(point), 20, [ 0, 255, 0], 5)

  # STEP 6-3
  points = points1 + points2
  points = list(set(points))

  # STEP 6-4
  new_points = []
  for p0 in points:
    
    i = -1
    for index,c0 in enumerate(max_contour):
      c0 = tuple(c0[0])

      if p0 == c0 or distanceBetweenTwoPoints(p0,c0)<20:
        i = index
        break

    if i >= 0:
      pre = i - 1
      if pre < 0:
        pre = max_contour[len(max_contour)-1][0]
      else:
        pre = max_contour[i-1][0]
      
      next = i + 1
      if next > len(max_contour)-1:
        next = max_contour[0][0]
      else:
        next = max_contour[i+1][0]

      if isinstance(pre, np.ndarray):
            pre = tuple(pre.tolist())
      if isinstance(next, np.ndarray):
        next = tuple(next.tolist())
    
      angle = calculateAngle( np.array(pre) - np.array(p0), np.array(next) - np.array(p0))     

      if angle < 90:
        new_points.append(p0)
  
  return 1,new_points

cv2.namedWindow('img_bgr')
cv2.setMouseCallback('img_bgr', mouse_callback)

cv2.namedWindow('img_bgr')
cv2.createTrackbar('threshold1', 'img_bgr', 0, 255, nothing)
cv2.setTrackbarPos('threshold1', 'img_bgr', 60)
cv2.createTrackbar('threshold2', 'img_bgr', 0, 255, nothing)
cv2.setTrackbarPos('threshold2', 'img_bgr', 60)

rs = RealsenseCamera()

def process(img_bgr, debug):
    img_result = img_bgr.copy()

    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    # 범위 값으로 HSV 이미지에서 마스크를 생성합니다.
    img_mask1 = cv2.inRange(img_hsv, lower_blue1, upper_blue1)
    img_mask2 = cv2.inRange(img_hsv, lower_blue2, upper_blue2)
    img_mask3 = cv2.inRange(img_hsv, lower_blue3, upper_blue3)
    img_mask = img_mask1 | img_mask2 | img_mask3

    kernel = np.ones((11,11), np.uint8)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_OPEN, kernel)
    img_mask = cv2.morphologyEx(img_mask, cv2.MORPH_CLOSE, kernel)
    cv2.imshow("img_mask", img_mask)

    contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if debug:
        for cnt in contours:
            area_test = cv2.contourArea(cnt)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.3 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            cv2.drawContours(img_result, [cnt], 0, (255, 0, 0), 3)
            cv2.putText(img_result, str(int(area_test)), (x+w+20, y+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
    '''
    for i in contours:
      rect = cv2.minAreaRect(i)
      box = cv2.boxPoints(rect)

      box_x0 = np.int0(box[0][0])
      box_y0 = np.int0(box[0][1])
      box_x1 = np.int0(box[1][0])
      box_y1 = np.int0(box[1][1])
      box_x2 = np.int0(box[2][0])
      box_y2 = np.int0(box[2][1])
      box_x3 = np.int0(box[3][0])
      box_y3 = np.int0(box[3][1])

      cv2.circle(img_result, (box_x0, box_y0), 20, (0, 255, 0), 5)
      cv2.circle(img_result, (box_x1, box_y1), 20, (0, 255, 0), 5)
      cv2.circle(img_result, (box_x2, box_y2), 20, (0, 255, 0), 5)
      cv2.circle(img_result, (box_x3, box_y3), 20, (0, 255, 0), 5)
    '''
    max_area, max_contour = findMaxArea(contours)
    
    if max_area == -1:
      pass
      '''
        for i in contours:
          rect = cv2.minAreaRect(i)
          box = cv2.boxPoints(rect)

          box_x0 = np.int0(box[0][0])
          box_y0 = np.int0(box[0][1])
          box_x1 = np.int0(box[1][0])
          box_y1 = np.int0(box[1][1])
          box_x2 = np.int0(box[2][0])
          box_y2 = np.int0(box[2][1])
          box_x3 = np.int0(box[3][0])
          box_y3 = np.int0(box[3][1])

          cv2.circle(img_result, (box_x0, box_y0), 20, (0, 255, 0), 5)
          cv2.circle(img_result, (box_x1, box_y1), 20, (0, 255, 0), 5)
          cv2.circle(img_result, (box_x2, box_y2), 20, (0, 255, 0), 5)
          cv2.circle(img_result, (box_x3, box_y3), 20, (0, 255, 0), 5)

          center_xx0 = str(int((box_x0 + box_x2) / 2))
          center_yy0 = str(int((box_y0 + box_y2) / 2))

          center_xx1 = str(int((box_x1 + box_x3) / 2))
          center_yy1 = str(int((box_y1 + box_y3) / 2))

          cv2.putText(img_result, center_xx0, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
          cv2.putText(img_result, center_yy0, (120, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
          cv2.putText(img_result, center_xx1, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
          cv2.putText(img_result, center_yy1, (120, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

          xx0 = abs(box_x1 - box_x2)
          yy0 = abs(box_y1 - box_y2)
          radian0 = math.atan2(yy0, xx0)
          degree0 = radian0 * 180 / math.pi

          xx1 = abs(box_x1 - box_x0)
          yy1 = abs(box_y1 - box_y0)
          radian1 = math.atan2(yy1, xx1)
          degree1 = radian1 * 180 / math.pi
          #cv2.putText(img_result, str(int(degree0)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
          cv2.putText(img_result, str(int(degree1)), (box_x0, box_y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)


        return img_result
      '''
    if debug:
      cv2.drawContours(img_result, [max_contour], 0, (0, 0, 255), 3)
      for i in max_contour:
        rect = cv2.minAreaRect(i)
        box = cv2.boxPoints(rect)

        box_x0 = np.int0(box[0][0])
        box_y0 = np.int0(box[0][1])
        box_x1 = np.int0(box[1][0])
        box_y1 = np.int0(box[1][1])
        box_x2 = np.int0(box[2][0])
        box_y2 = np.int0(box[2][1])
        box_x3 = np.int0(box[3][0])
        box_y3 = np.int0(box[3][1])

        cv2.circle(img_result, (box_x0, box_y0), 20, (0, 255, 0), 5)
        cv2.circle(img_result, (box_x1, box_y1), 20, (0, 255, 0), 5)
        cv2.circle(img_result, (box_x2, box_y2), 20, (0, 255, 0), 5)
        cv2.circle(img_result, (box_x3, box_y3), 20, (0, 255, 0), 5)

        center_xx0 = str(int((box_x0 + box_x2) / 2))
        center_yy0 = str(int((box_y0 + box_y2) / 2))

        center_xx1 = str(int((box_x1 + box_x3) / 2))
        center_yy1 = str(int((box_y1 + box_y3) / 2))

        cv2.putText(img_result, center_xx0, (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, center_yy0, (120, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, center_xx1, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, center_yy1, (120, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        xx0 = abs(box_x1 - box_x2)
        yy0 = abs(box_y1 - box_y2)
        radian0 = math.atan2(yy0, xx0)
        degree0 = radian0 * 180 / math.pi

        xx1 = abs(box_x1 - box_x0)
        yy1 = abs(box_y1 - box_y0)
        radian1 = math.atan2(yy1, xx1)
        degree1 = radian1 * 180 / math.pi
        #cv2.putText(img_result, str(int(degree0)), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(img_result, str(int(degree1)), (box_x0, box_y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2, cv2.LINE_AA)
        '''
        for j in max_contour:
          rect = cv2.minAreaRect(j)
          box = cv2.boxPoints(rect)

          box_x0 = np.int0(box[0][0])
          box_y0 = np.int0(box[0][1])
          box_x1 = np.int0(box[1][0])
          box_y1 = np.int0(box[1][1])
          box_x2 = np.int0(box[2][0])
          box_y2 = np.int0(box[2][1])
          box_x3 = np.int0(box[3][0])
          box_y3 = np.int0(box[3][1])

          cv2.circle(img_result, (box_x0, box_y0), 20, (255, 0, 255), 5)
          cv2.circle(img_result, (box_x1, box_y1), 20, (255, 0, 255), 5)
          cv2.circle(img_result, (box_x2, box_y2), 20, (255, 0, 255), 5)
          cv2.circle(img_result, (box_x3, box_y3), 20, (255, 0, 255), 5)
    '''
    #contours2, hierarchy = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      

    '''
    ret,points = getFingerPosition(max_contour, img_result, debug)
  
    if ret > 0 and len(points) > 0:  
        for point in points:
            cv2.circle(img_result, point, 20, (255, 0, 255), 5)
    '''
    
    
    
    return img_result

while(True):
    
    ret, img_bgr, img_depth = rs.get_frame_stream()

    if ret == False:
        break

    img_result = process(img_bgr, debug=True)
    
    cv2.imshow("img_bgr", img_bgr)
    cv2.imshow("Result", img_result)

    # ESC 키누르면 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()