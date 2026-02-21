import sys, os, pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from music.musicPlayer.Player.Player import Player
from music.musicPlayer.GuiWindow.headers.headers import Headers
from music.musicPlayer.GuiWindow.settings.settings import Settings
from music.musicPlayer.GuiWindow.song_window.song_window import SongWindow

class PlayerThread(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, player):
        super().__init__()
        self.player = player

    def run(self):
        try:
            self.player.play_songs()
        except Exception as e:
            self.error.emit(str(e))
        self.finished.emit()

class PlayerWindow(QWidget):
    def __init__(self, playlist_file, song_folder):
        super().__init__()

        # Player
        self.player = Player(playlist_file, song_folder)
        self.player.get_songs()
        pygame.mixer.init()

        # Widgets
        self.header_section = Headers()
        self.song_section = SongWindow(self.player)
        self.settings_section = Settings()

        # Layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header_section)
        main_layout.addWidget(self.song_section)
        main_layout.addWidget(self.settings_section)
        self.setWindowTitle("Music Player")

        # Connect signals
        self.settings_section.playClicked.connect(self.start_or_resume)
        self.settings_section.pauseClicked.connect(self.pause)
        self.settings_section.skipClicked.connect(self.skip)
        self.settings_section.backClicked.connect(self.back)
        self.settings_section.loopClicked.connect(self.loop)
        self.settings_section.restartClicked.connect(self.restart)
        self.settings_section.volume.sliderReleased.connect(self.commit_volume)

        self.song_section.songSelected.connect(self.jump_to_song)

        # Thread
        self.thread = PlayerThread(self.player)
        self.thread.error.connect(self.thread_error)

        # Player → headers
        self.player.songChanged.connect(
            lambda idx: self.header_section.set_title(os.path.basename(self.player.song_dirs[idx]))
        )
        self.player.pausedChanged.connect(self.header_section.set_paused)

    # ----------------------
    # Button handlers
    # ----------------------
    def start_or_resume(self):
        if not self.thread.isRunning():
            self.thread.start()
        else:
            self.player.unpause()
            pygame.mixer.music.unpause()
        self.header_section.set_paused(False)

    def pause(self):
        self.player.pause()
        pygame.mixer.music.pause()
        self.header_section.set_paused(True)

    def skip(self):
        self.player.skip()
        self.player.pause_song = False
        self.player.loop = False
        self.header_section.set_paused(False)

    def back(self):
        self.player.back()
        self.player.pause_song = False
        self.player.loop = False
        self.header_section.set_paused(False)

    def restart(self):
        self.player.skip_song = True
        self.player.skip_n_songs = 0
        self.player.pause_song = False
        pygame.mixer.music.unpause()
        self.header_section.set_paused(False)

    def loop(self):
        self.player.tog_loop()
        self.header_section.set_loop(self.player.loop)

    def jump_to_song(self, index: int):
        diff = index - self.player.current_idx
        self.player.skip_n_songs = diff
        self.player.pause_song = False
        self.player.loop = False
        self.player.skip_song = True
        pygame.mixer.music.unpause()

    def commit_volume(self):
        value = self.settings_section.volume.value()
        pygame.mixer.music.set_volume(value / 100)
        self.player.volume = value / 100

    def thread_error(self, msg):
        print("Thread error:", msg)