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
import pdb
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
    #joint 동작에 동작 속도 비율을 설정
    rb.override(50)

    data = Teachdata( "teach_data" )
  
    ## 3. 교시 포인트 설정 ######################
    p1 = data.get_position( "pos2", 4 ) #물건집는 위치
    p2 = data.get_position( "pos2", 6 ) #물건집는 위치2
    p3 = data.get_position( "pos2", 7 ) #물건집는 위치3
    p4 = data.get_position( "pos2", 8 ) #물건집는 위치4 
    #p11 = p1.offset(dx=10,dy=20,dz=-10)
    
    #팔레트 정의
    pal = Pallet() 
    pal.init_4(p1,p2,p3,p4,5,4)#팔레트를 정의했는데 3점교시를 하겠다. 팔레트 위치 크기정의 (5,4)

    #작업 위치 검색
    p00 = pal.get_pos(0,0) # 원점
    #p01 = pal.get_pos(4,0) # x축 끝단
    #p02 = pal.get_pos(0,3) # y축 끝단
    #p03 = pal.get_pos(4,3) # 원점 대각선 (pij지점)
    p04 = pal.get_pos(2,0) # 작업지점1
    p05 = pal.get_pos(0,1) # 작업지점2
    p06 = pal.get_pos(1,2) # 작업지점3
    p07 = pal.get_pos(1,1) # 작업지점4
    #작업지점분류
    p08 = pal.get_pos(4,3) # 작업지점5
    p09 = pal.get_pos(4,2) # 작업지점6
    p001 = pal.get_pos(3,3) # 작업지점7
    p002 = pal.get_pos(3,2) # 작업지점8

    p11 = p1.offset(dz=200) #1번 물체 up
    p041 = p04.offset(dz=200)
    p051 = p05.offset(dz=200)
    p061 = p06.offset(dz=200)
    p071 = p07.offset(dz=200)
    #작업지점 분류
    p081 = p08.offset(dz=200)
    p091 = p09.offset(dz=200)
    p0011 = p001.offset(dz=200)
    p0021 = p002.offset(dz=200)

    j1 = data.get_joint( "joint1", 1 ) #물건위치 위
    j2 = data.get_joint( "joint1", 2 ) #놓을위치 위
 
    ## 4. 동작 조건 설정 ##################################
    #MotionParam 생성자에서 동작 조건 설정
    m = MotionParam( jnt_speed=10, lin_speed=70 )
    m1 = MotionParam( jnt_speed=20, lin_speed=140 )
    m2 = MotionParam( jnt_speed=30, lin_speed=210)
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
    dout(48,'100') #작업1 놓고
    pdb.set_trace() #디버깅 모드 다음스텝은 n , 그냥 진행은 c

    rb.move(p11) #1위
    rb.sleep(0.5)
    rb.move(p00) #1아래
    rb.sleep(0.5)
    dout(48,'001') #집고
    rb.sleep(0.5)
    rb.move(p11) #1위
    rb.sleep(0.5)
    rb.move(p081) #작업1 위로이동
    rb.sleep(0.5)
    rb.move(p08) #작업1 아래
    dout(48,'100') #작업1 놓고
    rb.sleep(0.5)
    rb.move(p081) #작업1 위
    rb.sleep(0.5)
    rb.move(p041) #2위로 이동
    rb.sleep(0.5)
    rb.move(p04) #2아래
    rb.sleep(0.5)
    dout(48,'001') #집고
    rb.sleep(0.5)
    rb.move(p041) #2위로 이동
    rb.sleep(0.5)
    rb.move(p091) #작업2 위로 이동
    rb.sleep(0.5)
    rb.move(p09) #작업2 아래 
    rb.sleep(0.5)
    dout(48,'100') #놓고
    rb.sleep(0.5)
    rb.move(p091) #작업2 위로이동
    rb.sleep(0.5)
    rb.move(p051) #3위로 이동
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