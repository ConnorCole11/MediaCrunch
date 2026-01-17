import sys
import os
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QListWidget, QLabel, QHBoxLayout, QSlider
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QColor, QBrush
from music.musicPlayer.Player.Player import Player  # your class

# ---------------------------
# Worker thread for playback
# ---------------------------
class PlayerThread(QThread):
    song_changed = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, player: Player):
        super().__init__()
        self.player = player

    def run(self):
        try:
            while not self.player.end and self.player.song_dirs:
                self.song_changed.emit(self.player.current_idx)
                self.player.play_songs()
        except Exception as e:
            self.error.emit(str(e))
        self.finished.emit()


# ---------------------------
# Main Window
# ---------------------------
class PlayerWindow(QWidget):
    def __init__(self, playlist_file, song_folder):
        super().__init__()

        self.initPlayer(playlist_file, song_folder)
        self.initStatus()
        self.initButtons()
        self.initVolume()
        self.initUI()
        self.applyStyles()

        self.setWindowTitle("Music Player")

    

        for s in self.player.song_dirs:
            self.playlist.addItem(os.path.basename(s))

        # Background thread
        self.thread = PlayerThread(self.player)
        self.thread.error.connect(self.thread_error)
        self.thread.song_changed.connect(self.highlight_current_song)
        self.thread.song_changed.connect(self.updateSongStatus)

        self.highlight_color = "#00CCFF"  # Default highlight color

    def initPlayer(self, playlist_file, song_folder):
        self.player = Player(
            playlist_file, 
            song_folder, 
            on_song_change=lambda idx: (
                self.highlight_current_song(idx),
                self.updateSongStatus(idx)
            )
        )
        self.player.get_songs()
        pygame.mixer.init()

    def initUI(self):
        self.playlist = QListWidget()
        self.playlist.itemDoubleClicked.connect(self.jump_to_song)

        self.initStatus()
        self.mainBuild()

    def initStatus(self):
        status_layout = QVBoxLayout()

        self.status_song = QLabel("Song: None")
        self.status_paused = QLabel("Paused: ❌")
        self.status_loop = QLabel("Looping: ❌")
        status_layout.addWidget(self.status_song)
        status_layout.addWidget(self.status_paused)
        status_layout.addWidget(self.status_loop)

    def initButtons(self):
        # Buttons
        self.btn_play = QPushButton("▶ Play")
        self.btn_pause = QPushButton("⏸ Pause")
        self.btn_skip = QPushButton("⏭ Skip")
        self.btn_back = QPushButton("⏮ Back")
        self.btn_restart = QPushButton("⭮ Restart") 
        self.btn_loop = QPushButton("Loop")

        # Functions of buttons
        self.btn_play.clicked.connect(self.start_or_resume)
        self.btn_pause.clicked.connect(self.pause)
        self.btn_skip.clicked.connect(self.skip)
        self.btn_back.clicked.connect(self.back)
        self.btn_restart.clicked.connect(self.restart)
        self.btn_loop.clicked.connect(self.loop)


    def initVolume(self):
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(50)  # default volume
        self.volume_slider.setTickInterval(10)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)

        # Initial volume of slider
        pygame.mixer.music.set_volume(self.volume_slider.value() / 100)

    def applyStyles(self):
        self.playlist.setStyleSheet("""
            QListWidget::item:selected {
                background: rgba(0, 120, 215, 100);  /* semi-transparent blue */
                color: black;
            }
            """)


    # ===========================
    # Build UI
    # ===========================
    def mainBuild(self):
        btn_row = self.buildButtonRow()
        vol_row = self.buildVolumeRow()

        layout = QVBoxLayout()
        layout.addWidget(self.status_song)
        layout.addWidget(self.status_paused)
        layout.addWidget(self.status_loop)
        layout.addWidget(self.playlist)
        layout.addLayout(btn_row)
        layout.addLayout(vol_row)

        self.setLayout(layout)

    def buildButtonRow(self):
        row = QHBoxLayout()
        row.addWidget(self.btn_back)
        row.addWidget(self.btn_loop)
        row.addWidget(self.btn_restart)
        row.addWidget(self.btn_pause)
        row.addWidget(self.btn_play)
        row.addWidget(self.btn_skip)
        return row

    def buildVolumeRow(self):
        volume_layout = QHBoxLayout()
        volume_label = QLabel("Volume:")
        volume_layout.addWidget(volume_label)
        volume_layout.addWidget(self.volume_slider)

        self.volume_slider.sliderReleased.connect(self.commit_volume)
        return volume_layout


    # --------------------------
    # Button Handlers
    # --------------------------

    def updateLoopEmoji(self):
        if self.player.loop == True:
            emoji = "✅"
        else:
            emoji = "❌"
        self.status_loop.setText(f"Looped: {emoji}")
        return emoji
    


    def updateSongStatus(self, index=None):
        if index is None:
            index = self.player.current_idx
        if 0 <= index < len(self.player.song_dirs):
            song_path = self.player.song_dirs[index]
            song_name = os.path.basename(song_path)
            self.status_song.setText(f"Song: {song_name}")
        else:
            self.status_song.setText("Song: None")

    # ===========================
    # Button Handlers (cleaned)
    # ===========================
    def start_or_resume(self):
        if not self.thread.isRunning():
            self.thread.start()
        else:
            self.player.unpause()
            pygame.mixer.music.unpause()
        self.status_paused.setText("Paused: ❌")
        self.updateLoopEmoji()

    def pause(self):
        self.player.pause()
        pygame.mixer.music.pause()
        self.status_paused.setText("Paused: ✅")

    def skip(self):
        self.player.skip()
        self.player.pause_song = False
        self.player.loop = False
        self.status_paused.setText("Paused: ❌")
        self.updateLoopEmoji()

    def back(self):
        self.player.back()
        self.player.pause_song = False
        self.player.loop = False
        self.status_paused.setText("Paused: ❌")
        self.updateLoopEmoji()

    def restart(self):
        self.player.skip_song = True
        self.player.skip_n_songs = 0
        self.player.pause_song = False
        pygame.mixer.music.unpause()
        self.status_paused.setText("Paused: ❌")
        self.updateLoopEmoji()

    def loop(self):
        self.player.tog_loop()
        self.updateLoopEmoji()

    def jump_to_song(self, item):
        name = item.text().lower()
        for idx, full in enumerate(self.player.song_dirs):
            if full.lower().endswith(name):
                diff = idx - self.player.current_idx
                self.player.skip_n_songs = diff
                self.player.pause_song = False
                self.player.loop = False
                self.player.skip_song = True
                pygame.mixer.music.unpause()
                break


    def preview_volume(self, value):
        # This runs WHILE dragging — optional
        pygame.mixer.music.set_volume(value / 100)

    def commit_volume(self):
        # This runs AFTER clicking or finishing a drag — stable
        value = self.volume_slider.value()
        pygame.mixer.music.set_volume(value / 100)
        self.player.volume = value / 100

    # --------------------------
    # Highlight currently playing
    # --------------------------
    def highlight_current_song(self, index):
        for i in range(self.playlist.count()):
            self.playlist.item(i).setBackground(QBrush(QColor("white")))

        if 0 <= index < self.playlist.count():
            item = self.playlist.item(index)
            item.setBackground(QBrush(QColor(self.highlight_color)))
            self.playlist.setCurrentRow(index)
            self.playlist.scrollToItem(item)
            # self.now_playing.setText(f"Playing: {os.path.basename(self.player.song_dirs[index])}")

    def thread_error(self, msg):
        # self.now_playing.setText("Error!")
        print("Thread error:", msg)

