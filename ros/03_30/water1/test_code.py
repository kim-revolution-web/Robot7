import cv2
from pathlib import Path
from ultralytics import YOLO

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "runs" / "water_train" / "weights" / "best.pt"

def main():
    if not MODEL_PATH.exists():
        print(f"모델 파일이 없습니다: {MODEL_PATH}")
        return

    model = YOLO(str(MODEL_PATH))
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("디버그 탐지 시작, q 누르면 종료")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임 읽기 실패")
            break

        results = model.predict(
            source=frame,
            conf=0.05,
            verbose=False
        )

        result = results[0]
        boxes = result.boxes

        print("-" * 40)
        print("탐지 개수:", len(boxes))

        if len(boxes) > 0:
            for i, box in enumerate(boxes):
                cls_id = int(box.cls[0].item())
                conf = float(box.conf[0].item())
                name = model.names.get(cls_id, str(cls_id))
                print(f"{i+1}. class={name}, conf={conf:.3f}")

        annotated_frame = result.plot()
        cv2.imshow("YOLO Camera Debug", annotated_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()