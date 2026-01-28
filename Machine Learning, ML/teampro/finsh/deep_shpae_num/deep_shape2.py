import cv2
import numpy as np
import threading
import time
from queue import Queue
import tensorflow as tf
import os

# [모듈 1] 도형 인식 클래스
class ShapeDetector:
    def __init__(self, queue):
        self.queue = queue
        self.base_speed = 0.1
        self.labels = ['CIRCLE', 'SQUARE', 'TRIANGLE', 'X']
        self.input_size = 64

        if os.path.exists('shape_model.h5'):
            self.model = tf.keras.models.load_model('shape_model.h5')
            print("[AI] 모델 로드 완료")
        else:
            self.model = None
            print("[System] 모델 없음 - 테스트 모드로 동작")

    def handle_events(self, shape):
        """도형별 가속, 감속, U턴, 정지 명령 생성"""
        command_data = {
            'source': 'SHAPE',
            'type': shape,
            'speed': self.base_speed,
            'action': 'RUN'
        }

        if shape == "TRIANGLE":
            print(">> 세모 감지: 감속 모드 (0.5x)")
            command_data['speed'] = self.base_speed * 0.5
            command_data['action'] = 'SLOW'
        elif shape == "SQUARE":
            print(">> 네모 감지: 가속 모드 (2.0x)")
            command_data['speed'] = self.base_speed * 2.0
            command_data['action'] = 'FAST'
        elif shape == "CIRCLE":
            print(">> 원 감지: U턴 수행")
            command_data['speed'] = self.base_speed
            command_data['action'] = 'UTURN'
        elif shape == "X":
            print(">> X 감지: 긴급 정지")
            command_data['speed'] = 0
            command_data['action'] = 'STOP'

        self.queue.put(command_data)
        hold_time = 2.5 if shape == "CIRCLE" else 1.5
        time.sleep(hold_time)

    def run(self, frame, thresh):
        h, w = thresh.shape
        # 상단 ROI 설정
        sx1, sx2, sy1, sy2 = int(w*0.25), int(w*0.75), int(0), int(h*0.5)
        roi_shape = thresh[sy1:sy2, sx1:sx2]
        cv2.rectangle(frame, (sx1, sy1), (sx2, sy2), (0, 255, 255), 2)
        cv2.imshow("roi_shape",roi_shape)
        contours, _ = cv2.findContours(roi_shape, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_shape = None
        for cnt in contours:
            if cv2.contourArea(cnt) > 3000:
                x, y, bw, bh = cv2.boundingRect(cnt)

                if self.model is not None:
                    crop = cv2.resize(roi_shape[y:y+bh, x:x+bw], (self.input_size, self.input_size))
                    test_img = crop.reshape(1, self.input_size, self.input_size, 1) / 255.0
                    preds = self.model.predict(test_img, verbose=0)
                    if np.max(preds) > 0.9:
                        detected_shape = self.labels[np.argmax(preds)]

                if detected_shape:
                    cv2.rectangle(frame, (x+sx1, y+sy1), (x+sx1+bw, y+sy1+bh), (0, 0, 255), 3)
                    # 스레드 실행
                    threading.Thread(target=self.handle_events, args=(detected_shape,), daemon=True).start()
                    return detected_shape  # 수정: 도형 이름을 반환하도록 변경
        return None
