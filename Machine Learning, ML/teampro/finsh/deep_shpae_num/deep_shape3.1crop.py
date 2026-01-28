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

    # ROI 설정 (상단 영역)
    h, w, _ = frame.shape
    y1, y2 = 0, 240
    x1, x2 = 180, 480
    y1, y2 = max(0, y1), min(h, y2)
    x1, x2 = max(0, x1), min(w, x2)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    roi = frame[y1:y2, x1:x2]

    # --- [전처리 단계] ---
    # 그레이스케일 및 블러
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 이진화 (배경 검정, 도형 흰색)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 테두리 5픽셀 자르기
    margin = 5
    if thresh.shape[0] > margin*2 and thresh.shape[1] > margin*2:
        thresh = thresh[margin:-margin, margin:-margin]

    # 4. 모델 입력 크기로 리사이즈
    resized = cv2.resize(thresh, (IMG_SIZE, IMG_SIZE))

    # --- [예측 제어 로직] ---
    # 흰색 픽셀 비율 계산
    total_pixels = resized.size
    white_pixels = np.sum(resized == 255)
    white_ratio = (white_pixels / total_pixels) * 100

    result_text = "Waiting..."
    funt_color = (255, 255, 255) # 기본 흰색

    # 조건 확인: 5% 이상 17% 미만일 때만 예측
    if 5.0 <= white_ratio < 17.0:
        input_data = resized.reshape(1, IMG_SIZE, IMG_SIZE, 1).astype('float32')
        prediction = model.predict(input_data, verbose=0)
        result_idx = np.argmax(prediction)
        confidence = np.max(prediction) * 100

        result_text = f"{class_names[result_idx]} ({confidence:.1f}%)"
        funt_color = (0, 0, 255) # 조건 충족 시 빨간색 표시

        print(f" [분석 중] 비율: {white_ratio:.1f}% | 결과: {result_text}")

        # 확률이 95% 이상일 때 특정 액션 (예: circle인 경우 2초 대기)
        if confidence > 95.0:
            final_result = class_names[result_idx]
            print(f"✅ [확정] 결과: {final_result}")
            if final_result == "circle":
                # 여기에 전송 로직 추가 가능
                time.sleep(2)
    else:
        result_text = f"Ratio({white_ratio:.1f}%)"
        funt_color = (255, 255, 255)
        # print(f"⏸ [대기] 비율: {white_ratio:.1f}%")

    # --- 화면 표시 ---
    # 1. 모델이 실제로 보는 전처리 이미지 (디버깅용)
    display_roi = cv2.cvtColor(resized, cv2.COLOR_GRAY2BGR)
    cv2.putText(display_roi, f"Ratio: {white_ratio:.1f}%", (5, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # 2. 메인 화면에 결과 표시
    # 위치를 가이드박스 근처나 화면 우측 상단에 배치
    cv2.putText(frame, result_text, (w - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, funt_color, 2)


    cv2.imshow('Shape Scanner', frame)
    cv2.imshow('binary_roi', display_roi)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
