# link.py
# 역할: ROS2를 직접 쓰지 않고도 rosbridge_websocket으로 /cmd_vel 발행
# - 웹소켓 연결
# - op: advertise로 토픽 선언
# - op: publish로 geometry_msgs/Twist 형식 JSON을 전송

import json
import websocket

class RosbridgePublisher:
    def __init__(self, ws_url: str):
        self.ws_url = ws_url

        # rosbridge 웹소켓 연결
        self.ws = websocket.WebSocket()
        self.ws.connect(self.ws_url)
        print(f"[link] rosbridge 연결됨: {self.ws_url}")

        # /cmd_vel 토픽을 쓰겠다고 ROS에 "광고(advertise)" 선언
        self.ws.send(json.dumps({
            "op": "advertise",
            "topic": "/cmd_vel",
            "type": "geometry_msgs/Twist"
        }))

    def publish_cmd_vel(self, linear_x: float, angular_z: float):
        # geometry_msgs/Twist의 형식을 JSON으로 맞춰 publish
        msg = {
            "op": "publish",
            "topic": "/cmd_vel",
            "msg": {
                "linear":  {"x": linear_x, "y": 0.0, "z": 0.0},
                "angular": {"x": 0.0, "y": 0.0, "z": angular_z}
            }
        }
        self.ws.send(json.dumps(msg))

    def close(self):
        self.ws.close()
