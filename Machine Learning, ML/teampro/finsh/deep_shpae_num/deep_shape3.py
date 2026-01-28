import time
import cv2
import numpy as np
import tensorflow as tf
import os

# 1. 모델 불러오기
model_path = 'shape_model_6.keras'
if not os.path.exists(model_path):
    print(" 모델 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
    exit()

model = tf.keras.models.load_model(model_path)
class_names = ['circle', 'rectangle', 'triangle', 'x']

if not os.path.exists('./test'):
    os.makedirs('./test')

cap = cv2.VideoCapture(0)
IMG_SIZE = 128

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)

    # ROI 설정
    h, w, _ = frame.shape
    y1, y2 = 0, 240
    x1, x2 = 180, 480
    y1, y2 = max(0, y1), min(h, y2)
    x1, x2 = max(0, x1), min(w, x2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    roi = frame[y1:y2, x1:x2]

    # 전처리 과정
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    resized = cv2.resize(thresh, (IMG_SIZE, IMG_SIZE))

    # ----- 픽셀 비율 계산 및 조건부 예측 -----

    # 1. 전체 픽셀 수와 흰색(255) 픽셀 수 계산
    total_pixels = resized.size
    white_pixels = np.sum(resized == 255)
    white_ratio = (white_pixels / total_pixels) * 100  # 백분율로 변환

    result_text = "Waiting..."

    # 2. 조건 확인: 5% 이상 17% 미만일 때만 실행
    if 5.0 <= white_ratio < 17.0:
        # 모델 예측 실행
        input_data = resized.reshape(1, IMG_SIZE, IMG_SIZE, 1).astype('float32')
        prediction = model.predict(input_data, verbose=0)
        result_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100
        result_text = f"{class_names[result_idx]} ({confidence:.1f}%)"
        funt_color = (0, 0, 255)
        # 저장 (예측될 때만 저장)
        # save_path = f"./test/captured_{np.random.randint(1000)}.png"
        # cv2.imwrite(save_path, resized)
        print(f" [예측 성공] 비율: {white_ratio:.1f}% | 결과: {result_text}")

        if confidence > 95.0:
            final_result = class_names[result_idx]
            if final_result == "circle":

                time.sleep(2)
            # 값을 보냄
    else:
        # 조건에 맞지 않을 때
        result_text = f"white_ratio({white_ratio:.1f}%)"
        funt_color = (255, 255, 255)
        print(f"⏸ [대기 중] 흰색 비율이 적절하지 않음: {white_ratio:.1f}%")

    # --- 화면 표시 ---
    display_roi = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    # 현재 상태를 화면에 표시 (비율 포함)
    cv2.putText(display_roi, result_text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
    cv2.putText(frame, result_text, (w-150, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, funt_color, 1)
    cv2.imshow('Shape Scanner', frame)
    cv2.imshow('Model Input (Preprocessed)', display_roi)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
