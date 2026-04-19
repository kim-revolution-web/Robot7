import cv2
import numpy as np
import threading
import time
from queue import Queue

class ShapeDetector:
    def __init__(self, queue):
        self.queue = queue
        self.base_speed = 0.1
        print("[System] 도형 감지 모듈 초기화 완료")

    def handle_events(self, shape):
        """도형별 동작 결정 및 큐 전송"""
        command_data = {'source': 'SHAPE', 'type': shape, 'speed': self.base_speed * 0.5, 'action': 'SLOW'}
        print(f">> [EVENT TRIGGER] {shape} 감지! 명령 전송")
        self.queue.put(command_data)
        time.sleep(1.5) # 1.5초 동안 상태 유지 (선 인식 차단 시간)

    def run(self, frame, thresh_roi, sx1, sy1, sx2, sy2):
        """
        thresh_roi: 이미 ROI 크기로 잘려진 이진화 영상
        sx1, sy1: 원본 프레임에서의 시작 좌표 (박스 그리기에 필요)
        """
        # 윤곽선 찾기 (이미 잘려진 roi 영상에서 찾으므로 가볍습니다)
        contours, _ = cv2.findContours(thresh_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 원본 영상에 노란색 가이드라인 표시
        cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), (0, 255, 255), 2)

        detected = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 3000: # 물체 크기 기준
                x, y, bw, bh = cv2.boundingRect(cnt)

                # 시각화: 빨간색 박스와 텍스트 (sx1, sy1을 더해 원본 위치에 정확히 표시)
                cv2.rectangle(frame, (x+sx1, y+sy1), (x+sx1+bw, y+sy1+bh), (0, 0, 255), 3)
                cv2.putText(frame, "Shape", (x+sx1, sy1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # 스레드 실행
                threading.Thread(target=self.handle_events, args=("TRIANGLE",), daemon=True).start()
                detected = True
                break
        return detected

class TestSystem:
    def __init__(self):
        self.is_running = True
        self.q = Queue()
        self.detector = ShapeDetector(self.q)

    def start(self):
        cap = cv2.VideoCapture(0) # 0번 카메라 오픈
        if not cap.isOpened():
            print("카메라를 열 수 없습니다.")
            return

        print("테스트 시작: 'q'를 누르면 종료됩니다.")

        while self.is_running:
            ret, frame = cap.read()
            if not ret: break

            frame = cv2.flip(frame, 1) # 좌우 반전
            display_img = cv2.resize(frame, (640, 480))
            h, w = display_img.shape[:2]

            # --- [ROI 설정] ---
            # 원하시는 영역 좌표 계산
            sx1, sx2, sy1, sy2 = int(w*0.2), int(w*0.8), int(h*0.1), int(h*0.6)

            # --- [ROI 부분만 전처리] ---
            # 1. 원본에서 해당 영역만 자르기 (Slicing)
            roi_img = display_img[sy1:sy2, sx1:sx2]

            # 2. 잘라낸 부분에 대해서만 이진화 진행
            gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh_roi = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

            # --- 모듈 실행 (잘린 thresh_roi와 좌표값 전달) ---
            is_active = self.detector.run(display_img, thresh_roi, sx1, sy1, sx2, sy2)

            if is_active:
                cv2.putText(display_img, "STATUS: Shape Recognition", (10, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 3)

            # --- 화면 표시 ---
            cv2.imshow("Main Stream", display_img) # 원본+결과
            cv2.imshow("Thresh View (ROI ONLY)", thresh_roi) # 이제 창 크기가 박스만해집니다.

            # 큐 데이터 출력
            while not self.q.empty():
                print(f"[Queue Data] {self.q.get()}")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    sys = TestSystem()
    sys.start()
