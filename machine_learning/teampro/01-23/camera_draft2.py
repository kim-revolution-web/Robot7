import cv2                    # OpenCV: 카메라 읽기/영상처리/화면 표시
import numpy as np            # (현재 코드에선 직접 사용은 거의 없음, 보통 영상처리에 자주 씀)
import threading              # 스레드로 opencv_thread 실행
import time                   # 루프 대기/속도 조절
from queue import Queue       # 스레드 간 데이터 전달(오차값 error 전달)

class RobotSystem:
    def __init__(self):
        self.is_running = True                 # 프로그램 전체 실행 플래그 (False면 종료)
        self.control_mode = "AUTO"             # 시작 모드: "AUTO" 또는 "MANUAL"
        self.command_queue = Queue()           # OpenCV가 계산한 error를 넣는 큐

        # opencv_thread를 백그라운드(daemon) 스레드로 실행
        self.thread = threading.Thread(target=self.opencv_thread)
        self.thread.daemon = True              # 메인 프로그램 종료 시 스레드도 같이 종료
        self.thread.start()                    # 스레드 시작

    def opencv_thread(self):
        print("[RobotSystem] 테스트 시작 (모드 변경: 'm', 종료: 'q')")

        cap = cv2.VideoCapture(0)              # PC 기본 웹캠(0번) 열기
        if not cap.isOpened():
            print("에러: 캠을 찾을 수 없습니다.")
            return

        while self.is_running:
            ret, frame = cap.read()            # 카메라에서 한 프레임 읽기
            if not ret:
                break                          # 프레임 읽기 실패하면 종료

            # 좌우 반전(거울 모드) 및 크기 조절
            img = cv2.flip(frame, 1)           # 1이면 좌우 반전
            img = cv2.resize(img, (640, 480))  # 화면 크기 고정(가로 640, 세로 480)

            h, w = img.shape[:2]               # 이미지 높이/너비

            # AUTO 모드일 때만 라인 인식 수행
            if self.control_mode == "AUTO":
                # 1) 전처리: 그레이 변환 + 블러(노이즈 제거)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)          # 컬러 -> 그레이
                blur = cv2.GaussianBlur(gray, (5, 5), 0)              # 가우시안 블러(5x5)

                # 2) 이진화: Otsu로 임계값 자동 결정 + (검은 선을 흰색으로 뒤집기)
                # - THRESH_BINARY_INV: 어두운 선을 흰색(255)으로 만들기 쉬움
                # - THRESH_OTSU: 적절한 임계값을 자동으로 찾아줌
                _, thresh = cv2.threshold(
                    blur, 120, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
                )

                # 3) ROI 설정: 화면의 하단 1/3 영역 + 가로는 중앙 50%만 본다
                #    - 가로: w/4 ~ 3w/4
                #    - 세로: 2h/3 ~ h
                x_start, x_end = int(w / 4), int(3 * w / 4)
                y_start, y_end = int(2 * h / 3), h

                roi = thresh[y_start:y_end, x_start:x_end]            # ROI 잘라내기

                # 4) 모멘트(moment) 계산으로 흰색(선)의 무게중심 찾기
                M = cv2.moments(roi)

                if M['m00'] > 0:
                    # roi 내부(잘라낸 영상 기준)에서의 중심 x좌표
                    cx_relative = int(M['m10'] / M['m00'])

                    # [중요] roi는 x_start부터 잘라냈으므로,
                    # 전체 화면 좌표로 바꾸려면 x_start 오프셋을 더해줘야 함
                    cx_global = cx_relative + x_start

                    # 오차(error) 계산: 화면 중앙(w/2) 기준 얼마나 왼/오로 치우쳤는지
                    # +면 선이 오른쪽, -면 선이 왼쪽
                    error = cx_global - (w / 2)

                    # 큐에 오차값 전송(다른 스레드/로직이 이 값을 받아 제어에 사용 가능)
                    self.command_queue.put({'source': 'OPENCV', 'cmd': error})

                    # 시각화: 중심점(빨간 원) 표시
                    # y는 ROI 세로 중앙쯤에 찍기 위해 y_start + ROI높이/2 사용
                    cv2.circle(
                        img,
                        (cx_global, int(y_start + (y_end - y_start) / 2)),
                        10, (0, 0, 255), -1
                    )
                else:
                    # 선(흰색 영역)을 못 찾으면 0을 보내서 “오차 없음” 또는 “감속 유도”로 처리
                    self.command_queue.put({'source': 'OPENCV', 'cmd': 0})

                # ROI 영역 시각화(초록 사각형)
                cv2.rectangle(img, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)

                # 디버그 창 표시
                cv2.imshow("Auto View (Thresh)", thresh)              # 이진화된 전체 화면
                cv2.imshow("Original with Centroid", img)             # 원본 + ROI/중심점 표시

            # 키 입력 처리(1ms 대기하면서 키 읽음)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                self.is_running = False                                # q 누르면 종료
            elif key == ord('m'):
                # m 누르면 AUTO<->MANUAL 토글
                self.control_mode = "MANUAL" if self.control_mode == "AUTO" else "AUTO"
                print(f"모드 변경: {self.control_mode}")

        # 루프 종료 시 리소스 정리
        cap.release()                                                 # 카메라 해제
        cv2.destroyAllWindows()                                       # OpenCV 창 닫기

# 이 파일을 직접 실행했을 때만 동작하는 테스트 코드
if __name__ == "__main__":
    robot = RobotSystem()                                             # RobotSystem 생성 → 스레드 자동 시작

    try:
        while robot.is_running:
            # OpenCV 스레드가 큐에 넣은 데이터가 있으면 꺼내기
            if not robot.command_queue.empty():
                data = robot.command_queue.get()                      # {'source':'OPENCV','cmd':error}

                # 데이터 흐름 확인용 (필요하면 주석 해제)
                # print(f"Error: {data['cmd']}")

            time.sleep(0.01)                                          # CPU 과점유 방지(10ms 쉬기)

    except KeyboardInterrupt:
        # 터미널에서 Ctrl+C로 종료
        robot.is_running = False