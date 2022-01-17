import cv2

# 컴퓨터에 연결된 카메라 on
# 괄호 안에는 0부터 번호 넣어보면서 포트번호 찾으면 된다.
cap = cv2.VideoCapture(0)

# 카메라를 열지 못했을 때를 알기 위해 예외처리를 한다.
if not cap.isOpened():
    print('Camera not opened')
    exit()

# 이미지를 연속으로 출력하여 영상을 만드는 개념이기 때문에
# while 반복문을 사용해서 이미지 처리를 무한반복시켜 영상으로 보이게 한다.
while(True):
    # 앞에 정의한 cap의 순간을 읽어서 이미지로 frame에 저장
    ret, frame = cap.read()

    # 영상(이미지)을 정의하지 못했을 때 반복문 탈출하는 예외처리를 한다.
    if not ret:
        print('image error!')
        break

    # frame에 저장된 이미지를 창을 띄워서 출력
    # 미리 cv2.nameWindow로 정의한 창이 없으면 자동으로 입력된(아래서는 'image')
    # 창을 만들어서 띄워준다.
    cv2.imshow('image', frame)

    # 특정 키가 눌리면 반복문을 벗어나게 하는 처리
    # 27이 ESC 버튼이고 찾아보면 키보드 버튼마다 지정된 번호가 있다.
    if cv2.waitKey(1) == 27:
        break

# 모든 창 종료
cv2.destroyAllWindows()