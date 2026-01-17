# MainWindow.py
import sys, os, pygame
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import pyqtSignal
from music.musicPlayer.Player.Player import Player  # your class
from music.musicPlayer.GuiWindow.buttons import PlayerControls
from music.musicPlayer.GuiWindow.controls import StatusWidget, VolumeWidget
from music.musicPlayer.GuiWindow.layouts import build_main_layout


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


class PlayerWindow(QWidget):
    def __init__(self, playlist_file, song_folder):
        super().__init__()

        # Player
        self.player = Player(playlist_file, song_folder,
                             on_song_change=lambda idx: (
                                 self.highlight_current_song(idx),
                                 self.status.set_song(os.path.basename(self.player.song_dirs[idx]))
                             ))
        self.player.get_songs()
        pygame.mixer.init()

        # Widgets
        self.status = StatusWidget()
        self.volume = VolumeWidget()
        self.controls = PlayerControls()
        self.playlist = QListWidget()

        for s in self.player.song_dirs:
            self.playlist.addItem(os.path.basename(s))

        # Layout
        self.setLayout(build_main_layout(self.status, self.playlist, self.controls, self.volume))
        self.apply_styles()
        self.setWindowTitle("Music Player")

        # Connect button signals
        self.controls.playClicked.connect(self.start_or_resume)
        self.controls.pauseClicked.connect(self.pause)
        self.controls.skipClicked.connect(self.skip)
        self.controls.backClicked.connect(self.back)
        self.controls.loopClicked.connect(self.loop)
        self.controls.restartClicked.connect(self.restart)

        # Thread
        self.thread = PlayerThread(self.player)
        self.thread.song_changed.connect(self.highlight_current_song)
        self.thread.song_changed.connect(lambda idx: self.status.set_song(os.path.basename(self.player.song_dirs[idx])))
        self.thread.error.connect(self.thread_error)

        self.highlight_color = "#00CCFF"

        # Volume slider
        self.volume.slider.sliderReleased.connect(self.commit_volume)

        # Playlist double click
        self.playlist.itemDoubleClicked.connect(self.jump_to_song)

    # ----------------------
    # UI helpers
    # ----------------------
    def apply_styles(self):
        self.playlist.setStyleSheet("""
            QListWidget::item:selected {
                background: rgba(0, 120, 215, 100);
                color: black;
            }
        """)

    def highlight_current_song(self, index):
        for i in range(self.playlist.count()):
            self.playlist.item(i).setBackground(QBrush(QColor("white")))
        if 0 <= index < self.playlist.count():
            item = self.playlist.item(index)
            item.setBackground(QBrush(QColor(self.highlight_color)))
            self.playlist.setCurrentRow(index)
            self.playlist.scrollToItem(item)

    # ----------------------
    # Button handlers
    # ----------------------
    def start_or_resume(self):
        if not self.thread.isRunning():
            self.thread.start()
        else:
            self.player.unpause()
            pygame.mixer.music.unpause()
        self.status.set_paused(False)

    def pause(self):
        self.player.pause()
        pygame.mixer.music.pause()
        self.status.set_paused(True)

    def skip(self):
        self.player.skip()
        self.player.pause_song = False
        self.player.loop = False
        self.status.set_paused(False)

    def back(self):
        self.player.back()
        self.player.pause_song = False
        self.player.loop = False
        self.status.set_paused(False)

    def restart(self):
        self.player.skip_song = True
        self.player.skip_n_songs = 0
        self.player.pause_song = False
        pygame.mixer.music.unpause()
        self.status.set_paused(False)

    def loop(self):
        self.player.tog_loop()
        self.status.set_loop(self.player.loop)

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

    def commit_volume(self):
        value = self.volume.slider.value()
        pygame.mixer.music.set_volume(value / 100)
        self.player.volume = value / 100

    def thread_error(self, msg):
        print("Thread error:", msg)

