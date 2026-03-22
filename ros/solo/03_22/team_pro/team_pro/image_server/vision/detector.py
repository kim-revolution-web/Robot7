import cv2
import numpy as np

class VisionDetector:
    def __init__(self):
        pass

    #image_node.py
    def detect(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #원래 BGR 이미지를
        #HSV 형식으로 바꾼다

        lower_blue = np.array([100, 100, 100])
        upper_blue = np.array([130, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)#색 검출 hsv

        #윤곽선(외곽선) 찾는 함수
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.RETR_EXTERNAL
        #바깥쪽 윤곽선만 찾겠다는 뜻
        #cv2.CHAIN_APPROX_SIMPLE
        #윤곽선 점을 너무 많이 저장하지 말고
        #필요한 점만 간단히 저장하라는 뜻
        #contours → 윤곽선 목록
        #_ → 안 쓰는 값

        if not contours:
            return {
                "success": False,
                "label": "NONE",
                "center": (0, 0)
            }
        #면적이 가장 큰 contour 하나를 뽑는다
        largest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest)

        center_x = x + w // 2
        center_y = y + h // 2

        return {
            "success": True,
            "label": "BLUE",
            "center": (center_x, center_y),
            "rect": (x, y, w, h)
        }
