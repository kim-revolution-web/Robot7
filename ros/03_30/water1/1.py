import cv2
from ultralytics import YOLO

model = YOLO('yolov8n.pt')

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap.isOpened():
    raise IOError("Cannot open webcam")

while cap.isOpened():
    success, frame = cap.read()

    if not success:
        print("Failed to read frame")
        break

    results = model(frame, conf=0.5)

    person_detected = False

    # Check if a person is detected
    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0].item())
            if class_id == 0:
                person_detected = True
                break
        if person_detected:
            break

    if person_detected:
        print("Person detected!")
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Inference (Person Detected)", annotated_frame)
    else:
        cv2.imshow("YOLOv8 Inference (No Person)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
