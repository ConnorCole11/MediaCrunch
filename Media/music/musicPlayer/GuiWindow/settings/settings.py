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

    def __init__(self):
        super().__init__()

        # Buttons
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_skip = QPushButton("⏭ Skip")
        self.btn_back = QPushButton("⏮ Back")
        self.btn_restart = QPushButton("⭮ Restart")
        self.btn_loop = QPushButton("Loop")

        # Connect buttons
        self.btn_play.clicked.connect(self.playClicked.emit)
        self.btn_pause.clicked.connect(self.pauseClicked.emit)
        self.btn_skip.clicked.connect(self.skipClicked.emit)
        self.btn_back.clicked.connect(self.backClicked.emit)
        self.btn_loop.clicked.connect(self.loopClicked.emit)
        self.btn_restart.clicked.connect(self.restartClicked.emit)

        # Button layout (horizontal)
        button_layout = QHBoxLayout()
        for btn in (self.btn_back, self.btn_loop, self.btn_restart,
                    self.btn_pause, self.btn_play, self.btn_skip):
            button_layout.addWidget(btn)

        # Volume slider
        self.volume = QSlider()
        self.volume.setOrientation(Qt.Horizontal)
        self.volume.setMinimum(0)
        self.volume.setMaximum(100)
        self.volume.setValue(50)
        self.volume.setTickInterval(10)
        self.volume.setTickPosition(QSlider.TicksBelow)
        pygame.mixer.music.set_volume(0.5)

        volume_layout = QHBoxLayout()
        volume_layout.addWidget(QLabel("Volume:"))
        volume_layout.addWidget(self.volume)

        # Main layout (vertical)
        main_layout = QVBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(volume_layout)