import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, \
    QTableWidget
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.videoSource = "/Users/frank/Movies/TV/sapphire and steel/Assignment_1/Part1.1.MP4"

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1024, 768)

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.media_player.setAudioOutput(self.audioOutput)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_video)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)

        #tag in/ out buttons
        self.tagin_button = QPushButton("[")
        self.tagout_button = QPushButton("]")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(self.videoSource))
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Mark In", "Mark Out"])

        layout =QVBoxLayout()
        Buttonlayout = QHBoxLayout()
        Buttonlayout.addWidget(self.start_button)
        Buttonlayout.addWidget(self.pause_button)
        Buttonlayout.addWidget(self.stop_button)

        layout.addLayout(Buttonlayout)
        layout.addWidget(self.video_widget)
        layout.addWidget(self.slider)


        TagButtonLayout = QHBoxLayout()
        TagButtonLayout.addWidget(self.tagin_button)
        TagButtonLayout.addWidget(self.tagout_button)


        layout.addLayout(TagButtonLayout)

        tableLayout =QVBoxLayout()
        tableLayout.addWidget(self.table)
        #layout.addLayout(tableLayout)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()
    def tag_in(self):
        pass
    def tag_out(self):
        pass

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())
