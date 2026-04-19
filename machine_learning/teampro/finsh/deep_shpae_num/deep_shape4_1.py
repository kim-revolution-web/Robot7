import time
import cv2
import numpy as np
import tensorflow as tf
import os
import threading
from queue import Queue

# 1. 모델 불러오기
model_path = 'shape_model_6.keras'
if not os.path.exists(model_path):
    print(" 모델 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    exit()

model = tf.keras.models.load_model(model_path)
class_names = ['circle', 'rectangle', 'triangle', 'x']

# [추가] 오토 모드 상태 변수 (True면 AI 가동, False면 중지)
auto_mode = True

command_queue = Queue()

def send_command(shape):
    base_speed = 0.1
    cmd = {'action': 'RUN', 'speed': base_speed}

    if shape == 'triangle':
        cmd = {'action': 'SLOW', 'speed': base_speed * 0.5}
    elif shape == 'rectangle':
        cmd = {'action': 'FAST', 'speed': base_speed * 2.0}
    elif shape == 'circle':
        cmd = {'action': 'UTURN', 'speed': base_speed}
    elif shape == 'x':
        cmd = {'action': 'STOP', 'speed': 0}

    command_queue.put(cmd)
    hold_time = 3.0 if shape == 'circle' else 1.5
    time.sleep(hold_time)

cap = cv2.VideoCapture(0)
IMG_SIZE = 128

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape
    y1, y2 = 0, 240
    x1, x2 = 180, 480
    y1, y2 = max(0, y1), min(h, y2)
    x1, x2 = max(0, x1), min(w, x2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    roi = frame[y1:y2, x1:x2]

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    margin = 5
    if thresh.shape[0] > margin*2 and thresh.shape[1] > margin*2:
        thresh = thresh[margin:-margin, margin:-margin]

    resized = cv2.resize(thresh, (IMG_SIZE, IMG_SIZE))

    total_pixels = resized.size
    white_pixels = np.sum(resized == 255)
    white_ratio = (white_pixels / total_pixels) * 100

    # [수정] 오토 모드 여부에 따른 텍스트 초기화
    result_text = "Waiting..." if auto_mode else "Manual Mode"
    funt_color = (255, 255, 255)

    # [수정] auto_mode가 True일 때만 AI 예측 로직 실행
    if auto_mode and (5.0 <= white_ratio < 17.0):
        input_data = resized.reshape(1, IMG_SIZE, IMG_SIZE, 1).astype('float32')

        prediction = model.predict(input_data, verbose=0)
        result_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100

        result_text = f"{class_names[result_idx]} ({confidence:.1f}%)"
        funt_color = (0, 0, 255)

        if confidence > 95.0:
            final_result = class_names[result_idx]
            threading.Thread(target=send_command, args=(final_result,), daemon=True).start()

    # [추가] 오토 모드가 꺼져있을 때 표시할 내용
    elif not auto_mode:
        result_text = "AI OFF"
        funt_color = (150, 150, 150) # 비활성화 느낌의 회색
    else:
        result_text = f"Ratio({white_ratio:.1f}%)"

    display_roi = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    cv2.putText(display_roi, f"Ratio: {white_ratio:.1f}%", (5, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    cv2.putText(frame, result_text, (w - 200, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, funt_color, 2)

    if not command_queue.empty():
        current_cmd = command_queue.get()
        print(f"📦 [명령 수신함] {current_cmd}")

    cv2.imshow('Shape Scanner', frame)
    cv2.imshow('binary_roi', display_roi)

    # [수정] 키 입력 처리 부분 (실시간 모드 전환)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'): # 'a' 누르면 자율주행 모드 ON
        auto_mode = True
        print(">> 자율주행 모드(AUTO) 활성화")
    elif key == ord('m'): # 'm' 누르면 수동 모드 ON (AI 인식 중지)
        auto_mode = False
        print(">> 수동 모드(MANUAL) 활성화")

cap.release()
cv2.destroyAllWindows()
