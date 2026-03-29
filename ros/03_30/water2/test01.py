import cv2
import numpy as np
from tensorflow import keras
from pathlib import Path

import tensorflow as tf

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "water_classifier.keras"
IMG_SIZE = (150, 150)

model = keras.models.load_model(MODEL_PATH)

def predict_frame(frame):
    img = cv2.resize(frame, IMG_SIZE)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    prob = model.predict(img, verbose=0)[0][0]
    return prob

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("카메라 분류 시작, q 누르면 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break

        prob = predict_frame(frame)

        if prob >= 0.5:
            label = f"water ({prob:.2f})"
            color = (0, 255, 0)
        else:
            label = f"no_water ({1 - prob:.2f})"
            color = (0, 0, 255)

        cv2.putText(
            frame,
            label,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            color,
            2,
            cv2.LINE_AA
        )

        cv2.imshow("Water Classifier", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()