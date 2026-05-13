from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal

from src.music_player.gui_window.player_window import PlayerWindow
from src.music_player.gui_window.playlist_picker import PlaylistPicker
try:
    from config_local import Config
except:
    from config import Config
import sys

class MainPlayerWindow(QWidget):
    
    def __init__(self, config):

        self.config = config
        self.song_folder = config.song_folder
        super().__init__()

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

        # Begin with playlist selection
        self.stack.setCurrentWidget(self.playlist_picker)




    
    def _create_widgets(self):
        self.playlist_picker = PlaylistPicker(self.config)

    def _create_layouts(self):
        self.stack = QStackedWidget()
        self.stack.addWidget(self.playlist_picker)

        self.my_layout = QHBoxLayout()
        self.my_layout.addWidget(self.stack)

        self.setLayout(self.my_layout)

    def _connect_signals(self):
        self.playlist_picker.playlistSelected.connect(self._create_and_swap_to_player_window)
    
    def _create_and_swap_to_player_window(self, playlist_path):
        self.player_window = PlayerWindow(playlist_path, self.song_folder)
        self.stack.addWidget(self.player_window)
        self.stack.setCurrentWidget(self.player_window)
        self.player_window.back_to_picker.connect(self._swap_to_picker)

    def _swap_to_picker(self):
        self.stack.setCurrentWidget(self.playlist_picker)



if __name__ == "__main__":
    import pygame
    pygame.mixer.init()

    config = Config()
    app = QApplication(sys.argv)

    window = MainPlayerWindow(config)
    window.resize(1000, 700)
    window.show()

    sys.exit(app.exec_())