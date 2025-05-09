import os.path
import sys

from PyQt6.QtGui import QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QHBoxLayout, \
    QTableWidget, QTextEdit, QTableWidgetItem, QStyle, QFileDialog, QLineEdit
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, Qt


class VideoPlayer(QMainWindow):
    speeds = [0.1,0.5,1,2,10,30,60]

    @property
    def mark_in(self):
        if self.table.currentRow() == 0:
            pass
        else:
            return self.media_player.position()

    @mark_in.setter
    def mark_in(self,position):
        if self.table.currentRow() > 0:
            row = self.table.currentRow()
            self.table.setItem(row, 0, QTableWidgetItem("Cut " + str(row + 1)))
            self.table.setItem(row, 1, QTableWidgetItem(str(position)))
            self.mark_in_pos = None
        else:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem("Cut "+str(row+1)))
            self.table.setItem(row, 1, QTableWidgetItem(str(position)))
            self.mark_in_pos = None
        self.table.setCurrentCell(0,0)

    @property
    def mark_out(self):
        if self.table.currentRow() == 0:
            pass
        else:
            return self.media_player.position()

    @mark_out.setter
    def mark_out(self,position):

        if self.table.currentRow() > 0:
            row = self.table.currentRow()
            self.table.setItem(row, 2, QTableWidgetItem(str(position)))

        else:
            row = self.table.rowCount() - 1
            self.table.setItem(row, 2, QTableWidgetItem(str(position)))
        self.table.setCurrentCell(0,0)

    def __init__(self):
        self.newStep = 3
        buttonHeight = 32
        self.filename = ""
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
        self.frb_button.clicked.connect(lambda: self.rewind(self.newStep*2))

        self.rb_button = QPushButton("")
        self.rb_button.setFixedSize(40,buttonHeight)
        self.rb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekBackward))
        self.rb_button.clicked.connect(lambda: self.rewind(self.newStep))

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
        midbit = int(len(self.speeds)/2)
        self.trslider.setValue(midbit)
        self.trslider.setTickInterval(1)
        self.trslider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.trslider.sliderMoved.connect(self.trStepChanged)

        self.trsSliderKeyForward = QShortcut(QKeySequence("."), self)
        self.trsSliderKeyBackward = QShortcut(QKeySequence(","), self)
        self.trsSliderKeyForward.activated.connect(self.trsForward)
        self.trsSliderKeyBackward.activated.connect(self.trsBackward)
        self.trsTracker = QTextEdit(str(self.speeds[int(len(self.speeds)/2)]))
        self.trsTracker.setFixedSize(96,24)
        self.trsTracker.setReadOnly(True)

        self.fb_button = QPushButton("")
        self.fb_button.setFixedSize(40,buttonHeight)
        self.fb_button.clicked.connect(lambda: self.fast_forward(self.newStep))
        self.fb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSeekForward))

        self.left_arrow_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.left_arrow_shortcut.activated.connect(self.on_left_arrow)

        self.right_arrow_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.right_arrow_shortcut.activated.connect(self.on_right_arrow)

        self.ffb_button = QPushButton("")
        self.ffb_button.setFixedSize(40,buttonHeight)
        self.ffb_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaSkipForward))
        self.ffb_button.clicked.connect(lambda: self.fast_forward(self.newStep*2))



        # tag in/ out buttons
        self.tagin_button = QPushButton("[")
        self.tagin_button.setFixedSize(32,buttonHeight)
        self.tagin_button.clicked.connect(self.tag_in)

        self.inKeyShortcut = QShortcut(QKeySequence("i"), self)
        self.inKeyShortcut.activated.connect(self.tag_in)

        self.tagout_button = QPushButton("]")
        self.tagout_button.setFixedSize(32,buttonHeight)
        self.tagout_button.clicked.connect(self.tag_out)

        self.outKeyShortcut = QShortcut(QKeySequence("o"), self)
        self.outKeyShortcut.activated.connect(self.tag_out)

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

        layout = QVBoxLayout()
        Buttonlayout = QHBoxLayout()
        LowerButtonlayout = QHBoxLayout()

        Buttonlayout.addWidget(self.frb_button)
        Buttonlayout.addWidget(self.rb_button)

        LowerButtonlayout.addWidget(self.trslider,alignment=Qt.AlignmentFlag.AlignHCenter)
        LowerButtonlayout.addWidget(self.trsTracker)
        Buttonlayout.addWidget(self.start_button)
        Buttonlayout.addWidget(self.stop_button)

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

        self.openButton = QPushButton("Open")
        self.saveButton = QPushButton("Save")
        self.saveAsButton = QPushButton("Save As")
        self.resetButton = QPushButton("Clear")

        self.openButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogOpenButton))
        self.saveButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.saveAsButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton))
        self.saveAsButton.clicked.connect(self.saveAs)
        self.resetButton.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton))

        tableLayout = QHBoxLayout()
        FileButtons = QVBoxLayout()
        tableLayout.addWidget(self.table)
        tableLayout.addLayout(FileButtons)

        FileButtons.addWidget(self.openButton)
        FileButtons.addWidget(self.saveButton)
        FileButtons.addWidget(self.saveAsButton)
        FileButtons.addWidget(self.resetButton)

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
        self.newStep = self.speeds[position]
        self.new_position = round(position / step) * step
        self.trsTracker.setText(str(self.newStep))

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)

    def rewind(self,ss=10):
        ms = ss*1000
        newpos = int(max(0, self.media_player.position() - ms))
        self.media_player.pause()
        self.media_player.setPosition(newpos)  # Rewind by 5 seconds

    def fast_forward(self,ff=10):
        ms = ff*1000
        newpos = int(min(self.media_player.duration(), self.media_player.position() + ms))
        self.media_player.pause()
        self.media_player.setPosition(newpos)

    def load_video(self, file_path):
        self.media_player.setSource(QUrl.fromLocalFile(file_path))
        self.videoSource = file_path
        self.setWindowTitle(file_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        if file_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
            self.load_video(file_path)
            self.filename = file_path.split(os.path.sep)[-1]

    def convert_millisecondsToString(self,ms):
        centiseconds = (ms // 100) % 10
        seconds = (ms // 1000) % 60
        minutes = (ms // (1000 * 60)) % 60
        hours = (ms // (1000 * 60 * 60))
        return f"{hours:02}:{minutes:02}:{seconds:02}:{centiseconds:01}"
    def trsForward(self):
        self.trslider.setValue(self.trslider.sliderPosition()+1)
        self.trStepChanged()
        pass
    def trsBackward(self):
        self.trslider.setValue(self.trslider.sliderPosition() - 1)
        self.trStepChanged()
        pass

    def on_right_arrow(self):
        focus_widget = QApplication.focusWidget()

        if isinstance(focus_widget, (QTextEdit, QLineEdit)):
            print("Shortcut ignored: focus is on an interactive widget.")
            return
        if isinstance(focus_widget, QTableWidget):
            # Check if it has an active cell editor
            if focus_widget.state() == QTableWidget.State.EditingState:
                print("Shortcut ignored: table is actively editing.")
                return

        # Your custom action goes here
        print("Right Arrow shortcut activated!")

    def on_left_arrow(self):
        focus_widget = QApplication.focusWidget()

        if isinstance(focus_widget, (QTextEdit, QLineEdit)):
            print("Shortcut ignored: focus is on an interactive widget.")
            return
        if isinstance(focus_widget, QTableWidget):
            # Check if it has an active cell editor
            if focus_widget.state() == QTableWidget.State.EditingState:
                print("Shortcut ignored: table is actively editing.")
                return

        # Your custom action goes here
        print("Right Arrow shortcut activated!")

    def saveAs(self):
        filename = self.filename.rsplit('.',1)[0]+".avutils"
        file_path, _ = QFileDialog.getSaveFileName(self,"Save As",filename,"avutils File (*.avutils);;All Files (*)")
        if len(file_path.strip()) >0:
            with (open(file_path, 'w', encoding='utf-8') as myfile):
                myfile.write("file=\""+self.videoSource+"\"\n")
                myfile.write("timeformat=ms\n")
                for irow in range(self.table.rowCount()):
                    itemName = self.table.item(irow,00)
                    if not itemName or not itemName.text():
                        continue
                    itemNametext = itemName.text()
                    myfile.write(itemNametext + "=")

                    startTime= self.table.item(irow,1)
                    if not startTime or not startTime.text():
                        startTimeText ='0'

                    else:
                        startTimeText=startTime.text()
                    myfile.write(startTimeText)
                    endtime = self.table.item(irow,2)
                    if not endtime or not endtime.text():
                        endtimeText = None
                    else:
                        endtimeText=endtime.text()
                        myfile.write(" - "+endtimeText)
                    myfile.write("\n")

            myfile.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())
