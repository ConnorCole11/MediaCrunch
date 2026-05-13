from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QSlider, QLabel
import pygame

class Settings(QWidget):
    # Signals for PlayerWindow
    playClicked = pyqtSignal()
    pauseClicked = pyqtSignal()
    skipClicked = pyqtSignal()
    backClicked = pyqtSignal()
    loopClicked = pyqtSignal()
    restartClicked = pyqtSignal()
    shuffleClicked = pyqtSignal()
    back_to_picker = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_skip = QPushButton("⏭ Skip")
        self.btn_back = QPushButton("⏮ Back")
        self.btn_restart = QPushButton("⭮ Restart")
        self.btn_loop = QPushButton("Loop")
        self.btn_shuffle = QPushButton("Shuffle")
        self.volume = QSlider()
        self.btn_return_to_picker = QPushButton("Return to Playlist Selection")
    
    def _create_layouts(self):
        self.button_line = QHBoxLayout()
        self.button_line.addWidget(self.btn_back)
        self.button_line.addWidget(self.btn_loop)
        self.button_line.addWidget(self.btn_restart)
        self.button_line.addWidget(self.btn_pause)
        self.button_line.addWidget(self.btn_play)
        self.button_line.addWidget(self.btn_skip)
        self.button_line.addWidget(self.btn_shuffle)
        self._set_volume_layout()
        
        self.button_layout = QVBoxLayout()
        self.button_layout.addLayout(self.button_line)
        self.button_layout.addLayout(self.volume_layout)
        self.button_layout.addWidget(self.btn_return_to_picker)

        self.setLayout(self.button_layout)

    def _connect_signals(self):
        self.btn_play.clicked.connect(self.playClicked.emit)
        self.btn_pause.clicked.connect(self.pauseClicked.emit)
        self.btn_skip.clicked.connect(self.skipClicked.emit)
        self.btn_back.clicked.connect(self.backClicked.emit)
        self.btn_loop.clicked.connect(self.loopClicked.emit)
        self.btn_restart.clicked.connect(self.restartClicked.emit)
        self.btn_shuffle.clicked.connect(self.shuffleClicked.emit)
        self.btn_return_to_picker.clicked.connect(self.back_to_picker)


    def _set_volume_layout(self):
        pygame.mixer.music.set_volume(0.5)
        self.volume.setOrientation(Qt.Horizontal)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(50)
        self.volume.setTickInterval(10)
        self.volume.setTickPosition(QSlider.TicksBelow)

        self.volume_layout = QHBoxLayout()
        self.volume_layout.addWidget(QLabel("Volume:"))
        self.volume_layout.addWidget(self.volume)