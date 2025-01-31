import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, \
    QTableWidget, QTextEdit
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lastTimeToDisplay = None
        self.videoSource = "/Users/frank/Movies/TV/sapphire and steel/Assignment_1/Part1.1.MP4"

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1024, 768)

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.media_player.setAudioOutput(self.audioOutput)

        self.frb_button = QPushButton("<<<")
        self.frb_button.clicked.connect(lambda : self.rewind(30))
        self.rb_button = QPushButton("<<")
        self.rb_button.clicked.connect(lambda: self.rewind(10))

        self.start_button = QPushButton("> ||")
        self.start_button.clicked.connect(self.start_video)



        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_video)

        self.fb_button = QPushButton(">>")
        self.fb_button.clicked.connect(lambda: self.fast_forward(10))
        self.ffb_button = QPushButton(">>>")
        self.ffb_button.clicked.connect(lambda: self.fast_forward(30))


        #tag in/ out buttons
        self.tagin_button = QPushButton("[")
        self.tagout_button = QPushButton("]")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        self.playheadTracker = QTextEdit("00:00:00")
        self.playheadTracker.setFixedSize(88,24)
        self.playheadTracker.setReadOnly(True)



        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(self.videoSource))
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name","Mark In", "Mark Out"])

        layout =QVBoxLayout()
        Buttonlayout = QHBoxLayout()
        Buttonlayout.addWidget(self.frb_button)
        Buttonlayout.addWidget(self.rb_button)

        Buttonlayout.addWidget(self.start_button)
        Buttonlayout.addWidget(self.stop_button)
        Buttonlayout.addWidget(self.fb_button)
        Buttonlayout.addWidget(self.ffb_button)


        layout.addLayout(Buttonlayout)
        video_player_layout = QVBoxLayout()
        self.video_widget.setFixedSize(800,600)

        layout.addWidget(self.video_widget, alignment=Qt.AlignmentFlag.AlignHCenter,stretch=3)

        playheadLayer = QHBoxLayout()
        playheadLayer.addWidget(self.slider)
        playheadLayer.addWidget(self.playheadTracker)
        layout.addLayout(playheadLayer)



        TagButtonLayout = QHBoxLayout()
        TagButtonLayout.addWidget(self.tagin_button)
        TagButtonLayout.addWidget(self.tagout_button)


        layout.addLayout(TagButtonLayout)

        tableLayout =QVBoxLayout()
        tableLayout.addWidget(self.table)
        layout.addLayout(tableLayout)


        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_video(self):
        if self.media_player.isPlaying():
            self.media_player.pause()
        else:
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
        self.timeToDisplay = self.convert_millisecondsToString(position)
        if self.timeToDisplay != self.lastTimeToDisplay:
            self.playheadTracker.setText(self.timeToDisplay)
            self.lastTimeToDisplay = self.timeToDisplay

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def rewind(self,ss=10):
        ms = ss*1000
        (self.media_player.setPosition(max(0, self.media_player.position() - ms)))  # Rewind by 5 seconds

    def fast_forward(self,ff=10):
        ms = ff*1000
        self.media_player.setPosition(min(self.media_player.duration(), self.media_player.position() + ms))

    def convert_millisecondsToString(self,ms):
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        hours = (ms // (1000 * 60 * 60))
        return f"{hours}:{minutes}:{seconds}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())
