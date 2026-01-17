# Controls.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt
import pygame

class StatusWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.status_song = QLabel("Song: None")
        self.status_paused = QLabel("Paused: ❌")
        self.status_loop = QLabel("Looped: ❌")

        layout = QVBoxLayout(self)
        layout.addWidget(self.status_song)
        layout.addWidget(self.status_paused)
        layout.addWidget(self.status_loop)

    def set_song(self, name):
        self.status_song.setText(f"Song: {name}")

    def set_paused(self, paused: bool):
        self.status_paused.setText(f"Paused: {'✅' if paused else '❌'}")

    def set_loop(self, looped: bool):
        self.status_loop.setText(f"Looped: {'✅' if looped else '❌'}")


class VolumeWidget(QWidget):
    def __init__(self, initial=50):
        super().__init__()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(initial)
        self.slider.setTickInterval(10)
        self.slider.setTickPosition(QSlider.TicksBelow)

        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Volume:"))
        layout.addWidget(self.slider)

        # Initial volume
        pygame.mixer.music.set_volume(initial / 100)
