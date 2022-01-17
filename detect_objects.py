import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import numpy as np
import pyrealsense2
from realsense_depth import *

dc = DepthCamera()

while True:
    ret, depth_frame, color_frame = dc.get_frame()
    
    #15inch x 15inch figure 생성
    fig = plt.figure(figsize=(15,15)) 
    for i in range(1, 4):
        # image_path에서 이미지 읽어오기
        #image_path = './image/image'+ str(i) +'.jpeg'
        #im = cv2.imread(image_path)
        
        # object detection 수행
        # bbox : detect한 부분, label : 물체를 detect한 라벨, conf : label로 분류된 확률
        bbox, label, conf = cv.detect_common_objects(color_frame)
        
        # 결과 이미지에 detect한 부분을 네모로 표시하고 라벨 붙이기
        output_image = draw_bbox(color_frame, bbox, label, conf)
        # BGR -> RGB
        output_image = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
        
        # figure를 3x1 그리드 나누고 i번째 좌표계에 이미지 표시하기
        plt.subplot(3, 1, i)
        plt.imshow(output_image)
        # 좌표축 삭제
        plt.axis('off')
        
    # padding 등 subplot layout 자동 조정
    plt.tight_layout()
    plt.show()

    cv2.imshow(color_frame)

    if cv2.waitKey(1) == 27:
        break 

