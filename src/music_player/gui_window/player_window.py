import sys, os, pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from src.music_player.player.player import Player
from src.music_player.gui_window.headers import Headers
from src.music_player.gui_window.settings import Settings
from src.music_player.gui_window.song_window import SongWindow

class PlaybackController(QThread):

    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, player):
        super().__init__()

        self.player = player

        self.timer = QTimer()
        self.timer.setInterval(200)

        self.timer.timeout.connect(self.tick)
    
    def start(self):

        if not self.player.song_dirs:
            return
        self.player.play_current()
        self.timer.start()

    def tick(self):
        """The loop."""
        try:
            if self.player.ps.end:
                self.timer.stop()
                self.finished.emit()
                return

            # skip
            if self.player.ps.skip_song:
                self.player.ps.skip_song = False
                self.player.next_song()
                return

            # back
            if self.player.ps.back_a_song:
                self.player.ps.back_a_song = False
                self.player.previous_song()
                return

            # jump
            if self.player.ps.jump_to_index is not None:
                idx = self.player.ps.jump_to_index
                self.player.ps.jump_to_index = None
                self.player.play_index(idx)
                return

            # song ended naturally
            if not pygame.mixer.music.get_busy() and not self.player.ps.pause_song:
                if self.player.ps.loop:
                    self.player.play_current()
                else:
                    self.player.next_song()
        except Exception as e:
            self.timer.stop()
            self.error.emit(str(e))



class PlayerWindow(QWidget):

    back_to_picker = pyqtSignal()

    def __init__(self, playlist_file, song_folder):
        super().__init__()

        self._create_widgets(playlist_file, song_folder)
        self._create_layouts()
        self._connect_signals()


    def _create_widgets(self, playlist_file, song_folder):
        self.player = Player(playlist_file, song_folder)
        self.player.get_songs()

        self.header_section = Headers()
        self.song_section = SongWindow(self.player)
        self.settings_section = Settings()

        # Thread
        self.controller = PlaybackController(self.player)

    def _create_layouts(self):
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.header_section)
        main_layout.addWidget(self.song_section)
        main_layout.addWidget(self.settings_section)
        self.setWindowTitle("Music Player")

    def _connect_signals(self):
        self.settings_section.playClicked.connect(self.start_or_resume)
        self.settings_section.pauseClicked.connect(self.pause)
        self.settings_section.skipClicked.connect(self.skip)
        self.settings_section.backClicked.connect(self.back)
        self.settings_section.loopClicked.connect(self.loop)
        self.settings_section.restartClicked.connect(self.restart)
        self.settings_section.volume.sliderReleased.connect(self.commit_volume)
        self.settings_section.shuffleClicked.connect(self.shuffle)
        self.settings_section.back_to_picker.connect(self.return_to_picker)
        self.song_section.songClicked.connect(self.player.jump_to_song)

        self.controller.error.connect(self.thread_error)

        self.player.songChanged.connect(
            lambda idx: self.header_section.set_title(os.path.basename(self.player.song_dirs[idx]))
        )

    # Button handlers
    # ----------------------
    def start_or_resume(self):
        if not self.controller.timer.isActive():
            self.controller.start()
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
        self.header_section.set_loop(False)

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

    def return_to_picker(self):
        self.back_to_picker.emit()

    def stop_and_reset(self):

        self.controller.timer.stop()

        self.player.stop()

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        self.player.reset()