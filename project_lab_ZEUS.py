#!/usr/bin/python
# -*- coding: utf-8 -*-

## 1. 초기 설정① #######################################
# 라이브러리 가져오기
import socket
from i611_MCS import * #로봇 제어에 필요한 기본기능을 사용
from i611_extend import * #확장 기능을 사용(팔레트 기능)
from i611_io import * #i/o 신호를 제어
from teachdata import * #교시 데이터를 사용
from rbsys import * #관리 프로그램을 사용
from i611_common import * #i611 robot 클래스의 예외 처리
from i611shm import * # 공유 메모리에 엑세스
import time 
def main(): #메소드 생성자
  
    ## 2. 초기 설정② ####################################
    # i611 로봇 생성자
    rb = i611Robot()
    # 좌표계의 정의
    _BASE = Base()
    # 로봇과 연결 시작 초기화
    rb.open()
    # I/O 입출력 기능의 초기화 (I/O 미사용시 생략 가능 )
    IOinit( rb )

    data = Teachdata( "teach_data" )
    
    #소켓 설정
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)
    sock.connect(('192.168.0.45',8888))
    Send_Data = 'OK'
    
    ## 3. 교시 포인트 설정 ######################
    p1 = data.get_position( "pos1", 6 ) #물건집는 위치1 기준 0,0
    p2 = data.get_position( "pos1", 8 ) #물건집는 위치2 x->y값수정
    p3 = data.get_position( "pos1", 7 ) #물건집는 위치3 y->x값수정
    p1 = p1.offset(dz=+12)
    p2 = p2.offset(dz=+12)
    p3 = p3.offset(dz=+12)
    
    #p11 = p1.offset(dx=10,dy=20,dz=-10)
    #팔레트 정의
    pal = Pallet() 
    pal.init_3(p1,p2,p3,301,301)#팔레트를 정의했는데 3점교시를 하겠다. 팔레트 위치 크기정의 (5,4)

    #p01 = pal.get_pos(0,0) #설정후 잡을 위치설정

    #p02 = pal.get_pos(104,60)
    #p03 = pal.get_pos(2,3)

    ## 4. 동작 조건 설정 ##################################
    #MotionParam 생성자에서 동작 조건 설정
    m = MotionParam( jnt_speed=10, lin_speed=70 )
    m1 = MotionParam( jnt_speed=30, lin_speed=210 )
    m2 = MotionParam( jnt_speed=20, lin_speed=10)

    #MotionParam 형으로 동작 조건 설정
    rb.motionparam( m1 )
    
    j2=Joint(89.226, 19.909, 93.297, 0.180, 66.159, -1.809)
    j3=Joint(85.588, 24.246, 99.409, -0.116, 55.450, -4.751)
    j4=Joint(85.588, 32.996, 106.109, -0.054, 40.031, -4.750)
    p02 = data.get_position( "pos1", 4 )

    rb.move(p02)
    rb.sleep(0.5)
    ## 5. 로봇 동작을 정의 ##############################
    # 작업 시작

    while True:
        socket_data_x = sock.recv(65535)
        socket_data_x = socket_data_x.decode()

        socket_data_y = sock.recv(65535)
        socket_data_y = socket_data_y.decode()

        p00 = pal.get_pos(int(socket_data_x),int(socket_data_y))
        p01 = pal.get_pos(int(socket_data_x),int(socket_data_y)+150)
        p01 = p01.offset(dz=-20)

        rb.motionparam( m2 )
        rb.move(p00)
        rb.sleep(2.49)
        rb.move(p01)

        rb.move(p02)
        rb.sleep(0.5)
        
        rb.move(j3)
        rb.sleep(0.5)
        rb.move(j4)
        Send_Data = Send_Data.encode()
        sock.send(Send_Data)
        rb.sleep(3)
        rb.move(j3)
        rb.sleep(0.5)

        rb.move(p02)
        rb.sleep(0.5)

        print("Finish")
        rb.sleep(0.5)

 
    ## 6. 종료 ######################################
    # 로봇과의 연결을 종료

if __name__ == '__main__':
    main()