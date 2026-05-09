import sys, os, pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from src.music_player.player.player import Player
from src.music_player.gui_window.headers import Headers
from src.music_player.gui_window.settings import Settings
from src.music_player.gui_window.song_window import SongWindow

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
        self.settings_section.shuffleClicked.connect(self.shuffle)

        self.song_section.songClicked.connect(self.player.jump_to_song)
        

        # Thread
        self.thread = PlayerThread(self.player)
        self.thread.error.connect(self.thread_error)

        # Player → headers
        self.player.songChanged.connect(
            lambda idx: self.header_section.set_title(os.path.basename(self.player.song_dirs[idx]))
        )
        # self.settings_.shuffleChanged.connect(lambda _: self.song_section.set_songs(self.player.song_dirs))

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
        self.header_section.set_paused(False)

    def back(self):
        self.player.back()
        self.header_section.set_paused(False)

    def restart(self):
        self.player.restart()
        self.header_section.set_paused(False)

    def loop(self):
        self.player.tog_loop()
        self.header_section.set_loop(self.player.ps.loop)

    def shuffle(self):
        self.player.change_shuffle()
        self.header_section.set_shuffle(self.player.ps.shuffle)

    def commit_volume(self):
        value = self.settings_section.volume.value() / 100
        self.player.set_volume(value) 
        pygame.mixer.music.set_volume(value)

    def thread_error(self, msg):
        print("Thread error:", msg)