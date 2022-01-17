#!/usr/bin/python
# -*- coding: utf-8 -*-
## 1. 초기 설정① #######################################
# 라이브러리 가져오기
## 1．초기 설정 ①　모듈 가져오기 ######################
from i611_MCS import *
from teachdata import *
from i611_extend import *
from rbsys import *
from i611_common import *
from i611_io import *
from i611shm import * 
import thread

def main():
    ## 2. 초기 설정② ####################################
    # ZERO 로봇 생성자
    rb = i611Robot()
    # 좌표계의 정의
    _BASE = Base()
    # 로봇과 연결 시작 초기화
    rb.open()
    # I/O 입출력 기능의 초기화 
    IOinit( rb )
    # 교시 데이터 파일 읽기
    data = Teachdata( "teach_data" )
    
    ## 1. 교시 포인트 설정 ######################
    p1 = data.get_position( "pos1", 0 )
    p2 = data.get_position( "pos1", 1 )
    ## 2. 동작 조건 설정 ######################## 
    rb.override(100)
    m = MotionParam( jnt_speed=20, lin_speed=70, pose_speed=15)
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam( m )
    
    #소켓 설정 
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)
    sock.connect(('192.168.0.23',8888))
    Send_Data = 'OK'
   
    j1=Joint(89.227, 19.894, 93.720, 1.672, 61.122, -0.896)#박스 잡는 위치
    j2=Joint(89.224, 42.764, 93.712, 1.879, 43.554, -0.296)#box1잡음 수정본
    j3=Joint(89.228, 31.419, 93.722, 1.878, 45.628, -2.373)#올
    j4=Joint(176.599, 27.579, 93.733, 1.671, 58.148, -2.372)#옆 옮
    j5=Joint(176.600, 41.700, 93.735, 1.791, 47.148, -1.852)#내림
    j6=Joint(176.598, 23.626, 93.736, 1.671, 47.154, -1.796)#올림
	

	
    j7=Joint(89.286, 43.390, 93.719, 1.880, 44.572, -2.377)#box2잡음 수정본
    j8=Joint(89.237, 29.740, 93.725, 1.671, 55.780, -2.371)#올
    j9=Joint(153.518, 29.753, 93.732, 1.671, 55.757, -26.432)#옆 옮
    j10=Joint(156.281, 42.340, 93.120, 1.746, 46.562, -23.176)#내림
    j11=Joint(156.279, 28.906, 93.122, 1.671, 46.564, -23.172)#올림
	

    j12=Joint(89.239, 24.721, 93.724, 1.671, 60.805, -2.369)#box3올림
    j13=Joint(176.535, 24.744, 93.734, 1.671, 60.814, -2.372)#옆 옮
    j14=Joint(176.635, 35.044, 90.697, 1.671, 55.672, -2.372)#내림
    j15=Joint(176.635, 24.316, 90.697, 1.671, 64.959, -2.372)#올림
	

    j16=Joint(89.159, 43.342, 93.735, 1.880, 42.974, -0.298)#잡음box4 수정본
    j17=Joint(89.232, 25.067, 93.727, 1.671, 60.522, -0.292)#올림
    j18=Joint(156.191, 25.378, 89.855, 1.671, 54.047, -21.679)#옆 옮
    j19=Joint(156.521, 36.245, 89.861, 1.755, 53.988, -21.680)#내림
    j20=Joint(156.043, 26.818, 91.110, 1.671, 62.006, -21.683)#올림

    j21=Joint(89.229, 14.461, 92.658, 1.073, 72.101,-0.296)#올림box5,box6
    j22=Joint(177.068, 20.635, 85.205, 1.073, 64.912, -0.296)#옆 옮
    j23=Joint(177.068, 30.00, 85.208, 1.073, 64.973, -0.296)#내림
    j24=Joint(177.068, 20.180, 85.209, 1.073, 73.595, -0.296)#올림
    j25=Joint(90.638, 20.184, 85.211, 1.073, 72.993, -0.296)#원위치2

    j26=Joint(156.306, 18.866, 81.599, 1.372, 68.046, -21.659)#옆 옮box6
    j27=Joint(156.315, 33.243, 81.602, 1.502, 67.998, -21.678)#내림
    j28=Joint(156.315, 25.973, 81.606, 1.372, 67.953, -21.678)#올림
    j29=Joint(98.412, 24.557, 81.595, 1.372, 73.002, -22.873)#원위치3

    ## 3. 로봇 동작을 정의 ##############################
    # 작업 시작
    try:
        while True:
            Socket_data = sock.recv(65535) 
            Socket_data = Socket_data.decode()
            print (Socket_data)  

            if Socket_data == '1':
                rb.move(j1,j2)
                rb.sleep(sec=2)
                
                rb.move(j3,j4,j5)
	        rb.sleep(sec=1)
		

		rb.move(j6,j1)


                Send_Data = Send_Data.encode()
                sock.send(Send_Data) 

            elif Socket_data == '2':   
                rb.move(j7)
		rb.sleep(sec=2)

		rb.move(j8,j9,j10)
		rb.sleep(sec=1)

		rb.move(j11, j1)

                Send_Data = Send_Data.encode()
                sock.send(Send_Data) 

            elif Socket_data == '3':
                rb.move(j2)
                rb.sleep(sec=2)
                
                rb.move(j12,j13,j14)
	        rb.sleep(sec=1)
		
		rb.move(j15,j1)

		Send_Data = Send_Data.encode()
                sock.send(Send_Data)
		
	    elif Socket_data == '4':
                rb.move(j16)
                rb.sleep(sec=2)
                
                rb.move(j17,j18,j19)
	        rb.sleep(sec=1)
		
		rb.move(j20,j1)
		Send_Data = Send_Data.encode()
                sock.send(Send_Data)

	    elif Socket_data == '5':
		rb.move(j2)
		rb.sleep(sec=3)
	
		rb.move(j21,j22,j23)

		rb.sleep(sec=1)

		rb.move(j24,j25,j1)
		Send_Data = Send_Data.encode()
                sock.send(Send_Data)

	    elif Socket_data == '6':
		rb.move(j2)
		rb.sleep(sec=3)
	
		rb.move(j21,j26,j27)

		rb.sleep(sec=1)
	
		rb.move(j28,j29,j1)

		Send_Data = Send_Data.encode()
                sock.send(Send_Data)
                
    except Robot_emo:
        rb.close() 
        rb.exit(1)

    #finally:
        #rb.close()
        #rb.exit(1)

 
    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    rb.close()
if __name__ == '__main__':
    main()