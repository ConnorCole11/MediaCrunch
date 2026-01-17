# Buttons.py
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class PlayerControls(QWidget):
    # Signals for MainWindow to connect
    playClicked = pyqtSignal()
    pauseClicked = pyqtSignal()
    skipClicked = pyqtSignal()
    backClicked = pyqtSignal()
    loopClicked = pyqtSignal()
    restartClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Create buttons
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_skip = QPushButton("⏭ Skip")
        self.btn_back = QPushButton("⏮ Back")
        self.btn_restart = QPushButton("⭮ Restart")
        self.btn_loop = QPushButton("Loop")

        # Layout
        layout = QHBoxLayout(self)
        for btn in (self.btn_back, self.btn_loop, self.btn_restart,
                    self.btn_pause, self.btn_play, self.btn_skip):
            layout.addWidget(btn)

        # Connect button clicks to signals
        self.btn_play.clicked.connect(self.playClicked.emit)
        self.btn_pause.clicked.connect(self.pauseClicked.emit)
        self.btn_skip.clicked.connect(self.skipClicked.emit)
        self.btn_back.clicked.connect(self.backClicked.emit)
        self.btn_loop.clicked.connect(self.loopClicked.emit)
        self.btn_restart.clicked.connect(self.restartClicked.emit)
