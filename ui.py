import sys

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, \
    QTableWidget, QTextEdit, QTableWidgetItem, QStyle
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt




class VideoPlayer(QMainWindow):
    speeds =[0.1,0.5,5,10,30,60]
    @property
    def mark_in(self):
        if self.table.currentRow() ==0:
            pass
        else:
            return self.media_player.position()
    @mark_in.setter
    def mark_in(self,position):
        if self.table.currentRow() >-1:
            self.table.currentRow()[0]= 3
        else:
            row=self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Cut "+str(row+1)))
            self.table.setItem(row, 1, QTableWidgetItem(str(position)))
            self.mark_in_pos = None
    @property
    def mark_out(self,position):
        if self.table.currentRow() == 0:
            pass
        else:
            return self.media_player.position()
    @mark_out.setter
    def mark_out(self,position):

        if self.table.currentRow() >-1:
            row = self.table.currentRow()
            self.table.setItem(row, 2, QTableWidgetItem(str(position)))

        else:
            row = self.table.rowCount() -1
            self.table.setItem(row, 2, QTableWidgetItem(str(position)))

    def __init__(self):
        self.newStep=3
        buttonHeight=32
        super().__init__()
        self.lastTimeToDisplay = None
        self.videoSource = ""

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 1024, 768)
        self.setAcceptDrops(True)

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()
        self.audioOutput = QAudioOutput()
        self.media_player.setAudioOutput(self.audioOutput)
       

        self.frb_button = QPushButton("")
        self.frb_button.setFixedSize(40,buttonHeight)
        self.frb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipBackward))
        self.frb_button.clicked.connect(lambda : self.rewind(self.newStep/1000))

        self.rb_button = QPushButton("")
        self.rb_button.setFixedSize(40,buttonHeight)
        self.rb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward))
        self.rb_button.clicked.connect(lambda: self.rewind(10))

        self.sr_button = QPushButton("<-")
        self.sr_button.setFixedSize(40,buttonHeight)
        self.sr_button.clicked.connect(lambda : self.rewind(1))
        self.ssr_button = QPushButton("<--")
        self.ssr_button.setFixedSize(40,buttonHeight)
        self.ssr_button.clicked.connect(lambda : self.rewind(0.1))


        self.start_button = QPushButton("")
        self.start_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.start_button.setFixedSize(40,buttonHeight)
        self.start_button.clicked.connect(self.start_video)
        self.playShortcut = QShortcut(QKeySequence("Space"), self)
        self.playShortcut.activated.connect(self.start_video)



        self.stop_button = QPushButton()
        self.stop_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaStop))
        self.stop_button.setFixedSize(48,buttonHeight)
        self.stop_button.clicked.connect(self.stop_video)

        self.trslider = QSlider(Qt.Orientation.Horizontal)
        self.trslider.setFixedSize(100, 24)
        self.trslider.setRange(0,len(self.speeds)-1)
        self.trslider.setSingleStep(1)
        # self.trslider.setTracking(True)
        self.trslider.setToolTip("Skip Speed")
        self.trslider.setValue(self.newStep)
        self.trslider.setTickInterval(1)
        self.trslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.trslider.sliderMoved.connect(self.trStepChanged)

        self.trsTracker = QTextEdit(str(self.newStep))
        self.trsTracker.setFixedSize(96,24)
        self.trsTracker.setReadOnly(True)



        self.sf_button = QPushButton("-")
        self.sf_button.setFixedSize(40,buttonHeight)
        self.sf_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.sf_button.clicked.connect(lambda: self.fast_forward(1))
        self.ssf_button = QPushButton(">--")
        self.ssf_button.setFixedSize(40,buttonHeight)
        self.ssf_button.clicked.connect(lambda: self.fast_forward(0.1))


        self.fb_button = QPushButton("")
        self.fb_button.setFixedSize(40,buttonHeight)
        self.fb_button.clicked.connect(lambda: self.fast_forward(10))
        self.fb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward))

        self.ffb_button = QPushButton("")
        self.ffb_button.setFixedSize(40,buttonHeight)
        self.ffb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.ffb_button.clicked.connect(lambda: self.fast_forward(30))


        #tag in/ out buttons
        self.tagin_button = QPushButton("[")
        self.tagin_button.setFixedSize(32,buttonHeight)
        self.tagin_button.clicked.connect(self.tag_in)

        self.tagout_button = QPushButton("]")
        self.tagout_button.setFixedSize(32,buttonHeight)
        self.tagout_button.clicked.connect(self.tag_out)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setFixedSize(800,24)

        self.slider.sliderMoved.connect(self.set_position)

        self.playheadTracker = QTextEdit("00:00:00:0")
        self.playheadTracker.setFixedSize(96,24)
        self.playheadTracker.setReadOnly(True)



        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile(self.videoSource))
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Name","Mark In", "Mark Out"])

        layout =QVBoxLayout()
        Buttonlayout = QHBoxLayout()
        LowerButtonlayout = QHBoxLayout()


        Buttonlayout.addWidget(self.frb_button)
        Buttonlayout.addWidget(self.rb_button)

        LowerButtonlayout.addWidget(self.ssr_button,alignment=Qt.AlignmentFlag.AlignHCenter)  # slow slow rewind
        LowerButtonlayout.addWidget(self.sr_button,alignment=Qt.AlignmentFlag.AlignHCenter)   # slow rewind
        LowerButtonlayout.addWidget(self.trslider,alignment=Qt.AlignmentFlag.AlignHCenter)
        LowerButtonlayout.addWidget(self.trsTracker)
        Buttonlayout.addWidget(self.start_button)
        Buttonlayout.addWidget(self.stop_button)
        LowerButtonlayout.addWidget(self.ssf_button,alignment=Qt.AlignmentFlag.AlignHCenter)
        LowerButtonlayout.addWidget(self.sf_button,alignment=Qt.AlignmentFlag.AlignHCenter)
        Buttonlayout.addWidget(self.fb_button)
        Buttonlayout.addWidget(self.ffb_button)




        layout.addLayout(Buttonlayout)
        layout.addLayout(LowerButtonlayout)
        video_player_layout = QVBoxLayout()
        self.video_widget.setFixedSize(800,600)

        layout.addWidget(self.video_widget, alignment=Qt.AlignmentFlag.AlignHCenter,stretch=3)

        playheadLayer = QHBoxLayout()
        playheadLayer.addWidget(self.slider,alignment=Qt.AlignmentFlag.AlignLeft)
        playheadLayer.addWidget(self.playheadTracker,alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(playheadLayer)



        TagButtonLayout = QHBoxLayout()
        TagButtonLayout.addWidget(self.tagin_button,alignment=Qt.AlignmentFlag.AlignLeft, stretch=3)
        TagButtonLayout.addWidget(self.tagout_button,alignment=Qt.AlignmentFlag.AlignRight, stretch=3)


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
            self.start_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.media_player.play()
            self.start_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()

    def tag_in(self):
        self.mark_in = self.media_player.position()

    def tag_out(self):
        self.mark_out = self.media_player.position()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)
        self.timeToDisplay = self.convert_millisecondsToString(position)
        if self.timeToDisplay != self.lastTimeToDisplay:
            self.playheadTracker.setText(self.timeToDisplay)
            self.lastTimeToDisplay = self.timeToDisplay

    def trStepChanged(self):
        step = 100  # 1-second step
        position = self.trslider.sliderPosition()
        self.newStep =self.speeds[position]
        new_position = round(position / step) * step
      #  self.trslider.setValue(new_position)

      #  self.newStep = self.trslider.value()
        self.trsTracker.setText(str(self.newStep))

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def rewind(self,ss=10):
        ms = ss*1000
        newpos = int(max(0, self.media_player.position() - ms))
        self.media_player.setPosition(newpos)  # Rewind by 5 seconds

    def fast_forward(self,ff=10):
        ms = ff*1000
        newpos= int(min(self.media_player.duration(), self.media_player.position() + ms))
        self.media_player.setPosition(newpos)

    def load_video(self, file_path):
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        #self.media_player.play()
        self.setWindowTitle(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
            self.load_video(file_path)
    def convert_millisecondsToString(self,ms):
        centiseconds =(ms // 100) %10
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        hours = (ms // (1000 * 60 * 60))
        return f"{hours:02}:{minutes:02}:{seconds:02}:{centiseconds:01}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())
