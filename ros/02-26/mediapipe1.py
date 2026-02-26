import cv2
import mediapipe as mp

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
# -*- coding: utf-8 -*-


def classify_hand(hand_landmarks):
    results = "I dont know"
    landmarks = hand_landmarks.landmark
    def is_finger_straight(finger_tip_idx, finger_dip_idx):
        return landmarks[finger_tip_idx].y < landmarks[finger_dip_idx].y

    # 손가락 펼침 여부
    index_straight = is_finger_straight(8, 6)
    middle_straight = is_finger_straight(12, 10)
    ring_straight = is_finger_straight(16, 14)
    pinky_straight = is_finger_straight(20, 18)

    if index_straight and not middle_straight and not ring_straight and not pinky_straight:
        results = "one"
    elif index_straight and middle_straight and not ring_straight and not pinky_straight:
        results = "sissor"
    elif index_straight and middle_straight and ring_straight and not pinky_straight:
        results = "three"
    elif not index_straight and not middle_straight and not ring_straight and not pinky_straight:
        results = "Rock"
    elif index_straight and middle_straight and ring_straight and pinky_straight:
        results = "paper"

    return results


def move_what(gesture: str):
    # 제스처 -> w/a/s/d/x 매핑
    if gesture == "one":
        return 'w'
    elif gesture == "sissor":
        return 'a'
    elif gesture == "three":
        return 'd'
    elif gesture == "paper":
        return 'x'
    elif gesture == "Rock":
        return 's'
    else:
        return 's'


class MediapipePub(Node):
    def __init__(self):
        super().__init__('mediapipe_pub')
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(String, 'mediapipe_topic', qos)


def main():
    # ROS2 init + publisher node
    rclpy.init()
    node = MediapipePub()

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened() and rclpy.ok():
            success, image = cap.read()
            if not success:
                print("카메라를 찾을 수 없습니다.")
                continue

            # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
            image.flags.writeable = False
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            # 이미지에 손 주석을 그립니다.
            image.flags.writeable = True

            gesture = "hands detect"
            key_char = 's'  # 기본값(정지)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )
                    gesture = classify_hand(hand_landmarks)
                    # 원본처럼 "마지막 손" 기준으로 gesture가 결정됨(원본 유지)

                key_char = move_what(gesture)

            # ===== ROS2 publish (추가된 핵심) =====
            msg = String()
            msg.data = key_char          # 'w'/'a'/'s'/'d'/'x' 한 글자
            node.pub.publish(msg)
            # spin_once는 타이머 없더라도 안전하게 이벤트 처리용
            rclpy.spin_once(node, timeout_sec=0.0)
            # ===================================

            cv2.putText(image, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow('MediaPipe Hands', image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
