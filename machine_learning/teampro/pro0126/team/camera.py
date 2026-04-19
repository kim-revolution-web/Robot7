class RobotSystem:
    def __init__(self):
        self.is_running = True
        self.control_mode = "AUTO"
        self.command_queue = Queue()
        self.shape_detector = ShapeDetector(self.command_queue)

        self.target_center = 320
        self.deadzone = 20
        self.full_threshold = 0.8
        self.fixed_thresh_val = 100

        self.thread = threading.Thread(target=self.opencv_thread)
        self.thread.daemon = True
        self.thread.start()

    def opencv_thread(self):
        print(f"[AUTO] 시스템 시작 ")
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("에러: 캠을 찾을 수 없습니다.")
            return

        while self.is_running:
            ret, frame = cap.read()
            if not ret: break

            img = cv2.flip(frame, 1)
            img = cv2.resize(img, (640, 480))
            h, w = img.shape[:2]

            # 1. 전처리 (이진화)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (9, 9), 0)
            _, full_thresh = cv2.threshold(blurred, self.fixed_thresh_val, 255, cv2.THRESH_BINARY_INV)

            if self.control_mode == "AUTO":
                # 2. [우선순위 1] 도형 인식 수행 및 화면 표시 수정
                shape_name = self.shape_detector.run(img, full_thresh)

                if shape_name: # 도형이 감지된 경우
                    status_text = f"EVENT: {shape_name}"
                    display_color = (0, 0, 255) # 빨간색

                    # 화면 중앙에 큰 글씨로 강조 표시 추가
                    cv2.putText(img, "!!! SHAPE DETECTED !!!", (w//2-200, h//2),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
                else:
                    # 3. [우선순위 2] 선 인식 (주행) 수행
                    y1, y2 = 320, 480
                    roi_rate, roi_size = 2, 80
                    center_x = int(2*w / 4)
                    x1, x2 = max(0, int(center_x - roi_rate * roi_size)), min(w, int(center_x + roi_rate * roi_size))

                    roi_line = full_thresh[y1:y2, x1:x2]
                    white_pixels = cv2.countNonZero(roi_line)
                    white_ratio = white_pixels / (roi_line.shape[0] * roi_line.shape[1])
                    M = cv2.moments(roi_line)

                    # 가이드라인 그리기
                    cv2.line(img, (self.target_center - self.deadzone, y1), (self.target_center - self.deadzone, y2), (0, 255, 255), 2)
                    cv2.line(img, (self.target_center + self.deadzone, y1), (self.target_center + self.deadzone, y2), (0, 255, 255), 2)

                    if white_ratio > self.full_threshold:
                        status_text, display_color = "STOP (FULL)", (0, 0, 255)
                        self.command_queue.put({'source': 'CAMERA', 'status': 'STOP', 'cmd': 0})
                    elif white_pixels == 0:
                        status_text, display_color = "LINE LOST!", (0, 0, 255)
                        self.command_queue.put({'source': 'CAMERA', 'status': 'STOP', 'cmd': 0})
                    elif M['m00'] > 0:
                        cx_global = int(M['m10'] / M['m00']) + x1
                        error_value = self.target_center - cx_global

                        if abs(error_value) <= self.deadzone:
                            status_text, display_color = "GO", (255, 255, 0)
                            self.command_queue.put({'source': 'CAMERA', 'status': 'GO', 'cmd': 0})
                        else:
                            status_text = "LEFT" if error_value > 0 else "RIGHT"
                            display_color = (0, 255, 0) if error_value > 0 else (0, 165, 255)
                            self.command_queue.put({'source': 'CAMERA', 'status': status_text, 'cmd': error_value})

                        cv2.circle(img, (cx_global, int(y1 + 80)), 10, (0, 0, 255), -1)
                    else:
                        status_text, display_color = "SEARCHING...", (0, 0, 255)

                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.imshow("Binary View", roi_line)

                # 공통 상태 텍스트 출력
                cv2.putText(img, status_text, (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 1.2, display_color, 3)

            cv2.imshow("Main View", img)
            if cv2.waitKey(1) & 0xFF == ord('q'): self.is_running = False

        cap.release()
        cv2.destroyAllWindows()

# [메인 실행부]
if __name__ == "__main__":
    robot = RobotSystem()
    try:
        while robot.is_running:
            if not robot.command_queue.empty():
                data = robot.command_queue.get()

                # [유턴 동작 실행 예시]
                if data.get('action') == 'UTURN':
                    print(">>> [ACTION] 로봇 유턴 기동 중... (모터 제어 코드 연결 필요)")
                    # 여기에 실제 모터 유턴 함수를 넣으렴!

                print(f"[CONTROL] Source: {data.get('source')} | Action/Status: {data.get('action') or data.get('status')} | Speed: {data.get('speed', 'N/A')}")
            time.sleep(0.01)
    except KeyboardInterrupt:
        robot.is_running = False