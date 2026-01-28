import time
import cv2
import numpy as np
import tensorflow as tf
import os
import threading
from queue import Queue # 명령 전달을 위한 바구니


# 1. 모델 불러오기
model_path = 'shape_model_6.keras'
if not os.path.exists(model_path):
    print(" 모델 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    exit()

model = tf.keras.models.load_model(model_path)
class_names = ['circle', 'rectangle', 'triangle', 'x']

# 로봇 제어 명령을 담을 큐 (바구니)
command_queue = Queue()

def send_command(shape):
    """도형별 속도 제어 명령을 생성하여 바구니에 넣는 함수"""
    # 기본 속도 설정
    base_speed = 0.1
    cmd = {'action': 'RUN', 'speed': base_speed}

    if shape == 'triangle':   # 세모: 감속
        print(">> [ACTION] 감속 (0.5x)")
        cmd = {'action': 'SLOW', 'speed': base_speed * 0.5}
    elif shape == 'rectangle': # 네모: 가속
        print(">> [ACTION] 가속 (2.0x)")
        cmd = {'action': 'FAST', 'speed': base_speed * 2.0}
    elif shape == 'circle':    # 원: U턴
        print(">> [ACTION] U턴 시작")
        cmd = {'action': 'UTURN', 'speed': base_speed}
    elif shape == 'x':         # X: 정지
        print(">> [ACTION] 긴급 정지")
        cmd = {'action': 'STOP', 'speed': 0}

    # 바구니에 명령 넣기
    command_queue.put(cmd)

    # 동작이 수행되는 동안 잠시 대기 (스레드 내부에서만 멈춤)
    hold_time = 3.0 if shape == 'circle' else 1.5
    time.sleep(hold_time)
    print(">> [SYSTEM] 이벤트 종료, 일반 주행 복귀")

cap = cv2.VideoCapture(0)
IMG_SIZE = 128

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)

    # ROI 설정 (상단 영역)
    h, w, _ = frame.shape
    y1, y2 = 0, 240
    x1, x2 = 180, 480
    y1, y2 = max(0, y1), min(h, y2)
    x1, x2 = max(0, x1), min(w, x2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    roi = frame[y1:y2, x1:x2]

    # --- [전처리 단계] ---
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

		# 5픽셀 자르기
    margin = 5
    if thresh.shape[0] > margin*2 and thresh.shape[1] > margin*2:
        thresh = thresh[margin:-margin, margin:-margin]

    resized = cv2.resize(thresh, (IMG_SIZE, IMG_SIZE))

    # --- [예측 및 제어 로직] ---
    total_pixels = resized.size
    white_pixels = np.sum(resized == 255)
    white_ratio = (white_pixels / total_pixels) * 100

    result_text = "Waiting..."
    funt_color = (255, 255, 255)

    if 5.0 <= white_ratio < 17.0:
		    # [중요] 픽셀값 정규화 -> 모델이 입력받을때 정규화를 해서 안해도 됨
        input_data = resized.reshape(1, IMG_SIZE, IMG_SIZE, 1).astype('float32')
 
        prediction = model.predict(input_data, verbose=0)
        result_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100

        result_text = f"{class_names[result_idx]} ({confidence:.1f}%)"
        funt_color = (0, 0, 255)

        # 확정 판정 (95% 이상)
        if confidence > 95.0:
            final_result = class_names[result_idx]
            # 비동기 방식으로 명령 전송 (화면 멈춤 방지)
            threading.Thread(target=send_command, args=(final_result,), daemon=True).start()
    else:
        result_text = f"Ratio({white_ratio:.1f}%)"
        funt_color = (255, 255, 255)

    # --- 화면 표시 ---
    display_roi = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    cv2.putText(display_roi, f"Ratio: {white_ratio:.1f}%", (5, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    cv2.putText(frame, result_text, (w - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, funt_color, 2)

    # [디버깅] 현재 바구니에 담긴 명령 확인
    if not command_queue.empty():
        current_cmd = command_queue.get()
        print(f" [명령 수신함] {current_cmd}")

    cv2.imshow('Shape Scanner', frame)
    cv2.imshow('binary_roi', display_roi)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
