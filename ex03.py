#!/usr/bin/python
# -*- coding: utf-8 -*-

## 1. 초기 설정① #######################################
# 라이브러리 가져오기
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
  
    ## 3. 교시 포인트 설정 ######################
    p1 = data.get_position( "pos2", 4 ) #물건집는 위치
    p2 = data.get_position( "pos2", 6 ) #물건집는 위치2
    p3 = data.get_position( "pos2", 7 ) #물건집는 위치3
    #p11 = p1.offset(dx=10,dy=20,dz=-10)
    #팔레트 정의
    pal = Pallet() 
    pal.init_3(p1,p2,p3,3,3)#팔레트를 정의했는데 3점교시를 하겠다. 팔레트 위치 크기정의 (5,4)

    #작업 위치 검색
    p00 = pal.get_pos(0,0)
    p01 = pal.get_pos(2,0)
    p02 = pal.get_pos(0,2)
    p03 = pal.get_pos(2,2)
    p04 = pal.get_pos(1,1)
    #j1 = data.get_joint( "joint1", 1 ) #물건위치 위
    #j2 = data.get_joint( "joint1", 2 ) #놓을위치 위
 
    ## 4. 동작 조건 설정 ##################################
    #MotionParam 생성자에서 동작 조건 설정
    m = MotionParam( jnt_speed=10, lin_speed=70 )
    m1 = MotionParam( jnt_speed=20, lin_speed=140 )
    m2 = MotionParam( jnt_speed=30, lin_speed=210 )
    m3 = MotionParam( jnt_speed=40, lin_speed=280,overlap=50 )
    #현재 매니플레이터 값 불러오기
    pos200 = rb.getpos() 
    xyz=pos200.pos2list()
    print(xyz)
    #MotionParam 형으로 동작 조건 설정
    rb.motionparam( m2 )
    ## 5. 로봇 동작을 정의 ##############################
    # 작업 시작
    rb.home()
    rb.move(p00)
    rb.sleep(0.5)
    rb.move(p01)
    rb.sleep(0.5)
    rb.move(p02)
    rb.sleep(0.5)
    rb.move(p03)
    rb.sleep(0.5)
    rb.move(p04)
    rb.sleep(0.5)
    rb.home()
        #if i==2:
            #rb.motionparam(m1)
            
        #elif i==2:
            #rb.motionparam(m2)
        #else:
            #rb.motionparam(m3)




            #break

    rb.home()
 
    ## 6. 종료 ######################################
    # 로봇과의 연결을 종료
    rb.close()

if __name__ == '__main__':
    main()