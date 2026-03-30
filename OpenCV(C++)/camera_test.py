import cv2
import cv2

for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened(): #True → 카메라 장치를 여는 데 성공
        ret, frame = cap.read() # → 카메라에서 한 장 읽기 . frame 실제 영상 이미지 데이터가 들어감
        if ret: # ret 읽기 성공 여부 성공하면 True 실패하면 False
            print(f"{i} 번 카메라 사용 가능")
        else:
            print(f"{i} 번 카메라 열림, 하지만 프레임 못 읽음")
        cap.release() # → 카메라 사용 끝내기
    else:
        print(f"{i} 번 카메라 열기 실패")
