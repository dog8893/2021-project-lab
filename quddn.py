# 라이브러리 선언
import cv2
import winsound as sd
import time

# 비프음 함수 선언
def beepsound():
    fr = 2000 # 소리의 주파수를 헤르츠 단위로 지정 (범위 : 37~32767)
    du = 250 # 소리의 지속시간을 밀리초로 지정
    sd.Beep(fr, du)

num = 0

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) # 캡쳐를 사용할 시 cv2.CAP_DSHOW 추가
if cap.isOpened() == False:
    print('can not open the cam 1')

while(True):
    ret, img_ori  = cap.read()
    if img_ori is None:
        print('frame is not exist')

    # q누를시 작동
    if cv2.waitKey(1) & 0xFF == 113:
        beepsound()
        time.sleep(0.25)
        beepsound()
        time.sleep(0.25)
        beepsound()
        print('capture!')
        file_name = 'capture_'+str(num)+'.png' #  파일명 정의
        print(file_name)
        cv2.imwrite('capture_file/'+str(file_name), img_ori, params=[cv2.IMWRITE_PNG_COMPRESSION,0]) # (경로설정, 캡쳐할 화면, 선명도 0~100 현재 0)
        num = num + 1

    # 화면 띄우기
    cv2.imshow('img_ori', img_ori)

    # ESC 누르면 프로그램 종료
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()