import cv2
import numpy as np
import threading
import time
from queue import Queue

class RobotSystem:
    def __init__(self):
        self.is_running = True
        self.control_mode = "AUTO"
        self.command_queue = Queue()

        # --- 제어 설정  ---
        self.target_center = 320
        self.deadzone = 20
        self.full_threshold = 0.8
        self.fixed_thresh_val = 120


        self.thread = threading.Thread(target=self.opencv_thread)
        self.thread.daemon = True
        self.thread.start()

    def opencv_thread(self):
        print(f"[AUTO] 시스템 시작 ")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("에러: 캠을 찾을 수 없습니다.")
            return

        # 창 크기 조절 가능 설정 # check
        cv2.namedWindow("Main View", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 1: ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 2: Warped ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 3: Binary View", cv2.WINDOW_NORMAL)

        while self.is_running:
            ret, frame = cap.read()
            if not ret: break

            img = cv2.flip(frame, 1)
            img = cv2.resize(img, (640, 480)) 
            h, w = img.shape[:2]

            if self.control_mode == "AUTO":
                # --- ROI 설정 ---
                y1, y2 = 320, 480
                roi_rate = 2
                roi_size = 80
                center_x = int(2 * w / 4)

                x1, x2 = max(0, int(center_x - roi_rate * roi_size)), min(w, int(center_x + roi_rate * roi_size))

                roi_w, roi_h = x2 - x1, y2 - y1
                roi_raw = img[y1:y2, x1:x2].copy()

                # top_ratio: 0.0 ~ 1.0 (윗변이 아랫변 대비 얼마나 넓은지)
                top_ratio = 0.8

                top_width = roi_w * top_ratio
                top_margin = (roi_w - top_width) / 2

                src_pts = np.float32([
                    [top_margin, 0],               # 좌상 (Top Left)
                    [roi_w - top_margin, 0],       # 우상 (Top Right)
                    [roi_w, roi_h],                # 우하 (Bottom Right)
                    [0, roi_h]                     # 좌하 (Bottom Left)
                ])

                # 최적화도니 ratio 값 구하기

                dst_pts = np.float32([[0, 0], [roi_w, 0], [roi_w, roi_h], [0, roi_h]])
                matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
                roi_color = cv2.warpPerspective(roi_raw, matrix, (roi_w, roi_h))

                # ---  전처리 및 분석 ---
                gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
                blurred = cv2.GaussianBlur(gray, (9, 9), 0)
                _, thresh = cv2.threshold(blurred, self.fixed_thresh_val, 255, cv2.THRESH_BINARY_INV)

                total_pixels = thresh.shape[0] * thresh.shape[1]
                white_pixels = cv2.countNonZero(thresh)
                white_ratio = white_pixels / total_pixels
                M = cv2.moments(thresh)

                # --- 결과 판단 및 명령 전송 ---
                status_text = "LOST"
                display_color = (0, 0, 255)

                if white_ratio > self.full_threshold:
                    status_text, display_color = "STOP", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})
                elif white_pixels == 0:
                    status_text, display_color = "LINE LOST! (STOP)", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})
                elif M['m00'] > 0:
                    cx_roi = int(M['m10'] / M['m00'])
                    cx_global = cx_roi + x1
                    # error_value를 변형해서 보냄
                    error_value = self.target_center - cx_global

                    if abs(error_value) <= self.deadzone:
                        status_text, display_color = "GO", (255, 255, 0)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_GO', 'value': error_value})
                    elif error_value > 0:
                        status_text, display_color = f"LEFT: +{abs(round(error_value, 1))}", (0, 255, 0)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_LEFT', 'value': error_value})
                    else:
                        status_text, display_color = f"RIGHT: -{abs(round(error_value, 1))}", (0, 165, 255)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_RIGHT', 'value': error_value})

                    cv2.circle(img, (cx_global, int(y1 + roi_h/2)), 10, (0, 0, 255), -1)
                else:
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                # ---  시각화 업데이트 ---
                # ROI 네모
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 원근 사다리꼴
                trap_pts = np.array([
                    [src_pts[0][0] + x1, src_pts[0][1] + y1],
                    [src_pts[1][0] + x1, src_pts[1][1] + y1],
                    [src_pts[2][0] + x1, src_pts[2][1] + y1],
                    [src_pts[3][0] + x1, src_pts[3][1] + y1]
                ], dtype=np.int32)
                cv2.polylines(img, [trap_pts], True, (0, 0, 255), 2)

                # 타겟 범위
                left_boundary = self.target_center - self.deadzone
                right_boundary = self.target_center + self.deadzone
                cv2.line(img, (left_boundary, y1), (left_boundary, y2), (0, 255, 255), 2)
                cv2.line(img, (right_boundary, y1), (right_boundary, y2), (0, 255, 255), 2)
                cv2.circle(img, (self.target_center, int(y1 + roi_h/2)), 3, (0, 212, 255), -1)

                cv2.putText(img, status_text, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, display_color, 3)

                cv2.imshow("Check 1: ROI", roi_raw)             # check
                cv2.imshow("Check 2: Warped ROI", roi_color)    # check
                cv2.imshow("Check 3: Binary View", thresh)      # check

            cv2.imshow("Main View", img)                        # check
            key = cv2.waitKey(1) & 0xFF                         # check
            if key == ord('q'): self.is_running = False         # check
            elif key == ord('m'): self.control_mode = "MANUAL" if self.control_mode == "AUTO" else "AUTO"       # check

        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    robot = RobotSystem()
    try:
        while robot.is_running:
            if not robot.command_queue.empty():
                data = robot.command_queue.get()
            time.sleep(0.01)
    except KeyboardInterrupt:
        robot.is_running = False
