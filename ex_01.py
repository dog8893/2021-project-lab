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

def main():
    ## 2. 초기 설정 ####################################
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
    m = MotionParam( jnt_speed=10, lin_speed=10, pose_speed=10, overlap = 30 )
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam( m )
   
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1)
    sock.connect(('192.168.0.50',5000))
    
    ## 3. 로봇 동작을 정의 ##############################
    # 작업 시작
    Socket_data = 'loop'
    while True:
        Socket_data = Socket_data.encode()
        sock.send(Socket_data) 

        Socket_data = sock.recv(65535) 
        Socket_data = Socket_data.decode()
        print Socket_data
        rb.sleep(1)

    ## 4. 종료 ######################################
    # 로봇과의 연결을 종료
    rb.close()
if __name__ == '__main__':
    main()