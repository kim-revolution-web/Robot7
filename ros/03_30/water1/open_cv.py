import cv2

def main():
    cap = cv2.VideoCapture(0)  # 기본 카메라

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("카메라 연결 성공")
    print("종료하려면 q 키를 누르세요.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽지 못했습니다.")
            break

        cv2.imshow("Camera Test", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()