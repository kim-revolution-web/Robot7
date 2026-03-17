import os
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget

class FaceVideoPlayer:
    def __init__(self, parent, container_widget):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        layout = container_widget.layout() #이게 뭐야
        if layout is None:
            layout = QVBoxLayout(container_widget) #영상을 화면에 보여주는 칸
            layout.setContentsMargins(0, 0, 0, 0)#빈 테두리 공간 없이 꽉 차게 넣겠다

        self.video_widget = QVideoWidget(container_widget)
        layout.addWidget(self.video_widget)

        self.audio_output = QAudioOutput() #소리 출력 장치 객체
        self.media_player = QMediaPlayer(parent) #상위 개념은 QMediaPlayer
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.mediaStatusChanged.connect(self.on_media_status_changed)#상태 변화 감지 후 함수 연결

        self.audio_output.setVolume(0.0)
        self.video_widget.hide()

        self.video_map = {
            "angry": os.path.join(self.base_dir, "faces", "angry.mp4"),
            "neutral": os.path.join(self.base_dir, "faces", "normal.mp4"),
            "heart": os.path.join(self.base_dir, "faces", "heart.mp4"),
            "blink": os.path.join(self.base_dir, "faces", "blink.mp4"),
        }

    def on_media_status_changed(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.clear_video()

    def clear_video(self):
        self.media_player.stop()#현재 재생 중이면 멈춰.
        self.video_widget.hide()

    def play_video(self, path: str):
        if not os.path.exists(path):
            print(f"파일 없음: {path}")
            return

        self.video_widget.show()
        self.media_player.setSource(QUrl.fromLocalFile(path)) #로컬 파일 경로를 QUrl로 바꿔서 플레이어에 넣는 것
        self.media_player.play()

    def play_face(self, face_name: str):#다른 파일에서 실행할 동여상 함수
        path = self.video_map.get(face_name)
        if not path:
            print(f"영상 없음: {face_name}")
            return

        self.play_video(path)
