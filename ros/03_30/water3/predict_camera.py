import cv2
import numpy as np
import tensorflow as tf

# =========================
# 설정
# =========================
MODEL_PATH = "water_transfer.keras"
# MODEL_PATH = "water_cnn.keras"
IMG_SIZE = 224
CAM_INDEX = 0   # 기본 웹캠

# ROI 좌표 (직접 화면 보면서 조절)
# frame[y1:y2, x1:x2]
ROI_X1 = 150
ROI_Y1 = 100
ROI_X2 = 500
ROI_Y2 = 400

# =========================
# 모델 로드
# =========================
model = tf.keras.models.load_model(MODEL_PATH)

# =========================
# 예측 함수
# =========================
def preprocess_frame(frame):
    # BGR(OpenCV) -> RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 크기 조정
    resized = cv2.resize(rgb, (IMG_SIZE, IMG_SIZE))

    # 정규화
    normalized = resized.astype("float32") / 255.0

    # 배치 차원 추가
    input_data = np.expand_dims(normalized, axis=0)
    return input_data

def predict_water(frame):
    input_data = preprocess_frame(frame)
    pred = model.predict(input_data, verbose=0)[0][0]

    # sigmoid 출력: 0~1
    if pred >= 0.5:
        label = "WATER"
        confidence = pred
    else:
        label = "NO WATER"
        confidence = 1.0 - pred

    return label, float(confidence), float(pred)

# =========================
# 카메라 실행
# =========================
cap = cv2.VideoCapture(CAM_INDEX)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    exit()

print("q 키를 누르면 종료됩니다.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다.")
        break

    # ROI 자르기
    roi = frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    # ROI가 비어 있지 않은지 확인
    if roi.size == 0:
        print("ROI 범위가 잘못되었습니다.")
        break

    # ROI만 가지고 예측
    label, confidence, raw_pred = predict_water(roi)

    # 화면 출력용 문구
    text = f"{label} ({confidence*100:.1f}%)"

    # 색상
    if label == "WATER":
        color = (255, 0, 0)   # 파랑(BGR)
    else:
        color = (0, 0, 255)   # 빨강(BGR)

    # 원본 화면에 ROI 사각형 표시
    cv2.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 255, 255), 2)

    # 원본 화면에 예측 글자 출력
    cv2.putText(
        frame,
        text,
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        color,
        2
    )

    # 예측값 표시
    cv2.putText(
        frame,
        f"raw sigmoid: {raw_pred:.3f}",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # ROI 창도 따로 보기
    cv2.imshow("ROI", roi)
    cv2.imshow("Water Detection Camera", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()