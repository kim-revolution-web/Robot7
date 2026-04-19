import cv2                    # OpenCV: 카메라 읽기/영상처리/시각화
import numpy as np            # 원근변환(좌표 배열) 등에서 사용
import threading              # OpenCV 처리 스레드 실행
import time                   # 메인 루프 대기
from queue import Queue       # 스레드 간 데이터 전달(명령 전송)

class RobotSystem:
    def __init__(self):
        # ------------------------------
        # 시스템 상태
        # ------------------------------
        self.is_running = True                 # 전체 실행 플래그(False면 종료)
        self.control_mode = "AUTO"             # 시작 모드: AUTO / MANUAL
        self.command_queue = Queue()           # 카메라 스레드가 만든 명령을 메인으로 전달

        # ------------------------------
        # --- 제어 설정(튜닝 값들) ---
        # ------------------------------
        self.target_center = 320               # 화면 중앙 목표 x좌표(640폭 기준 중앙=320)
        self.deadzone = 20                     # 중앙 근처 허용 오차 범위(+/-20 안이면 GO로 간주)
        self.full_threshold = 0.8              # ROI가 너무 하얗게 꽉 차면(예: 바닥 반사/과노출) STOP
        self.fixed_thresh_val = 120            # 이진화 임계값(고정 threshold)

        # ------------------------------
        # OpenCV 처리 스레드 시작
        # ------------------------------
        self.thread = threading.Thread(target=self.opencv_thread)
        self.thread.daemon = True              # 메인 종료 시 스레드도 같이 종료
        self.thread.start()

    def opencv_thread(self):
        print(f"[AUTO] 시스템 시작 ")
        cap = cv2.VideoCapture(0)              # PC 웹캠(0번) 열기

        if not cap.isOpened():
            print("에러: 캠을 찾을 수 없습니다.")
            return

        # ------------------------------
        # 디버그용 창 생성: 크기 조절 가능한 WINDOW_NORMAL
        # ------------------------------
        cv2.namedWindow("Main View", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 1: ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 2: Warped ROI", cv2.WINDOW_NORMAL)
        cv2.namedWindow("Check 3: Binary View", cv2.WINDOW_NORMAL)

        while self.is_running:
            ret, frame = cap.read()            # 프레임 읽기
            if not ret:
                break                          # 카메라 읽기 실패 시 종료

            # 좌우 반전(거울 모드) + 화면 크기 고정
            img = cv2.flip(frame, 1)
            img = cv2.resize(img, (640, 480)) 
            h, w = img.shape[:2]               # h=480, w=640

            # AUTO일 때만 영상처리 + 명령 생성
            if self.control_mode == "AUTO":
                # ------------------------------
                # 1) ROI(관심영역) 설정
                #    - y1~y2: 화면 하단 영역만 보기 (라인은 보통 바닥쪽에 있음)
                #    - x1~x2: 화면 중앙 주변만 보기
                # ------------------------------
                y1, y2 = 320, 480              # 세로 ROI: 아래쪽(320~480)
                roi_rate = 2                    # roi_size에 곱해서 ROI 가로 폭 조절
                roi_size = 80                   # 기본 반폭 느낌 (중앙 기준 좌우 80*roi_rate)

                center_x = int(2 * w / 4)       # 화면 중앙(=w/2)인데 2*w/4로 쓴 것 (w/2와 동일)

                # ROI의 좌우 경계 계산(화면 밖으로 나가지 않게 clamp)
                x1 = max(0, int(center_x - roi_rate * roi_size))
                x2 = min(w, int(center_x + roi_rate * roi_size))

                roi_w, roi_h = x2 - x1, y2 - y1                     # ROI 폭/높이
                roi_raw = img[y1:y2, x1:x2].copy()                  # ROI 원본(컬러) 잘라오기

                # ------------------------------
                # 2) 원근 변환(사다리꼴 -> 직사각형)
                #    - top_ratio: 위쪽 폭을 아래쪽 폭 대비 얼마나 줄일지
                #    - 바닥 라인이 원근 때문에 위로 갈수록 좁아지는 걸 보정하는 용도
                # ------------------------------
                top_ratio = 0.8                                     # 위쪽 폭 = 아래 폭 * 0.8
                top_width = roi_w * top_ratio
                top_margin = (roi_w - top_width) / 2                # 위쪽 좌/우 여백

                # 원본(사다리꼴) 4점 좌표 (ROI 내부 좌표 기준)
                src_pts = np.float32([
                    [top_margin, 0],                                # 좌상
                    [roi_w - top_margin, 0],                        # 우상
                    [roi_w, roi_h],                                 # 우하
                    [0, roi_h]                                      # 좌하
                ])

                # 목적지(직사각형) 4점 좌표
                dst_pts = np.float32([
                    [0, 0], [roi_w, 0], [roi_w, roi_h], [0, roi_h]
                ])

                matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)     # 원근변환 행렬
                roi_color = cv2.warpPerspective(roi_raw, matrix, (roi_w, roi_h))  # ROI를 평평하게 펴기

                # ------------------------------
                # 3) 전처리 및 이진화
                # ------------------------------
                gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)        # 컬러 -> 그레이
                blurred = cv2.GaussianBlur(gray, (9, 9), 0)               # 노이즈 제거(9x9)
                # 검은 선을 찾기 위해 INV 사용(선이 흰색이 되도록)
                _, thresh = cv2.threshold(
                    blurred, self.fixed_thresh_val, 255, cv2.THRESH_BINARY_INV
                )

                # ------------------------------
                # 4) 흰색 비율/모멘트 계산(라인 검출)
                # ------------------------------
                total_pixels = thresh.shape[0] * thresh.shape[1]          # ROI 총 픽셀 수
                white_pixels = cv2.countNonZero(thresh)                   # 흰색 픽셀 수(=선으로 인식된 픽셀)
                white_ratio = white_pixels / total_pixels                 # 흰색 비율(0~1)
                M = cv2.moments(thresh)                                   # 모멘트(중심/면적 계산용)

                # ------------------------------
                # 5) 결과 판단 및 명령 전송
                #    - status_text: 화면에 띄울 상태
                #    - display_color: 텍스트 색상(디버그용)
                # ------------------------------
                status_text = "LOST"                                      # 기본 상태(못 찾음)
                display_color = (0, 0, 255)                                # 빨강(BGR)

                # (A) 흰색이 너무 많으면(ROI가 거의 흰색) -> 과검출/바닥 반사 가능 -> STOP
                if white_ratio > self.full_threshold:
                    status_text, display_color = "STOP", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                # (B) 흰색이 아예 없으면 -> 라인을 못 찾음 -> STOP
                elif white_pixels == 0:
                    status_text, display_color = "LINE LOST! (STOP)", (0, 0, 255)
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                # (C) 모멘트 면적이 있으면(선이 존재) -> 중심 계산 후 좌/우/직진 판단
                elif M['m00'] > 0:
                    # ROI 내부 기준 중심 x좌표
                    cx_roi = int(M['m10'] / M['m00'])

                    # 전체 화면 기준 x좌표로 변환(ROI가 x1부터 시작하니까 오프셋 더함)
                    cx_global = cx_roi + x1

                    # error_value: 목표 중앙(320) - 현재 중심(cx_global)
                    #  +면 라인이 왼쪽(현재가 작음) -> 왼쪽으로 치우침 -> LEFT로 보정하려는 의도
                    #  -면 라인이 오른쪽 -> RIGHT로 보정하려는 의도
                    error_value = self.target_center - cx_global

                    # 데드존 안이면 중앙 근처 -> GO
                    if abs(error_value) <= self.deadzone:
                        status_text, display_color = "GO", (255, 255, 0)
                        # AUTO_GO + 오차값(value) 같이 전송
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_GO', 'value': error_value})

                    # error_value > 0: 목표가 더 오른쪽(=현재 라인이 왼쪽) -> LEFT 보정
                    elif error_value > 0:
                        status_text, display_color = f"LEFT: +{abs(round(error_value, 1))}", (0, 255, 0)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_LEFT', 'value': error_value})

                    # error_value < 0: 현재 라인이 오른쪽 -> RIGHT 보정
                    else:
                        status_text, display_color = f"RIGHT: -{abs(round(error_value, 1))}", (0, 165, 255)
                        self.command_queue.put({'source': 'CAMERA', 'cmd': 'AUTO_RIGHT', 'value': error_value})

                    # 중심점 표시(빨간 원)
                    cv2.circle(img, (cx_global, int(y1 + roi_h / 2)), 10, (0, 0, 255), -1)

                # (D) 그 외 예외 상황 -> STOP
                else:
                    self.command_queue.put({'source': 'CAMERA', 'cmd': 'STOP'})

                # ------------------------------
                # 6) 시각화 업데이트(디버그용)
                # ------------------------------

                # ROI 사각형 표시(파랑)
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

                # 원근 사다리꼴(ROI 안의 src_pts)을 전체 화면 좌표로 변환해서 표시
                trap_pts = np.array([
                    [src_pts[0][0] + x1, src_pts[0][1] + y1],
                    [src_pts[1][0] + x1, src_pts[1][1] + y1],
                    [src_pts[2][0] + x1, src_pts[2][1] + y1],
                    [src_pts[3][0] + x1, src_pts[3][1] + y1]
                ], dtype=np.int32)
                cv2.polylines(img, [trap_pts], True, (0, 0, 255), 2)      # 빨간 사다리꼴

                # 데드존(타겟 범위) 표시: target_center ± deadzone
                left_boundary = self.target_center - self.deadzone
                right_boundary = self.target_center + self.deadzone
                cv2.line(img, (left_boundary, y1), (left_boundary, y2), (0, 255, 255), 2)  # 왼쪽 경계
                cv2.line(img, (right_boundary, y1), (right_boundary, y2), (0, 255, 255), 2) # 오른쪽 경계
                cv2.circle(img, (self.target_center, int(y1 + roi_h / 2)), 3, (0, 212, 255), -1)  # 목표점 표시

                # 상태 텍스트 출력
                cv2.putText(img, status_text, (10, 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, display_color, 3)

                # 디버그 창 3개 출력
                cv2.imshow("Check 1: ROI", roi_raw)             # ROI 원본(컬러)
                cv2.imshow("Check 2: Warped ROI", roi_color)    # 원근보정된 ROI(컬러)
                cv2.imshow("Check 3: Binary View", thresh)      # 이진화 결과(흑/백)

            # AUTO가 아니어도 메인 화면은 계속 보여줌(현재 프레임)
            cv2.imshow("Main View", img)

            key = cv2.waitKey(1) & 0xFF                          # 키 입력 처리
            if key == ord('q'):
                self.is_running = False                          # q: 종료
            elif key == ord('m'):
                # m: AUTO <-> MANUAL 토글
                self.control_mode = "MANUAL" if self.control_mode == "AUTO" else "AUTO"

        # 종료 처리: 카메라/창 정리
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    robot = RobotSystem()                                        # 객체 생성 -> OpenCV 스레드 자동 시작
    try:
        while robot.is_running:
            # 카메라 스레드가 큐에 넣은 명령을 여기서 꺼내서(테스트용)
            if not robot.command_queue.empty():
                data = robot.command_queue.get()                 # {'source':'CAMERA','cmd':..., 'value':...}
                # 여기서 data를 실제 로봇 제어 로직에 전달하거나 print로 확인할 수 있음
            time.sleep(0.01)                                     # CPU 점유 낮추기(10ms)
    except KeyboardInterrupt:
        robot.is_running = False                                 # Ctrl+C로 종료